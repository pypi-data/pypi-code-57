import os, sys, re, subprocess

try:
    from aos.usertrace.report import Report
    from aos.constant import AOS_INVESTIGATION_FILE, DEBUG_PRINT
    from aos.util import debug, get_locale
except Exception as e:
    print("Failure when import modules in do_repot: %s" % format(e))
    sys.exit(1)

def is_report_enabled():
    ret = False

    if os.path.isfile(AOS_INVESTIGATION_FILE):
        try:
            with open(AOS_INVESTIGATION_FILE, 'r') as f:
                lines = f.read().splitlines()
                for l in lines:
                    l = l.strip()
                    if l.startswith('participate:'):
                        choice = re.findall(r'^participate:\s*(\S+)', l)
                        if not choice:
                            break
                        choice = choice[0].strip()
                        debug("participate? %s" % choice)
                        if choice == 'Yes' or choice == 'Y' or \
                           choice == 'yes' or choice == 'y':
                            ret =True
                            break
        except Exception as e:
            pass

    return ret

def do_report(args=None):
    if not args:
        cmd = ['python', __file__]
    elif len(args) == 3:
        cmd = ['python', __file__] + args
    else:
        return

    try:
        proc = subprocess.Popen(cmd,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                stdin=subprocess.PIPE)

        if DEBUG_PRINT:
            out, err = proc.communicate()
            if out:
                debug(out.decode(get_locale()))
            if err:
                debug(err.decode(get_locale()))
    except:
        debug("Failure when reporting: %s" % format(e))
        pass

op_report = {'op': '', 'content': '', 'result': ''}

def format_escaped(str):
    newstr = ''
    first = True

    if str:
        str = str.replace('\\', '/')
        for l in str.splitlines():
            if first:
                first = False
            else:
                # fix escaped newline char issue in json string
                newstr += "\\n"

            newstr += l

    return newstr

def init_op():
    #global op_report
    #op_report = {'op': '', 'content': '', 'result': ''}
    pass

def set_op(op=None, content=None, result=None):
    global op_report
    if op:
        op_report['op'] = format_escaped(op)
    if content:
        op_report['content'] = format_escaped(content)
    if result:
        op_report['result'] = format_escaped(result)

def report_op():
    global op_report
    if op_report['op'] and op_report['result']:
        do_report([op_report['op'], op_report['content'], op_report['result']])
        op_report = {'op': '', 'content': '', 'result': ''}

if __name__ == '__main__':
    if is_report_enabled():
        reporter = Report()
        if len(sys.argv) == 1:
            if not reporter.report_install():
                sys.exit(1)
        elif len(sys.argv) == 4:
            if not reporter.report_operate(sys.argv[1], sys.argv[2], sys.argv[3]):
                sys.exit(1)

    sys.exit(0)
