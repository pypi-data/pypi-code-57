

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
from javatools.cheetah import xml_entity_escape as escape

##################################################
## MODULE CONSTANTS
VFFSL=valueFromFrameOrSearchList
VFSL=valueFromSearchList
VFN=valueForName
currentTime=time.time
__CHEETAH_version__ = '3.1.0'
__CHEETAH_versionTuple__ = (3, 1, 0, 'final', 1)
__CHEETAH_src__ = 'javatools/cheetah/change_Change.tmpl'
__CHEETAH_srcLastModified__ = 'Mon Aug 11 10:25:57 2014'
__CHEETAH_docstring__ = '" "'

if __CHEETAH_versionTuple__ < RequiredCheetahVersionTuple:
    raise AssertionError(
      'This template was compiled with Cheetah version'
      ' %s. Templates compiled before version %s must be recompiled.'%(
         __CHEETAH_version__, RequiredCheetahVersion))

##################################################
## CLASSES

class change_Change(Template):

    ##################################################
    ## CHEETAH GENERATED METHODS


    def __init__(self, *args, **KWs):

        super(change_Change, self).__init__(*args, **KWs)
        if not self._CHEETAH__instanceInitialized:
            cheetahKWArgs = {}
            allowedKWs = 'searchList namespaces filter filtersLib errorCatcher'.split()
            for k,v in KWs.items():
                if k in allowedKWs: cheetahKWArgs[k] = v
            self._initCheetahInstance(**cheetahKWArgs)
        

    def description(self, **KWS):



        ## CHEETAH: generated from #block description at line 24, col 1.
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
<div class="description">
''')
        _v = VFFSL(SL,"escape",False)(VFFSL(SL,"change.label",True)) # u'$escape($change.label)' on line 26, col 1
        if _v is not None: write(_filter(_v, rawExpr=u'$escape($change.label)'))
        write(u'''
</div>
''')
        write(u'''
<!-- END BLOCK: description -->
''')
        
        ########################################
        ## END - generated method body
        
        return _dummyTrans and trans.response().getvalue() or ""
        

    def details(self, **KWS):



        ## CHEETAH: generated from #block details at line 31, col 1.
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
''')
        write(u'''
<!-- END BLOCK: details -->
''')
        
        ########################################
        ## END - generated method body
        
        return _dummyTrans and trans.response().getvalue() or ""
        

    def collect(self, **KWS):



        ## CHEETAH: generated from #block collect at line 35, col 1.
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
        if VFN(VFFSL(SL,"change",True),"collect",False)(): # generated from line 36, col 1
            write(u'''<div class="collect">
''')
            for child in VFN(VFFSL(SL,"change",True),"collect",False)(): # generated from line 38, col 1
                _v = VFFSL(SL,"render_change",False)(child) # u'$render_change(child)' on line 39, col 1
                if _v is not None: write(_filter(_v, rawExpr=u'$render_change(child)'))
                write(u'''
''')
            write(u'''</div>
''')
        write(u'''
<!-- END BLOCK: collect -->
''')
        
        ########################################
        ## END - generated method body
        
        return _dummyTrans and trans.response().getvalue() or ""
        

    def respond(self, trans=None):



        ## CHEETAH: main method generated for this template
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
        ch = getattr(self, "change")
        opts = getattr(self, "options")
        
        cl = ["Change"]
        cl.append(type(ch).__name__)
        
        if ch.is_change():
            cl.append("is_changed")
            if ch.is_ignored(opts):
                cl.append("is_ignored")
        else:
            cl.append("is_unchanged")
        
        cl = " ".join(cl)
        write(u'''


<div class="''')
        write(_filter( cl))
        write(u'''">

''')
        self.description(trans=trans)
        write(u'''

''')
        self.details(trans=trans)
        write(u'''

''')
        self.collect(trans=trans)
        write(u'''
</div>


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

    _mainCheetahMethod_for_change_Change = 'respond'

## END CLASS DEFINITION

if not hasattr(change_Change, '_initCheetahAttributes'):
    templateAPIClass = getattr(change_Change,
                               '_CHEETAH_templateClass',
                               Template)
    templateAPIClass._addCheetahPlumbingCodeToClass(change_Change)


# CHEETAH was developed by Tavis Rudd and Mike Orr
# with code, advice and input from many other volunteers.
# For more information visit http://cheetahtemplate.org/

##################################################
## if run from command line:
if __name__ == '__main__':
    from Cheetah.TemplateCmdLineIface import CmdLineIface
    CmdLineIface(templateObj=change_Change()).run()


