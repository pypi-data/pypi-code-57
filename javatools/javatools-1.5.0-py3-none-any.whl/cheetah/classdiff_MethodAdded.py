

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
from javatools.cheetah.change_Change import change_Change
from javatools.cheetah import xml_entity_escape as escape

##################################################
## MODULE CONSTANTS
VFFSL=valueFromFrameOrSearchList
VFSL=valueFromSearchList
VFN=valueForName
currentTime=time.time
__CHEETAH_version__ = '3.1.0'
__CHEETAH_versionTuple__ = (3, 1, 0, 'final', 1)
__CHEETAH_src__ = 'javatools/cheetah/classdiff_MethodAdded.tmpl'
__CHEETAH_srcLastModified__ = 'Fri Jun 21 12:20:09 2019'
__CHEETAH_docstring__ = '" "'

if __CHEETAH_versionTuple__ < RequiredCheetahVersionTuple:
    raise AssertionError(
      'This template was compiled with Cheetah version'
      ' %s. Templates compiled before version %s must be recompiled.'%(
         __CHEETAH_version__, RequiredCheetahVersion))

##################################################
## CLASSES

class classdiff_MethodAdded(change_Change):

    ##################################################
    ## CHEETAH GENERATED METHODS


    def __init__(self, *args, **KWs):

        super(classdiff_MethodAdded, self).__init__(*args, **KWs)
        if not self._CHEETAH__instanceInitialized:
            cheetahKWArgs = {}
            allowedKWs = 'searchList namespaces filter filtersLib errorCatcher'.split()
            for k,v in KWs.items():
                if k in allowedKWs: cheetahKWArgs[k] = v
            self._initCheetahInstance(**cheetahKWArgs)
        

    def description(self, **KWS):



        ## CHEETAH: generated from #block description at line 6, col 1.
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
''')
        change = getattr(self, "change")
        info = change.get_rdata()
        a = info.get_name()
        b = ", ".join(info.pretty_arg_types())
        c = info.pretty_type()
        write(u'''
<h3>''')
        write(_filter( escape("%s(%s):%s" % (a, b, c))))
        write(u'''</h3>
<div class="description">Method Added</div
''')
        write(u'''
<!-- END BLOCK: description -->
''')
        
        ########################################
        ## END - generated method body
        
        return _dummyTrans and trans.response().getvalue() or ""
        

    def details(self, **KWS):



        ## CHEETAH: generated from #block details at line 20, col 1.
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
        _v = VFFSL(SL,"method_table",False)(VFN(VFFSL(SL,"change",True),"get_rdata",False)()) # u'$method_table($change.get_rdata())' on line 23, col 1
        if _v is not None: write(_filter(_v, rawExpr=u'$method_table($change.get_rdata())'))
        write(u'''
</div>
</div>
''')
        write(u'''
<!-- END BLOCK: details -->
''')
        
        ########################################
        ## END - generated method body
        
        return _dummyTrans and trans.response().getvalue() or ""
        

    def method_table(self, info, **KWS):



        ## CHEETAH: generated from #def method_table(info) at line 30, col 1.
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
        
        write(u'''<table class="left-headers">
''')
        _v = VFFSL(SL,"row",False)("Method Name", info.get_name()) # u'$row("Method Name", info.get_name())' on line 32, col 1
        if _v is not None: write(_filter(_v, rawExpr=u'$row("Method Name", info.get_name())'))
        write(u'''
''')
        _v = VFFSL(SL,"row",False)("Return Type", info.pretty_type()) # u'$row("Return Type", info.pretty_type())' on line 33, col 1
        if _v is not None: write(_filter(_v, rawExpr=u'$row("Return Type", info.pretty_type())'))
        write(u'''
''')
        _v = VFFSL(SL,"row",False)("Argument Types", "(%s)" % ", ".join(info.pretty_arg_types())) # u'$row("Argument Types", "(%s)" % ", ".join(info.pretty_arg_types()))' on line 34, col 1
        if _v is not None: write(_filter(_v, rawExpr=u'$row("Argument Types", "(%s)" % ", ".join(info.pretty_arg_types()))'))
        write(u'''
''')
        _v = VFFSL(SL,"row",False)("Method Flags", "0x%04x: %s" %
      (info.access_flags, " ".join(info.pretty_access_flags())))
        if _v is not None: write(_filter(_v, rawExpr=u'$row("Method Flags", "0x%04x: %s" %\n      (info.access_flags, " ".join(info.pretty_access_flags())))'))
        write(u'''

''')
        if info.get_signature(): # generated from line 38, col 1
            _v = VFFSL(SL,"row",False)("Generics Signature", info.get_signature()) # u'$row("Generics Signature", info.get_signature())' on line 39, col 1
            if _v is not None: write(_filter(_v, rawExpr=u'$row("Generics Signature", info.get_signature())'))
            write(u'''
''')
        write(u'''
''')
        if info.get_exceptions(): # generated from line 42, col 1
            _v = VFFSL(SL,"row",False)("Exceptions", ", ".join(info.pretty_exceptions())) # u'$row("Exceptions", ", ".join(info.pretty_exceptions()))' on line 43, col 1
            if _v is not None: write(_filter(_v, rawExpr=u'$row("Exceptions", ", ".join(info.pretty_exceptions()))'))
            write(u'''
''')
        write(u'''
''')
        if not info.get_code(): # generated from line 46, col 1
            _v = VFFSL(SL,"row",False)("Abstract", "True") # u'$row("Abstract", "True")' on line 47, col 1
            if _v is not None: write(_filter(_v, rawExpr=u'$row("Abstract", "True")'))
            write(u'''
''')
        write(u'''
''')
        if info.is_deprecated(): # generated from line 50, col 1
            _v = VFFSL(SL,"row",False)("Deprecated", "True") # u'$row("Deprecated", "True")' on line 51, col 1
            if _v is not None: write(_filter(_v, rawExpr=u'$row("Deprecated", "True")'))
            write(u'''
''')
        write(u'''
</table>
''')
        
        ########################################
        ## END - generated method body
        
        return _dummyTrans and trans.response().getvalue() or ""
        

    def row(self, label, data, **KWS):



        ## CHEETAH: generated from #def row(label, data) at line 59, col 1.
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
        
        write(u'''<tr>
<th>''')
        _v = VFFSL(SL,"label",True) # u'$label' on line 61, col 5
        if _v is not None: write(_filter(_v, rawExpr=u'$label'))
        write(u'''</th>
<td>''')
        write(_filter( escape(data)))
        write(u'''</td>
</tr>
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
        self.description(trans=trans)
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

    _mainCheetahMethod_for_classdiff_MethodAdded = 'writeBody'

## END CLASS DEFINITION

if not hasattr(classdiff_MethodAdded, '_initCheetahAttributes'):
    templateAPIClass = getattr(classdiff_MethodAdded,
                               '_CHEETAH_templateClass',
                               Template)
    templateAPIClass._addCheetahPlumbingCodeToClass(classdiff_MethodAdded)


# CHEETAH was developed by Tavis Rudd and Mike Orr
# with code, advice and input from many other volunteers.
# For more information visit http://cheetahtemplate.org/

##################################################
## if run from command line:
if __name__ == '__main__':
    from Cheetah.TemplateCmdLineIface import CmdLineIface
    CmdLineIface(templateObj=classdiff_MethodAdded()).run()


