""" main source for Flint "Because our fortran code stinks"""

import sys


BLOCKS = [
    "PROGRAM",
    "SUBROUTINE",
    "MODULE",
    "FUNCTION",
]

__all__ = ["struct_analysis", "print_errors", "print_score"]

class LangFtn():
    """ class with all info and function specific to a fortran statement
    """

    def __init__(self, raw_st):

        lowerblck = [str_.lower() for str_ in BLOCKS]
        self.block_lst = lowerblck
       
        self.raw_st = raw_st
        self.statement_lst = list()
        self._str_to_statements()

    def _str_to_statements(self):
        """ transform a raw code into a list of statement
        initialize the self.statement_lst
        """
        # TODO : perform continuations
        ass_st = str()
        for char in self.raw_st:
            if char == "\n":
                self.statement_lst.append(ass_st)
                ass_st = str()
            ass_st += char
        self.statement_lst.append(ass_st)

    def bstart(self, statement):
        """ return true when statement is a starting block
        """
        clean_st = rm_comment(statement)
        clean_st = clean_st.lower()
        # needed else end block  can be understood as start
        out = False
        for st_match in self.block_lst:
            if clean_st.startswith(st_match):
                out = True
                self.cur_block = clean_st.split()[1]

        return out

    def bstop(self, statement):
        """ return true when statement is an ending block
        """
        clean_st = rm_comment(statement)
        clean_st = clean_st.lower()
        for st_match in self.block_lst:
            if clean_st.startswith("end " + st_match):
                return True
        return False


def testifdo(statement, cur_ifdo, cur_depth):
    """ return true when statement is a starting block
    """
    clean_st = rm_comment(statement)
    # needed else end block  can be understood as start

    for st_match in ["IF", "DO", "if", "do"]:
        if clean_st.startswith(st_match):
            cur_ifdo += 1
            cur_depth = max(cur_depth, cur_ifdo)

        for ending in ["END", "END ", "end", "end "]:
            if clean_st.startswith(ending + st_match):
                cur_ifdo -= 1

    return cur_ifdo, cur_depth


def rm_comment(statement_str):
    """remove comment in statement_string
    """
    if statement_str[0] in ["!", "c", "C"]:
        return str()
    if "!" in statement_str:
        return statement_str.split("!")[0]
    return statement_str.strip()


def get_arguments(head):
    """ get arguments in the header of a block
    """
    start_idx = head.find("(") + 1
    end_idx = head.find(")")
    list_args = head[start_idx: end_idx].split(",")
    list_args = [name.strip() for name in list_args]
    return list_args


def get_variables(statement_lst):
    """ identifie a declaration line and give the list of varaibles
    """
    types_lst = ["REAL",
                 "DOUBLE PRECISION",
                 "LOGICAL",
                 "INTEGER",
                 "CHARACTER"]
    list_var = list()
    for statement in statement_lst:
        for typename in types_lst:
            if statement.startswith(typename):
                if "::" in statement:
                    list_var.extend(statement.split("::")[-1].split(","))
    list_var = [name.strip() for name in list_var]
    return list_var


def test_blockst(statement_lst):
    """ analysis of a block """

    print("Analysis of :", statement_lst[0])
    clean_statement_lst = list(filter(None, (rm_comment(st)
                                             for st in statement_lst)))
    out = {
        "statements": clean_statement_lst,
        "args": get_arguments(statement_lst[0]),
        "locals": list(),
        "errors": list()
    }
    for name in get_variables(clean_statement_lst):
        if name not in out["args"]:
            out["locals"].append(name)

    cur_ifdo = 0
    cur_depth = 0
    for statement in clean_statement_lst:
        cur_ifdo, cur_depth = testifdo(
            statement, cur_ifdo, cur_depth)
    
    out["errors"].extend(statements_errors(clean_statement_lst))
    out["errors"].extend(vars_errors(out["locals"]))
    out["errors"].extend(args_errors(out["args"]))
    out["errors"].extend(ifdoerrors(cur_depth))

    return out


def statements_errors(stt_list):
    out = list()
    lstat = len(stt_list)
    if lstat > 50:
        out.append("too-many-lines : " + str(lstat) + "/50")

    for stat in stt_list:
        if len(stat) > 100:
            out.append("line-too-long : " + str(len(stat)) + "/100")
    return out


def vars_errors(var_list):
    out = list()
    lstat = len(var_list)
    if lstat > 12:
        out.append("too-many-locals : " + str(lstat) + "/12")

    for varname in var_list:
        if len(varname) < 3:
            out.append("invalid-name : local var " + varname + " is too short")
    return out


def ifdoerrors(maxdepth):
    out = list()
    if maxdepth > 5:
        out.append(
            "too-many-levels : " +
            str(maxdepth) +
            "/5 nested IF and DO blocks")

    return out


def args_errors(arg_list):
    out = list()
    larg = len(arg_list)
    if larg > 5:
        out.append("too-many-arguments : " + str(larg) + "/5")

    for varname in arg_list:
        if len(varname) < 3:
            out.append("invalid-name : argument " + varname + " is too short")
    return out


def print_errors(info_errors):

    for block in info_errors:
        print(block + " :")
        for err in info_errors[block]["errors"]:
            print("  ", err)


def print_score(info_errors):

    tot_stat = 0
    tot_errors = 0
    for block in info_errors:
        tot_stat += len(info_errors[block]["statements"])
        tot_errors += len(info_errors[block]["errors"])

    if tot_stat == 0:
        print("No statement found... ")
        score = 10
    else:
        score = 10 - (tot_errors / tot_stat) * 100

    print("\n------------------------------------------------------------------")
    print("Your code has been rated at " + '{0:4.2f}'.format(score) + "/10\n")


def struct_analysis(st_code):
    """ split a code into blocks
    st_code : raw string of file with carriage returns
    output a dictionary of blocks
    """
    code = LangFtn(st_code)
    buff_list = list()
    out = dict()
    for statement in code.statement_lst:
        buff_list.append(statement)
        if code.bstart(statement):
            buff_list = [statement]
            continue

        if code.bstop(statement):
            out[code.cur_block] = test_blockst(buff_list)
            buff_list = list()
            continue
    return out
