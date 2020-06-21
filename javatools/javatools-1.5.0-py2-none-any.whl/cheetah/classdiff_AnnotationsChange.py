

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
__CHEETAH_src__ = 'javatools/cheetah/classdiff_AnnotationsChange.tmpl'
__CHEETAH_srcLastModified__ = 'Fri Jun 21 12:18:28 2019'
__CHEETAH_docstring__ = '" "'

if __CHEETAH_versionTuple__ < RequiredCheetahVersionTuple:
    raise AssertionError(
      'This template was compiled with Cheetah version'
      ' %s. Templates compiled before version %s must be recompiled.'%(
         __CHEETAH_version__, RequiredCheetahVersion))

##################################################
## CLASSES

class classdiff_AnnotationsChange(subreport):

    ##################################################
    ## CHEETAH GENERATED METHODS


    def __init__(self, *args, **KWs):

        super(classdiff_AnnotationsChange, self).__init__(*args, **KWs)
        if not self._CHEETAH__instanceInitialized:
            cheetahKWArgs = {}
            allowedKWs = 'searchList namespaces filter filtersLib errorCatcher'.split()
            for k,v in KWs.items():
                if k in allowedKWs: cheetahKWArgs[k] = v
            self._initCheetahInstance(**cheetahKWArgs)
        

    def details(self, **KWS):



        ## CHEETAH: generated from #block details at line 6, col 1.
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
        if VFN(VFFSL(SL,"change",True),"is_change",False)(): # generated from line 9, col 1
            _v = VFFSL(SL,"render_dual_annotations",False)(VFN(VFFSL(SL,"change",True),"get_ldata",False)(), VFN(VFFSL(SL,"change",True),"get_rdata",False)()) # u'$render_dual_annotations($change.get_ldata(), $change.get_rdata())' on line 10, col 1
            if _v is not None: write(_filter(_v, rawExpr=u'$render_dual_annotations($change.get_ldata(), $change.get_rdata())'))
            write(u'''
''')
        else: # generated from line 11, col 1
            _v = VFFSL(SL,"render_annotations",False)(VFN(VFFSL(SL,"change",True),"get_ldata",False)()) # u'$render_annotations($change.get_ldata())' on line 12, col 1
            if _v is not None: write(_filter(_v, rawExpr=u'$render_annotations($change.get_ldata())'))
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
        

    def description(self, **KWS):



        ## CHEETAH: generated from #block description at line 19, col 1.
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
<!-- START BLOCK: description -->
<div class="description">''')
        _v = VFFSL(SL,"change.label",True) # u'$change.label' on line 20, col 26
        if _v is not None: write(_filter(_v, rawExpr=u'$change.label'))
        write(u'''</div>
''')
        write(u'''
<!-- END BLOCK: description -->
''')
        
        ########################################
        ## END - generated method body
        
        return _dummyTrans and trans.response().getvalue() or ""
        

    def render_annotations(self, annos, **KWS):



        ## CHEETAH: generated from #def render_annotations(annos) at line 24, col 1.
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
        
        write(u'''<table class="annotations">
<thead>
<tr>
<th>Index</th>
<th>Annotation</th>
</tr>
</thead>
''')
        for index in range(0, len(annos)): # generated from line 32, col 1
            write(u'''<tr>
<td class="const-index">''')
            write(_filter( index))
            write(u'''</td>
<td class="const-value">''')
            write(_filter( annos[index].pretty_annotation()))
            write(u'''</td>
</tr>
''')
        write(u'''</table>
''')
        
        ########################################
        ## END - generated method body
        
        return _dummyTrans and trans.response().getvalue() or ""
        

    def render_dual_annotations(self, left, right, **KWS):



        ## CHEETAH: generated from #def render_dual_annotations(left, right) at line 42, col 1.
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
        
        write(u'''<table class="annotations">
<thead>
<tr>
<th rowspan="2">Index</th>
<th colspan="2">Annotation</th>
</tr>
<tr>
<th>Original</th>
<th>Changed</th>
</tr>
</thead>
''')
        index = 0
        write(u'''
''')
        for la, ra in zip_longest(left, right): # generated from line 55, col 1
            write(u'''<tr>
<td class="const-index">''')
            write(_filter( index))
            write(u'''</td>
<td class="const-value">
''')
            write(_filter( (la and la.pretty_annotation()) or ""))
            write(u'''</td>

''')
            if (la == ra): # generated from line 61, col 1
                write(u'''<td class="const-value is_unchanged">
''')
                write(_filter( (ra and ra.pretty_annotation()) or ""))
                write(u'''</td>
''')
            else: # generated from line 64, col 1
                write(u'''<td class="const-value is_changed">
''')
                write(_filter( (ra and ra.pretty_annotation()) or ""))
                write(u'''</td>
''')
            write(u'''</tr>
''')
            index += 1
            write(u'''
''')
        write(u'''</table>
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
        self.description(trans=trans)
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

    _mainCheetahMethod_for_classdiff_AnnotationsChange = 'writeBody'

## END CLASS DEFINITION

if not hasattr(classdiff_AnnotationsChange, '_initCheetahAttributes'):
    templateAPIClass = getattr(classdiff_AnnotationsChange,
                               '_CHEETAH_templateClass',
                               Template)
    templateAPIClass._addCheetahPlumbingCodeToClass(classdiff_AnnotationsChange)


# CHEETAH was developed by Tavis Rudd and Mike Orr
# with code, advice and input from many other volunteers.
# For more information visit http://cheetahtemplate.org/

##################################################
## if run from command line:
if __name__ == '__main__':
    from Cheetah.TemplateCmdLineIface import CmdLineIface
    CmdLineIface(templateObj=classdiff_AnnotationsChange()).run()


