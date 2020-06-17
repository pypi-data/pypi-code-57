import datetime
from airtest.core.api import *
from airtest.cli.parser import cli_setup
from poco.drivers.unity3d import UnityPoco
import poco.exceptions
from airtest.cli.parser import cli_setup
import poco.exceptions
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
from airtest.core.android.adb import *
from airtest.core.android.android import *
import base64



class base(object):
    def __init__(self,id):
        self.activity = "com.onlines1.games/com.puzzle.sdk.unity.PZUnityPlayerActivity"
        self.id = id
        self.path = 'screen' + '/'
        self.poco = UnityPoco()
        connect_device("android:///" + self.id)
        self.android = Android(serialno=self.id)
        self.devices = ADB().devices()
    def count_time(func):
        def int_time(*args, **kwargs):
            start_time = datetime.datetime.now()
            func(*args, **kwargs)
            over_time = datetime.datetime.now()
            total_time = (over_time - start_time).total_seconds()
            print('共计%s秒' % total_time)
        return int_time

    def snapshot(self,name):
        a = self.poco.snapshot(2073600)
        print(a)
        print(type(a[0]))
        img = base64.b64decode(a[0])
        print(img)
        print(type(img))
        print(str(img))
        jpg = self.id + '/' + self.id + name + '.jpg'
        with open(jpg, 'wb') as f:
            f.write(img)

    def log(self,filename):
        a = self.android.logcat()
        filename = filename + '/' + self.id + 'log.txt'
        try:
            while True:
                with open(filename,'a+') as f:
                    f.write(str(next(a)))
                    f.write('\n')
        except StopIteration:
            pass

    @count_time
    def install(self):
        print('id = ' + self.id)
        if self.android.check_app('com.onlines1.games'):
            print('已存在安装包，开始卸载',self.id)
            self.android.uninstall_app('com.onlines1.games')
        print('开始安装')
        self.android.install_app('E:\\111\\testTools\compatible\\01-02_1709_debug.apk',False,install_options = ['-g'])

        try:
            self.android.check_app('com.onlines1.games')
            print('安装成功')
        except AirtestError:
            print(AirtestError)
            raise ('安装失败！！！！！！！')

        print('安装完成')

    @count_time
    def startup(self):
        self.android.start_app('com.onlines1.games')
        time.sleep(1)
        try:
            b = self.android.shell('dumpsys activity | grep -i run | grep %s'%self.activity)
            print(b)
        except Exception:
            print(Exception)
            self.snapshot('启动失败')
            raise ("启动失败！！！！！！！！！")
        print('启动进程完成')

    def update(self):
        while True:
            try:
                self.poco = UnityPoco()
                if self.poco("Slider").exists() :
                    print('exist')
                    self.snapshot('开始热更')
                    starttime = time.time()
                    break
                elif self.poco("Enter_btn_user").child("image").exists():
                    print('检测到登录界面')
                    self.snapshot('检测到登录界面')
                    break
            except Exception as e:
                continue

        while True:
            if self.poco("Slider").exists():
                endtime = time.time()
                if endtime - starttime >300:
                    print('热更超时')
                    self.snapshot('热更超时')
                    raise ('热更超时')
                    break
            elif self.poco("Enter_btn_user").child("image").exists():
                endtime = time.time()
                usetime = str(endtime - starttime)
                print('热更正常')
                self.snapshot('热更正常')
                print('热更用时' + usetime + 's')
                break

        print('更新检查完毕')
        sys.exit(1)

    def login(self):
        print('login')
        if self.poco("Enter_btn_user").child("image").exists():
            self.poco("Enter_btn_user").child("image").click()
            print('登录成功')
            self.snapshot('找到登录按钮')
        else:
            print('未找到登录按钮')
            self.snapshot('未找到登录按钮')

    def uninstall(self):
        self.android.uninstall_app('com.onlines1.games')


# print(os.sep)
# print(('E:\\111\\testTools\compatible\\test.air\\01-02_1709_debug.apk').replace("\\",os.sep))