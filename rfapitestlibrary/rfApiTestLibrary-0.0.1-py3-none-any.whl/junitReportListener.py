'''
Documentation: 监听，把robot framework test数据转成junit报告,junit数据类似于如下:
<?xml version="1.0" encoding="UTF-8" ?>
<testsuite errors="0" failures="2" hostname="barry-HP" name="null" tests="3" time="0.069" timestamp="2013-06-18T07:49:02">
  <properties />
  <testcase classname="barrypitman.junitXmlFormatter.SampleTests" name="testException" time="0.007">
    <failure type="testException(barrypitman.junitXmlFormatter.SampleTests)">java.lang.IllegalArgumentException
	at barrypitman.junitXmlFormatter.SampleTests.testException(SampleTests.java:27)
	at barrypitman.junitXmlFormatter.Runner.runTests(Runner.java:27)
	at barrypitman.junitXmlFormatter.RunnerTest.testRunnerWithSampleTests(RunnerTest.java:18)
	at com.intellij.junit4.JUnit4IdeaTestRunner.startRunnerWithArgs(JUnit4IdeaTestRunner.java:77)
	at com.intellij.rt.execution.junit.JUnitStarter.prepareStreamsAndStart(JUnitStarter.java:195)
	at com.intellij.rt.execution.junit.JUnitStarter.main(JUnitStarter.java:63)
	at com.intellij.rt.execution.application.AppMain.main(AppMain.java:120)
</failure>
  </testcase>
  <testcase classname="barrypitman.junitXmlFormatter.SampleTests" name="testAssertionError" time="0.002">
    <failure type="testAssertionError(barrypitman.junitXmlFormatter.SampleTests)">java.lang.AssertionError
	at barrypitman.junitXmlFormatter.SampleTests.testAssertionError(SampleTests.java:22)
	at barrypitman.junitXmlFormatter.Runner.runTests(Runner.java:27)
	at barrypitman.junitXmlFormatter.RunnerTest.testRunnerWithSampleTests(RunnerTest.java:18)
	at com.intellij.junit4.JUnit4IdeaTestRunner.startRunnerWithArgs(JUnit4IdeaTestRunner.java:77)
	at com.intellij.rt.execution.junit.JUnitStarter.prepareStreamsAndStart(JUnitStarter.java:195)
	at com.intellij.rt.execution.junit.JUnitStarter.main(JUnitStarter.java:63)
	at com.intellij.rt.execution.application.AppMain.main(AppMain.java:120)
</failure>
  </testcase>
  <testcase classname="barrypitman.junitXmlFormatter.SampleTests" name="testSuccess" time="0.0" />
</testsuite>
'''
import os
import re

ROBOT_LISTENER_API_VERSION = 2
JUNIT_XML_DIR_PATH= '../'

junit_xml_result='<?xml version="1.0" encoding="utf-8"?>\n\n'
test_suite_result=''
test_case_result=''
test_case_format='<testcase classname ="%s" name = "%s" time = "%s" %s>\n'
test_case_failuer_format='<failure>%s</failure>\n'
test_suite_format='<testsuite failures="%s" name="%s" tests="%s" time="%s" timestamp="%s">\n'
test_suite_end_format='</testsuite>\n'
test_case_end_format='</testcase>\n'
junit_result_xml_name='abc'


def write_junit_xml(file_dir,file_name,content):
    '''
    如果是路径存在,但是是个文件夹，直接退出。
    :param file_path: 文件路径
    '''
    file_path=file_dir + file_name
    if(os.path.exists(file_path)):
        if os.path.isdir(file_path):
            #不能轻易删除文件夹
            print("监听生成文件【"+file_path+"】是个文件夹")
            exit -1
        #删除文件,并且创建文件
        os.remove(file_path)
        create_file(file_path,content)
    else:
        #创建文件
        create_file(file_path,content)


def create_file(file_path,content):
    f=open(file_path,"a")
    f.write(content)
    f.close

def end_suite(name, attrs):
    '''
    {'id': 's1', 'longname': '2', 'doc': '', 'metadata': {}, 'starttime': '20191118 15:09:48.760', 'endtime': '20191118 15:09:48.799', 'elapsedtime': 39, 'status': 'PASS', 'message': '', 'tests': ['Demo 4', 'Demo 5'], 'suites': [], 'totaltests': 2, 'source': '<绝对路径>/test/2.robot', 'statistics': '2 critical tests, 2 passed, 0 failed\n2 tests total, 2 passed, 0 failed'}
    :param name:
    :param attrs:
    :return:
    '''
    global test_suite_result
    global junit_result_xml_name
    statistics=attrs['statistics']
    test_suite_result=test_suite_format %(_get_suite_total_failed(statistics),attrs['longname'],attrs['totaltests'],attrs['elapsedtime']/1000,attrs['starttime'])

def end_test(name, attrs):
    global test_case_result
    the_test_case_result=''
    elapsedtime=attrs["elapsedtime"]/1000
    if attrs['status']=='PASS':
        '''
        解析成功例子，attrs
        {'id': 's1-t1', 'longname': '1.Demo 1', 'doc': '', 'tags': [], 'starttime': '20191118 14:05:06.033', 'endtime': '20191118 14:05:06.035', 'elapsedtime': 2, 'status': 'PASS', 'message': '', 'critical': 'yes', 'template': ''}
        '''
        the_test_case_result=test_case_format % (name,name,elapsedtime,'/')
    else:
        '''
        解析错误例子
        {'id': 's1-t2', 'longname': '1.Demo 2', 'doc': '', 'tags': [], 'starttime': '20191118 14:05:06.036', 'endtime': '20191118 14:05:06.037', 'elapsedtime': 1, 'status': 'FAIL', 'message': 'erorr', 'critical': 'yes', 'template': ''}
        '''
        the_test_case_result=test_case_format % (name,name,elapsedtime,'')
        the_test_case_result+=test_case_failuer_format % (attrs['message'])
        the_test_case_result+=test_case_end_format
    test_case_result+=the_test_case_result

def close():
    global junit_xml_result
    global junit_result_xml_name
    junit_xml_result+=test_suite_result
    junit_xml_result+=test_case_result
    junit_xml_result+=test_suite_end_format
    write_junit_xml(JUNIT_XML_DIR_PATH,junit_result_xml_name+'.xml',junit_xml_result)


def _get_suite_total_passed(statistics):
    '''
    处理如下statistics的值，获取成功的数量
    '3 critical tests, 2 passed, 1 failed\n3 tests total, 2 passed, 1 failed'
    :return: 数字,多少个用例passed
    '''
    pattern = re.compile(r'\s+(\d+)\s+passed,')
    passed_count_list=pattern.findall(statistics)
    if len(passed_count_list)==0:
        print('获取suite成功数目出错')
        exit(-1)
    return passed_count_list[0]

def _get_suite_total_failed(statistics):
    '''
    处理如下statistics的值，获取成功的数量
    '3 critical tests, 2 passed, 1 failed\n3 tests total, 2 passed, 1 failed'
    :return: 数字,多少个用例passed
    '''
    pattern = re.compile(r'\s+(\d+)\s+failed')
    failed_count_list=pattern.findall(statistics)
    if len(failed_count_list)==0:
        print('获取suite失败数目出错')
        exit(-1)
    return failed_count_list[0]