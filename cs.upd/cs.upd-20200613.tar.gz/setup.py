#!/usr/bin/env python
from setuptools import setup
setup(
  name = 'cs.upd',
  author = 'Cameron Simpson',
  author_email = 'cs@cskk.id.au',
  version = '20200613',
  url = 'https://bitbucket.org/cameron_simpson/css/commits/all',
  description =
    'Single and multiple line status updates with minimal update sequences.',
  long_description =
    ('Single and multiple line status updates with minimal update sequences.\n'    
 '\n'    
 '*Latest release 20200613*:\n'    
 '* New UpdProxy.__call__ which sets the .text property in the manner of '    
 'logging calls, with (msg,*a).\n'    
 '* New Upd.normalise static method exposing the text normalisation '    
 '`unctrl(text.rstrip())`.\n'    
 '* New UpdProxy.prefix attribute with a fixed prefix for status updates; '    
 '`prefix+text` is left cropped for display purposes when updated.\n'    
 '* New UpdProxy.width property computing the space available after the '    
 'prefix, useful for sizing things like progress bars.\n'    
 '* Make UpdProxy a context manager which self deletes on exit.\n'    
 '* Upd: make default backend=sys.stderr, eases the common case.\n'    
 '* New Upd.above() context manager to support interleaving another stream '    
 'with the output, as when stdout (for print) is using the same terminal as '    
 'stderr (for Upd).\n'    
 '* New out() top level function for convenience use with the default Upd().\n'    
 '* New nl() top level function for writing a line to stderr.\n'    
 '* New print() top level function wrapping the builtin print; callers can use '    
 '"from cs.upd import print" to easily interleave print() with cs.upd use.\n'    
 '\n'    
 'This is available as an output mode in `cs.logutils`.\n'    
 '\n'    
 'Single line example:\n'    
 '\n'    
 '    from cs.upd import Upd, nl, print\n'    
 '    .....\n'    
 '    with Upd() as U:\n'    
 '        for filename in filenames:\n'    
 '            U.out(filename)\n'    
 '            ... process filename ...\n'    
 "            U.nl('an informational line to stderr')\n"    
 "            print('a line to stdout')\n"    
 '\n'    
 'Multiline multithread example:\n'    
 '\n'    
 '    from threading import Thread\n'    
 '    from cs.upd import Upd, print\n'    
 '    .....\n'    
 '    def runner(filename, proxy):\n'    
 '        # initial status message\n'    
 '        proxy.text = "process %r" % filename\n'    
 '        ... at various points:\n'    
 '            # update the status message with current progress\n'    
 "            proxy.text = '%r: progress status here' % filename\n"    
 '        # completed, remove the status message\n'    
 '        proxy.close()\n'    
 '        # print completion message to stdout\n'    
 '        print("completed", filename)\n'    
 '    .....\n'    
 '    with Upd() as U:\n'    
 '        U.out("process files: %r", filenames)\n'    
 '        Ts = []\n'    
 '        for filename in filenames:\n'    
 '            proxy = U.insert(1) # allocate an additional status line\n'    
 '            T = Thread(\n'    
 '                "process "+filename,\n'    
 '                target=runner,\n'    
 '                args=(filename, proxy))\n'    
 '            Ts.append(T)\n'    
 '            T.start()\n'    
 '        for T in Ts:\n'    
 '            T.join()\n'    
 '\n'    
 '## Function `cleanupAtExit()`\n'    
 '\n'    
 'Cleanup function called at programme exit to clear the status line.\n'    
 '\n'    
 '## Function `nl(msg, *a, **kw)`\n'    
 '\n'    
 'Write `msg` to `file` (default `sys.stdout`),\n'    
 'without interfering with the `Upd` instance.\n'    
 'This is a thin shim for `Upd.print`.\n'    
 '\n'    
 '## Function `out(msg, *a, **outkw)`\n'    
 '\n'    
 'Update the status line of the default `Upd` instance.\n'    
 'Parameters are as for `Upd.out()`.\n'    
 '\n'    
 '## Function `print(*a, **kw)`\n'    
 '\n'    
 'Wrapper for the builtin print function\n'    
 'to call it inside `Upd.above()` and enforce a flush.\n'    
 '\n'    
 'The function supports an addition parameter beyond the builtin print:\n'    
 '* `upd`: the `Upd` instance to use, default `Upd()`\n'    
 '\n'    
 'Programmes intregrating `cs.upd` with use of the builtin `print`\n'    
 'function should use this as import time:\n'    
 '\n'    
 '    from cs.upd import print\n'    
 '\n'    
 '## Class `Upd(cs.obj.SingletonMixin)`\n'    
 '\n'    
 'A `SingletonMixin` subclass for maintaining a regularly updated status '    
 'line.\n'    
 '\n'    
 'The default backend is `sys.stderr`.\n'    
 '\n'    
 '## Class `UpdProxy`\n'    
 '\n'    
 'A proxy for a status line of a multiline `Upd`.\n'    
 '\n'    
 'This provides a stable reference to a status line after it has been\n'    
 'instantiated by `Upd.insert`.\n'    
 '\n'    
 'The status line can be accessed and set via the `.text` property.\n'    
 '\n'    
 'An `UpdProxy` is also a context manager which self deletes on exit:\n'    
 '\n'    
 '    U = Upd()\n'    
 '    ....\n'    
 "    with U.insert(1, 'hello!') as proxy:\n"    
 '        .... set proxy.text as needed ...\n'    
 '    # proxy now removed\n'    
 '\n'    
 '# Release Log\n'    
 '\n'    
 '\n'    
 '\n'    
 '*Release 20200613*:\n'    
 '* New UpdProxy.__call__ which sets the .text property in the manner of '    
 'logging calls, with (msg,*a).\n'    
 '* New Upd.normalise static method exposing the text normalisation '    
 '`unctrl(text.rstrip())`.\n'    
 '* New UpdProxy.prefix attribute with a fixed prefix for status updates; '    
 '`prefix+text` is left cropped for display purposes when updated.\n'    
 '* New UpdProxy.width property computing the space available after the '    
 'prefix, useful for sizing things like progress bars.\n'    
 '* Make UpdProxy a context manager which self deletes on exit.\n'    
 '* Upd: make default backend=sys.stderr, eases the common case.\n'    
 '* New Upd.above() context manager to support interleaving another stream '    
 'with the output, as when stdout (for print) is using the same terminal as '    
 'stderr (for Upd).\n'    
 '* New out() top level function for convenience use with the default Upd().\n'    
 '* New nl() top level function for writing a line to stderr.\n'    
 '* New print() top level function wrapping the builtin print; callers can use '    
 '"from cs.upd import print" to easily interleave print() with cs.upd use.\n'    
 '\n'    
 '*Release 20200517*:\n'    
 '* Multiline support!\n'    
 '* Multiline support!\n'    
 '* Multiline support!\n'    
 '* New UpdProxy class to track a status line of a multiline Upd in the face '    
 'of further inserts and deletes.\n'    
 '* Upd(...) now returns a context manager to clean up the display on its '    
 'exit.\n'    
 '* Upd(...) is now a SingletonMixin in order to use the same state if set up '    
 'in multiple places.\n'    
 '\n'    
 '*Release 20200229*:\n'    
 '* Upd: can now be used as a context manager, clearing the line on exit.\n'    
 '* Upd.without is now a context manager, returning the older state, and '    
 'accepting an optional inner state (default "").\n'    
 '* Upd is now a singleton factory, obsoleting upd_for.\n'    
 '* Upd.nl: use "insert line above" mode if supported.\n'    
 '\n'    
 '*Release 20181108*:\n'    
 'Documentation improvements.\n'    
 '\n'    
 '*Release 20170903*:\n'    
 '* New function upd_for(stream) returning singleton Upds.\n'    
 '* Drop noStrip keyword argument/mode - always strip trailing whitespace.\n'    
 '\n'    
 '*Release 20160828*:\n'    
 '* Use "install_requires" instead of "requires" in DISTINFO.\n'    
 '* Add Upd.flush method.\n'    
 '* Upd.out: fix longstanding trailing text erasure bug.\n'    
 '* Upd.nl,out: accept optional positional parameters, use with %-formatting '    
 'if supplied, just like logging.\n'    
 '\n'    
 '*Release 20150118*:\n'    
 'metadata fix\n'    
 '\n'    
 '*Release 20150116*:\n'    
 'Initial PyPI release.'),
  classifiers = ['Programming Language :: Python', 'Programming Language :: Python :: 2', 'Programming Language :: Python :: 3', 'Development Status :: 4 - Beta', 'Intended Audience :: Developers', 'Operating System :: OS Independent', 'Topic :: Software Development :: Libraries :: Python Modules', 'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)'],
  install_requires = ['cs.gimmicks', 'cs.lex', 'cs.obj', 'cs.tty'],
  keywords = ['python2', 'python3'],
  license = 'GNU General Public License v3 or later (GPLv3+)',
  long_description_content_type = 'text/markdown',
  package_dir = {'': 'lib/python'},
  py_modules = ['cs.upd'],
)
