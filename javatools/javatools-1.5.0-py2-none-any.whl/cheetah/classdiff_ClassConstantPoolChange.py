

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
from javatools.cheetah.subreport import subreport
from javatools.classdiff import pretty_merge_constants
from javatools.cheetah import xml_entity_escape as escape

##################################################
## MODULE CONSTANTS
VFFSL=valueFromFrameOrSearchList
VFSL=valueFromSearchList
VFN=valueForName
currentTime=time.time
__CHEETAH_version__ = '3.1.0'
__CHEETAH_versionTuple__ = (3, 1, 0, 'final', 1)
__CHEETAH_src__ = 'javatools/cheetah/classdiff_ClassConstantPoolChange.tmpl'
__CHEETAH_srcLastModified__ = 'Fri Jun 21 12:16:42 2019'
__CHEETAH_docstring__ = '" "'

if __CHEETAH_versionTuple__ < RequiredCheetahVersionTuple:
    raise AssertionError(
      'This template was compiled with Cheetah version'
      ' %s. Templates compiled before version %s must be recompiled.'%(
         __CHEETAH_version__, RequiredCheetahVersion))

##################################################
## CLASSES

class classdiff_ClassConstantPoolChange(subreport):

    ##################################################
    ## CHEETAH GENERATED METHODS


    def __init__(self, *args, **KWs):

        super(classdiff_ClassConstantPoolChange, self).__init__(*args, **KWs)
        if not self._CHEETAH__instanceInitialized:
            cheetahKWArgs = {}
            allowedKWs = 'searchList namespaces filter filtersLib errorCatcher'.split()
            for k,v in KWs.items():
                if k in allowedKWs: cheetahKWArgs[k] = v
            self._initCheetahInstance(**cheetahKWArgs)
        

    def details(self, **KWS):



        ## CHEETAH: generated from #block details at line 7, col 1.
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
        if VFN(VFFSL(SL,"change",True),"is_change",False)(): # generated from line 10, col 1
            _v = VFFSL(SL,"render_dual_constant_pool",False)(VFN(VFFSL(SL,"change",True),"get_ldata",False)(), VFN(VFFSL(SL,"change",True),"get_rdata",False)()) # u'$render_dual_constant_pool($change.get_ldata(), $change.get_rdata())' on line 11, col 1
            if _v is not None: write(_filter(_v, rawExpr=u'$render_dual_constant_pool($change.get_ldata(), $change.get_rdata())'))
            write(u'''
''')
        else: # generated from line 12, col 1
            _v = VFFSL(SL,"render_constant_pool",False)(VFN(VFFSL(SL,"change",True),"pretty_ldata",False)()) # u'$render_constant_pool($change.pretty_ldata())' on line 13, col 1
            if _v is not None: write(_filter(_v, rawExpr=u'$render_constant_pool($change.pretty_ldata())'))
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
        

    def render_constant_pool(self, consts, **KWS):



        ## CHEETAH: generated from #def render_constant_pool(consts) at line 21, col 1.
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
        
        write(u'''<table class="constant-pool">
<thead>
<tr>
<th>Index</th>
<th>Type</th>
<th>Value</th>
</tr>
</thead>

''')
        for i, t, v in consts: # generated from line 31, col 1
            write(u'''<tr>
<td class="const-index">''')
            write(_filter( i))
            write(u'''</td>
<td class="const-type">''')
            write(_filter( t))
            write(u'''</td>
<td class="const-value">''')
            write(_filter( escape(str(v))))
            write(u'''</td>
</tr>
''')
        write(u'''
</table>
''')
        
        ########################################
        ## END - generated method body
        
        return _dummyTrans and trans.response().getvalue() or ""
        

    def render_dual_constant_pool(self, left, right, **KWS):



        ## CHEETAH: generated from #def render_dual_constant_pool(left, right) at line 44, col 1.
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
        
        write(u'''<table class="dual-constant-pool">
<thead>
<tr>
<th>Index</th>
<th>Original Type</th>
<th>Original Value</th>
<th>Modified Type</th>
<th>Modified Value</th>
</tr>
</thead>

''')
        for index, lt, lv, rt, rv in pretty_merge_constants(left, right): # generated from line 56, col 1
            row_class = (" is_changed")[(lt, lv) == (rt, rv)]
            write(u'''
<tr>
<td class="const-index">''')
            write(_filter( index))
            write(u'''</td>
<td class="const-type">''')
            write(_filter( lt or ""))
            write(u'''</td>
<td class="const-value">''')
            write(_filter( escape(str(lv or ""))))
            write(u'''</td>
''')
            if (lt, lv) == (rt, rv): # generated from line 64, col 1
                write(u'''<td class="const-type empty"></td>
<td class="const-value empty"></td>
''')
            else: # generated from line 67, col 1
                write(u'''<td class="const-type is_changed">''')
                write(_filter( rt or ""))
                write(u'''</td>
<td class="const-value is_changed">''')
                write(_filter( escape(str(rv or ""))))
                write(u'''</td>
</tr>
''')
        write(u'''
</table>
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
        self.details(trans=trans)
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

    _mainCheetahMethod_for_classdiff_ClassConstantPoolChange = 'writeBody'

## END CLASS DEFINITION

if not hasattr(classdiff_ClassConstantPoolChange, '_initCheetahAttributes'):
    templateAPIClass = getattr(classdiff_ClassConstantPoolChange,
                               '_CHEETAH_templateClass',
                               Template)
    templateAPIClass._addCheetahPlumbingCodeToClass(classdiff_ClassConstantPoolChange)


# CHEETAH was developed by Tavis Rudd and Mike Orr
# with code, advice and input from many other volunteers.
# For more information visit http://cheetahtemplate.org/

##################################################
## if run from command line:
if __name__ == '__main__':
    from Cheetah.TemplateCmdLineIface import CmdLineIface
    CmdLineIface(templateObj=classdiff_ClassConstantPoolChange()).run()


