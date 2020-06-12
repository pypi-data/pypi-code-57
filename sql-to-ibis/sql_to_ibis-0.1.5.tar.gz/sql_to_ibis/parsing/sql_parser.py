"""
Module containing all lark internal_transformer classes
"""
import re
from typing import Dict, List, Set, Tuple, Union

import ibis
from ibis.expr.types import TableExpr
from lark import Token, Tree, v_args

from sql_to_ibis.exceptions.sql_exception import (
    ColumnNotFoundError,
    InvalidQueryException,
    TableExprDoesNotExist,
)
from sql_to_ibis.parsing.transformers import InternalTransformer, TransformerBaseClass
from sql_to_ibis.query_info import QueryInfo
from sql_to_ibis.sql_objects import (
    Aggregate,
    AliasRegistry,
    AmbiguousColumn,
    Column,
    CrossJoin,
    DerivedColumn,
    Expression,
    GroupByColumn,
    Join,
    JoinBase,
    Literal,
    Subquery,
    Table,
    Value,
)

GET_TABLE_REGEX = re.compile(
    r"^(?P<table>[a-z_]\w*)\.(?P<column>[a-z_]\w*)$", re.IGNORECASE
)
PANDAS_TYPE_PYTHON_TYPE_FUNCTION = {
    "object": str,
    "string": str,
    "int16": int,
    "int32": int,
    "int64": int,
    "float16": float,
    "float32": float,
    "float64": float,
    "bool": bool,
}

TYPE_TO_PANDAS_TYPE = {
    "varchar": "string",
    "int": "int32",
    "bigint": "int64",
    "float": "float64",
    "timestamp": "datetime64",
    "datetime64": "datetime64",
    "timedelta[ns]": "timedelta[ns]",
    "category": "category",
}

for TYPE in PANDAS_TYPE_PYTHON_TYPE_FUNCTION:
    TYPE_TO_PANDAS_TYPE[TYPE] = TYPE


@v_args(inline=True)
class SQLTransformer(TransformerBaseClass):
    """
    Transformer for the lark sql_to_ibis parser
    """

    def __init__(
        self,
        table_name_map=None,
        table_map=None,
        column_name_map=None,
        column_to_table_name=None,
    ):
        if table_name_map is None:
            table_name_map = {}
        if table_map is None:
            table_map = {}
        if column_name_map is None:
            column_name_map = {}
        if column_to_table_name is None:
            column_to_table_name = {}
        TransformerBaseClass.__init__(
            self,
            table_name_map,
            table_map,
            column_name_map,
            column_to_table_name,
            _temp_dataframes_dict={},
        )
        self._alias_registry = AliasRegistry()

    def add_column_to_column_to_dataframe_name_map(self, column, table):
        """
        Adds a column to the column_to_dataframe_name_map
        :param column:
        :param table:
        :return:
        """
        if self._column_to_table_name.get(column) is None:
            self._column_to_table_name[column] = table
            return
        table_name = self._column_to_table_name[column]
        if isinstance(table_name, AmbiguousColumn):
            table_name.tables.add(table)
        else:
            original_table = table_name
            self._column_to_table_name[column] = AmbiguousColumn(
                {original_table, table}
            )

    def table(self, table_name, alias=""):
        """
        Check for existence of pandas dataframe with same name
        If not exists raise TableExprDoesNotExist
        Otherwise return the name of the actual TableExpr
        :return:
        """
        table_name = table_name.lower()
        if table_name not in self._table_name_map:
            raise TableExprDoesNotExist(table_name)
        true_name = self._table_name_map[table_name]
        if isinstance(alias, Tree) and alias.data == "alias_string":
            alias_token: Token = alias.children[0]
            alias = alias_token.value
        table = Table(
            value=self._table_map[true_name].get_table_expr(),
            name=true_name,
            alias=alias,
        )
        if alias:
            self._alias_registry.add_to_registry(alias, table)
        return table

    def order_by_expression(self, rank_tree):
        """
        Returns the column name for the order sql_object
        :param rank_tree: Tree containing order info
        :return:
        """
        order_type = rank_tree.data
        ascending = order_type == "order_asc"
        return Token("order_by", (rank_tree.children[0].children, ascending))

    def integer(self, integer_token):
        """
        Returns the integer value
        :param integer_token:
        :return:
        """
        integer_value = int(integer_token.value)
        return integer_value

    def limit_count(self, limit_count_value):
        """
        Returns a limit token_or_tree
        :param limit_count_value:
        :return:
        """
        return Token("limit", limit_count_value)

    def query_expr(self, query_info: QueryInfo, *args):
        """
        Handles the full query, including order and set operations such as union
        :param query_info: Map of all query information
        :param args: Additional arguments aside from query info
        :return: Query info
        """
        for token in args:
            if isinstance(token, Token):
                if token.type == "order_by":
                    query_info.order_by.append(token.value)
                elif token.type == "limit":
                    query_info.limit = token.value
        return query_info

    def subquery(self, query_info: QueryInfo, alias: Tree):
        """
        Handle subqueries amd return a subquery object
        :param query_info:
        :param alias:
        :return:
        """
        assert alias.data == "alias_string"
        alias_name = alias.children[0].value
        subquery_value = self.to_ibis_table(query_info)
        subquery = Subquery(
            name=alias_name, query_info=query_info, value=subquery_value
        )
        self._table_map[alias_name] = subquery
        self._column_name_map[alias_name] = {}
        for column in subquery.column_names:
            self.add_column_to_column_to_dataframe_name_map(column.lower(), alias_name)
            self._column_name_map[alias_name][column.lower()] = column
        return subquery

    def column_name(self, *names):
        full_name = ".".join([str(name) for name in names])
        return Tree("column_name", full_name)

    def join(self, join_expression):
        """
        Handle join tree
        :param join_expression:
        :return:
        """
        return join_expression

    def _determine_column_side(self, column, left_table: Table, right_table: Table):
        """
        Check if column table prefix is one of the two tables (if there is one) AND
        the column has to be in one of the two tables
        """
        # TODO Refactor so that this fits with the new table object framework
        column_match = GET_TABLE_REGEX.match(column)
        column_table = ""
        if column_match:
            column = column_match.group("column").lower()
            column_table = column_match.group("table").lower()
        left_columns = self._column_name_map[left_table.name]
        right_columns = self._column_name_map[right_table.name]
        if column not in left_columns and column not in right_columns:
            raise ColumnNotFoundError(column, [left_table.name, right_table.name])

        left_table_name = left_table.name.lower()
        right_table_name = right_table.name.lower()
        if column_table:
            if column_table == left_table_name and column in left_columns:
                return "left", column
            if column_table == right_table_name and column in right_columns:
                return "right", column
            raise Exception("Table specified in join columns not present in join")
        if column in left_columns and column in right_columns:
            raise Exception(
                f"Ambiguous column: {column}\nSpecify table name with table_name"
                f".{column}"
            )
        if column in left_columns:
            return "left", column
        if column in right_columns:
            return "right", column
        raise Exception("Column does not exist in either table")

    def comparison_type(self, comparison):
        """
        Return the comparison expression
        :param comparison:
        :return:
        """
        return comparison

    def join_expression(self, *args):
        # There will only ever be four args if a join is specified and three if a
        # join isn't specified
        if len(args) == 3:
            join_type = "inner"
            table1 = args[0]
            table2 = args[1]
            join_condition = args[2]
        else:
            table1 = args[0]
            join_type = args[1]
            table2 = args[2]
            join_condition = args[3]
            if "outer" in join_type:
                match = re.match(r"(?P<type>.*)\souter", join_type)
                if match:
                    join_type = match.group("type")
            if join_type in {"full", "cross"}:
                join_type = "outer"

        # Check that there is a column from both sides
        column_comparison = join_condition.children[0].children[0].children
        column1 = str(column_comparison[0].children)
        column2 = str(column_comparison[1].children)

        column1_side, column1 = self._determine_column_side(column1, table1, table2)
        column2_side, column2 = self._determine_column_side(column2, table1, table2)
        if column1_side == column2_side:
            raise Exception("Join columns must be one column from each join table!")
        column1 = self._column_name_map[table1.name][column1]
        column2 = self._column_name_map[table2.name][column2]
        if column1_side == "left":
            left_on = column1
            right_on = column2
        else:
            left_on = column2
            right_on = column1

        return Join(
            left_table=table1,
            right_table=table2,
            join_type=join_type,
            left_on=left_on,
            right_on=right_on,
        )

    @staticmethod
    def has_star(column_list: List[str]):
        """
        Returns true if any columns have a star
        :param column_list:
        :return:
        """
        for column_name in column_list:
            if re.match(r"\*", column_name):
                return True
        return False

    @staticmethod
    def handle_non_token_non_tree(query_info: QueryInfo, token, token_pos):
        """
        Handles non token_or_tree non tree items and extracts necessary query
        information from it

        :param query_info: Dictionary of all info about the query
        :param token: Item being handled
        :param token_pos: Ordinal position of the item
        :return:
        """
        query_info.all_names.append(token.final_name)
        query_info.name_order[token.final_name] = token_pos

        if isinstance(token, GroupByColumn):
            query_info.group_columns.append(token)
        elif isinstance(token, (Column, Literal, Expression)):
            query_info.columns.append(token)
        elif isinstance(token, Aggregate):
            query_info.aggregates[token.final_name] = token

    def handle_token_or_tree(self, query_info: QueryInfo, token_or_tree, item_pos):
        """
        Handles token and extracts necessary query information from it
        :param query_info: Dictionary of all info about the query
        :param token_or_tree: Item being handled
        :param item_pos: Ordinal position of the token
        :return:
        """
        if isinstance(token_or_tree, Token):
            if token_or_tree.type == "from_expression":
                query_info.add_table(token_or_tree.value)
            elif token_or_tree.type == "where_expr":
                query_info.where_expr = token_or_tree.value
        elif isinstance(token_or_tree, Tree):
            if token_or_tree.data == "having_expr":
                query_info.having_expr = token_or_tree
        else:
            self.handle_non_token_non_tree(query_info, token_or_tree, item_pos)

    def select(self, *select_expressions: Tuple[Tree]) -> QueryInfo:
        """
        Forms the final sequence of methods that will be executed
        :param select_expressions:
        :return:
        """
        tables: List[Token] = []
        having_expr = None
        where_expr = None
        for select_expression in select_expressions:
            if isinstance(select_expression, Tree):
                if select_expression.data == "from_expression":
                    table_object = select_expression.children[0]
                    if isinstance(table_object, JoinBase):
                        tables += [
                            table_object.right_table,
                            table_object.left_table,
                        ]
                    elif (
                        isinstance(table_object, Tree)
                        and table_object.data == "cross_join_expression"
                    ):
                        cross_join: CrossJoin = table_object.children[0]
                        tables += [
                            cross_join.right_table,
                            cross_join.left_table,
                        ]
                    else:
                        tables.append(table_object)
                elif select_expression.data == "having_expr":
                    having_expr = select_expression
                elif select_expression.data == "where_expr":
                    where_expr = select_expression

        select_expressions_no_boolean_clauses = tuple(
            select_expression
            for select_expression in select_expressions
            if isinstance(select_expression, Tree)
            and select_expression.data not in ("having_expr", "where_expr")
            or not isinstance(select_expression, Tree)
        )
        internal_transformer = InternalTransformer(
            tables,
            self._table_map,
            self._column_name_map,
            self._column_to_table_name,
            self._table_name_map,
            self._alias_registry,
        )

        select_expressions = internal_transformer.transform(
            Tree("select", select_expressions_no_boolean_clauses)
        ).children

        distinct = False
        if isinstance(select_expressions[0], Token):
            if str(select_expressions[0]) == "distinct":
                distinct = True
            select_expressions = select_expressions[1:]

        query_info = QueryInfo(having_expr, where_expr, internal_transformer, distinct)

        for token_pos, token in enumerate(select_expressions):
            self.handle_token_or_tree(query_info, token, token_pos)

        return query_info

    def cross_join(self, table1: Table, table2: Table):
        """
        Returns the crossjoin between two dataframes
        :param table1: TableExpr1
        :param table2: TableExpr2
        :return: Crossjoined dataframe
        """
        return CrossJoin(left_table=table1, right_table=table2,)

    def from_item(self, item):
        return item

    @staticmethod
    def format_column_needs_agg_or_group_msg(column):
        return f"For column '{column}' you must either group or provide an aggregation"

    def _get_aggregate_ibis_columns(self, aggregates: Dict[str, Aggregate]):
        aggregate_ibis_columns = []
        for aggregate_column in aggregates:
            column = aggregates[aggregate_column].value.name(aggregate_column)
            aggregate_ibis_columns.append(column)
        return aggregate_ibis_columns

    def _handle_having_expressions(
        self,
        having_expr: Tree,
        internal_transformer: InternalTransformer,
        table: TableExpr,
        aggregates: Dict[str, Aggregate],
        group_column_names: List[str],
    ):
        having = None
        if having_expr:
            having = internal_transformer.transform(having_expr.children[0]).value
        if having is not None and not aggregates:
            for column in table.columns:
                if column not in group_column_names:
                    raise InvalidQueryException(
                        self.format_column_needs_agg_or_group_msg(column)
                    )
        return having

    def handle_aggregation(
        self,
        aggregates: Dict[str, Aggregate],
        group_columns: List[GroupByColumn],
        table: TableExpr,
        having_expr: Tree,
        internal_transformer: InternalTransformer,
        selected_columns: List[Value],
    ):
        """
        Handles all aggregation operations when translating from dictionary info
        to dataframe
        """
        selected_column_names = {
            column.get_name().lower() for column in selected_columns
        }
        aggregate_ibis_columns = self._get_aggregate_ibis_columns(aggregates)
        having = self._handle_having_expressions(
            having_expr,
            internal_transformer,
            table,
            aggregates,
            [group_column.get_name() for group_column in group_columns],
        )

        if group_columns and not selected_column_names:
            for group_column in group_columns:
                group_column.set_ibis_name_to_name()

        if group_columns and having is not None and not aggregates:
            raise NotImplementedError(
                "Group by, having, without aggregation not yet implemented"
            )
        if group_columns and not aggregates:
            for column in [
                selected_column.get_name() for selected_column in selected_columns
            ]:
                if column not in group_columns:
                    raise InvalidQueryException(
                        self.format_column_needs_agg_or_group_msg(column)
                    )
            table = table.distinct()
        elif aggregates and not group_columns:
            table = table.aggregate(aggregate_ibis_columns, having=having)
        elif aggregates and group_columns:
            table = table.group_by(
                [group_column.value for group_column in group_columns]
            )
            if having is not None:
                table = table.having(having)
            table = table.aggregate(aggregate_ibis_columns)

        non_selected_columns = []
        if group_columns and aggregates:
            for group_column in group_columns:
                if group_column.get_name().lower() not in selected_column_names:
                    non_selected_columns.append(group_column.group_by_name)
            if non_selected_columns:
                table = table.drop(non_selected_columns)

        return table

    def handle_filtering(
        self,
        ibis_table: TableExpr,
        where_expr: Tree,
        internal_transformer: InternalTransformer,
    ):
        """
        Returns frame with appropriately selected and named columns
        :param ibis_table: Ibis expression table to manipulate
        :param where_expr: Syntax tree containing where clause
        :param internal_transformer: Transformer to transform the where clauses
        :return: Filtered TableExpr
        """
        where_value = None
        if where_expr is not None:
            where_value_token = internal_transformer.transform(where_expr)
            where_value = where_value_token.value
        if where_value is not None:
            return ibis_table.filter(where_value)
        return ibis_table

    def subquery_in(self, column: Tree, subquery: Subquery):
        return Tree("subquery_in", (column, subquery))

    def handle_selection(
        self, ibis_table: TableExpr, columns: List[Value]
    ) -> TableExpr:
        column_mutation = []
        for column in columns:
            if column.get_name() == "*":
                return ibis_table
            column_value = column.get_value().name(column.get_name())
            column_mutation.append(column_value)
        if column_mutation:
            return ibis_table.projection(column_mutation)
        return ibis_table

    def handle_duplicate_columns_in_join(
        self, right_table: TableExpr, left_table: TableExpr, join: JoinBase
    ):
        duplicate_columns = set(left_table.columns).intersection(right_table.columns)
        for column in duplicate_columns:
            left_table = left_table.relabel({column: f"{join.left_table}." f"{column}"})
            right_table = right_table.relabel(
                {column: f"{join.right_table}" f".{column}"}
            )

        if isinstance(join, Join) and join.left_on == join.right_on:
            join.left_on = f"{join.left_table}.{join.left_on}"
            join.right_on = f"{join.right_table}.{join.right_on}"

        return left_table, right_table

    @staticmethod
    def _columns_have_select_star(columns: List[Value]):
        for column in columns:
            if column.get_name() == "*":
                return True
        return False

    @staticmethod
    def _rename_duplicates(
        table: Table, duplicates: Set[str], table_name: str, table_columns: list
    ):
        for i, column in enumerate(table.column_names):
            if column in duplicates:
                table_columns[i] = table_columns[i].name(f"{table_name}.{column}")
        return table_columns

    def _get_all_join_columns_handle_duplicates(
        self, left: Table, right: Table, join: JoinBase
    ):
        left_columns = left.get_ibis_columns()
        right_columns = right.get_ibis_columns()
        duplicates = set(left.column_names).intersection(right.column_names)
        left_columns = self._rename_duplicates(
            left, duplicates, join.left_table.name, left_columns
        )
        right_columns = self._rename_duplicates(
            right, duplicates, join.right_table.name, right_columns
        )
        return left_columns + right_columns

    def _get_all_columns_rename_duplicates(self, tables: List[Table]):
        columns = {table: table.get_ibis_columns() for table in tables}

        def set_dict_column_name(table: Table, col_name: str):
            index = table.column_names.index(col_name)
            columns[table][index] = columns[table][index].name(
                f"{table.get_alias_else_name()}.{col_name}"
            )

        for i, table1 in enumerate(tables):
            for table2 in tables[i + 1 :]:
                table1_column_names = set(table1.column_names)
                table2_column_names = set(table2.column_names)
                intersect = table1_column_names.intersection(table2_column_names)
                for column_name in intersect:
                    for table in [table1, table2]:
                        set_dict_column_name(table, column_name)

        all_columns = []
        for table in columns:
            all_columns += columns[table]
        return all_columns

    def handle_join(self, join: JoinBase, columns: List[Value]) -> TableExpr:
        """
        Return the table expr resulting from the join
        :param join:
        :param columns: List of all column values
        :return:
        """
        result: TableExpr = None
        all_columns: List[Value] = []
        left_table = join.left_table
        right_table = join.right_table

        if self._columns_have_select_star(columns):
            all_columns = self._get_all_join_columns_handle_duplicates(
                left_table, right_table, join
            )

        left_ibis_table = left_table.get_table_expr()
        right_ibis_table = right_table.get_table_expr()
        if isinstance(join, Join):
            result = left_ibis_table.join(
                right_ibis_table,
                predicates=left_ibis_table.get_column(join.left_on)
                == right_ibis_table.get_column(join.right_on),
                how=join.join_type,
            )
        if isinstance(join, CrossJoin):
            result = ibis.cross_join(left_ibis_table, right_ibis_table)

        if all_columns:
            return result[all_columns]
        return result

    def _set_casing_for_groupby_names(
        self, groupby_columns: List[GroupByColumn], selected_columns: List[Value]
    ):
        lower_case_to_true_column_name = {
            column.get_name().lower(): column.get_name() for column in selected_columns
        }
        for groupby_column in groupby_columns:
            lower_case_group_name = groupby_column.get_name().lower()
            if lower_case_group_name in lower_case_to_true_column_name:
                selection_statement_name = lower_case_to_true_column_name[
                    lower_case_group_name
                ]
                groupby_column.group_by_name = selection_statement_name
                groupby_column.value = groupby_column.value.name(
                    selection_statement_name
                )

    def get_table_value(self, table: Union[Table, JoinBase, Subquery]):
        assert isinstance(table, (Table, JoinBase, Subquery))
        if isinstance(table, Table):
            return table.get_table_expr()
        if isinstance(table, JoinBase):
            return table

    def to_ibis_table(self, query_info: QueryInfo):
        """
        Returns the dataframe resulting from the SQL query
        :return:
        """
        tables = query_info.tables
        if not query_info.tables:
            raise Exception("No table specified")
        first_table = self.get_table_value(tables[0])

        if isinstance(first_table, JoinBase):
            first_table = self.handle_join(join=first_table, columns=query_info.columns)
        for table in tables[1:]:
            next_table = self.get_table_value(table)
            first_table = first_table.cross_join(next_table)
        if len(tables) > 1 and self._columns_have_select_star(query_info.columns):
            all_columns = self._get_all_columns_rename_duplicates(tables)
            first_table = first_table[all_columns]

        self._set_casing_for_groupby_names(query_info.group_columns, query_info.columns)

        selected_group_columns = []
        group_column_names = {
            group_column.group_by_name for group_column in query_info.group_columns
        }
        if query_info.group_columns and query_info.aggregates:
            selection_column_names = [
                column.get_name() for column in query_info.columns
            ]
            remaining_columns = set(selection_column_names) - group_column_names
            if remaining_columns:
                raise InvalidQueryException(
                    f"Must have grouping for columns in {remaining_columns}"
                )
            selected_group_columns = [
                column
                for column in query_info.columns
                if column.get_name() in set(group_column_names)
            ]

            query_info.columns = [
                column
                for column in query_info.columns
                if column.get_name() in remaining_columns
            ]
        new_table = self.handle_selection(first_table, query_info.columns)
        new_table = self.handle_filtering(
            new_table, query_info.where_expr, query_info.internal_transformer
        )
        new_table = self.handle_aggregation(
            query_info.aggregates,
            query_info.group_columns,
            new_table,
            query_info.having_expr,
            query_info.internal_transformer,
            selected_group_columns,
        )

        if query_info.distinct:
            new_table = new_table.distinct()

        order_by = query_info.order_by
        if order_by:
            new_table = new_table.sort_by(order_by)

        if query_info.limit is not None:
            new_table = new_table.head(query_info.limit)

        return new_table

    def set_expr(self, query_info):
        """
        Return different sql_object with set relational operations performed
        :param query_info:
        :return:
        """
        frame = self.to_ibis_table(query_info)
        return frame

    def union_all(
        self, expr1: TableExpr, expr2: TableExpr,
    ):
        """
        Return union distinct of two TableExpr
        :param expr1: Left TableExpr
        :param expr2: Right TableExpr
        :return:
        """
        return expr1.union(expr2)

    def union_distinct(
        self, expr1: TableExpr, expr2: TableExpr,
    ):
        """
        Return union distinct of two TableExpr
        :param expr1: Left TableExpr
        :param expr2: Right TableExpr
        :return:
        """
        return expr1.union(expr2, distinct=True)

    def intersect_distinct(self, expr1: TableExpr, expr2: TableExpr):
        """
        Return distinct intersection of two TableExpr
        :param expr1: Left TableExpr
        :param expr2: Right TableExpr
        :return:
        """
        raise NotImplementedError("Waiting on ibis for intersect implementation")

    def except_distinct(self, expr1: TableExpr, expr2: TableExpr):
        """
        Return distinct set difference of two TableExpr
        :param expr1: Left TableExpr
        :param expr2: Right TableExpr
        :return:
        """
        raise NotImplementedError("Waiting on ibis for except implementation")

    def except_all(self, expr1: TableExpr, expr2: TableExpr):
        """
        Return set difference of two TableExpr
        :param expr1: Left TableExpr
        :param expr2: Right TableExpr
        :return:
        """
        raise NotImplementedError("Waiting on ibis for except implementation")

    def final(self, table):
        """
        Returns the final dataframe
        :param table:
        :return:
        """
        DerivedColumn.reset_expression_count()
        return table
