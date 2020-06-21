

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
__CHEETAH_src__ = 'javatools/cheetah/classdiff_ClassInfoChange.tmpl'
__CHEETAH_srcLastModified__ = 'Fri Jun 21 12:21:14 2019'
__CHEETAH_docstring__ = '" "'

if __CHEETAH_versionTuple__ < RequiredCheetahVersionTuple:
    raise AssertionError(
      'This template was compiled with Cheetah version'
      ' %s. Templates compiled before version %s must be recompiled.'%(
         __CHEETAH_version__, RequiredCheetahVersion))

##################################################
## CLASSES

class classdiff_ClassInfoChange(subreport):

    ##################################################
    ## CHEETAH GENERATED METHODS


    def __init__(self, *args, **KWs):

        super(classdiff_ClassInfoChange, self).__init__(*args, **KWs)
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
''')
        change = getattr(self, "change")
        data = collect_by_typename(change.collect())
        write(u'''
<div class="details">
<div class="lrdata">

<table class="left-headers">
''')
        _v = VFFSL(SL,"sub_classname",False)(data["ClassNameChange"][0]) # u'$sub_classname(data["ClassNameChange"][0])' on line 16, col 1
        if _v is not None: write(_filter(_v, rawExpr=u'$sub_classname(data["ClassNameChange"][0])'))
        write(u'''
''')
        _v = VFFSL(SL,"sub_flags",False)(data["ClassAccessflagsChange"][0]) # u'$sub_flags(data["ClassAccessflagsChange"][0])' on line 17, col 1
        if _v is not None: write(_filter(_v, rawExpr=u'$sub_flags(data["ClassAccessflagsChange"][0])'))
        write(u'''
''')
        _v = VFFSL(SL,"sub_super",False)(data["ClassSuperclassChange"][0]) # u'$sub_super(data["ClassSuperclassChange"][0])' on line 18, col 1
        if _v is not None: write(_filter(_v, rawExpr=u'$sub_super(data["ClassSuperclassChange"][0])'))
        write(u'''
''')
        _v = VFFSL(SL,"sub_inter",False)(data["ClassInterfacesChange"][0]) # u'$sub_inter(data["ClassInterfacesChange"][0])' on line 19, col 1
        if _v is not None: write(_filter(_v, rawExpr=u'$sub_inter(data["ClassInterfacesChange"][0])'))
        write(u'''
''')
        _v = VFFSL(SL,"sub_version",False)(data["ClassVersionChange"][0]) # u'$sub_version(data["ClassVersionChange"][0])' on line 20, col 1
        if _v is not None: write(_filter(_v, rawExpr=u'$sub_version(data["ClassVersionChange"][0])'))
        write(u'''
''')
        _v = VFFSL(SL,"sub_platform",False)(data["ClassPlatformChange"][0]) # u'$sub_platform(data["ClassPlatformChange"][0])' on line 21, col 1
        if _v is not None: write(_filter(_v, rawExpr=u'$sub_platform(data["ClassPlatformChange"][0])'))
        write(u'''
''')
        _v = VFFSL(SL,"sub_signature",False)(data["ClassSignatureChange"][0]) # u'$sub_signature(data["ClassSignatureChange"][0])' on line 22, col 1
        if _v is not None: write(_filter(_v, rawExpr=u'$sub_signature(data["ClassSignatureChange"][0])'))
        write(u'''
''')
        _v = VFFSL(SL,"sub_deprecation",False)(data["ClassDeprecationChange"][0]) # u'$sub_deprecation(data["ClassDeprecationChange"][0])' on line 23, col 1
        if _v is not None: write(_filter(_v, rawExpr=u'$sub_deprecation(data["ClassDeprecationChange"][0])'))
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



        ## CHEETAH: generated from #block collect at line 32, col 1.
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
        

    def sub_classname(self, subch, **KWS):



        ## CHEETAH: generated from #def sub_classname(subch) at line 37, col 1.
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
        
        label = "Class Name"
        if subch.is_change(): # generated from line 39, col 1
            write(u'''<tr>
<th rowspan="2">''')
            _v = VFFSL(SL,"label",True) # u'$label' on line 41, col 17
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
        else: # generated from line 47, col 1
            write(u'''<tr>
<th>''')
            _v = VFFSL(SL,"label",True) # u'$label' on line 49, col 5
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
        

    def sub_flags(self, subch, **KWS):



        ## CHEETAH: generated from #def sub_flags(subch) at line 57, col 1.
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
        
        label = "Class Flags"
        if subch.is_change(): # generated from line 59, col 1
            write(u'''<tr>
<th rowspan="2">''')
            _v = VFFSL(SL,"label",True) # u'$label' on line 61, col 17
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
        else: # generated from line 70, col 1
            write(u'''<tr>
<th>''')
            _v = VFFSL(SL,"label",True) # u'$label' on line 72, col 5
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
        

    def sub_super(self, subch, **KWS):



        ## CHEETAH: generated from #def sub_super(subch) at line 81, col 1.
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
        
        label = "Extends"
        if subch.is_change(): # generated from line 83, col 1
            write(u'''<tr>
<th rowspan="2">''')
            _v = VFFSL(SL,"label",True) # u'$label' on line 85, col 17
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
        else: # generated from line 91, col 1
            write(u'''<tr>
<th>''')
            _v = VFFSL(SL,"label",True) # u'$label' on line 93, col 5
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
        

    def sub_inter(self, subch, **KWS):



        ## CHEETAH: generated from #def sub_inter(subch) at line 101, col 1.
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
        
        label = "Implements"
        if subch.is_change(): # generated from line 103, col 1
            write(u'''<tr>
<th rowspan="2">''')
            _v = VFFSL(SL,"label",True) # u'$label' on line 105, col 17
            if _v is not None: write(_filter(_v, rawExpr=u'$label'))
            write(u'''</th>
<td>''')
            write(_filter( ", ".join(subch.pretty_ldata()) or "(None)"))
            write(u'''</td>
</tr>
<tr>
<td class="is_changed">
''')
            write(_filter( ", ".join(subch.pretty_rdata()) or "(None)"))
            write(u'''</td>
</tr>
''')
        elif subch.get_ldata(): # generated from line 112, col 1
            write(u'''<tr>
<th>''')
            _v = VFFSL(SL,"label",True) # u'$label' on line 114, col 5
            if _v is not None: write(_filter(_v, rawExpr=u'$label'))
            write(u'''</th>
<td>''')
            write(_filter( ", ".join(subch.pretty_ldata())))
            write(u'''</td>
</tr>
''')
        
        ########################################
        ## END - generated method body
        
        return _dummyTrans and trans.response().getvalue() or ""
        

    def sub_version(self, subch, **KWS):



        ## CHEETAH: generated from #def sub_version(subch) at line 122, col 1.
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
        
        label = "Java Version"
        templ = "Major: %i, Minor: %i"
        if subch.is_change(): # generated from line 125, col 1
            write(u'''<tr>
<th rowspan="2">''')
            _v = VFFSL(SL,"label",True) # u'$label' on line 127, col 17
            if _v is not None: write(_filter(_v, rawExpr=u'$label'))
            write(u'''</th>
<td>''')
            write(_filter( templ % subch.get_ldata()))
            write(u'''</td>
</tr>
<tr>
<td class="is_changed">''')
            write(_filter( templ % subch.get_rdata()))
            write(u'''</td>
</tr>
''')
        else: # generated from line 133, col 1
            write(u'''<tr>
<th>''')
            _v = VFFSL(SL,"label",True) # u'$label' on line 135, col 5
            if _v is not None: write(_filter(_v, rawExpr=u'$label'))
            write(u'''</th>
<td>''')
            write(_filter( templ % subch.get_ldata()))
            write(u'''</td>
</tr>
''')
        
        ########################################
        ## END - generated method body
        
        return _dummyTrans and trans.response().getvalue() or ""
        

    def sub_platform(self, subch, **KWS):



        ## CHEETAH: generated from #def sub_platform(subch) at line 143, col 1.
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
        
        label = "Java Platform"
        if subch.is_change(): # generated from line 145, col 1
            write(u'''<tr>
<th rowspan="2">''')
            _v = VFFSL(SL,"label",True) # u'$label' on line 147, col 17
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
        else: # generated from line 153, col 1
            write(u'''<tr>
<th>''')
            _v = VFFSL(SL,"label",True) # u'$label' on line 155, col 5
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
        

    def sub_signature(self, subch, **KWS):



        ## CHEETAH: generated from #def sub_signature(subch) at line 163, col 1.
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
        if subch.is_change(): # generated from line 165, col 1
            write(u'''<tr>
<th rowspan="2">''')
            _v = VFFSL(SL,"label",True) # u'$label' on line 167, col 17
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
        elif subch.get_ldata(): # generated from line 174, col 1
            write(u'''<tr>
<th>''')
            _v = VFFSL(SL,"label",True) # u'$label' on line 176, col 5
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



        ## CHEETAH: generated from #def sub_deprecation(subch) at line 184, col 1.
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
        if subch.is_change(): # generated from line 186, col 1
            write(u'''<tr>
<th rowspan="2">''')
            _v = VFFSL(SL,"label",True) # u'$label' on line 188, col 17
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
        elif subch.get_ldata(): # generated from line 194, col 1
            write(u'''<tr>
<th>''')
            _v = VFFSL(SL,"label",True) # u'$label' on line 196, col 5
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

    _mainCheetahMethod_for_classdiff_ClassInfoChange = 'writeBody'

## END CLASS DEFINITION

if not hasattr(classdiff_ClassInfoChange, '_initCheetahAttributes'):
    templateAPIClass = getattr(classdiff_ClassInfoChange,
                               '_CHEETAH_templateClass',
                               Template)
    templateAPIClass._addCheetahPlumbingCodeToClass(classdiff_ClassInfoChange)


# CHEETAH was developed by Tavis Rudd and Mike Orr
# with code, advice and input from many other volunteers.
# For more information visit http://cheetahtemplate.org/

##################################################
## if run from command line:
if __name__ == '__main__':
    from Cheetah.TemplateCmdLineIface import CmdLineIface
    CmdLineIface(templateObj=classdiff_ClassInfoChange()).run()


