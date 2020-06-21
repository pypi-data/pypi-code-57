

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
from javatools.change import collect_by_typename
from javatools.cheetah import xml_entity_escape as escape

##################################################
## MODULE CONSTANTS
VFFSL=valueFromFrameOrSearchList
VFSL=valueFromSearchList
VFN=valueForName
currentTime=time.time
__CHEETAH_version__ = '3.1.0'
__CHEETAH_versionTuple__ = (3, 1, 0, 'final', 1)
__CHEETAH_src__ = 'javatools/cheetah/classdiff_FieldChange.tmpl'
__CHEETAH_srcLastModified__ = 'Fri Jun 21 12:21:54 2019'
__CHEETAH_docstring__ = '" "'

if __CHEETAH_versionTuple__ < RequiredCheetahVersionTuple:
    raise AssertionError(
      'This template was compiled with Cheetah version'
      ' %s. Templates compiled before version %s must be recompiled.'%(
         __CHEETAH_version__, RequiredCheetahVersion))

##################################################
## CLASSES

class classdiff_FieldChange(change_Change):

    ##################################################
    ## CHEETAH GENERATED METHODS


    def __init__(self, *args, **KWs):

        super(classdiff_FieldChange, self).__init__(*args, **KWs)
        if not self._CHEETAH__instanceInitialized:
            cheetahKWArgs = {}
            allowedKWs = 'searchList namespaces filter filtersLib errorCatcher'.split()
            for k,v in KWs.items():
                if k in allowedKWs: cheetahKWArgs[k] = v
            self._initCheetahInstance(**cheetahKWArgs)
        

    def description(self, **KWS):



        ## CHEETAH: generated from #block description at line 7, col 1.
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
        ldata = change.get_ldata()
        nom = ldata.get_name()
        write(u'''
<h3>''')
        write(_filter( escape(nom)))
        write(u'''</h3>
''')
        write(u'''
<!-- END BLOCK: description -->
''')
        
        ########################################
        ## END - generated method body
        
        return _dummyTrans and trans.response().getvalue() or ""
        

    def details(self, **KWS):



        ## CHEETAH: generated from #block details at line 18, col 1.
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
        change = getattr(self, "change")
        data = collect_by_typename(change.collect())
        write(u'''

<div class="details">
<div class="lrdata">

<table class="left-headers">
''')
        _v = VFFSL(SL,"sub_name",False)(data.pop("FieldNameChange")[0]) # u'$sub_name(data.pop("FieldNameChange")[0])' on line 28, col 1
        if _v is not None: write(_filter(_v, rawExpr=u'$sub_name(data.pop("FieldNameChange")[0])'))
        write(u'''
''')
        _v = VFFSL(SL,"sub_type",False)(data.pop("FieldTypeChange")[0]) # u'$sub_type(data.pop("FieldTypeChange")[0])' on line 29, col 1
        if _v is not None: write(_filter(_v, rawExpr=u'$sub_type(data.pop("FieldTypeChange")[0])'))
        write(u'''
''')
        _v = VFFSL(SL,"sub_flags",False)(data.pop("FieldAccessflagsChange")[0]) # u'$sub_flags(data.pop("FieldAccessflagsChange")[0])' on line 30, col 1
        if _v is not None: write(_filter(_v, rawExpr=u'$sub_flags(data.pop("FieldAccessflagsChange")[0])'))
        write(u'''
''')
        _v = VFFSL(SL,"sub_signature",False)(data.pop("FieldSignatureChange")[0]) # u'$sub_signature(data.pop("FieldSignatureChange")[0])' on line 31, col 1
        if _v is not None: write(_filter(_v, rawExpr=u'$sub_signature(data.pop("FieldSignatureChange")[0])'))
        write(u'''
''')
        _v = VFFSL(SL,"sub_const",False)(data.pop("FieldConstvalueChange")[0]) # u'$sub_const(data.pop("FieldConstvalueChange")[0])' on line 32, col 1
        if _v is not None: write(_filter(_v, rawExpr=u'$sub_const(data.pop("FieldConstvalueChange")[0])'))
        write(u'''
''')
        _v = VFFSL(SL,"sub_deprecation",False)(data.pop("FieldDeprecationChange")[0]) # u'$sub_deprecation(data.pop("FieldDeprecationChange")[0])' on line 33, col 1
        if _v is not None: write(_filter(_v, rawExpr=u'$sub_deprecation(data.pop("FieldDeprecationChange")[0])'))
        write(u'''
</table>

</div>
</div>
''')
        write(u'''
<!-- END BLOCK: details -->
''')
        
        ########################################
        ## END - generated method body
        
        return _dummyTrans and trans.response().getvalue() or ""
        

    def collect(self, **KWS):



        ## CHEETAH: generated from #block collect at line 42, col 1.
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
        change = getattr(self, "change")
        data = collect_by_typename(change.collect())
        write(u'''
<div class="collect">
''')
        _v = VFFSL(SL,"render_change",False)(data.pop("FieldAnnotationsChange")[0]) # u'$render_change(data.pop("FieldAnnotationsChange")[0])' on line 48, col 1
        if _v is not None: write(_filter(_v, rawExpr=u'$render_change(data.pop("FieldAnnotationsChange")[0])'))
        write(u'''
''')
        _v = VFFSL(SL,"render_change",False)(data.pop("FieldInvisibleAnnotationsChange")[0]) # u'$render_change(data.pop("FieldInvisibleAnnotationsChange")[0])' on line 49, col 1
        if _v is not None: write(_filter(_v, rawExpr=u'$render_change(data.pop("FieldInvisibleAnnotationsChange")[0])'))
        write(u'''
</div>
''')
        write(u'''
<!-- END BLOCK: collect -->
''')
        
        ########################################
        ## END - generated method body
        
        return _dummyTrans and trans.response().getvalue() or ""
        

    def sub_name(self, subch, **KWS):



        ## CHEETAH: generated from #def sub_name(subch) at line 55, col 1.
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
        
        label = "Field Name"
        if subch.is_change(): # generated from line 57, col 1
            write(u'''<tr>
<th rowspan="2">''')
            _v = VFFSL(SL,"label",True) # u'$label' on line 59, col 17
            if _v is not None: write(_filter(_v, rawExpr=u'$label'))
            write(u'''</th>
<td>''')
            write(_filter( escape(subch.pretty_ldata())))
            write(u'''</td>
</tr>
<tr>
<td>''')
            write(_filter( escape(subch.pretty_rdata())))
            write(u'''</td>
</tr>
''')
        else: # generated from line 65, col 1
            write(u'''<tr>
<th>''')
            _v = VFFSL(SL,"label",True) # u'$label' on line 67, col 5
            if _v is not None: write(_filter(_v, rawExpr=u'$label'))
            write(u'''</th>
<td>''')
            write(_filter( escape(subch.pretty_ldata())))
            write(u'''
</tr>
''')
        
        ########################################
        ## END - generated method body
        
        return _dummyTrans and trans.response().getvalue() or ""
        

    def sub_type(self, subch, **KWS):



        ## CHEETAH: generated from #def sub_type(subch) at line 75, col 1.
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
        
        label = "Field Type"
        if subch.is_change(): # generated from line 77, col 1
            write(u'''<tr>
<th rowspan="2">''')
            _v = VFFSL(SL,"label",True) # u'$label' on line 79, col 17
            if _v is not None: write(_filter(_v, rawExpr=u'$label'))
            write(u'''</th>
<td>''')
            write(_filter( subch.pretty_ldata()))
            write(u'''</td>
</tr>
<tr>
<td>''')
            write(_filter( subch.pretty_rdata()))
            write(u'''</td>
</tr>
''')
        else: # generated from line 85, col 1
            write(u'''<tr>
<th>''')
            _v = VFFSL(SL,"label",True) # u'$label' on line 87, col 5
            if _v is not None: write(_filter(_v, rawExpr=u'$label'))
            write(u'''</th>
<td>''')
            write(_filter( subch.pretty_ldata()))
            write(u'''
</tr>
''')
        
        ########################################
        ## END - generated method body
        
        return _dummyTrans and trans.response().getvalue() or ""
        

    def sub_flags(self, subch, **KWS):



        ## CHEETAH: generated from #def sub_flags(subch) at line 95, col 1.
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
        
        label = "Field Flags"
        if subch.is_change(): # generated from line 97, col 1
            write(u'''<tr>
<th rowspan="2">''')
            _v = VFFSL(SL,"label",True) # u'$label' on line 99, col 17
            if _v is not None: write(_filter(_v, rawExpr=u'$label'))
            write(u'''</th>
<td>''')
            write(_filter( "0x%04x" % subch.get_ldata()))
            write(u''':
    ''')
            write(_filter( " ".join(subch.pretty_ldata())))
            write(u'''</td>
</tr>
<tr>
<td class="is_changed">
''')
            write(_filter( "0x%04x" % subch.get_rdata()))
            write(u''':
''')
            write(_filter( " ".join(subch.pretty_rdata())))
            write(u'''</td>
</tr>
''')
        else: # generated from line 108, col 1
            write(u'''<tr>
<th>''')
            _v = VFFSL(SL,"label",True) # u'$label' on line 110, col 5
            if _v is not None: write(_filter(_v, rawExpr=u'$label'))
            write(u'''</th>
<td>''')
            write(_filter( "0x%04x" % subch.get_ldata()))
            write(u''':
    ''')
            write(_filter( " ".join(subch.pretty_ldata())))
            write(u'''</td>
</tr>
''')
        
        ########################################
        ## END - generated method body
        
        return _dummyTrans and trans.response().getvalue() or ""
        

    def sub_signature(self, subch, **KWS):



        ## CHEETAH: generated from #def sub_signature(subch) at line 119, col 1.
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
        
        label = "Generics Signature"
        if subch.is_change(): # generated from line 121, col 1
            write(u'''<tr>
<th rowspan="2">''')
            _v = VFFSL(SL,"label",True) # u'$label' on line 123, col 17
            if _v is not None: write(_filter(_v, rawExpr=u'$label'))
            write(u'''</th>
<td>''')
            write(_filter( escape(subch.pretty_ldata() or "(None)")))
            write(u'''</td>
</tr>
<tr>
<td class="is_changed">
 ''')
            write(_filter( escape(subch.pretty_rdata() or "(None)")))
            write(u'''</td>
</tr>
''')
        elif subch.get_ldata(): # generated from line 130, col 1
            write(u'''<tr>
<th>''')
            _v = VFFSL(SL,"label",True) # u'$label' on line 132, col 5
            if _v is not None: write(_filter(_v, rawExpr=u'$label'))
            write(u'''</th>
<td>''')
            write(_filter( escape(subch.pretty_ldata())))
            write(u'''</td>
</tr>
''')
        
        ########################################
        ## END - generated method body
        
        return _dummyTrans and trans.response().getvalue() or ""
        

    def sub_const(self, subch, **KWS):



        ## CHEETAH: generated from #def sub_const(subch) at line 140, col 1.
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
        
        label = "Const Value"
        if subch.is_change(): # generated from line 142, col 1
            write(u'''<tr>
<th rowspan="2">''')
            _v = VFFSL(SL,"label",True) # u'$label' on line 144, col 17
            if _v is not None: write(_filter(_v, rawExpr=u'$label'))
            write(u'''</th>
<td>''')
            write(_filter( escape(subch.pretty_ldata() or "(None)")))
            write(u'''</td>
</tr>
<tr>
<td class="is_changed">
 ''')
            write(_filter( escape(subch.pretty_rdata() or "(None)")))
            write(u'''</td>
</tr>
''')
        elif subch.get_ldata(): # generated from line 151, col 1
            write(u'''<tr>
<th>''')
            _v = VFFSL(SL,"label",True) # u'$label' on line 153, col 5
            if _v is not None: write(_filter(_v, rawExpr=u'$label'))
            write(u'''</th>
<td>''')
            write(_filter( escape(subch.pretty_ldata())))
            write(u'''</td>
</tr>
''')
        
        ########################################
        ## END - generated method body
        
        return _dummyTrans and trans.response().getvalue() or ""
        

    def sub_deprecation(self, subch, **KWS):



        ## CHEETAH: generated from #def sub_deprecation(subch) at line 161, col 1.
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
        
        label = "Deprecated"
        if subch.is_change(): # generated from line 163, col 1
            write(u'''<tr>
<th rowspan="2">''')
            _v = VFFSL(SL,"label",True) # u'$label' on line 165, col 17
            if _v is not None: write(_filter(_v, rawExpr=u'$label'))
            write(u'''</th>
<td>''')
            write(_filter( subch.pretty_ldata()))
            write(u'''</td>
</tr>
<tr>
<td class="is_changed">''')
            write(_filter( subch.pretty_rdata()))
            write(u'''</td>
</tr>
''')
        elif subch.get_ldata(): # generated from line 171, col 1
            write(u'''<tr>
<th>''')
            _v = VFFSL(SL,"label",True) # u'$label' on line 173, col 5
            if _v is not None: write(_filter(_v, rawExpr=u'$label'))
            write(u'''</th>
<td>''')
            write(_filter( subch.pretty_ldata()))
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

    _mainCheetahMethod_for_classdiff_FieldChange = 'writeBody'

## END CLASS DEFINITION

if not hasattr(classdiff_FieldChange, '_initCheetahAttributes'):
    templateAPIClass = getattr(classdiff_FieldChange,
                               '_CHEETAH_templateClass',
                               Template)
    templateAPIClass._addCheetahPlumbingCodeToClass(classdiff_FieldChange)


# CHEETAH was developed by Tavis Rudd and Mike Orr
# with code, advice and input from many other volunteers.
# For more information visit http://cheetahtemplate.org/

##################################################
## if run from command line:
if __name__ == '__main__':
    from Cheetah.TemplateCmdLineIface import CmdLineIface
    CmdLineIface(templateObj=classdiff_FieldChange()).run()


