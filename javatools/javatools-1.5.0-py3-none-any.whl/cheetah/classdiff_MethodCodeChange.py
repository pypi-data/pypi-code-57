

# pylint: disable=C,W,R,F



##################################################
## DEPENDENCIES
import sys
import os
import os.path
try:
    import builtins as builtin
except ImportError:
    import __builtin__ as builtin
from os.path import getmtime, exists
import time
import types
from Cheetah.Version import MinCompatibleVersion as RequiredCheetahVersion
from Cheetah.Version import MinCompatibleVersionTuple as RequiredCheetahVersionTuple
from Cheetah.Template import Template
from Cheetah.DummyTransaction import *
from Cheetah.NameMapper import NotFound, valueForName, valueFromSearchList, valueFromFrameOrSearchList
from Cheetah.CacheRegion import CacheRegion
import Cheetah.Filters as Filters
import Cheetah.ErrorCatchers as ErrorCatchers
from Cheetah.compat import unicode
from javatools.cheetah.change_SuperChange import change_SuperChange
from javatools.classdiff import merge_code
from javatools.opcodes import has_const_arg, get_opname_by_code
from javatools.cheetah import xml_entity_escape as escape
from six.moves import zip_longest

##################################################
## MODULE CONSTANTS
VFFSL=valueFromFrameOrSearchList
VFSL=valueFromSearchList
VFN=valueForName
currentTime=time.time
__CHEETAH_version__ = '3.1.0'
__CHEETAH_versionTuple__ = (3, 1, 0, 'final', 1)
__CHEETAH_src__ = 'javatools/cheetah/classdiff_MethodCodeChange.tmpl'
__CHEETAH_srcLastModified__ = 'Fri Jun 21 12:20:37 2019'
__CHEETAH_docstring__ = '" "'

if __CHEETAH_versionTuple__ < RequiredCheetahVersionTuple:
    raise AssertionError(
      'This template was compiled with Cheetah version'
      ' %s. Templates compiled before version %s must be recompiled.'%(
         __CHEETAH_version__, RequiredCheetahVersion))

##################################################
## CLASSES

class classdiff_MethodCodeChange(change_SuperChange):

    ##################################################
    ## CHEETAH GENERATED METHODS


    def __init__(self, *args, **KWs):

        super(classdiff_MethodCodeChange, self).__init__(*args, **KWs)
        if not self._CHEETAH__instanceInitialized:
            cheetahKWArgs = {}
            allowedKWs = 'searchList namespaces filter filtersLib errorCatcher'.split()
            for k,v in KWs.items():
                if k in allowedKWs: cheetahKWArgs[k] = v
            self._initCheetahInstance(**cheetahKWArgs)
        

    def details_changed(self, **KWS):



        ## CHEETAH: generated from #block details_changed at line 8, col 1.
        trans = KWS.get("trans")
        if (not trans and not self._CHEETAH__isBuffering and not callable(self.transaction)):
            trans = self.transaction # is None unless self.awake() was called
        if not trans:
            trans = DummyTransaction()
            _dummyTrans = True
        else: _dummyTrans = False
        write = trans.response().write
        SL = self._CHEETAH__searchList
        _filter = self._CHEETAH__currentFilter
        
        ########################################
        ## START - generated method body
        
        write(u'''
<!-- START BLOCK: details_changed -->
<table>
<thead>
<tr>
<th>Relative</th>
<th colspan="4">Original</th>
<th colspan="4">Modified</th>
</tr>
<tr>
<th>line</th>
<th>line</th>
<th>offset</th>
<th>opcode</th>
<th>args</th>
<th>line</th>
<th>offset</th>
<th>opcode</th>
<th>args</th>
</tr>
</thead>

''')
        change = getattr(self, "change")
        ldata = change.get_ldata()
        rdata = change.get_rdata()
        merged = merge_code(ldata, rdata)
        write(u'''
''')
        for rel_line, (left, right) in sorted(merged.items()): # generated from line 35, col 1
            first = True
            last = False
            
            left_line = None
            left_dis = tuple()
            if left is not None:
                left_line, left_dis = left
            
            right_line = None
            right_dis = tuple()
            if right is not None:
                right_line, right_dis = right
            
            rowspan = max(len(left_dis), len(right_dis))
            lastrow = (rowspan - min(len(left_dis), len(right_dis)))
            write(u'''
''')
            for l_instruction, r_instruction in zip_longest(left_dis, right_dis): # generated from line 53, col 1
                write(u'''<tr>

''')
                if first: # generated from line 56, col 1
                    write(u'''<td rowspan="''')
                    write(_filter( rowspan))
                    write(u'''">''')
                    write(_filter( rel_line))
                    write(u'''</td>
''')
                write(u'''
''')
                if l_instruction is not None: # generated from line 60, col 1
                    if first: # generated from line 61, col 1
                        write(u'''<td rowspan="''')
                        write(_filter( rowspan))
                        write(u'''">''')
                        write(_filter( left[0]))
                        write(u'''</td>
''')
                    l_offset, l_code, l_args = l_instruction
                    write(u'''
<td>''')
                    write(_filter( l_offset))
                    write(u'''</td>
<td>''')
                    write(_filter( get_opname_by_code(l_code)))
                    write(u'''</td>
<td>''')
                    write(_filter( ((has_const_arg(l_code) and ("#%s" % l_args[0]))
         or ", ".join(map(str, l_args)))))
                    write(u'''</td>
''')
                else: # generated from line 69, col 1
                    if not last: # generated from line 70, col 1
                        if first: # generated from line 71, col 1
                            write(u'''<td colspan="4" rowspan="''')
                            write(_filter( lastrow))
                            write(u'''"></td>
''')
                        else: # generated from line 73, col 1
                            write(u'''<td colspan="3" rowspan="''')
                            write(_filter( lastrow))
                            write(u'''"></td>
''')
                        last = True
                        write(u'''
''')
                write(u'''
''')
                if r_instruction is not None: # generated from line 80, col 1
                    if first: # generated from line 81, col 1
                        write(u'''<td rowspan="''')
                        write(_filter( rowspan))
                        write(u'''">''')
                        write(_filter( right[0]))
                        write(u'''</td>
''')
                    r_offset, r_code, r_args = r_instruction
                    write(u'''
<td>''')
                    write(_filter( r_offset))
                    write(u'''</td>
<td>''')
                    write(_filter( get_opname_by_code(r_code)))
                    write(u'''</td>
<td>''')
                    write(_filter( ((has_const_arg(r_code) and ("#%s" % r_args[0]))
         or ", ".join(map(str, r_args)))))
                    write(u'''</td>
''')
                else: # generated from line 89, col 1
                    if not last: # generated from line 90, col 1
                        if first: # generated from line 91, col 1
                            write(u'''<td colspan="4" rowspan="''')
                            write(_filter( lastrow))
                            write(u'''"></td>
''')
                        else: # generated from line 93, col 1
                            write(u'''<td colspan="3" rowspan="''')
                            write(_filter( lastrow))
                            write(u'''"></td>
''')
                        last = True
                        write(u'''
''')
                write(u'''</tr>
''')
                first = False
                write(u'''
''')
        write(u'''</table>
''')
        write(u'''
<!-- END BLOCK: details_changed -->
''')
        
        ########################################
        ## END - generated method body
        
        return _dummyTrans and trans.response().getvalue() or ""
        

    def details_unchanged(self, **KWS):



        ## CHEETAH: generated from #block details_unchanged at line 108, col 1.
        trans = KWS.get("trans")
        if (not trans and not self._CHEETAH__isBuffering and not callable(self.transaction)):
            trans = self.transaction # is None unless self.awake() was called
        if not trans:
            trans = DummyTransaction()
            _dummyTrans = True
        else: _dummyTrans = False
        write = trans.response().write
        SL = self._CHEETAH__searchList
        _filter = self._CHEETAH__currentFilter
        
        ########################################
        ## START - generated method body
        
        write(u'''
<!-- START BLOCK: details_unchanged -->
''')
        change = getattr(self, "change")
        ldata = change.get_ldata()
        write(u'''
''')
        if ldata is None: # generated from line 113, col 1
            write(u'''<!-- abstract -->
''')
        else: # generated from line 115, col 1
            write(u'''<table>
<thead>
<tr>
<th>Relative</th>
<th colspan="4">Method Code</th>
</tr>
<tr>
<th>line</th>
<th>line</th>
<th>offset</th>
<th>opcode</th>
<th>args</th>
</tr>
</thead>
''')
            for abs_line, rel_line, dis in ldata.iter_code_by_lines(): # generated from line 130, col 1
                rowspan = len(dis)
                first = True
                write(u'''
''')
                for offset, code, args in dis: # generated from line 135, col 1
                    write(u'''<tr>
''')
                    if first: # generated from line 137, col 1
                        write(u'''<td rowspan="''')
                        write(_filter( rowspan))
                        write(u'''">''')
                        write(_filter( rel_line))
                        write(u'''</td>
<td rowspan="''')
                        write(_filter( rowspan))
                        write(u'''">''')
                        write(_filter( abs_line))
                        write(u'''</td>
''')
                    write(u'''<td>''')
                    write(_filter( offset))
                    write(u'''</td>
<td>''')
                    write(_filter( get_opname_by_code(code)))
                    write(u'''</td>
<td>''')
                    write(_filter( ((has_const_arg(code) and ("#%s" % args[0]))
         or ", ".join(map(str, args)))))
                    write(u'''</td>
</tr>
''')
                    first = False
                    write(u'''
''')
            write(u'''</table>
''')
        write(u'''
<!-- END BLOCK: details_unchanged -->
''')
        
        ########################################
        ## END - generated method body
        
        return _dummyTrans and trans.response().getvalue() or ""
        

    def details(self, **KWS):



        ## CHEETAH: generated from #block details at line 157, col 1.
        trans = KWS.get("trans")
        if (not trans and not self._CHEETAH__isBuffering and not callable(self.transaction)):
            trans = self.transaction # is None unless self.awake() was called
        if not trans:
            trans = DummyTransaction()
            _dummyTrans = True
        else: _dummyTrans = False
        write = trans.response().write
        SL = self._CHEETAH__searchList
        _filter = self._CHEETAH__currentFilter
        
        ########################################
        ## START - generated method body
        
        write(u'''
<!-- START BLOCK: details -->
<div class="details">
<div class="lrdata">
''')
        change = getattr(self, "change")
        lcode = (change.ldata and change.ldata.code) or tuple()
        rcode = (change.rdata and change.rdata.code) or tuple()
        write(u'''
''')
        if change.is_change() or (lcode != rcode): # generated from line 165, col 1
            _v = VFFSL(SL,"details_changed",True) # u'$details_changed' on line 166, col 1
            if _v is not None: write(_filter(_v, rawExpr=u'$details_changed'))
            write(u'''
''')
        else: # generated from line 167, col 1
            _v = VFFSL(SL,"details_unchanged",True) # u'$details_unchanged' on line 168, col 1
            if _v is not None: write(_filter(_v, rawExpr=u'$details_unchanged'))
            write(u'''
''')
        write(u'''</div>
</div>
''')
        write(u'''
<!-- END BLOCK: details -->
''')
        
        ########################################
        ## END - generated method body
        
        return _dummyTrans and trans.response().getvalue() or ""
        

    def collect(self, **KWS):



        ## CHEETAH: generated from #block collect at line 176, col 1.
        trans = KWS.get("trans")
        if (not trans and not self._CHEETAH__isBuffering and not callable(self.transaction)):
            trans = self.transaction # is None unless self.awake() was called
        if not trans:
            trans = DummyTransaction()
            _dummyTrans = True
        else: _dummyTrans = False
        write = trans.response().write
        SL = self._CHEETAH__searchList
        _filter = self._CHEETAH__currentFilter
        
        ########################################
        ## START - generated method body
        
        write(u'''
<!-- START BLOCK: collect -->
''')
        write(u'''
<!-- END BLOCK: collect -->
''')
        
        ########################################
        ## END - generated method body
        
        return _dummyTrans and trans.response().getvalue() or ""
        

    def writeBody(self, **KWS):



        ## CHEETAH: main method generated for this template
        trans = KWS.get("trans")
        if (not trans and not self._CHEETAH__isBuffering and not callable(self.transaction)):
            trans = self.transaction # is None unless self.awake() was called
        if not trans:
            trans = DummyTransaction()
            _dummyTrans = True
        else: _dummyTrans = False
        write = trans.response().write
        SL = self._CHEETAH__searchList
        _filter = self._CHEETAH__currentFilter
        
        ########################################
        ## START - generated method body
        
        write(u'''

''')
        self.details_changed(trans=trans)
        write(u'''


''')
        self.details_unchanged(trans=trans)
        write(u'''


''')
        self.details(trans=trans)
        write(u'''


''')
        self.collect(trans=trans)
        write(u'''


''')
        # 
        #  The end.
        
        ########################################
        ## END - generated method body
        
        return _dummyTrans and trans.response().getvalue() or ""
        
    ##################################################
    ## CHEETAH GENERATED ATTRIBUTES


    _CHEETAH__instanceInitialized = False

    _CHEETAH_version = __CHEETAH_version__

    _CHEETAH_versionTuple = __CHEETAH_versionTuple__

    _CHEETAH_src = __CHEETAH_src__

    _CHEETAH_srcLastModified = __CHEETAH_srcLastModified__

    _mainCheetahMethod_for_classdiff_MethodCodeChange = 'writeBody'

## END CLASS DEFINITION

if not hasattr(classdiff_MethodCodeChange, '_initCheetahAttributes'):
    templateAPIClass = getattr(classdiff_MethodCodeChange,
                               '_CHEETAH_templateClass',
                               Template)
    templateAPIClass._addCheetahPlumbingCodeToClass(classdiff_MethodCodeChange)


# CHEETAH was developed by Tavis Rudd and Mike Orr
# with code, advice and input from many other volunteers.
# For more information visit http://cheetahtemplate.org/

##################################################
## if run from command line:
if __name__ == '__main__':
    from Cheetah.TemplateCmdLineIface import CmdLineIface
    CmdLineIface(templateObj=classdiff_MethodCodeChange()).run()


