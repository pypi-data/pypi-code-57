import os
from nose import run
from utils import log
import time


class NoseEngine(object):

    def __init__(self):
        self.working_path = os.environ["working_path"]
        self.log_path = self.get_log_path()

    def get_log_path(self):
        log_path = os.path.join(self.working_path, "log")
        if os.path.exists(log_path) is False:
            os.mkdir(log_path)
        return log_path

    def run(self, test_case, test_path, parameters, queue):
        test_function = test_case.split(".")
        xml_name = "nosetests_%s_%s.xml" % (test_function[-1], time.time())
        xml_path = os.path.join(self.log_path, xml_name)
        argv = (['--exe', '--nocapture', '--with-printlog', '--with-xunit', '--xunit-file=%s'%xml_path, '-x'])
        argv.append(test_path)
        log.INFO("************ Begin to run tests:%s", test_case)
        ret = run(argv=argv, exit=False)
        if ret is True:
            log.INFO("TestCase run succeed.%s", test_case)
        else:
            log.ERR("TestCase run failed. %s", test_case)
        result = {"name":test_case, "result": ret, "log_path": xml_path, "xml_path": xml_path}
        queue.put(result)
        return ret
