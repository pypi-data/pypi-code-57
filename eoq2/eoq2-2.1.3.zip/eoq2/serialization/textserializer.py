'''
 Bjoern Annighoefer 2019
 Modified: Christian Mollière 2020
'''

from .serializer import Serializer

from ..query.query import QRY_SYMBOLS, QrySegTypes, Qry, Obj, His, Cls, Ino, Met, Idx, Pth, Arr, Equ, Eqa, Neq, Les, \
    Gre, Not, Zip, All, Any
from ..command.command import CmdTypes, Get, Set, Add, Rem, Mov, Clo, Crt, Crn, Sts, Chg, Gaa, Cal, Asc, Abc, Cmp, Umm, \
    Rmm, Gmm, Obs, Ubs, Hel, Ses, Gby
from ..util.error import EoqError

from copy import deepcopy
from enum import Enum
import re

"""
    CONSTANTS & SETTINGS
"""

# Create dictionary from external symbol definition.
# This will be needed later to convert i.e. "!" -> "CLS"
SYMBOLS_2_QRY_DICT = dict((v, k) for k, v in QRY_SYMBOLS.items())

# List all commands that need a list of args and not *args or a mix
QRY_CMDS_W_LIST_INPUT = ["[", "&ZIP", "&EQA"]
QRY_CMDS_W_SINGLE_OR_LIST_INPUT = [":"]
QRY_CMDS_W_MIXED_INPUT = ["@"]

# Settings of divider symbols
EXPRESSION_DIVIDERS = [";", "\r", "\n"]
QRY_ARG_DIVIDER = ","
CMD_ARG_DIVIDER = " "

# Do not change! This way parsing is needed for re.split
EXPRESSION_DIVIDERS_ = "[" + "".join(EXPRESSION_DIVIDERS) + "]"

# Change this constant to control the context distance of
# the error message if parsing fails.
ERROR_MSG_VIEW_DISTANCE = 3

# Assign stop symbols to starters
STOPPING_SYMBOL_DICT = {
    "(": ")",
    "{": "}",
    "[": "]",
}


def DoNothing(*args, **kwargs):
    """ placeholder for unimplemented functions """
    pass


class ParsingCmds(Enum):
    STEP_IN = "INN"
    STEP_OUT = "OUT"


'''
    TEXT Serializer   
'''


class TextSerializer(Serializer):
    def __init__(self):
        """
            TEXTSERIALIZER implements a translation between EOQ expressions and Python commands to
            interact with the EOQ database.
        """

        """
            Toggles verbose output of construction steps within Des()
        """
        self._debugMode = False

        """
            PY2TXT Translators
        """
        self.cmdTranslator = lambda o: o.cmd + " " + self.Ser(o.a)

        self.qryTranslators = {
            QrySegTypes.OBJ: lambda o: QRY_SYMBOLS[QrySegTypes.OBJ] + self.Ser(o.v),
            QrySegTypes.HIS: lambda o: QRY_SYMBOLS[QrySegTypes.HIS] + self.Ser(o.v),
            QrySegTypes.PTH: lambda o: QRY_SYMBOLS[QrySegTypes.PTH] + self.Ser(o.v),
            QrySegTypes.CLS: lambda o: QRY_SYMBOLS[QrySegTypes.CLS] + self.Ser(o.v),
            QrySegTypes.INO: lambda o: QRY_SYMBOLS[QrySegTypes.INO] + self.Ser(o.v),
            QrySegTypes.MET: lambda o: QRY_SYMBOLS[QrySegTypes.MET] + "(" + self.Ser(o.v[0]) + (
                "," + self.Ser(o.v[1:]) if len(o.v) > 1 else "") + ")",
            QrySegTypes.NOT: lambda o: QRY_SYMBOLS[QrySegTypes.NOT],
            QrySegTypes.TRM: lambda o: QRY_SYMBOLS[QrySegTypes.TRM] + "(" + self.Ser(o.v[0]) + "," + self.Ser(
                o.v[1]) + ")",
            QrySegTypes.IDX: lambda o: QRY_SYMBOLS[QrySegTypes.IDX] + self.Ser(o.v),
            QrySegTypes.SEL: lambda o: "{" + self.Ser(o.v) + "}",
            QrySegTypes.ARR: lambda o: "[" + ",".join([self.Ser(a) for a in o.v]) + "]",
            QrySegTypes.ZIP: lambda o: QRY_SYMBOLS[QrySegTypes.ZIP] + self.Ser(o.v),
            QrySegTypes.QRY: lambda o: "(" + "".join([self.Ser(a) for a in o.v]) + ")",
            QrySegTypes.ANY: lambda o: QRY_SYMBOLS[QrySegTypes.ANY] + self.Ser(o.v),
            QrySegTypes.ALL: lambda o: QRY_SYMBOLS[QrySegTypes.ALL] + self.Ser(o.v),
            QrySegTypes.EQU: lambda o: QRY_SYMBOLS[QrySegTypes.EQU] + self.Ser(o.v),
            QrySegTypes.EQA: lambda o: QRY_SYMBOLS[QrySegTypes.EQA] + self.Ser(o.v),
            QrySegTypes.NEQ: lambda o: QRY_SYMBOLS[QrySegTypes.NEQ] + self.Ser(o.v),
            QrySegTypes.LES: lambda o: QRY_SYMBOLS[QrySegTypes.LES] + self.Ser(o.v),
            QrySegTypes.GRE: lambda o: QRY_SYMBOLS[QrySegTypes.GRE] + self.Ser(o.v),
            QrySegTypes.ADD: lambda o: QRY_SYMBOLS[QrySegTypes.ADD] + self.Ser(o.v),
            QrySegTypes.SUB: lambda o: QRY_SYMBOLS[QrySegTypes.SUB] + self.Ser(o.v),
            QrySegTypes.MUL: lambda o: QRY_SYMBOLS[QrySegTypes.MUL] + self.Ser(o.v),
            QrySegTypes.DIV: lambda o: QRY_SYMBOLS[QrySegTypes.DIV] + self.Ser(o.v),
            QrySegTypes.ORR: lambda o: QRY_SYMBOLS[QrySegTypes.ORR] + self.Ser(o.v),
            QrySegTypes.XOR: lambda o: QRY_SYMBOLS[QrySegTypes.XOR] + self.Ser(o.v),
            QrySegTypes.AND: lambda o: QRY_SYMBOLS[QrySegTypes.AND] + self.Ser(o.v),
            QrySegTypes.NAD: lambda o: QRY_SYMBOLS[QrySegTypes.NAD] + self.Ser(o.v),
            QrySegTypes.CSP: lambda o: QRY_SYMBOLS[QrySegTypes.CSP] + self.Ser(o.v),
            QrySegTypes.ITS: lambda o: QRY_SYMBOLS[QrySegTypes.ITS] + self.Ser(o.v),
            QrySegTypes.DIF: lambda o: QRY_SYMBOLS[QrySegTypes.DIF] + self.Ser(o.v),
            QrySegTypes.UNI: lambda o: QRY_SYMBOLS[QrySegTypes.UNI] + self.Ser(o.v),
            QrySegTypes.CON: lambda o: QRY_SYMBOLS[QrySegTypes.CON] + self.Ser(o.v)
        }
        self.priTranslators = {
            # primitive types
            bool: lambda o: str(o),
            int: lambda o: str(o),
            float: lambda o: str(o),
            str: lambda o: "'" + o + "'",
            list: lambda o: "(%s)" % (",".join([self.Ser(x) for x in o])),
            type(None): lambda o: str(o)
        }

        self.lastTranslation = None

        """
            TXT2PY Constructors
        """
        self.cmdConstructors = {
            # these are only the base constructors
            # chained constructors are handled separately
            # args is a list
            CmdTypes.GET: lambda args: Get(*args),
            CmdTypes.SET: lambda args: Set(*args),
            CmdTypes.ADD: lambda args: Add(*args),
            CmdTypes.REM: lambda args: Rem(*args),
            CmdTypes.MOV: lambda args: Mov(*args),
            CmdTypes.CLO: lambda args: Clo(*args),
            CmdTypes.CRT: lambda args: Crt(*args),
            CmdTypes.CRN: lambda args: Crn(*args),
            CmdTypes.HEL: lambda args: Hel(*args),
            CmdTypes.GBY: lambda args: Gby(*args),
            CmdTypes.SES: lambda args: Ses(*args),
            CmdTypes.GMM: lambda args: Gmm(),
            CmdTypes.RMM: lambda args: Rmm(*args),
            CmdTypes.UMM: lambda args: Umm(*args),
            CmdTypes.STS: lambda args: Sts(),
            CmdTypes.CHG: lambda args: Chg(*args),
            CmdTypes.OBS: lambda args: Obs(*args),
            CmdTypes.UBS: lambda args: Ubs(*args),
            CmdTypes.GAA: lambda args: Gaa(*args),
            CmdTypes.CAL: lambda args: Cal(*args),
            CmdTypes.ASC: lambda args: Asc(*args),
            CmdTypes.ABC: lambda args: Abc(*args),
            CmdTypes.CST: lambda args: DoNothing(),
            CmdTypes.CMP: lambda args: Cmp()
        }
        self.qryConstructors = {
            # these are only the base constructors
            # chained constructors are handled separately
            # args is a list
            QrySegTypes.OBJ: lambda args: Obj(*args),
            QrySegTypes.HIS: lambda args: His(*args),
            QrySegTypes.PTH: lambda args: Pth(*args),
            QrySegTypes.CLS: lambda args: Cls(*args),
            QrySegTypes.INO: lambda args: Ino(*args),
            QrySegTypes.MET: lambda args: Met(args[0], args[1:]),
            QrySegTypes.NOT: lambda args: Not(),
            QrySegTypes.IDX: lambda args: Idx(args),
            QrySegTypes.ARR: lambda args: Arr(args),
            QrySegTypes.ZIP: lambda args: Zip(args),
            QrySegTypes.QRY: lambda args: args if len(args) else Qry(),
            QrySegTypes.ANY: lambda args: Any(*args),
            QrySegTypes.ALL: lambda args: All(*args),
            QrySegTypes.EQU: lambda args: Equ(*args),
            QrySegTypes.EQA: lambda args: Eqa(args),
            QrySegTypes.NEQ: lambda args: Neq(*args),
            QrySegTypes.LES: lambda args: Les(*args),
            QrySegTypes.GRE: lambda args: Gre(*args)
        }
        self.combinedConstructors = {**self.cmdConstructors, **self.qryConstructors}

        # all segment symbols that are needed for segmentation of the code
        self.cmdAndQryRepresentations = list(QRY_SYMBOLS.values()) + list(CmdTypes.__dict__.values()) + ["}", "]", ")"]

    """ 
        GENERAL METHODS
    """

    def EnableDebugging(self):
        self._debugMode = True

    def DisableDebugging(self):
        self._debugMode = False

    """
        PY 2 TEXT METHODS
    """

    def _TranslateCmd(self, val):
        if val.cmd == "CMP":
            self.lastTranslation = "CMD"
            return ";".join([self.Ser(command) for command in val.a])
        self.lastTranslation = "CMD"
        return self.cmdTranslator(val)

    def _TranslateQry(self, val):
        if val.qry:
            self.lastTranslation = val.qry
        return self.qryTranslators[val.qry](val)

    def _TranslatePri(self, val):
        if type(val) == list:
            if self.lastTranslation == "CMD":
                res = "%s" % (" ".join([self.Ser(x) for x in val]))
            elif self.lastTranslation in ["QRY", "SEL", "ARR"]:
                res = "%s" % (",".join([self.Ser(x) for x in val]))
            else:
                res = "(%s)" % (",".join([self.Ser(x) for x in val]))
        else:
            res = self.priTranslators[type(val)](val)
        self.lastTranslation = "PRI"
        return res

    def Ser(self, val):
        """
            Translates a Python command to EOQ code
        """
        try:
            return self._TranslateCmd(val)
        except:
            try:
                return self._TranslateQry(val)
            except:
                try:
                    return self._TranslatePri(val)
                except:
                    raise EoqError(0, "Text serializer failed for %s" % (str(val)))

    """ 
        TEXT 2 PY METHODS 
    """

    @staticmethod
    def _IsCmd(segment):
        if segment in CmdTypes.__dict__.values():
            return True
        else:
            return False

    @staticmethod
    def _IsQry(segment):
        if SYMBOLS_2_QRY_DICT.get(segment, "") in QrySegTypes.__dict__.values():
            return True
        else:
            return False

    def _IsCmdOrQry(self, segment):
        if self._IsCmd(segment) or self._IsQry(segment):
            return True
        else:
            return False

    @staticmethod
    def _IsStarterSymbol(segment):
        return True if segment in ["(", "[", "{"] else False

    @staticmethod
    def _IsStopperSymbol(segment):
        return True if segment in [")", "]", "}"] else False

    @staticmethod
    def _IsQryStart(segment):
        return True if segment == "(" else False

    @staticmethod
    def _IsQryEnd(segment):
        return True if segment == ")" else False

    @staticmethod
    def _ShrinkWhitespace(segments):
        _segments = []
        for seg in segments:
            if seg == segments[-1] and seg == " ":
                pass
            else:
                _segments.append(seg)
        return _segments

    def _UnwrapSingleItemLists(self, ls):
        """
            Flattens single item lists in lists. I. e.
            [1,2,[3]] -> [1,2,3]
            [1,2,[3,4]] -> [1,2,[3,4]]
            This makes the parser more robust to unnecessary query parentheses!
        """
        if type(ls) == list:
            if len(ls) == 1:
                return self._UnwrapSingleItemLists(ls[-1])
            else:
                return [self._UnwrapSingleItemLists(item) for item in ls]
        else:
            return ls

    def _Unwrap(self, ls):
        """
            Avoids flattening of a top level single item list
        """
        ls = self._UnwrapSingleItemLists(ls)
        if type(ls) == list:
            return ls
        else:
            return [ls]

    @staticmethod
    def _IsQryDivider(segment):
        return True if segment == QRY_ARG_DIVIDER else False

    @staticmethod
    def _IsCmdDivider(segment):
        return True if segment == CMD_ARG_DIVIDER else False

    @staticmethod
    def _IsDivider(segment):
        return True if segment in [QRY_ARG_DIVIDER, CMD_ARG_DIVIDER] else False

    def _IsArgument(self, segment):
        if self._IsCmdOrQry(segment) or self._IsDivider(segment) or self._IsStopperSymbol(segment):
            return False
        else:
            return True

    def _GetSegments(self, code):
        """
        GETSEGMENTS splits a textual EOQ expression string into its segments.
        :param code: EOQ expression as a String
        :return: List of segment Strings
        """
        segments = []
        char_buffer = ""
        idx = 0
        while idx < len(code):
            # get current character
            char = code[idx]
            # get words in quotations
            if char in ["\"", "\'"]:
                if char_buffer:
                    segments.append(char_buffer)
                    char_buffer = ""
                n = 1
                while code[idx + n] != char:
                    n += 1
                segments.append("\'"+code[idx + 1:idx + n]+"\'")
                idx += n
            # get single symbol qrys or ws
            elif char in self.cmdAndQryRepresentations or self._IsDivider(char):
                if char_buffer:
                    segments.append(char_buffer)
                    char_buffer = ""
                segments.append(char)
            # get 3-char qrys or cmds
            elif code[idx: idx + 3].upper() in self.cmdAndQryRepresentations:
                if char_buffer:
                    segments.append(char_buffer)
                    char_buffer = ""
                segments.append(code[idx: idx + 3].upper())
                idx += 2
            # get &-codes
            elif char == "&":
                if char_buffer:
                    segments.append(char_buffer)
                    char_buffer = ""
                segments.append(QRY_SYMBOLS[code[idx + 1: idx + 4].upper()])
                idx += 3
            # fill char buffer otherwise
            else:
                char_buffer += char
            idx += 1
        # final buffer append
        if char_buffer:
            segments.append(char_buffer)
        # delete multiple consecutive whitespaces
        return self._ShrinkWhitespace(segments)

    def _GetBoundConstructor(self, cmd, obj):
        """
            returns a bound constructor of obj
        """
        # check if cmd takes list input
        takesList = QRY_SYMBOLS[cmd] in QRY_CMDS_W_LIST_INPUT
        takesSingleOrList = QRY_SYMBOLS[cmd] in QRY_CMDS_W_SINGLE_OR_LIST_INPUT
        takesMix = QRY_SYMBOLS[cmd] in QRY_CMDS_W_MIXED_INPUT

        # convert string to fit method names, i.e. GET -> Get
        cmd = cmd.lower().capitalize()

        # break if non-chainable
        if not hasattr(obj, cmd):
            raise EoqError(0, f"{obj} has no bound method {cmd}!")

        # construct function
        def func(args):
            if takesList:
                return getattr(obj, cmd)(args)
            elif takesMix:
                return getattr(obj, cmd)(args[0], args[1:])
            elif takesSingleOrList:
                if(1==len(args)):
                    return getattr(obj, cmd)(args[0])
                else:
                    return getattr(obj, cmd)(args)
            else:
                return getattr(obj, cmd)(*args)

        return func

    def _GetBaseConstructor(self, cmd):
        """
            returns a base constructor
        """
        return self.combinedConstructors[cmd]

    def _ConvertSegmentToFunction(self, seg, res):
        """
            Converts segment symbol to function if possible. I.e. "!" -> Cls()
        """
        if self._IsCmdOrQry(seg):
            if self._IsQry(seg):
                seg = SYMBOLS_2_QRY_DICT[seg]
            cmd = seg
            try:
                func = self._GetBoundConstructor(cmd, res[-1])
                isBoundCmd = True
            except:
                func = self._GetBaseConstructor(cmd)
                isBoundCmd = False
            return func, isBoundCmd
        else:
            raise EoqError(0, f"Segment {seg} is not convertible to a Python Function.")

    @staticmethod
    def _BalanceSteps(parsingList):
        """
            closes unclosed STEP_IN cmds, (currently unused)
        """
        toClose = 0
        for seg in parsingList:
            if seg == ParsingCmds.STEP_IN:
                toClose += 1
            elif seg == ParsingCmds.STEP_OUT:
                toClose -= 1
        for closing in range(toClose):
            parsingList.append(ParsingCmds.STEP_OUT)
        return parsingList

    @staticmethod
    def _HandlePrimitives(code):
        #find out the right primitive type
        #use the first char to decide
        val = None
        c = code[0]
        if(c == '\''): #quoted string
            val = code.strip("\'") #strip quotes
        elif(c in ['0','1','2','3','4','5','6','7','8','9','-','+']): #number
            if('.' in code): #float
                val = float(code)
            elif('E' in code): #engineering float
                val = float(code)
            else: #int
                val = int(code)
        elif(c in ['T','t','F','f']): #possible boolean
            if(code.lower() == 'true'): #Boolean True
                val = True
            elif(code.lower() == 'false'): #Boolean False
                val = False
            else: #unquoted string
                val = code  
        else: #unquoted string
            val = code 
        return val

    @staticmethod
    def _StripOuterWhitespace(code):
        return code.strip()

    def _SeparateCodes(self, code):
        codes = re.split(EXPRESSION_DIVIDERS_, code)
        return [self._StripOuterWhitespace(code) for code in codes]

    def _GetParsingList(self, segments):
        """
            Creates a list of segments and parsing commands.
            This function contains the main logic to identify EOQ syntax.
        """
        # list for result
        parsingList = []

        # buffer variables
        lastSeg = None
        cmdDividerSeen = False
        stepInSinceCmdDivider = 0  # flat counter
        stepInSinceQryStart = []  # keeps track of step ins since subqry start, list because nested qrys possible
        expectedStoppingSymbols = []  # keeps track of what stopping symbol is needed to end the current subqry

        # error handling variables
        segmentsCopy = deepcopy(segments)  # necessary for error handling

        while segments:
            seg = segments.pop(0)
            nextSeg = segments[0] if segments else None

            if self._IsStarterSymbol(seg):
                if self._IsArgument(lastSeg):
                    parsingList.append(ParsingCmds.STEP_OUT)
                    if stepInSinceQryStart:
                        stepInSinceQryStart[-1] = max(stepInSinceQryStart[-1] - 1, 0)
                    elif stepInSinceCmdDivider:
                        stepInSinceCmdDivider = max(stepInSinceCmdDivider - 1, 0)
                # keep track of subqueries
                stepInSinceQryStart.append(1)
                expectedStoppingSymbols.append(STOPPING_SYMBOL_DICT[seg])
                # handle difference between argument to subqry and cmd to subqry by shifting the expected stepout
                if self._IsCmdOrQry(lastSeg) and not self._IsStarterSymbol(lastSeg):
                    try:
                        stepInSinceQryStart[-1] += 1
                        stepInSinceQryStart[-2] -= 1
                    except:
                        pass
                # construct parsing list
                parsingList.append(seg)
                parsingList.append(ParsingCmds.STEP_IN)


            elif self._IsCmdOrQry(seg):
                if parsingList \
                        and not self._IsDivider(lastSeg) \
                        and not self._IsStarterSymbol(lastSeg) \
                        and not self._IsStopperSymbol(lastSeg):
                    # STEPOUT RULE for chained cmds and qrys, is disabled on first cmd
                    parsingList.append(ParsingCmds.STEP_OUT)
                    if stepInSinceQryStart:
                        stepInSinceQryStart[-1] = max(stepInSinceQryStart[-1] - 1, 0)
                    elif stepInSinceCmdDivider:
                        stepInSinceCmdDivider = max(stepInSinceCmdDivider - 1, 0)

                if self._IsCmdDivider(lastSeg) and self._IsCmd(seg):
                    # STEPOUT RULE for divided base cmds
                    parsingList.append(ParsingCmds.STEP_OUT)
                    stepInSinceCmdDivider = max(stepInSinceCmdDivider - 1, 0)

                # construct parsing list
                parsingList.append(seg)
                parsingList.append(ParsingCmds.STEP_IN)

                if self._IsCmd(seg):
                    # reset divider flag on new cmd to disable step balancing on first divider after a new cmd
                    cmdDividerSeen = False

                if stepInSinceQryStart:
                    # count step ins within subqrys
                    stepInSinceQryStart[-1] += 1
                elif cmdDividerSeen:
                    # count step ins within separated cmd arg blocks
                    stepInSinceCmdDivider += 1


            elif self._IsCmdDivider(seg):
                if not cmdDividerSeen:
                    cmdDividerSeen = True
                while cmdDividerSeen and stepInSinceCmdDivider:
                    # balancing step outs
                    parsingList.append(ParsingCmds.STEP_OUT)
                    stepInSinceCmdDivider -= 1


            elif self._IsQryDivider(seg):
                if stepInSinceQryStart:
                    # reset step-ins since qry to 1 start if qry divider met
                    stepIns = stepInSinceQryStart.pop()
                    while (stepIns - 1):
                        parsingList.append(ParsingCmds.STEP_OUT)
                        stepIns -= 1
                    stepInSinceQryStart.append(1)
                    parsingList.append(seg)


            elif self._IsStopperSymbol(seg):
                if not expectedStoppingSymbols:
                    # found stopping symbol without query start
                    faultyIdx = len(segmentsCopy) - len(segments)
                    errorMsg = f"\nSolving of code failed at segment {faultyIdx}\n" \
                               f"Unexpected stopping symbol {seg}\n" \
                               f"...{segmentsCopy[faultyIdx - ERROR_MSG_VIEW_DISTANCE:faultyIdx]}" \
                               f"-->{segmentsCopy[faultyIdx]}<--" \
                               f"{segmentsCopy[faultyIdx + 1:faultyIdx + 1 + ERROR_MSG_VIEW_DISTANCE]}...\n"
                    raise EoqError(0, errorMsg)
                if seg == expectedStoppingSymbols[-1]:
                    # correct stopping symbol
                    if stepInSinceQryStart:
                        stepIns = stepInSinceQryStart.pop()
                        while (stepIns):
                            parsingList.append(ParsingCmds.STEP_OUT)
                            stepIns -= 1
                    expectedStoppingSymbols.pop()
                else:
                    # wrong stopping symbol
                    faultyIdx = len(segmentsCopy) - len(segments) - 1
                    errorMsg = f"\nSolving of code failed at segment {faultyIdx}\n" \
                               f"Expected {expectedStoppingSymbols[-1]}, got {seg}\n" \
                               f"...{segmentsCopy[faultyIdx - ERROR_MSG_VIEW_DISTANCE:faultyIdx]}" \
                               f"-->{segmentsCopy[faultyIdx]}<--" \
                               f"{segmentsCopy[faultyIdx + 1:faultyIdx + 1 + ERROR_MSG_VIEW_DISTANCE]}...\n"
                    raise EoqError(0, errorMsg)


            else:
                # add argument to parsing list
                parsingList.append(seg)

            lastSeg = seg

        if expectedStoppingSymbols:
            errorMsg = f"\nSolving of code failed.\n" \
                       f"Expected {expectedStoppingSymbols[-1]} but reached end of code.\n"
            raise EoqError(0, errorMsg)

        return parsingList

    def _SolveParsingList(self, parsingList):
        """
            parses segments to actual constructors
        """
        res = []
        cmd = None
        isBoundCmd = None
        seg = None

        if self._debugMode:
            debugCounter = []

        while parsingList:

            lastSeg = seg
            seg = parsingList.pop(0)

            if self._IsCmdOrQry(seg):
                if self._debugMode:
                    # print(f"converting {seg} using res {res}")
                    debugCounter.append(seg)
                if self._IsQryDivider(lastSeg):
                    cmd, isBoundCmd = self._ConvertSegmentToFunction(seg, None)
                else:
                    cmd, isBoundCmd = self._ConvertSegmentToFunction(seg, res)

            elif seg == ParsingCmds.STEP_IN:
                if self._debugMode:
                    if isBoundCmd:
                        print(f"stepping in after bound {debugCounter[-1]}")
                    else:
                        print(f"stepping in after {debugCounter[-1]}")
                res_ = self._SolveParsingList(parsingList)
                res_ = self._Unwrap(res_)
                if res and isBoundCmd:
                    res[-1] = cmd(res_)
                elif res:
                    res.append(cmd(res_))
                else:
                    res = [cmd(res_)]

            elif seg == ParsingCmds.STEP_OUT:
                if self._debugMode:
                    print(f"stepping out returning {res}")
                return res
            elif not self._IsQryDivider(seg):
                res.append(self._HandlePrimitives(seg))

        if self._debugMode:
            print(f"stepping out with args {res}")
        return res

    def _ConstructCompound(self, commandList):
        """
            combines multiple commands to a compound
        """
        res = Cmp()
        for idx, cmd in enumerate(commandList):
            try:
                # get bound cmd for cmp
                func = getattr(res, cmd.cmd.lower().capitalize())
                # get content
                args = cmd.a
                if type(args) != list:
                    args = [args]
                # construct
                res = func(*args)
            except:
                errorMsg = f"\nSolving of code failed.\n" \
                           f"Could not add command {idx + 1} to Compound.\n"
                raise EoqError(0, errorMsg)
        return res

    def Des(self, code):
        """
            DES takes a textual representation EOQ code and constructs the cmd/qry chain
        """
        results = []
        codes = self._SeparateCodes(code)
        for code in codes:
            # split code into segments
            segments = self._GetSegments(code)
            # inject parsing commands
            parsingList = self._GetParsingList(segments)
            if self._debugMode:
                print(parsingList)
            # deepcopy parsingList for error handling
            parsingListCopy = deepcopy(parsingList)
            # solve combined segments and parsing commands
            try:
                results += self._SolveParsingList(parsingList)
            except:
                # solver failed
                faultyIdx = len(parsingListCopy) - max(1, len(parsingList))
                errorMsg = f"\nSolving of code failed at segment {faultyIdx}\n" \
                           f"...{(parsingListCopy[faultyIdx - ERROR_MSG_VIEW_DISTANCE:faultyIdx])}" \
                           f" -->{parsingListCopy[faultyIdx]}<-- " \
                           f"{(parsingListCopy[faultyIdx + 1:faultyIdx + 1 + ERROR_MSG_VIEW_DISTANCE])}...\n"
                raise EoqError(0, errorMsg)

        if len(results) == 1:
            return results[0]
        else:
            return self._ConstructCompound(results)

"""
    Quick overview for future maintanence.
    Des() calls the following functions in sequence:
    - _SeparateCodes() to detect if code is a compound of multiple codes
    - _GetSegments() to split the code into a list of segments
    - _GetParsingList()** identifies the EOQ syntax and constructs a modified list for recursive solving
    - _SolveParsingList() solves said list into a Python command
    - _ConstructCompound() if multiple codes were processed
    
    ** This function is the most difficult to debug, stepping the execution while considering the wanted behaviour at
    helps a lot.
"""