# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
/////////////////////////////////////////////////////////////////////////
//
// (c) Copyright University of Southampton IT Innovation, 2016
//
// Copyright in this software belongs to IT Innovation Centre of
// Gamma House, Enterprise Road, Southampton SO16 7NS, UK.
//
// This software may not be used, sold, licensed, transferred, copied
// or reproduced in whole or in part in any manner or form or in or
// on any media by any person other than in accordance with the terms
// of the Licence Agreement supplied with the software, or otherwise
// without the prior written consent of the copyright owners.
//
// This software is distributed WITHOUT ANY WARRANTY, without even the
// implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
// PURPOSE, except where stated in the Licence Agreement supplied with
// the software.
//
//    Created By :          Ken Meacham
//    Created Date :        2016/04/08
//    Created for Project:  REVEAL
//
/////////////////////////////////////////////////////////////////////////
//
// Dependencies: None
//
/////////////////////////////////////////////////////////////////////////
"""

import soton_corenlppy
import copy
import datetime
import logging
import re
import sys


class DummyLogger:
	def __init__(self):
		return

	def info(self, message):
		return

	def debug(self, message):
		return


# noinspection SqlNoDataSourceInspection
class SitAssessLib:
	def __init__(self, dictConfig, useLogger=True, sitAssessLogger=None):
		if useLogger:
			if sitAssessLogger is not None:
				self.logger = sitAssessLogger
				self.logger.info('sit_assess_lib using provided logger')
			else:
				self.logger = self.create_default_logger()
				self.logger.info('sit_assess_lib using default logger')
		else:
			self.logger = self.create_dummy_logger()

		self.dictConfig = copy.deepcopy(dictConfig)

		strUser = dictConfig['db_user']
		strPass = dictConfig['db_pass']
		strHost = dictConfig['db_host']
		nPort = int(dictConfig['db_port'])
		strDatabase = dictConfig['db_name']
		nTimeoutStatement = int(dictConfig['timeout_statement'])

		# connect to database
		self.dbHandler = soton_corenlppy.PostgresqlHandler.PostgresqlHandler(strUser, strPass, strHost, nPort, strDatabase, nTimeoutStatement)

		# initialize table definitions
		self.initialize_table_defs()

		# initialize SQL templates
		self.initialize_sql_templates()

	#
	# create default logger
	#
	def create_default_logger(self):
		# make logger (global to STDOUT)
		LOG_FORMAT = ('%(levelname) -s %(asctime)s %(name) -s %(funcName) -s %(lineno) -d: %(message)s')
		logger = logging.getLogger(__name__)
		logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
		return logger

	#
	# create dummy logger
	#
	@staticmethod
	def create_dummy_logger():
		logger = DummyLogger()
		return logger

	#
	# create tables
	#
	def create_tables(self, nTimeoutStatement=None, nTimeoutOverall=None):

		if nTimeoutStatement is None:
			nTimeoutStatement = int(self.dictConfig['timeout_statement'])

		if nTimeoutOverall is None:
			nTimeoutOverall = int(self.dictConfig['timeout_overall'])

		strIndexTableSuffix = self.dictConfig['index_table_suffix']
		item_table = self.dictConfig['item_table']
		itemTableDef = self.tableDefs[item_table]
		item_table_name = itemTableDef['table_name']
		item_primary_key = itemTableDef['primary_key']

		listStatements = []

		for table in self.tablesList:
			tableDef = self.tableDefs[table]
			table_name = tableDef['table_name']
			table_type = tableDef['table_type']
			self.logger.debug('Creating table: {0} {1}'.format(table, table_name))

			tableColNames = self.tableColNames[table]  # col names for table
			dictColDefs = self.tableColDefs[table]  # col defs for table

			tableSQL = []
			geomCols = []  # list of column names that have type 'geometry'

			table_primary_key = tableDef['primary_key']

			tableSQL.append('CREATE TABLE IF NOT EXISTS {0}'.format(table_name))
			tableSQL.append('(')

			tupleData = ()

			for i, col_name in enumerate(tableColNames):
				(col_type, col_create_sql, col_default, col_has_default) = dictColDefs[col_name]
				self.logger.debug(dictColDefs[col_name])

				# Set up regex to search for 'DEFAULT' (ignoring case)
				defaultRegex = re.compile('DEFAULT', re.I)

				if defaultRegex.search(col_create_sql) is None:
					if col_has_default:
						if col_type == 'timestamp' and col_default == 'current_timestamp':
							defaultSQL = ' DEFAULT {0}'.format(col_default)  # don't include quotes
						else:
							defaultSQL = ' DEFAULT %s'
							tupleData += (col_default,)

						col_create_sql += defaultSQL

				# Check that first column is the expected primary key
				if (i == 0) and (col_name != table_primary_key):
					raise Exception(
						'Expected primary key column "{0}" but found "{1}"'.format(table_primary_key, col_name))

				tableSQL.append('  {0} {1},'.format(col_name, col_create_sql))

				# Check if column is a geometry type
				if col_type == 'geometry':
					self.logger.debug('Located geometry column: {0}'.format(col_name))
					geomCols.append(col_name)

			primary_key_constraint = '  CONSTRAINT {0} PRIMARY KEY ({1})'.format(
				tableDef['primary_key_constraint_name'], table_primary_key)
			tableSQL.append(primary_key_constraint)

			""" N.B. don't make UNIQUE constraint here, as this causes problems with geometry columns
			# Create additional UNIQUE constraint for index_cols entry
			index_cols = tableDef['index_cols']
			tableSQL.append( ', UNIQUE (' + ', '.join(index_cols) + ')')
			"""

			# End of TABLE definition
			tableSQL.append(');')

			if len(geomCols) > 0:
				self.logger.debug('Geometry columns for {0} table: {1}'.format(repr(table), geomCols))
				self.logger.debug('Creating GIST indexes for geometry columns..')
				for geomCol in geomCols:
					self.appendGISTIndexSQL(tableSQL, table_name, geomCol)

			# print tableSQL
			tableSQLstr = '\n'.join(tableSQL)
			listStatements.append((tableSQLstr, tupleData))

			self.logger.debug("\n" + tableSQLstr)
			self.logger.debug(tupleData)

			# Create index table (N.B. only for annotation tables!)
			if table_type == 'annotation':
				tableSQL = []

				tableSQL.append('CREATE TABLE IF NOT EXISTS {0}_{1}'.format(table_name, strIndexTableSuffix))
				tableSQL.append('(')
				tableSQL.append('  {0} bigint NOT NULL REFERENCES {1}({2}),'.format(item_primary_key, item_table_name, item_primary_key))
				tableSQL.append('  {0} bigint NOT NULL REFERENCES {1}({2}),'.format(table_primary_key, table_name, table_primary_key))
				tableSQL.append(' UNIQUE ({0}, {1})'.format(item_primary_key, table_primary_key))
				tableSQL.append(')')

				tableSQLstr = '\n'.join(tableSQL)
				listStatements.append((tableSQLstr, None))

				self.logger.debug(tableSQLstr)

		self.logger.debug(listStatements)

		sqlHandler = self.get_sql_handler()
		sqlHandler.execute_sql_statement(listStatements, nTimeoutStatement, nTimeoutOverall)

	#
	# append GIST INDEX SQL for specified table and column
	#
	def appendGISTIndexSQL(self, tableSQL, strTableFullname, strCol):
		strTableName = re.split('\.', strTableFullname)[1]
		strIndexName = strTableName + '_gist_index'

		self.logger.debug('Creating GIST index: {0} ON {1} ( {2} )'.format(strIndexName, strTableFullname, strCol))

		# Example:
		"""
CREATE OR REPLACE FUNCTION create_index() RETURNS VOID AS $$
BEGIN
				CREATE INDEX assessment_id_1_db_loc_gist_index ON reveal.assessment_id_1_db_loc USING GIST ( shape );
EXCEPTION
				WHEN undefined_table THEN
								RETURN;
				WHEN duplicate_table THEN
								RETURN;
END;
$$ LANGUAGE plpgsql;

SELECT create_index();
		"""

		tableSQL.append('CREATE OR REPLACE FUNCTION create_index() RETURNS VOID AS $$')
		tableSQL.append('BEGIN')
		tableSQL.append('  CREATE INDEX {0} ON {1} USING GIST ( {2} );'.format(strIndexName, strTableFullname, strCol))
		tableSQL.append('EXCEPTION')
		tableSQL.append('  WHEN undefined_table THEN')
		tableSQL.append('    RETURN;')
		tableSQL.append('  WHEN duplicate_table THEN')
		tableSQL.append('    RETURN;')
		tableSQL.append('END;')
		tableSQL.append('$$ LANGUAGE plpgsql;')
		tableSQL.append('SELECT create_index();')

		return

	#
	# delete items and index entries for these items
	#
	def delete_items(self, expiryInterval, nTimeoutStatement=None, nTimeoutOverall=None):
		if nTimeoutStatement is None:
			nTimeoutStatement = int(self.dictConfig['timeout_statement'])

		if nTimeoutOverall is None:
			nTimeoutOverall = int(self.dictConfig['timeout_overall'])

		strIndexTableSuffix = self.dictConfig['index_table_suffix']

		item_table = self.dictConfig['item_table']  # normally 'item'
		itemTableDef = self.tableDefs[item_table]
		item_table_name = itemTableDef['table_name']

		listStatements = []

		for table in self.tablesList:
			tableDef = self.tableDefs[table]
			table_name = tableDef['table_name']
			table_type = tableDef['table_type']
			self.logger.debug('Deleting items from table: {0} {1}'.format(table, table_name))

			date_clause = "now() - interval '{0}'".format(expiryInterval) #e.g. "now() - interval '1 hour'"
			where_clause = "WHERE {0}.updated_time < {1}".format(item_table_name, date_clause)

			# Delete index entries first (N.B. only for annotation tables!)
			if table_type == 'annotation':
				tableSQL = []

				tableSQL.append("WITH selected_items AS (SELECT {0}.item_key".format(item_table_name))
				tableSQL.append("FROM {0}".format(item_table_name))
				tableSQL.append(where_clause + ")")
				tableSQL.append("DELETE FROM {0}_{1}".format(table_name, strIndexTableSuffix))
				tableSQL.append("WHERE item_key IN (SELECT item_key FROM selected_items);")

				tableSQLstr = '\n'.join(tableSQL)
				listStatements.append((tableSQLstr, None))

				self.logger.debug(tableSQLstr)

		tableSQL = []

		tableSQL.append("DELETE FROM {0}".format(item_table_name))
		tableSQL.append(where_clause)

		tableSQLstr = '\n'.join(tableSQL)
		listStatements.append((tableSQLstr, None))

		self.logger.debug(tableSQLstr)

		self.logger.debug(listStatements)

		sqlHandler = self.get_sql_handler()
		sqlHandler.execute_sql_statement(listStatements, nTimeoutStatement, nTimeoutOverall)

	#
	# delete all annotations and index entries but leave the items alone. this is useful if the annotations are to be re-created from the items (e.g. new configuration settings).
	#
	def delete_annotations(self, nTimeoutStatement=None, nTimeoutOverall=None):
		if nTimeoutStatement is None:
			nTimeoutStatement = int(self.dictConfig['timeout_statement'])

		if nTimeoutOverall is None:
			nTimeoutOverall = int(self.dictConfig['timeout_overall'])

		strIndexTableSuffix = self.dictConfig['index_table_suffix']

		item_table = self.dictConfig['item_table']  # normally 'item'
		itemTableDef = self.tableDefs[item_table]
		item_table_name = itemTableDef['table_name']

		listStatements = []

		for table in self.tablesList:
			tableDef = self.tableDefs[table]
			table_name = tableDef['table_name']
			table_type = tableDef['table_type']

			if table_type == 'annotation':
				self.logger.debug('Deleting annotations and index entries from table: {:s} {:s}'.format(table, table_name))

				# delete annotation index entries
				listStatements.append(
					( "DELETE FROM {0}_{1}".format(table_name, strIndexTableSuffix), None )
					)

				# delete annotations
				listStatements.append(
					( "DELETE FROM {0}".format(table_name), None )
					)

		self.logger.debug(listStatements)

		sqlHandler = self.get_sql_handler()
		sqlHandler.execute_sql_statement(listStatements, nTimeoutStatement, nTimeoutOverall)


	#
	# delete tables
	#
	def delete_tables(self, nTimeoutStatement=None, nTimeoutOverall=None):
		if nTimeoutStatement is None:
			nTimeoutStatement = int(self.dictConfig['timeout_statement'])

		if nTimeoutOverall is None:
			nTimeoutOverall = int(self.dictConfig['timeout_overall'])

		strIndexTableSuffix = self.dictConfig['index_table_suffix']

		listStatements = []

		for table in reversed(self.tablesList):  # drop tables in reverse order
			tableDef = self.tableDefs[table]
			table_name = tableDef['table_name']
			table_type = tableDef['table_type']
			self.logger.debug('Deleting table: {0} {1}'.format(table, table_name))

			# Drop index table first (N.B. only for annotation tables!)
			if table_type == 'annotation':
				tableSQL = []

				tableSQL.append('DROP TABLE IF EXISTS {0}_{1} CASCADE'.format(table_name, strIndexTableSuffix))

				tableSQLstr = '\n'.join(tableSQL)
				listStatements.append((tableSQLstr, None))

				self.logger.debug(tableSQLstr)

			tableSQL = []
			tableSQL.append('DROP TABLE IF EXISTS {0} CASCADE'.format(table_name))

			tableSQLstr = '\n'.join(tableSQL)
			listStatements.append((tableSQLstr, None))

			self.logger.debug(tableSQLstr)

		self.logger.debug(listStatements)

		sqlHandler = self.get_sql_handler()
		sqlHandler.execute_sql_statement(listStatements, nTimeoutStatement, nTimeoutOverall)

	#
	# close database connection
	#
	def close_db(self):
		# close database handles
		if self.dbHandler is not None:
			self.dbHandler.close()
			self.dbHandler = None

	#
	# insert data
	#
	def insert_data(self, dictDataValues, nTimeoutStatement=None, nTimeoutOverall=None):
		if nTimeoutStatement is None:
			nTimeoutStatement = int(self.dictConfig['timeout_statement'])

		if nTimeoutOverall is None:
			nTimeoutOverall = int(self.dictConfig['timeout_overall'])

		self.logger.debug('Inserting data:')
		self.logger.debug(dictDataValues)
		self.logger.debug('')

		# Loop through data items and insert each one
		for dataItem in dictDataValues:
			self.insert_data_item(dataItem, nTimeoutStatement, nTimeoutOverall)

	#
	# insert data item
	#
	def insert_data_item(self, dataItem, nTimeoutStatement, nTimeoutOverall):
		self.logger.debug('Inserting data item:')
		self.logger.debug(dataItem)

		item_table = self.dictConfig['item_table']  # normally 'item'
		tableDef = self.tableDefs[item_table]

		index_col = tableDef['index_cols'][0]  # assume only one unique column for an item
		source_uri_ann = item_table + ':' + index_col  # normally 'item:source_uri'

		if len(dataItem) <= 1:
			raise Exception("No annotations defined in dataItem: " + repr(dataItem))

		tableAnnotations = {}

		# Perform initial parse of annotations, to group by table
		for ann in dataItem :
			(table, col) = re.split(':', ann)

			if table not in tableAnnotations:
				tableAnnotations[table] = {}

			tableAnnotations[table][col] = dataItem[ann]

		self.logger.debug(tableAnnotations)

		# if there is an item entry then add new item and use its key in any further annotations so they are indexed
		# otherwise add annotations without an item index
		nItemKey = None
		if item_table in tableAnnotations :
			# Pop item annotations from list, leaving remaining (non-item) annotations
			itemAnnotations = tableAnnotations.pop(item_table)

			self.logger.debug('Inserting item annotations: {0}'.format(itemAnnotations))
			nItemKey = self.insert_item(itemAnnotations, nTimeoutStatement, nTimeoutOverall)  # ensure only item annotations inserted
			self.logger.debug('Remaining annotations {0}'.format(tableAnnotations))

		self.logger.debug( 'item KEY = ' + repr(nItemKey) )

		# Loop through remaining tables in tableAnnotations and insert for each annotation type
		for ann in tableAnnotations :
			self.logger.debug('Inserting annotations {0} {1}'.format(ann, repr(tableAnnotations[ann]) ))
			self.insert_annotation( nItemKey, ann, tableAnnotations[ann], nTimeoutStatement, nTimeoutOverall )

	# Either
	# 1) insert item into item table (if it does not exist)
	# 2) update existing item (if update cols are defined)
	# 3) select existing item
	#
	def insert_item(self, dataItem, nTimeoutStatement, nTimeoutOverall):
		sqlHandler = self.get_sql_handler()

		#
		# insert item data that does not need indexing
		# BUT avoid duplicate entries (source_uri as primary key)
		# to allow import mid-way through a failed run where we might
		# get duplicates (ignore duplicate)
		#

		item_table = self.dictConfig['item_table']  # normally 'item'
		strInsertOrUpdateTemplateName = 'insert_item'
		strInsertOrSelectTemplateName = 'insert_or_select_item'
		query = self.get_insert_item_query(item_table, strInsertOrUpdateTemplateName, strInsertOrSelectTemplateName,dataItem)

		if query is None:
			# No item annotations in dataItem
			return -1

		#self.logger.info( 'SQL = ' + repr(query) )

		listQueryResult = sqlHandler.execute_sql_query(query, nTimeoutStatement, nTimeoutOverall)

		if len(listQueryResult) == 1:
			(result, nItemKey) = listQueryResult[0]  # result should be either 'inserted' or 'updated'
			self.logger.debug(result + ' ' + 'ITEM KEY = ' + repr(nItemKey))
		else:
			raise Exception('Could not insert or update item: ' + repr(dataItem))

		if nItemKey == -1:
			raise Exception('No item key returned for insert or update item: ' + repr(dataItem))

		return nItemKey

	def insert_annotation(self, nItemKey, strAnnotation, dataItem, nTimeoutStatement, nTimeoutOverall):
		sqlHandler = self.get_sql_handler()

		self.logger.debug('Insert {0} annotations: {1}'.format(repr(strAnnotation), dataItem))

		#
		# first insert using index columns and mutable columns (with latest value) and see if we make a new item (i.e. bAssertImmutableCols = False)
		# if we make a new row then we do a second update to set the values for all immutable colums (to set thier unchangable value)
		# this avoids large SQL queries with immutable data values for cases where the annotation entry already exists. large SQL queries are slow due to network IO and will reduce data import rates a lot
		#

		query = self.get_insert_annotation_query(strAnnotation, dataItem, bAssertImmutableCols = False)
		listQueryResult = sqlHandler.execute_sql_query(query, nTimeoutStatement, nTimeoutOverall)
		self.logger.debug( 'insert annotation query 1 = ' + repr(query) )

		#
		# get key that was just inserted for use in index
		#
		if len(listQueryResult) == 1:
			(result, nAnnotationKey) = listQueryResult[0]  # result should be either 'inserted' or 'selected'
			self.logger.debug('{0} {1} ANNOTATION KEY (without geom) = {0} for {1}'.format(result, repr(strAnnotation), repr(nAnnotationKey),dataItem))

			# run insert again with geom this time
			if result == 'inserted' :
				query = self.get_insert_annotation_query(strAnnotation, dataItem, bAssertImmutableCols = True)
				self.logger.debug( 'insert annotation query 2 = ' + repr(query) )
				listQueryResult = sqlHandler.execute_sql_query(query, nTimeoutStatement, nTimeoutOverall)

				if len(listQueryResult) == 1:
					(result, nAnnotationKey) = listQueryResult[0]  # result should be either 'inserted' or 'selected'
					self.logger.debug('{0} {1} ANNOTATION KEY (with geom) = {0} for {1}'.format(result, repr(strAnnotation), repr(nAnnotationKey),dataItem))
				else:
					raise Exception('Could not insert or select annotation: ' + repr(dataItem))
		else:
			raise Exception('Could not insert or select annotation: ' + repr(dataItem))

		#
		# add an index entry to link item to this key (if an item key has been supplied)
		#
		if nItemKey != None :
			listIndexSQL = []
			query = self.get_insert_annotation_index_query(strAnnotation, nItemKey, nAnnotationKey)
			listIndexSQL.append(query)

			# TODO: maybe simply return query here, to be appended to collection of index queries to be executed in bulk,
			# once all annotations inserted?
			listQueryResult = sqlHandler.execute_sql_statement( listIndexSQL, nTimeoutStatement, nTimeoutOverall )


	#
	# initialize SQL templates
	#
	def initialize_sql_templates(self):
		self.logger.debug("Creating SQL templates")
		self.sqlTemplates = {}
		strItemTableSuffix = self.dictConfig['item_table_suffix']

		insert_item_template = self.create_insert_item_template()
		self.logger.debug('insert_item_template: \n\n' + insert_item_template + '\n')

		self.sqlTemplates['insert_item'] = insert_item_template

		insert_or_select_item_template = self.create_insert_or_select_template(strItemTableSuffix)
		self.logger.debug('insert_or_select_item_template: \n\n' + insert_or_select_item_template + '\n')
		self.sqlTemplates['insert_or_select_item'] = insert_or_select_item_template

		# Next create generic SQL template for insert annotation index
		generic_annotation_index_template = self.create_insert_generic_annotation_index_template()
		self.logger.debug("generic_annotation_index_template:\n" + generic_annotation_index_template)

		# Now create specific template for each annotation table def
		for annotationTableDef in self.annotationTableDefs:
			(strAnnotation, fullTableName, strIndexTableName, strKeyCol) = annotationTableDef

			self.sqlTemplates['insert_annotation_' + strAnnotation] = self.create_insert_annotation_template(
				strAnnotation)
			self.sqlTemplates['insert_or_select_annotation_' + strAnnotation] = self.create_insert_or_select_template(
				strAnnotation)

			self.sqlTemplates['insert_annotation_index_' + strAnnotation] = generic_annotation_index_template.format(
				strIndexTableName, strKeyCol, strIndexTableName, strKeyCol)

		for template_key in self.sqlTemplates:
			self.logger.debug('{0}:\n'.format(template_key) + self.sqlTemplates[template_key])

	#
	# create INSERT or UPDATE item template
	#
	def create_insert_item_template(self):
		strTable = self.dictConfig['item_table']
		tableDef = self.tableDefs[strTable]
		table_name = tableDef['table_name']
		primary_key = tableDef['primary_key']  # normally 'item_key'
		index_col = tableDef['index_cols'][0]  # assume only one unique column for an item

		"""
		-- Example SQL:
		WITH
			old AS (
				UPDATE reveal.assessment_id_tbd_db_item SET (text, lang)=('some text', 'en') WHERE source_uri = 'https://twitter.com/test/4'
				RETURNING item_key
			),
			new AS (
				INSERT INTO reveal.assessment_id_tbd_db_item (source_uri, text, lang)
				SELECT 'https://twitter.com/test/4', 'some text', 'en'
				WHERE NOT EXISTS( SELECT source_uri FROM reveal.assessment_id_tbd_db_item WHERE source_uri = 'https://twitter.com/test/4' )
				RETURNING item_key
			)
		SELECT 'updated', * FROM old
		UNION
		SELECT 'inserted', * FROM new;
		"""

		# note: some variables are instantiated by the user of this template later
		insertSQL = []
		insertSQL.append('WITH')
		insertSQL.append('  old AS (')
		insertSQL.append('    UPDATE {0} '.format(table_name) + 'SET ({0}) = ({1}) ' + 'WHERE {2}')
		insertSQL.append('    RETURNING {0}'.format(primary_key))
		insertSQL.append('  ),')
		insertSQL.append('  new AS (')
		insertSQL.append('    INSERT INTO {0} '.format(table_name) + '({3})')
		insertSQL.append('    SELECT {4}')
		insertSQL.append('    WHERE NOT EXISTS( SELECT {0} FROM {1} '.format(index_col, table_name) + 'WHERE {5} )')
		insertSQL.append('    RETURNING {0}'.format(primary_key))
		insertSQL.append('  )')
		insertSQL.append('SELECT \'updated\', * FROM old')
		insertSQL.append('UNION')
		insertSQL.append('SELECT \'inserted\', * FROM new;')

		strSQL = '\n'.join(insertSQL)

		return strSQL

	#
	# create generic INSERT or SELECT template
	#
	def create_insert_or_select_template(self, strTable):
		tableDef = self.tableDefs[strTable]
		table_name = tableDef['table_name']
		primary_key = tableDef['primary_key']  # normally 'item_key'
		index_col = tableDef['index_cols'][0]  # assume only one unique column for an item

		"""
		-- Example SQL:
		WITH
			old AS (
				SELECT item_key FROM reveal.assessment_id_1_db_item WHERE source_uri = 'https://twitter.com/test/5'
			),
			new AS (
				INSERT INTO reveal.assessment_id_1_db_item (source_uri)
				SELECT 'https://twitter.com/test/5'
				WHERE NOT EXISTS( SELECT source_uri FROM reveal.assessment_id_1_db_item WHERE source_uri = 'https://twitter.com/test/5' )
				RETURNING item_key
			)
		SELECT 'selected', * FROM old
		UNION
		SELECT 'inserted', * FROM new;
		"""

		# note: some variables are instantiated by the user of this template later
		insertSQL = []
		insertSQL.append('WITH')
		insertSQL.append('  old AS (')
		insertSQL.append('    SELECT {0} FROM {1} '.format(primary_key, table_name) + 'WHERE {0}')
		insertSQL.append('  ),')
		insertSQL.append('  new AS (')
		insertSQL.append('    INSERT INTO {0} '.format(table_name) + '({1})')
		insertSQL.append('    SELECT {2}')
		insertSQL.append('    WHERE NOT EXISTS( SELECT {0} FROM {1} '.format(index_col, table_name) + 'WHERE {3} )')
		insertSQL.append('    RETURNING {0}'.format(primary_key))
		insertSQL.append('  )')
		insertSQL.append('SELECT \'selected\', * FROM old')
		insertSQL.append('UNION')
		insertSQL.append('SELECT \'inserted\', * FROM new;')

		strSQL = '\n'.join(insertSQL)

		return strSQL

	#
	# create INSERT annotation template
	#
	def create_insert_annotation_template(self, strTable):
		tableDef = self.tableDefs[strTable]
		table_name = tableDef['table_name']
		primary_key = tableDef['primary_key']

		index_cols = tableDef['index_cols']
		index_cols_str = ', '.join(index_cols)

		insertSQL = []

		# note: some variables are instantiated by the user of this template later
		insertSQL.append('WITH')
		insertSQL.append('  old AS (')
		insertSQL.append('    UPDATE {0} '.format(table_name) + 'SET ({0}) = ({1}) ' + 'WHERE {2}')
		insertSQL.append('    RETURNING {0}'.format(primary_key))
		insertSQL.append('  ),')
		insertSQL.append('  new AS (')
		insertSQL.append('    INSERT INTO {0} '.format(table_name) + '({3})')
		insertSQL.append('    SELECT {4}')
		insertSQL.append('    WHERE NOT EXISTS( SELECT {0} FROM {0} '.format(index_cols_str, table_name) + 'WHERE {5} )')
		insertSQL.append('    RETURNING {0}'.format(primary_key))
		insertSQL.append('  )')
		insertSQL.append('SELECT \'updated\', * FROM old')
		insertSQL.append('UNION')
		insertSQL.append('SELECT \'inserted\', * FROM new;')

		strSQL = '\n'.join(insertSQL)

		return strSQL

	#
	# create INSERT annotation index template
	#
	def create_insert_generic_annotation_index_template(self):
		item_table = self.dictConfig['item_table']
		itemTableDef = self.tableDefs[item_table]
		item_primary_key = itemTableDef['primary_key']  # normally 'item_key'

		# Example:
		"""
		INSERT INTO reveal.assessment_id_1_db_author_item_index (
			item_key,
			author_key
		) SELECT 1, 3
		WHERE NOT EXISTS (
			SELECT * FROM reveal.assessment_id_1_db_author_item_index WHERE (item_key, author_key)=(1,3)
		)
		"""

		# note: some variables are instantiated by the user of this template later
		insertSQL = []
		insertSQL.append('INSERT INTO {0} (')
		insertSQL.append('  {0},'.format(item_primary_key))
		insertSQL.append('  {1}')
		insertSQL.append(') SELECT %s::bigint, %s::bigint ')
		insertSQL.append('WHERE NOT EXISTS (')
		insertSQL.append('SELECT * FROM {2}' + ' WHERE ({0},'.format(item_primary_key) + ' {3}) = (%s::bigint, %s::bigint)')
		insertSQL.append(')')

		strSQL = '\n'.join(insertSQL)

		return strSQL

	#
	# determine and store table definitions
	#
	def initialize_table_defs(self):
		self.logger.debug("Setting up table defs..")

		strSchema = self.dictConfig['db_schema_reveal']
		strAssessmentID = self.dictConfig['assessment_id']
		strItemTableSuffix = self.dictConfig['item_table_suffix']
		strIndexTableSuffix = self.dictConfig['index_table_suffix']
		table_specs = self.dictConfig['table_specs']

		self.tablesList = []
		self.annotationTableDefs = []
		self.tableDefs = {}
		self.tableColNames = {}
		self.tableColDefs = {}

		for tableSpec in table_specs:
			table_type = tableSpec['table_type']

			if table_type == 'annotation':
				strAnnotation = tableSpec['annotation_label']
				strTable = strAnnotation
				strTableName = '{0}_db_{1}'.format(strAssessmentID, strTable)
				strTableFullName = '{0}.{1}'.format(strSchema, strTableName)
				strKeyCol = strTable + '_key'
				strIndexTableName = strTableFullName + '_' + strIndexTableSuffix
				annotationTableDef = (strAnnotation, strTableFullName, strIndexTableName, strKeyCol)
				self.logger.debug(annotationTableDef)
				self.annotationTableDefs.append(annotationTableDef)
				self.tablesList.append(strTable)
				self.initialize_table_def_lookup(table_type, strTable, strTableName, tableSpec)
			elif table_type == 'item':
				strTable = strItemTableSuffix
				self.dictConfig['item_table'] = strTable
				strTableName = '{0}_db_{1}'.format(strAssessmentID, strTable)
				self.tablesList.append(strTable)
				self.initialize_table_def_lookup(table_type, strTable, strTableName, tableSpec)
			else:
				raise Exception('Illegal table_type: ' + table_type)

	#
	# Create lookup (dict) for table definition/spec
	#
	def initialize_table_def_lookup(self, table_type, strTable, table_short_name, tableSpec):
		strSchema = self.dictConfig['db_schema_reveal']
		strAssessmentID = self.dictConfig['assessment_id']
		table_name = '{0}.{1}'.format(strSchema, table_short_name)
		column_spec = tableSpec['column_spec']
		self.logger.debug('Defining table def lookup for {0} {1}: {2}'.format(table_type, strTable, table_name))

		max_assess_id_length = int(self.dictConfig['max_assess_id_length'])
		if len(strAssessmentID) > max_assess_id_length:
			raise Exception( 'assessment_id too long (length = {0}, max_length = {1}): {2}'.format(len(strAssessmentID),max_assess_id_length,strAssessmentID))

		max_table_length = int(self.dictConfig['max_table_length'])
		if len(table_short_name) > max_table_length:
			raise Exception('Table name too long (length = {0}, max_length = {1}): {2}'.format(len(table_short_name),max_table_length,table_name))

		listColNames = []
		dictColDefs = {}

		index_col_types = []

		if 'index_cols' in tableSpec:
			index_cols = tableSpec['index_cols']
			self.logger.debug('Table {0} has index_cols: {1}'.format(repr(strTable), index_cols))
		else:
			raise Exception("No 'index_cols' parameter in table definition: {0}".format(repr(strTable)))

		mutable_cols = []
		if 'mutable_cols' in tableSpec:
			mutable_cols = tableSpec['mutable_cols']
			self.logger.debug('Table {0} has mutable_cols: {1}'.format(repr(strTable), mutable_cols))

		for col in column_spec:
			col_name = col[0]  # column name
			col_create_sql = col[1]  # SQL for creating column
			col_default = None  # default value for column (optional)
			col_has_default = False  # need flag to specify if default value is set (as None value is acceptable as a default value itself)

			# Get default value, if specified
			if len(col) >= 3:
				col_default = col[2]  # default value
				col_has_default = True

			# Get column type from column SQL (first word)
			col_type = re.split("[ (]", col_create_sql)[0]  # basic type for column

			if col_name in index_cols:
				index_col_types.append(col_type)

			# self.logger.debug('{:s}, {:s}, {:s}, {:s}'.format( repr(col_name), repr(col_type), repr(col_create_sql), repr(col_default)) )

			listColNames.append(col_name)
			dictColDefs[col_name] = (
				col_type, col_create_sql, col_default,
				col_has_default)  # TODO: would be better to define as an object here

		self.logger.debug(listColNames)
		self.logger.debug(dictColDefs)

		tableDef = {}
		tableDef['table_name'] = table_name
		tableDef['table_type'] = table_type
		tableDef['primary_key'] = strTable + '_key'
		tableDef['primary_key_constraint_name'] = '{0}_db_{1}_pkey'.format(strAssessmentID, strTable)

		# We should now have either index_col or index_cols defined
		if index_cols is None or len(index_cols) == 0:
			raise Exception(
				"No UNIQUE column nor index_cols parameter defined in {0} table: {1}".format(table_type, strTable));

		tableDef['index_cols'] = index_cols
		tableDef['index_col_types'] = index_col_types
		tableDef['mutable_cols'] = mutable_cols
		self.tableDefs[strTable] = tableDef
		self.tableColNames[strTable] = listColNames
		self.tableColDefs[strTable] = dictColDefs

	#
	# get insert SQL and tuple data from jsonItem
	#
	def get_insert_item_query(self, strTable, strInsertOrUpdateTemplateName, strInsertOrSelectTemplateName, jsonItem, bAssertImmutableCols = True):
		tableDef = self.tableDefs[strTable]
		index_cols = tableDef['index_cols']  # e.g. ['osm_id', 'shape']
		if 'mutable_cols' in tableDef :
			mutable_cols = tableDef['mutable_cols']  # e.g. ['osm_id', 'shape']
		else :
			mutable_cols = []
		listColNames = self.tableColNames[strTable]  # get ordered column names

		# Lookup column defs for table
		dictColDefs = self.tableColDefs[strTable]

		listInsertCols = []
		listUpdateCols = []
		listInsertColFormats = []
		listUpdateColFormats = []

		unique_val_tuple = ()  # now set below
		insert_tuple = ()
		update_tuple = ()
		geometry_format = '%s'  # default format (e.g. for null value)

		# Set unique col vals to None to start with
		# These will be overridden by JSON values, if present
		uniqueColVals = {}
		for col in index_cols:
			uniqueColVals[col] = None

		for col in jsonItem :
			if col not in listColNames:
				raise Exception('Unknown annotation: {0}'.format(col))

		for col in listColNames:  # loop through columns in correct order
			if col not in jsonItem :
				continue

			# remove any geom column if we have the remove flag set. this is because sending a SQL query with a text encoded geometry can be very verbose and
			# extremely slow (e.g. 4 inserts per second) which is not acceptable. instead insert with geoms removed then insert again (with geom this time) if item is new to ensure value is correct
			if (bAssertImmutableCols == False) and (not col in mutable_cols) and (not col in index_cols) :
				continue

			(col_type, col_create_sql, col_default, col_has_default) = dictColDefs[col]
			# self.logger.debug('{:s}, {:s}, {:s}, {:s}'.format( repr(col), repr(col_type), repr(col_create_sql), repr(col_default)) )

			if '[' in col_type:
				col_val = list(jsonItem[col])
			else:
				col_val = jsonItem[col]

			if col_type == 'geometry':
				if col_val is not None and len(col_val) > 0:
					col_format = 'ST_GeomFromText(%s,4326)'
				else:
					col_val = None
					# col_format = 'null'
					col_format = '%s'
				geometry_format = col_format
			else:
				col_format = '%s::{0}'.format(col_type)

			if col in index_cols:
				listInsertCols.append(col)
				listInsertColFormats.append(col_format)
				insert_tuple += (col_val,)
				uniqueColVals[col] = col_val
			else:
				listUpdateCols.append(col)
				listUpdateColFormats.append(col_format)
				update_tuple += (col_val,)

		whereCond = []

		for col in index_cols:
			(col_type, col_create_sql, col_default, col_has_default) = dictColDefs[col]

			if uniqueColVals[col] is not None:
				if col_type == 'geometry':
					col_format = geometry_format
				else:
					col_format = '%s::{0}'.format(col_type)
				whereCondStr = '{0}={1}'.format(col, col_format)
				unique_val_tuple += (uniqueColVals[col],)
			else:
				whereCondStr = '{0} IS NULL'.format(col, col_format)

			whereCond.append(whereCondStr)

		where_clause = ' AND '.join(whereCond)

		listInsertCols += listUpdateCols
		listInsertColFormats += listUpdateColFormats
		insert_tuple += update_tuple

		self.logger.debug(listInsertCols)
		self.logger.debug(listInsertColFormats)
		self.logger.debug(listUpdateCols)
		self.logger.debug(listUpdateColFormats)

		insert_cols = ', '.join(listInsertCols)  # e.g. 'source_uri, text, lang'
		insert_data_formats = ', '.join(listInsertColFormats)  # e.g. "%s::text, %s::text, %s::text"
		update_cols = ', '.join(listUpdateCols)  # e.g. 'text, lang'
		update_data_formats = ', '.join(listUpdateColFormats)  # e.g. "%s::text, %s::text"

		self.logger.debug('unique_val_tuple = {0}'.format(repr(unique_val_tuple)))
		self.logger.debug('update_cols = {0}'.format(repr(update_cols)))
		self.logger.debug('update_data_formats = {0}'.format(repr(update_data_formats)))
		self.logger.debug('update_tuple = {0}'.format(repr(update_tuple)))
		self.logger.debug('insert_cols = {0}'.format(repr(insert_cols)))
		self.logger.debug('insert_data_formats = {0}'.format(repr(insert_data_formats)))
		self.logger.debug('insert_tuple = {0}'.format(repr(insert_tuple)))

		if len(update_tuple) > 0:
			strSQL = self.sqlTemplates[strInsertOrUpdateTemplateName].format(update_cols, update_data_formats, where_clause, insert_cols, insert_data_formats, where_clause)
			tupleData = update_tuple + unique_val_tuple + insert_tuple + unique_val_tuple
		else:
			strSQL = self.sqlTemplates[strInsertOrSelectTemplateName].format(where_clause, insert_cols, insert_data_formats, where_clause)
			tupleData = unique_val_tuple + insert_tuple + unique_val_tuple

		query = (strSQL, tupleData)
		self.logger.debug('insert item query:\n' + strSQL)
		self.logger.debug('insert item tuple:\n' + repr(tupleData))

		return query

	#
	# get INSERT query for generic annotation
	#
	def get_insert_annotation_query(self, strAnnotation, jsonItem, bAssertImmutableCols = True):
		strInsertOrUpdateTemplateName = 'insert_annotation_' + strAnnotation
		strInsertOrSelectTemplateName = 'insert_or_select_annotation_' + strAnnotation
		query = self.get_insert_item_query(strAnnotation, strInsertOrUpdateTemplateName, strInsertOrSelectTemplateName,jsonItem,bAssertImmutableCols)

		return query

	#
	# get INSERT annotation index query
	#
	def get_insert_annotation_index_query(self, strAnnotation, nItemKey, nAnnotationKey):
		# Use new template
		strSQL = self.sqlTemplates['insert_annotation_index_' + strAnnotation]

		tupleData = (nItemKey, nAnnotationKey, nItemKey, nAnnotationKey)

		query = (strSQL, tupleData)
		self.logger.debug('insert annotation index query:\n' + strSQL)
		self.logger.debug('insert annotation index tuple:\n' + repr(tupleData))

		return query

	#
	# export annotations from database
	#
	def export_annotations(self):
		return self.export_table_annotations_with_source_uri('author')

	#
	# export annotations from table, including corresponding source_uri
	#
	def export_table_annotations_with_source_uri(self, table):
		sqlHandler = self.get_sql_handler()
		nTimeoutStatement = int(self.dictConfig['timeout_statement'])
		nTimeoutOverall = int(self.dictConfig['timeout_overall'])

		strSQL = '''
SELECT 
  assessment_id_1_db_item.source_uri,
  assessment_id_1_db_author.author_entity, 
  assessment_id_1_db_author.inference 
FROM 
  reveal.assessment_id_1_db_author_item_index, 
  reveal.assessment_id_1_db_author, 
  reveal.assessment_id_1_db_item
WHERE 
  assessment_id_1_db_author_item_index.author_key = assessment_id_1_db_author.author_key AND
  assessment_id_1_db_author_item_index.item_key = assessment_id_1_db_item.item_key;
		'''
		self.logger.debug('select annotations query:\n' + strSQL)
		tupleData = ()
		query = (strSQL, tupleData)
		selectResult = sqlHandler.execute_sql_query(query, nTimeoutStatement, nTimeoutOverall)
		self.logger.debug('select annotations result: {0}'.format(selectResult))

		annotations = []

		for row in selectResult:
			dictEntry = {}

			(source_uri, author_entity, inference) = row
			self.logger.debug('{0}, {1}, {2}'.format(source_uri, author_entity, inference))

			dictEntry['item:source_uri'] = source_uri
			dictEntry[table + ':author_entity'] = author_entity
			dictEntry[table + ':inference'] = inference

			annotations.append(dictEntry)

		self.logger.debug('exported annotations: {0}'.format(annotations))
		return annotations

	#
	# export annotations from table
	#
	def export_table_annotations(self, table):
		sqlHandler = self.get_sql_handler()
		strSchema = self.dictConfig['db_schema_reveal']
		nTimeoutStatement = int(self.dictConfig['timeout_statement'])
		nTimeoutOverall = int(self.dictConfig['timeout_overall'])

		tableDef = self.tableDefs[table]
		primary_key = tableDef['primary_key']
		table_full_name = tableDef['table_name']
		table_name = re.split('\.', table_full_name)[1]

		strSQL = "SELECT column_name FROM information_schema.columns WHERE table_schema={0} AND table_name={1}" \
			.format(repr(strSchema), repr(table_name))

		tupleData = ()
		self.logger.debug('select columns query:\n' + strSQL)
		query = (strSQL, tupleData)

		columnsResult = sqlHandler.execute_sql_query(query, nTimeoutStatement, nTimeoutOverall)
		self.logger.debug('select columns result: {0}'.format(columnsResult))

		cols = []
		for col in columnsResult:
			cols.append(col[0])

		self.logger.debug('column names: {0}'.format(cols))

		strSQL = 'SELECT * FROM {0};'.format(table_full_name)
		self.logger.debug('select items query:\n' + strSQL)
		query = (strSQL, tupleData)
		selectResult = sqlHandler.execute_sql_query(query, nTimeoutStatement, nTimeoutOverall)
		self.logger.debug('select items result: {0}'.format(selectResult))

		annotations = []

		for row in selectResult:
			dictEntry = {}

			for i, col in enumerate(cols):
				if col == primary_key:
					continue

				self.logger.debug('{0} : {1} {2}'.format(repr(col), str(row[i]), type(row[i])))

				key = table + ':' + col

				if type(row[i]) is datetime.datetime:
					colVal = str(row[i])
				else:
					colVal = row[i]

				dictEntry[key] = colVal

			annotations.append(dictEntry)

		self.logger.debug('exported annotations: {0}'.format(annotations))
		return annotations

	# QUERIES

	#
	# query data
	# | note : unicode characters are returned as <str> 8-bit UTF-8 encoded strings. You can get back to <unicode> using strResultString.decode( 'utf-8' ).
	#
	def query_data(self, query, nTimeoutStatement=None, nTimeoutOverall=None):
		sqlHandler = self.get_sql_handler()

		if nTimeoutStatement is None:
			nTimeoutStatement = int(self.dictConfig['timeout_statement'])

		if nTimeoutOverall is None:
			nTimeoutOverall = int(self.dictConfig['timeout_overall'])

		params = self.getParams(query)
		strSQL = self.getSubClause(query, params)

		self.logger.debug('sql query : ' + repr( strSQL ))

		sqlQuery = self.getSQLquery(strSQL, params)
		
		self.logger.debug('SQL query:\n\n' + repr(sqlQuery))
		
		listQueryResult = sqlHandler.execute_sql_query(sqlQuery, nTimeoutStatement, nTimeoutOverall)

		return listQueryResult

	#
	# get params from query
	#
	def getParams(self, query):

		if 'params' not in query:
			self.logger.debug('No params defined')
			return None

		paramDefs = query['params']

		if paramDefs is None:
			self.logger.debug('No params defined')
			return None

		self.logger.debug('Extracting params...')

		paramNames = []
		paramTags = []
		paramValues = []
		paramNameValues = {}
		paramTagValues = {}

		for paramDef in paramDefs:
			self.logger.debug('name = {0}, tag = {1}, value = {2}'.format(paramDef['name'], paramDef['tag'], str(paramDef['value'])))

			paramName = paramDef['name']
			paramTag = paramDef['tag']
			paramValue = paramDef['value']

			paramNames.append(paramName)
			paramTags.append(paramTag)
			paramValues.append(paramValue)
			paramNameValues[paramName] = paramValue
			paramTagValues[paramTag] = paramValue

		self.logger.debug('Names: {0}'.format(paramNames))
		self.logger.debug('Tags: {0}'.format(paramTags))
		self.logger.debug('Values: {0}'.format(paramValues))
		self.logger.debug('Name:Values: {0}'.format(paramNameValues))
		self.logger.debug('Tag:Values: {0}'.format(paramTagValues))

		params = {}

		params['names'] = paramNames
		params['tags'] = paramTags
		params['values'] = paramValues
		params['nameValues'] = paramNameValues
		params['tagValues'] = paramTagValues

		self.logger.debug('Params: {0}'.format(params))
		return params

	#
	# convert value to list
	#
	def getSubClause(self, query, params, joinAliases=[]):
		if 'select' not in query:
			raise Exception("No 'select' entry in query {0}".format(query))

		if ('from' not in query) and ('join' not in query) :
			raise Exception("No 'from' ir 'join' entry in query {0}".format(query))

		clausesList = []
		joinClauses = None

		# Create JOIN clause (optional)
		hasJoin = 'join' in query
		# self.logger.debug('hasJoin = {0}'.format(hasJoin))
		if hasJoin:
			joinClauses = []
			joinEntry = query['join']
			self.logger.debug('joinEntry type: {0}'.format(type(joinEntry)))

			# If joinEntry is a list of joins, use this. Otherwise create list from the joinEntry
			if type(joinEntry) == list:
				joinEntriesList = joinEntry
			else:
				joinEntriesList = [joinEntry]

			for joinEnt in joinEntriesList:
				if 'alias' in joinEnt:
					joinAlias = joinEnt['alias']
				else:
					intAlias = len(joinAliases) + 1
					joinAlias = 'join' + str(intAlias)

				joinAliases.append(joinAlias)

				joinClause = self.getSubClause(joinEnt, params, joinAliases)
				joinClauses.append((joinClause, joinAlias))

		# Create SELECT clause
		selectEntry = query['select']

		if selectEntry is None:
			raise Exception("'select' clause is 'None' in query: {0}".format(query))

		selectStr = ', '.join(self.toList(selectEntry))
		selectClause = 'SELECT {0}'.format(selectStr)
		clausesList.append(selectClause)

		# Create FROM clause
		if 'from' in query :
			fromEntry = query['from']
		else :
			fromEntry = []

		fromList = self.toList(fromEntry)
		fromStr = ',\n'.join(self.getTableNames(fromList))

		# Append JOIN clause(s) if present
		if joinClauses is not None:
			if len(joinClauses) > 0:
				joinStrs = []

				if len(fromList) > 0:
					fromStr += ',\n'

				for joinTuple in joinClauses:
					(joinClause, joinAlias) = joinTuple
					joinStr = '({0}) AS {1}'.format(joinClause, joinAlias)
					joinStrs.append(joinStr)

				joinsStr = ',\n'.join(joinStrs)
				fromStr += joinsStr

		fromClause = 'FROM {0}'.format(fromStr)
		clausesList.append(fromClause)

		# Create WHERE clause (optional)
		hasWhere = 'where' in query
		# self.logger.debug('hasWhere = {0}'.format(hasWhere))
		if hasWhere:
			whereEntry = query['where']
			if whereEntry is not None:
				whereStr = '\nAND '.join(self.toList(whereEntry))
				whereClause = 'WHERE {0}'.format(whereStr)
				clausesList.append(whereClause)

		# Create GROUP BY clause (optional)
		hasGroupBy = 'group' in query
		# self.logger.debug('hasGroupBy = {0}'.format(hasGroupBy))
		if hasGroupBy:
			groupByEntry = query['group']
			if groupByEntry is not None:
				groupByStr = ', '.join(self.toList(groupByEntry))
				groupByClause = 'GROUP BY {0}'.format(groupByStr)
				clausesList.append(groupByClause)

		# Create ORDER BY clause (optional)
		hasOrderBy = 'order' in query
		# self.logger.debug('hasOrderBy = {0}'.format(hasOrderBy))
		if hasOrderBy:
			orderByEntry = query['order']
			if orderByEntry is not None:
				orderByStr = ', '.join(self.toList(orderByEntry))
				orderByClause = 'ORDER BY {0}'.format(orderByStr)
				clausesList.append(orderByClause)

		# Create LIMIT clause (optional)
		hasLimit = 'limit' in query
		# self.logger.debug('hasLimit = {0}'.format(hasLimit))
		if hasLimit:
			limitEntry = query['limit']
			if limitEntry is not None:
				if type(limitEntry) == str:
					limitClause = 'LIMIT {0}'.format(limitEntry)
				else:
					limitClause = 'LIMIT {0}'.format(limitEntry)

				clausesList.append(limitClause)

		strSQL = '\n'.join(clausesList)

		return strSQL

	#
	# convert value to list
	#
	def toList(self, val):
		if type(val) is list:
			return val
		else:
			newList = []
			newList.append(val)
			return newList

	#
	# get full table names for given tables
	#
	def getTableNames(self, tables):
		strIndexTableSuffix = self.dictConfig['index_table_suffix']
		tableNames = []
		for table in tables:
			if table.endswith('_index'):
				annotation = table.replace('_index', '')
			else:
				annotation = table

			tableDef = self.tableDefs[annotation]
			table_name = tableDef['table_name']

			if table.endswith('_index'):
				table_name = '{0}_{1}'.format(table_name, strIndexTableSuffix)

			tableNames.append(table_name + ' AS ' + table)

		return tableNames

	#
	# get SQL query (text), with data tuple
	#
	def getSQLquery(self, sourceSQL, params):

		valuesTuple = ()

		self.logger.debug('Source SQL:\n{0}'.format(sourceSQL))

		# matches any tag, e.g. '${LOCATION}', '${TIME0}' and extracts tag itself (e.g. 'LOCATION') as a group
		tagRegex = re.compile('\${(\w+)}')
		matches = tagRegex.finditer(sourceSQL)  # find all tags (see above)

		if params is None:
			return (sourceSQL, None)

		paramTagValues = params['tagValues']

		self.logger.debug('Tag values:')

		for match in matches:
			tag = match.group(1)  # extract the tag itself
			val = paramTagValues[tag]  # get the value for the tag
			self.logger.debug('{0} = {1}'.format(tag, str(val)))
			valuesTuple += (val,)  # add val to the tuple

		strSQL = tagRegex.sub('%s', sourceSQL)  # replace all tags with '%s'
		self.logger.debug('strSQL:\n{0}'.format(strSQL))
		self.logger.debug('tuple: {0}'.format(valuesTuple))

		return (strSQL, valuesTuple)

	def get_sql_handler(self):
		if self.dbHandler is None:
			raise Exception('sqlHandler is None (hint: close_db already called?)')
		return self.dbHandler


