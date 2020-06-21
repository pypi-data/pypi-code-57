

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
from os.path import join

##################################################
## MODULE CONSTANTS
VFFSL=valueFromFrameOrSearchList
VFSL=valueFromSearchList
VFN=valueForName
currentTime=time.time
__CHEETAH_version__ = '3.1.0'
__CHEETAH_versionTuple__ = (3, 1, 0, 'final', 1)
__CHEETAH_src__ = 'javatools/cheetah/report.tmpl'
__CHEETAH_srcLastModified__ = 'Mon Aug 11 10:25:58 2014'
__CHEETAH_docstring__ = '" "'

if __CHEETAH_versionTuple__ < RequiredCheetahVersionTuple:
    raise AssertionError(
      'This template was compiled with Cheetah version'
      ' %s. Templates compiled before version %s must be recompiled.'%(
         __CHEETAH_version__, RequiredCheetahVersion))

##################################################
## CLASSES

class report(Template):

    ##################################################
    ## CHEETAH GENERATED METHODS


    def __init__(self, *args, **KWs):

        super(report, self).__init__(*args, **KWs)
        if not self._CHEETAH__instanceInitialized:
            cheetahKWArgs = {}
            allowedKWs = 'searchList namespaces filter filtersLib errorCatcher'.split()
            for k,v in KWs.items():
                if k in allowedKWs: cheetahKWArgs[k] = v
            self._initCheetahInstance(**cheetahKWArgs)
        

    def title(self, **KWS):



        ## CHEETAH: generated from #def title at line 9, col 1.
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
        
        _v = VFFSL(SL,"change.__class__.__name__",True) # u'$change.__class__.__name__' on line 10, col 1
        if _v is not None: write(_filter(_v, rawExpr=u'$change.__class__.__name__'))
        write(u'''
''')
        
        ########################################
        ## END - generated method body
        
        return _dummyTrans and trans.response().getvalue() or ""
        

    def head_title(self, **KWS):



        ## CHEETAH: generated from #block head_title at line 17, col 1.
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
<!-- START BLOCK: head_title -->
<title>''')
        _v = VFFSL(SL,"title",True) # u'$title' on line 18, col 8
        if _v is not None: write(_filter(_v, rawExpr=u'$title'))
        write(u'''</title>
''')
        write(u'''
<!-- END BLOCK: head_title -->
''')
        
        ########################################
        ## END - generated method body
        
        return _dummyTrans and trans.response().getvalue() or ""
        

    def head_meta(self, **KWS):



        ## CHEETAH: generated from #block head_meta at line 22, col 1.
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
<!-- START BLOCK: head_meta -->
''')
        write(u'''
<!-- END BLOCK: head_meta -->
''')
        
        ########################################
        ## END - generated method body
        
        return _dummyTrans and trans.response().getvalue() or ""
        

    def head_stylesheets(self, **KWS):



        ## CHEETAH: generated from #block head_stylesheets at line 26, col 1.
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
<!-- START BLOCK: head_stylesheets -->
''')
        for ss in VFFSL(SL,"stylesheets",True): # generated from line 27, col 1
            write(u'''<link rel="stylesheet" type="text/css" href="''')
            _v = VFFSL(SL,"ss",True) # u'$ss' on line 28, col 46
            if _v is not None: write(_filter(_v, rawExpr=u'$ss'))
            write(u'''" />
''')
        write(u'''
<!-- END BLOCK: head_stylesheets -->
''')
        
        ########################################
        ## END - generated method body
        
        return _dummyTrans and trans.response().getvalue() or ""
        

    def head_javascripts(self, **KWS):



        ## CHEETAH: generated from #block head_javascripts at line 33, col 1.
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
<!-- START BLOCK: head_javascripts -->
''')
        if not getattr(VFFSL(SL,"options",True), "html_no_jquery", False): # generated from line 34, col 1
            write(u'''<script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.7.1/jquery.min.js" type="text/javascript"></script>
''')
        for js in VFFSL(SL,"javascripts",True): # generated from line 37, col 1
            write(u'''<script type="text/javascript" src="''')
            _v = VFFSL(SL,"js",True) # u'$js' on line 38, col 37
            if _v is not None: write(_filter(_v, rawExpr=u'$js'))
            write(u'''"></script>
''')
        write(u'''
<!-- END BLOCK: head_javascripts -->
''')
        
        ########################################
        ## END - generated method body
        
        return _dummyTrans and trans.response().getvalue() or ""
        

    def head_extra(self, **KWS):



        ## CHEETAH: generated from #block head_extra at line 43, col 1.
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
<!-- START BLOCK: head_extra -->
''')
        write(u'''
<!-- END BLOCK: head_extra -->
''')
        
        ########################################
        ## END - generated method body
        
        return _dummyTrans and trans.response().getvalue() or ""
        

    def body_breadcrumb(self, **KWS):



        ## CHEETAH: generated from #block body_breadcrumb at line 58, col 1.
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
<!-- START BLOCK: body_breadcrumb -->
<ul class="breadcrumbs">
''')
        for p,t in VFFSL(SL,"breadcrumbs",True): # generated from line 61, col 1
            write(u'''<li><a href="''')
            write(_filter( join(p,t+".html")))
            write(u'''">''')
            write(_filter( t))
            write(u'''</a></li>
''')
        write(u'''<li>''')
        _v = VFFSL(SL,"title",True) # u'$title' on line 64, col 5
        if _v is not None: write(_filter(_v, rawExpr=u'$title'))
        write(u'''</li>
</ul>
''')
        write(u'''
<!-- END BLOCK: body_breadcrumb -->
''')
        
        ########################################
        ## END - generated method body
        
        return _dummyTrans and trans.response().getvalue() or ""
        

    def body_heading(self, **KWS):



        ## CHEETAH: generated from #block body_heading at line 54, col 1.
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
<!-- START BLOCK: body_heading -->
<div id="report-heading">


''')
        self.body_breadcrumb(trans=trans)
        write(u'''

<h1>''')
        _v = VFFSL(SL,"title",True) # u'$title' on line 69, col 5
        if _v is not None: write(_filter(_v, rawExpr=u'$title'))
        write(u'''</h1>
</div>
''')
        write(u'''
<!-- END BLOCK: body_heading -->
''')
        
        ########################################
        ## END - generated method body
        
        return _dummyTrans and trans.response().getvalue() or ""
        

    def into(self, **KWS):



        ## CHEETAH: generated from #block into at line 74, col 1.
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
<!-- START BLOCK: into -->
<div id="report-intro">
</div>
''')
        write(u'''
<!-- END BLOCK: into -->
''')
        
        ########################################
        ## END - generated method body
        
        return _dummyTrans and trans.response().getvalue() or ""
        

    def details(self, **KWS):



        ## CHEETAH: generated from #block details at line 80, col 1.
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
<div id="report-details">
''')
        for child in VFN(VFFSL(SL,"change",True),"collect",False)(): # generated from line 82, col 1
            _v = VFFSL(SL,"render_change",False)(VFFSL(SL,"child",True)) # u'$render_change($child)' on line 83, col 1
            if _v is not None: write(_filter(_v, rawExpr=u'$render_change($child)'))
            write(u'''
''')
        write(u'''</div>
''')
        write(u'''
<!-- END BLOCK: details -->
''')
        
        ########################################
        ## END - generated method body
        
        return _dummyTrans and trans.response().getvalue() or ""
        

    def outro(self, **KWS):



        ## CHEETAH: generated from #block outro at line 89, col 1.
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
<!-- START BLOCK: outro -->
<div id="report-outro">
</div>
''')
        write(u'''
<!-- END BLOCK: outro -->
''')
        
        ########################################
        ## END - generated method body
        
        return _dummyTrans and trans.response().getvalue() or ""
        

    def body(self, **KWS):



        ## CHEETAH: generated from #block body at line 50, col 1.
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
<!-- START BLOCK: body -->
<body>


''')
        self.body_heading(trans=trans)
        write(u'''

''')
        self.into(trans=trans)
        write(u'''

''')
        self.details(trans=trans)
        write(u'''

''')
        self.outro(trans=trans)
        write(u'''

</body>
''')
        write(u'''
<!-- END BLOCK: body -->
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
        
        write(u'''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html 
     PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
    "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">





<head>


''')
        self.head_title(trans=trans)
        write(u'''

''')
        self.head_meta(trans=trans)
        write(u'''

''')
        self.head_stylesheets(trans=trans)
        write(u'''

''')
        self.head_javascripts(trans=trans)
        write(u'''

''')
        self.head_extra(trans=trans)
        write(u'''

</head>


''')
        self.body(trans=trans)
        write(u'''

</html>


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

    _mainCheetahMethod_for_report = 'respond'

## END CLASS DEFINITION

if not hasattr(report, '_initCheetahAttributes'):
    templateAPIClass = getattr(report,
                               '_CHEETAH_templateClass',
                               Template)
    templateAPIClass._addCheetahPlumbingCodeToClass(report)


# CHEETAH was developed by Tavis Rudd and Mike Orr
# with code, advice and input from many other volunteers.
# For more information visit http://cheetahtemplate.org/

##################################################
## if run from command line:
if __name__ == '__main__':
    from Cheetah.TemplateCmdLineIface import CmdLineIface
    CmdLineIface(templateObj=report()).run()


