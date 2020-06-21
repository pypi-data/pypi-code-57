# -*- coding: utf-8 -*-
import time,hashlib,json,re,os,platform,sys,shutil,zipfile,requests,importlib,traceback,pip
import datetime as core_datetime
from kcweb import config
from kcweb.utill.dateutil.relativedelta import relativedelta as core_relativedelta
from kcweb.utill.db import mysql as kcwmysql
from kcweb.utill.db import mongodb as kcwmongodb
from kcweb.utill.db import sqlite as kcwsqlite
from kcweb.utill.cache import cache as kcwcache
from kcweb.utill.redis import redis as kcwredis
from kcweb.utill.http import Http
from kcweb.utill.queues import Queues
from kcweb.utill.db import model
from mako.template import Template as kcwTemplate
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
from . import globals
redis=kcwredis()
def send_mail(user,text="邮件内容",theme="邮件主题",recNick="收件人昵称"):
    """发送邮件

    参数 user：接收邮件的邮箱地址

    参数 text：邮件内容

    参数 theme：邮件主题

    参数 recNick：收件人昵称

    return Boolean类型
    """
    ret=True
    if not theme:
        theme=config.email['theme']
    if not recNick:
        recNick=config.email['recNick']
    try:
        msg=MIMEText(text,'plain','utf-8')
        msg['From']=formataddr([config.email['sendNick'],config.email['sender']]) 
        msg['To']=formataddr([recNick,user]) 
        msg['Subject']=theme

        server=smtplib.SMTP_SSL("smtp.qq.com", 465) 
        server.login(config.email['sender'], config.email['pwd']) 
        server.sendmail(config.email['sender'],[user,],msg.as_string())
        server.quit()
    except Exception:
        ret=False
    return ret
get_sysinfodesffafew=None
def get_sysinfo():
    """获取系统信息

    return dict类型
    """
    global get_sysinfodesffafew
    if get_sysinfodesffafew:
        sysinfo=get_sysinfodesffafew
    else:
        sysinfo={}
        sysinfo['platform']=platform.platform()        #获取操作系统名称及版本号，'Linux-3.13.0-46-generic-i686-with-Deepin-2014.2-trusty'  
        sysinfo['version']=platform.version()         #获取操作系统版本号，'#76-Ubuntu SMP Thu Feb 26 18:52:49 UTC 2015'
        sysinfo['architecture']=platform.architecture()    #获取操作系统的位数，('32bit', 'ELF')
        sysinfo['machine']=platform.machine()         #计算机类型，'i686'
        sysinfo['node']=platform.node()            #计算机的网络名称，'XF654'
        sysinfo['processor']=platform.processor()       #计算机处理器信息，''i686'
        sysinfo['uname']=platform.uname()           #包含上面所有的信息汇总，('Linux', 'XF654', '3.13.0-46-generic', '#76-Ubuntu SMP Thu Feb 26 18:52:49 UTC 2015', 'i686', 'i686')
        sysinfo['start_time']=times()
        get_sysinfodesffafew=sysinfo
            # 还可以获得计算机中python的一些信息：
            # import platform
            # platform.python_build()
            # platform.python_compiler()
            # platform.python_branch()
            # platform.python_implementation()
            # platform.python_revision()
            # platform.python_version()
            # platform.python_version_tuple()
    return sysinfo
def Template(path,**context):
    "模板渲染引擎函数,使用配置的模板路径"
    return Templates(str(config.app['tpl_folder'])+str(path),**context)
def Templates(path,**context):
    "模板渲染引擎函数，需要完整的模板目录文件"
    body=''
    with open(path, 'r',encoding='utf-8') as f:
        content=f.read()
        t=kcwTemplate(content)
        body=t.render(**context)
    return body
def mysql(table=None,configss=None):
    """mysql数据库操作实例
    
    参数 table：表名

    参数 configss 数据库配置  可以传数据库名字符串
    """
    dbs=kcwmysql.mysql()
    if table is None:
        return dbs
    elif configss:
        return dbs.connect(configss).table(table)
    else:
        return dbs.connect(config.database).table(table)
def sqlite(table=None,configss=None):
    """sqlite数据库操作实例
    
    参数 table：表名

    参数 configss 数据库配置  可以传数据库名字符串
    """
    dbs=kcwsqlite.sqlite()
    if table is None:
        return dbs
    elif configss:
        return dbs.connect(configss).table(table)
    else:
        return dbs.connect(config.sqlite).table(table)
def M(table=None,confi=None):
    """数据库操作实例
    
    参数 table：表名

    参数 confi 数据库配置  可以传数据库名字符串
    """
    if confi:
        if confi['type']=='sqlite':
            return sqlite(table,confi)
        else:
            return mysql(table,confi)
    else:
        if config.database['type']=='sqlite':
            return sqlite(table)
        else:
            return mysql(table)
def mongo(table=None,configss=None):
    """mongodb数据库操作实例
    
    参数 table：表名(mongodb数据库集合名)

    参数 configss mongodb数据库配置  可以传数据库名字符串
    """
    mObj=kcwmongodb.mongo()
    if table is None:
        return mObj
    elif configss:
        return mObj.connect(configss).table(table)
    else:
        return mObj.connect(config.mongo).table(table)
def is_index(params,index):
    """判断列表或字典里的索引是否存在

    params  列表或字典

    index   索引值

    return Boolean类型
    """
    try:
        params[index]
    except KeyError:
        return False
    except IndexError:
        return False
    else:
        return True
def set_cache(name,values,expire="no"):
    """设置缓存

    参数 name：缓存名

    参数 values：缓存值

    参数 expire：缓存有效期 0表示永久  单位 秒
    
    return Boolean类型
    """
    return kcwcache.cache().set_cache(name,values,expire)
def get_cache(name):
    """获取缓存

    参数 name：缓存名

    return 或者的值
    """
    return kcwcache.cache().get_cache(name)
def del_cache(name):
    """删除缓存

    参数 name：缓存名

    return Boolean类型
    """
    return kcwcache.cache().del_cache(name)
def md5(strs):
    """md5加密
    
    参数 strs：要加密的字符串

    return String类型
    """
    m = hashlib.md5()
    b = strs.encode(encoding='utf-8')
    m.update(b)
    return m.hexdigest()
def times():
    """生成时间戳整数 精确到秒(10位数字)
    
    return int类型
    """
    return int(time.time())
def json_decode(strs):
    """json字符串转python类型"""
    try:
        return json.loads(strs)
    except Exception:
        return {}
def json_encode(strs):
    """python列表或字典转成字符串"""
    try:
        return json.dumps(strs,ensure_ascii=False)
    except Exception:
        return ""
def dateoperator(date,years=0,formats='%Y%m%d%H%M%S',months=0, days=0, hours=0, minutes=0,seconds=0,
                 leapdays=0, weeks=0, microseconds=0,
                 year=None, month=None, day=None, weekday=None,
                 yearday=None, nlyearday=None,
                 hour=None, minute=None, second=None, microsecond=None):
    """日期相加减计算
    date 2019-10-10
    formats 设置需要返回的时间格式 默认%Y%m%d%H%M%S
    
    years 大于0表示加年  反之减年
    months 大于0表示加月  反之减月
    days 大于0表示加日  反之减日

    return %Y%m%d%H%M%S
    """
    formatss='%Y%m%d%H%M%S'
    date=re.sub('[-年/月:：日 时分秒]','',date)
    if len(date) < 8:
        return None
    if len(date) < 14:
        s=14-len(date)
        i=0
        while i < s:
            date=date+"0"
            i=i+1
    d = core_datetime.datetime.strptime(date, formatss)
    strs=(d + core_relativedelta(years=years,months=months, days=days, hours=hours, minutes=minutes,seconds=seconds,
                 leapdays=leapdays, weeks=weeks, microseconds=microseconds,
                 year=year, month=month, day=day, weekday=weekday,
                 yearday=yearday, nlyearday=nlyearday,
                 hour=hour, minute=minute, second=second, microsecond=microsecond))
    strs=strs.strftime(formats)
    return strs
def get_folder():
    '获取当前框架目录'
    return os.path.split(os.path.realpath(__file__))[0][:-7] #当前框架目录
# aa=[]
def get_file(folder='./',is_folder=True,suffix="*",lists=[],append=False):
    """获取文件夹下所有文件夹和文件

    folder 要获取的文件夹路径

    is_folder  是否返回列表中包含文件夹

    suffix 获取指定后缀名的文件 默认全部
    """
    if not append:
        lists=[]
    lis=os.listdir(folder)
    for files in lis:
        if not os.path.isfile(folder+"/"+files):
            if is_folder:
                zd={"type":"folder","path":folder+"/"+files,'name':files}
                lists.append(zd)
            get_file(folder+"/"+files,is_folder,suffix,lists,append=True)
        else:
            if suffix=='*':
                zd={"type":"file","path":folder+"/"+files,'name':files}
                lists.append(zd)
            else:
                if files[-(len(suffix)+1):]=='.'+str(suffix):
                    zd={"type":"file","path":folder+"/"+files,'name':files}
                    lists.append(zd)
    return lists

def list_to_tree(data, pk = 'id', pid = 'pid', child = 'lowerlist', root=0,childstatus=True):
    """列表转换tree
    
    data 要转换的列表

    pk 关联节点字段

    pid 父节点字段

    lowerlist 子节点列表

    root 主节点值

    childstatus 当子节点列表为空时是否需要显示子节点字段
    """
    arr = []
    for v in data:
        if v[pid] == root:
            kkkk=list_to_tree(data,pk,pid,child,v[pk],childstatus)
            if childstatus:
                v[child]=kkkk
            else:
                if kkkk:
                    v[child]=kkkk
            arr.append(v)
    return arr

        
class zip:
    def packzip(dirname,zipfilename):
        filelist = []
        if os.path.isfile(dirname):
            filelist.append(dirname)
        for root, dirs, files in os.walk(dirname):
            for name in files:
                filelist.append(os.path.join(root, name))
        zf = zipfile.ZipFile(zipfilename, "w", zipfile.zlib.DEFLATED)
        for tar in filelist:
            arcname = tar[len(dirname):]
            zf.write(tar,arcname)
        zf.close()
    def unzip_file(zipfilename, unziptodir):
        zf = zipfile.ZipFile(zipfilename)
        zf.extractall(unziptodir)
        zf.close()



class response:
    def tpl(path=None,**context):
        "返回模板内容"
        getroutecomponent=globals.VAR.component
        if path:
            if path[:1]=="/":
                Temppath=path
            else:
                Temppath="/"+getroutecomponent[1]+"/controller/"+getroutecomponent[2]+"/tpl/"+path+".html"
        else:
            Temppath="/"+getroutecomponent[1]+"/controller/"+getroutecomponent[2]+"/tpl/"+getroutecomponent[3]+"/"+getroutecomponent[4]+".html"
        return Template(Temppath,config=config,**context)
    def json(res=[],status='200 ok'):
        "响应json内容"
        return json_encode(res),status,{"Content-Type":"application/json; charset=utf-8","Access-Control-Allow-Origin":"*"}
    def redirect(url,status="302 Found",html='',header={"Content-Type":"application/html; charset=utf-8"}):
        """重定向

        参数 url 重定向地址 必须

        参数 status 响应码  可选

        参数 html body响应内容 可选

        参数 header 响应头  可选
        """
        header['Location']=url
        return html,status,header

class create:
    appname=None
    modular=None
    path=get_folder() #当前框架目录
    def __init__(self,appname="app",modular="api"):
        self.appname=str(appname)
        self.modular=str(modular)
    def uninstallplug(self,plug):
        """卸载插件

        plug 插件名
        """
        f=open(self.appname+"/"+self.modular+"/controller/__init__.py","r",encoding='utf-8')
        text=f.read()
        f.close()
        text=re.sub("\nfrom . import "+plug,"",text)
        text=re.sub("from . import "+plug,"",text)
        f=open(self.appname+"/"+self.modular+"/controller/__init__.py","w",encoding='utf-8')
        f.write(text)
        f.close()
        shutil.rmtree(self.appname+"/"+self.modular+"/controller/"+plug)
        return True,"成功"
    def packplug(self,plug):
        """打包插件
        
        plug 插件名
        """
        """打包模块"""
        if os.path.exists(self.appname+"/"+self.modular+"/controller/"+plug):
            zip.packzip(self.appname+"/"+self.modular+"/controller/"+plug,self.appname+"/"+self.modular+"/controller/"+plug+".zip")
            return True,"成功"
        else:
            return False,"失败"
    def uploadplug(self,plug,username='',password='',cli=False):
        "上传一个插件"
        i=0
        http=Http()
        while True:
            timestamp=times()
            sign=md5(str(username)+str(timestamp)+md5(md5(password)))
            http=Http()
            http.set_header['username']=username
            http.set_header['timestamp']=str(timestamp)
            http.set_header['sign']=sign
            http.set_timeout=300
            http.openurl(config.domain['kcwebapi']+"/user/uploadplug/",'POST',
            data={'name':str(plug),'describes':'','modular':self.modular},
            files={'file':open(self.appname+"/"+self.modular+"/controller/"+plug+".zip", 'rb')})
            arr=json_decode(http.get_text)
            if not arr:
                os.remove(self.appname+"/"+self.modular+"/controller/"+plug+".zip")
                return False,"上传失败，服务器暂时无法处理上传"
            if (arr['code']==-1 or arr['code']==2) and cli:
                if i >= 3:
                    os.remove(self.appname+"/"+self.modular+"/controller/"+plug+".zip")
                    return False,"用户名或密码错误"
                elif i:
                    print("用户名或密码错误，请重新输入")
                    username = input("请输入用户名（手机号）\n")
                    password = input("请输入密码\n")
                else:
                    username = input("请输入用户名（手机号）\n")
                    password = input("请输入密码\n")
                i+=1
            elif arr['code']==-1:
                os.remove(self.appname+"/"+self.modular+"/controller/"+plug+".zip")
                return False,"用户名或密码错误"
            elif arr['code']==0:
                os.remove(self.appname+"/"+self.modular+"/controller/"+plug+".zip")
                return True,arr['msg']
            else:
                os.remove(self.appname+"/"+self.modular+"/controller/"+plug+".zip")
                return False,arr['msg']
    def installplug(self,plug,edition='',token='',cli=False):
        """创建一个插件，如果您的模块目录下没有插件包，则创建默认插件文件
        
        plug 插件名
        """
        plug=str(plug)
        if os.path.exists(self.appname+"/"+self.modular+"/controller/"+plug):
            return False,"该插件已存在"
        else:
            http=Http()
            i=0
            while True:
                http.openurl(config.domain['kcwebapi']+"/pub/plug","POST",data={"modular":self.modular,"name":str(plug),"edition":str(edition),"token":token})
                arr=json_decode(http.get_text)
                if arr:
                    if arr['code']==-1 and cli:
                        if i >= 3:
                            return False,plug+"插件授权码错误"
                        elif i:
                            token = input("授权码错误，请重新输入授权码，从而获得该插件\n")
                        else:
                            token = input("请输入授权码，从而获得该插件\n")
                        i+=1
                    elif arr['code']==-1:
                        return False,plug+"插件授权码错误"
                    elif arr['code']==0:
                        arr=arr['data']
                        r=requests.get(arr['dowurl'])
                        f = open(self.appname+"/"+self.modular+"/controller/"+plug+".zip", "wb")
                        for chunk in r.iter_content(chunk_size=512):
                            if chunk:
                                f.write(chunk)
                        f.close()
                        if os.path.isfile(self.appname+"/"+self.modular+"/controller/"+plug+".zip"):#安装打包好的插件
                            zip.unzip_file(self.appname+"/"+self.modular+"/controller/"+plug+".zip",self.appname+"/"+self.modular+"/controller/"+plug+"/")
                            os.remove(self.appname+"/"+self.modular+"/controller/"+plug+".zip")

                            if os.path.isfile(self.appname+"/"+self.modular+"/controller/"+plug+"/install.txt"): #安装依赖包
                                install_requires=[]
                                try:
                                    f=open(self.appname+"/"+self.modular+"/controller/"+plug+"/install.txt")
                                    while True:
                                        line = f.readline()
                                        if not line:
                                            break
                                        elif len(line) > 2:
                                            install_requires.append(line)
                                    f.close()
                                except:
                                    shutil.rmtree(self.appname+"."+self.modular+"/controller/"+plug)
                                    return False,"error"
                                if len(install_requires):
                                    try:
                                        install_requires.insert(0,"install")
                                        if 0 != pip.main(install_requires):
                                            shutil.rmtree(self.appname+"."+self.modular+"/controller/"+plug)
                                            return False,"error"
                                    except AttributeError as e:
                                        shutil.rmtree(self.appname+"."+self.modular+"/controller/"+plug)
                                        print("建议更新您的pip版本。参考命令：Python -m pip install --user --upgrade pip -i https://mirrors.aliyun.com/pypi/simple/")
                                        return False,str(e)
                                        
                            # try:
                            #     m=importlib.import_module(self.appname+"."+self.modular+"/controller/"+plug+".install")
                            # except:
                            #     shutil.rmtree(self.appname+"."+self.modular+"/controller/"+plug)
                            #     print(traceback.format_exc())
                            #     return False,"插件依赖包文件不存在或依赖包文件格式错误"
                            # else:
                            #     try:
                            #         a=m.install()
                            #     except:
                            #         shutil.rmtree(self.appname+"."+self.modular+"/controller/"+plug)
                            #         return False,"插件依赖包install函数被破坏"
                            #     if not a[0]:
                            #         shutil.rmtree(self.appname+"."+self.modular+"/controller/"+plug)
                            #         return False,str(a[1])
                            f=open(self.appname+"/"+self.modular+"/controller/__init__.py","a",encoding='utf-8')
                            text="\nfrom . import "+plug
                            f.write(text)
                            f.close()
                            return True,"插件安装成功，"+plug+"=="+str(arr['edition'])
                        else:
                            return False,str(plug)+"插件下载失败"
                    else:
                        return False,str(plug)+"插件下载失败"
                else:
                    return False,self.modular+"模块下找不到"+str(plug)+"插件"
    def uninstallmodular(self):
        "卸载模块"
        f=open(self.appname+"/__init__.py","r")
        text=f.read()
        f.close()
        text=re.sub("\nfrom . import "+self.modular,"",text)
        text=re.sub("from . import "+self.modular,"",text)
        f=open(self.appname+"/__init__.py","w")
        f.write(text)
        f.close()
        shutil.rmtree(self.appname+"/"+self.modular)
        return True,"成功"
    def packmodular(self):
        """打包模块"""
        if os.path.exists(self.appname+"/"+self.modular):
            zip.packzip(self.appname+"/"+self.modular,self.appname+"/"+self.modular+".zip")
            return True,"成功"
        else:
            return False,"失败"
    def uploadmodular(self,username='',password='',cli=False):
        "上传模块"
        i=0
        http=Http()
        while True:
            timestamp=times()
            sign=md5(str(username)+str(timestamp)+md5(md5(password)))
            http.set_header['username']=username
            http.set_header['timestamp']=str(timestamp)
            http.set_header['sign']=sign
            http.set_timeout=300
            http.openurl(config.domain['kcwebapi']+"/user/uploadmodular/",'POST',
            data={'name':str(self.modular),'describes':''},
            files={'file':open(self.appname+"/"+self.modular+".zip", 'rb')})
            arr=json_decode(http.get_text)
            if not arr:
                os.remove(self.appname+"/"+self.modular+".zip")
                return False,"上传失败，服务器暂时无法处理上传"
            if (arr['code']==-1 or arr['code']==2) and cli:
                if i >= 3:
                    os.remove(self.appname+"/"+self.modular+".zip")
                    return False,"用户名或密码错误"
                elif i:
                    print("用户名或密码错误，请重新输入")
                    username = input("请输入用户名（手机号）\n")
                    password = input("请输入密码\n")
                else:
                    username = input("请输入用户名（手机号）\n")
                    password = input("请输入密码\n")
                i+=1
            elif arr['code']==-1:
                os.remove(self.appname+"/"+self.modular+".zip")
                return False,"用户名或密码错误"
            elif arr['code']==0:
                os.remove(self.appname+"/"+self.modular+".zip")
                return True,arr['msg']
            else:
                os.remove(self.appname+"/"+self.modular+".zip")
                return False,arr['msg']
    def installmodular(self,token='',cli=False):
        "创建模块，如果应用不存，则创建默认应用，如果在您的应用目录下没有模块包，则创建默认模块文件"
        if not os.path.exists(self.appname):
            # os.makedirs(self.appname)
            r=requests.get(config.domain['kcwebfile']+"/kcweb/app.zip")
            f = open("./app.zip", "wb")
            for chunk in r.iter_content(chunk_size=512):
                if chunk:
                    f.write(chunk)
            f.close()
            zip.unzip_file("./app.zip","./")
            os.remove("./app.zip")
            if not os.path.isfile("./server.py"):
                if "Windows" in platform.platform():
                    pythonname="python"
                else:
                    pythonname="python3"
                servertext=('# -*- coding: utf-8 -*-\n #gunicorn -b 0.0.0.0:39010 '+self.appname+':app\n'+
                        'from kcweb import web\n'+
                        'import '+self.appname+' as application\n'+
                        'app=web(__name__,application)\n'+
                        'if __name__ == "__main__":\n'+
                        '    #host监听ip port端口 name python解释器名字 (windows一般是python  linux一般是python3)\n'+
                        '    app.run(host="0.0.0.0",port="39001",name="'+pythonname+'")')
                f=open("./server.py","w+",encoding='utf-8')
                f.write(servertext)
                f.close()
            return True,"应用创建成功"
        else:
            if not os.path.isfile(self.appname+"/__init__.py") or not os.path.exists(self.appname+"/common"):
                return False,self.appname+"不是kcweb应用"
        if os.path.exists(self.appname+"/"+self.modular):
            return False,self.appname+"/"+self.modular+"已存在"
        else:
            http=Http()
            i=0
            while True:
                http.openurl(config.domain['kcwebapi']+"/pub/modular","POST",data={"name":self.modular,"token":token})
                arr=json_decode(http.get_text)
                if arr:
                    if arr['code']==-1 and cli:
                        if i >= 3:
                            return False,self.modular+"模块授权码错误"
                        elif i:
                            token = input("授权码错误，请重新输入授权码，从而获得该模块\n")
                        else:
                            token = input("请输入授权码，从而获得该模块\n")
                        i+=1
                    elif arr['code']==-1:
                        return False,self.modular+"模块授权码错误"
                    elif arr['code']==0:
                        arr=arr['data']
                        r=requests.get(arr['dowurl'])
                        f = open(self.appname+"/"+self.modular+".zip", "wb")
                        for chunk in r.iter_content(chunk_size=1024*100):
                            if chunk:
                                f.write(chunk)
                        f.close()
                        if os.path.isfile(self.appname+"/"+self.modular+".zip"):#安装打包好的模块
                            zip.unzip_file(self.appname+"/"+self.modular+".zip",self.appname+"/"+self.modular+"/")
                            os.remove(self.appname+"/"+self.modular+".zip")

                            if os.path.isfile(self.appname+"/"+self.modular+"/install.txt"): #安装依赖包
                                install_requires=[]
                                try:
                                    f=open(self.appname+"/"+self.modular+"/install.txt")
                                    while True:
                                        line = f.readline()
                                        if not line:
                                            break
                                        elif len(line) > 3:
                                            install_requires.append(line)
                                    f.close()
                                except:
                                    shutil.rmtree(self.appname+"/"+self.modular)
                                    return False,"error"
                                if len(install_requires):
                                    try:
                                        install_requires.insert(0,"install")
                                        if 0 != pip.main(install_requires):
                                            shutil.rmtree(self.appname+"/"+self.modular)
                                            return False,"error"
                                    except AttributeError as e:
                                        shutil.rmtree(self.appname+"/"+self.modular)
                                        print("建议更新您的pip版本。参考命令：Python -m pip install --user --upgrade pip -i https://mirrors.aliyun.com/pypi/simple/")
                                        return False,str(e)
                            # try:
                            #     m=importlib.import_module(self.appname+'.'+self.modular+'.install')
                            # except:
                            #     shutil.rmtree(self.appname+"/"+self.modular)
                            #     print(traceback.format_exc())
                            #     return False,"模块依赖包文件不存在或依赖包文件格式错误"
                            # else:
                            #     try:
                            #         a=m.install()
                            #     except:
                            #         shutil.rmtree(self.appname+"/"+self.modular)
                            #         return False,"模块依赖包install方法被破坏"
                            #     if not a[0]:
                            #         shutil.rmtree(self.appname+"/"+self.modular)
                            #         return False,str(a[1])
                            content="\nfrom . import "+self.modular
                            f=open(self.appname+"/__init__.py","a",encoding='utf-8')
                            f.write(content)
                            f.close()
                        else:
                            return False,self.modular+"模块下载失败"
                        if not os.path.isfile("./server.py"):
                            if "Windows" in platform.platform():
                                pythonname="python"
                            else:
                                pythonname="python3"
                            # sys.argv[0]=re.sub('.py','',sys.argv[0])
                            servertext=('# -*- coding: utf-8 -*-\n#gunicorn -b 0.0.0.0:39010 '+self.appname+':app\n'+
                                    'from kcweb import web\n'+
                                    'import '+self.appname+' as application\n'+
                                    'app=web(__name__,application)\n'+
                                    'if __name__ == "__main__":\n'+
                                    '    #host监听ip port端口 name python解释器名字 (windows一般是python  linux一般是python3)\n'+
                                    '    app.run(host="0.0.0.0",port="39001",name="'+pythonname+'")')
                            f=open("./server.py","w+",encoding='utf-8')
                            f.write(servertext)
                            f.close()
                        return True,"安装成功"
                    else:
                        return False,"模块下载失败"
                else:
                    return False,"找不到"+self.modular+"模块"
    # def __zxmodular(self,sourcep): 
    #     "处理模块文件"
    #     path1=self.path+"/application/api"+sourcep
    #     path2=self.appname+"/"+self.modular+sourcep
    #     lists=os.listdir(path1)
    #     for files in lists:
    #         if os.path.isfile(path1+"/"+files):
    #             if ".py" in files:
    #                 content=Templates(path1+"/"+files,appname=self.appname,modular=self.modular)
    #                 f=open(path2+"/"+files,"w+",encoding='utf-8')
    #                 f.write(content)
    #                 f.close()
    #             else:
    #                 f=open(path1+"/"+files,"r",encoding='utf-8')
    #                 content=f.read()
    #                 f.close()
    #                 f=open(path2+"/"+files,"w+",encoding='utf-8')
    #                 f.write(content)
    #                 f.close()
    #         elif files != '__pycache__':
    #             if not os.path.exists(path2+"/"+files):
    #                 os.makedirs(path2+"/"+files)
    #             self.__zxmodular(sourcep+"/"+files)