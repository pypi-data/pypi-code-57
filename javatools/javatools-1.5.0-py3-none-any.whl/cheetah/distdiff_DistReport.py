

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
from javatools.cheetah.report import report
import javatools.distdiff
import javatools.change

##################################################
## MODULE CONSTANTS
VFFSL=valueFromFrameOrSearchList
VFSL=valueFromSearchList
VFN=valueForName
currentTime=time.time
__CHEETAH_version__ = '3.1.0'
__CHEETAH_versionTuple__ = (3, 1, 0, 'final', 1)
__CHEETAH_src__ = 'javatools/cheetah/distdiff_DistReport.tmpl'
__CHEETAH_srcLastModified__ = 'Fri Jun 21 12:39:34 2019'
__CHEETAH_docstring__ = '" "'

if __CHEETAH_versionTuple__ < RequiredCheetahVersionTuple:
    raise AssertionError(
      'This template was compiled with Cheetah version'
      ' %s. Templates compiled before version %s must be recompiled.'%(
         __CHEETAH_version__, RequiredCheetahVersion))

##################################################
## CLASSES

class distdiff_DistReport(report):

    ##################################################
    ## CHEETAH GENERATED METHODS


    def __init__(self, *args, **KWs):

        super(distdiff_DistReport, self).__init__(*args, **KWs)
        if not self._CHEETAH__instanceInitialized:
            cheetahKWArgs = {}
            allowedKWs = 'searchList namespaces filter filtersLib errorCatcher'.split()
            for k,v in KWs.items():
                if k in allowedKWs: cheetahKWArgs[k] = v
            self._initCheetahInstance(**cheetahKWArgs)
        

    def render_by_class(self, changes, label, **KWS):



        ## CHEETAH: generated from #def render_by_class(changes, label) at line 5, col 1.
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
        
        if changes: # generated from line 6, col 1
            write(u'''
<div class="change-category">
<h2>''')
            _v = VFFSL(SL,"label",True) # u'$label' on line 9, col 5
            if _v is not None: write(_filter(_v, rawExpr=u'$label'))
            write(u'''</h2>

''')
            chm = dict((ch.entry,ch) for ch in changes)
            write(u'''

''')
            for entry in sorted(chm.keys()): # generated from line 15, col 1
                _v = VFFSL(SL,"render_change",False)(chm[entry]) # u'$render_change(chm[entry])' on line 16, col 1
                if _v is not None: write(_filter(_v, rawExpr=u'$render_change(chm[entry])'))
                write(u'''
''')
            write(u'''
</div>
''')
        
        ########################################
        ## END - generated method body
        
        return _dummyTrans and trans.response().getvalue() or ""
        

    def details(self, **KWS):



        ## CHEETAH: generated from #block details at line 25, col 1.
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
        #  collect the changes into buckets by type
        change = getattr(self, "change")
        changemap = javatools.change.collect_by_type(change.collect())
        changeorder = (
            javatools.distdiff.DistClassAdded,
            javatools.distdiff.DistClassRemoved,
            javatools.distdiff.DistClassChange,
            javatools.distdiff.DistJarAdded,
            javatools.distdiff.DistJarRemoved,
            javatools.distdiff.DistJarChange,
            javatools.distdiff.DistJarChange,
            javatools.distdiff.DistTextChange,
            javatools.distdiff.DistManifestChange,
            javatools.distdiff.DistContentAdded,
            javatools.distdiff.DistContentRemoved,
            javatools.distdiff.DistContentChange,
        )
        
        ## gather SquashedChange instances under a more appropriate heading
        for sq in changemap.pop(javatools.change.SquashedChange, ()):
            oc = sq.origclass
            if oc is javatools.distdiff.DistJarReport:
                oc = javatools.distdiff.DistJarChange
            elif oc is javatools.distdiff.DistClassReport:
                oc = javatools.distdiff.DistClassChange
            sqm = changemap.setdefault(oc, [])
            sqm.append(sq)
        write(u'''

''')
        #  print the above types gathered in order
        for ct in changeorder: # generated from line 61, col 1
            _v = VFFSL(SL,"render_by_class",False)(changemap.pop(ct, tuple()), ct.label) # u'$render_by_class(changemap.pop(ct, tuple()), ct.label)' on line 62, col 1
            if _v is not None: write(_filter(_v, rawExpr=u'$render_by_class(changemap.pop(ct, tuple()), ct.label)'))
            write(u'''
''')
        write(u'''
''')
        #  print the remaining types
        for ct, changes in changemap.items(): # generated from line 66, col 1
            _v = VFFSL(SL,"render_by_class",False)(changes, ct.label) # u'$render_by_class(changes, ct.label)' on line 67, col 1
            if _v is not None: write(_filter(_v, rawExpr=u'$render_by_class(changes, ct.label)'))
            write(u'''
''')
        write(u'''
''')
        write(u'''
<!-- END BLOCK: details -->
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
        #  render a collection of changes that are all of the same type
        write(u'''

''')
        #  the overridden details block
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

    _mainCheetahMethod_for_distdiff_DistReport = 'writeBody'

## END CLASS DEFINITION

if not hasattr(distdiff_DistReport, '_initCheetahAttributes'):
    templateAPIClass = getattr(distdiff_DistReport,
                               '_CHEETAH_templateClass',
                               Template)
    templateAPIClass._addCheetahPlumbingCodeToClass(distdiff_DistReport)


# CHEETAH was developed by Tavis Rudd and Mike Orr
# with code, advice and input from many other volunteers.
# For more information visit http://cheetahtemplate.org/

##################################################
## if run from command line:
if __name__ == '__main__':
    from Cheetah.TemplateCmdLineIface import CmdLineIface
    CmdLineIface(templateObj=distdiff_DistReport()).run()


