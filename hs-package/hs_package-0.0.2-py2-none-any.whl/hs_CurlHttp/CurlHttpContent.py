# -*- coding:utf-8 -*-
import pycurl,StringIO,urllib,sys


class CurlHttpContent:
    def __init__(self):
        self.c = pycurl.Curl()
        
    def __del__(self):
        self.c.close()

    def getContent(self,url,method="GET",data=None,header=[],cookie = ""):
        print "url:",url
        print "data:",data
        '''
        发起网络请求\n
        url:请求路由\n
        method:请求方法，GET/POST/PATCH/PUT/DELETE\n
        data:请求体参数\n
        header:请求头部信息\n
        cookie:请求携带cookie\n
        '''
        
        if len(header) != 0:
            self.c.setopt(pycurl.HTTPHEADER,header)
            
        if len(cookie) != 0:
            self.c.setopt(pycurl.COOKIE, cookie)
        
        self.c.setopt(pycurl.URL,str(url))
        self.c.setopt(pycurl.FOLLOWLOCATION, 0)

        if method in ("POST","PATCH","PUT","DELETE") :
            if not data:
                data="{}"
            try:
                self.c.setopt(pycurl.POSTFIELDS, data)
                
            except Exception,e:
                print "Data Error:",str(e)


        respContents = StringIO.StringIO()
        respHeaders = StringIO.StringIO()
        

        self.c.setopt(pycurl.CONNECTTIMEOUT, 5)    #连接的等待时间，设置为0则不等待 
        self.c.setopt(pycurl.TIMEOUT, 600)           #请求超时时间  
        self.c.setopt(pycurl.DNS_CACHE_TIMEOUT,60) #设置保存DNS信息的时间，默认为120秒  
        self.c.setopt(pycurl.SSL_VERIFYPEER, 0)   
        self.c.setopt(pycurl.SSL_VERIFYHOST, 0)

        
        self.c.setopt(pycurl.WRITEFUNCTION, respContents.write)
        self.c.setopt(pycurl.HEADERFUNCTION, respHeaders.write)
        self.c.setopt(pycurl.CUSTOMREQUEST, method)

        # pycurl.NAMELOOKUP_TIME 域名解析时间
        # pycurl.CONNECT_TIME 远程服务器连接时间
        # pycurl.PRETRANSFER_TIME 连接上后到开始传输时的时间
        # pycurl.STARTTRANSFER_TIME 接收到第一个字节的时间
        # pycurl.TOTAL_TIME 上一请求总的时间
        # pycurl.REDIRECT_TIME 如果存在转向的话，花费的时间
        # pycurl.SIZE_DOWNLOAD 下载的数据大小
     
        try:
            self.c.perform()
        except Exception,e:
            print str(e)
            
        namelookupTime = self.c.getinfo(pycurl.NAMELOOKUP_TIME)
        httpConnTime =  self.c.getinfo(pycurl.CONNECT_TIME)
        httpPreTran =  self.c.getinfo(pycurl.PRETRANSFER_TIME)
        httpStartTran =  self.c.getinfo(pycurl.STARTTRANSFER_TIME)
        httpTotalTime = self.c.getinfo(pycurl.TOTAL_TIME)
        httpSize = self.c.getinfo(pycurl.SIZE_DOWNLOAD)
        httpCode = self.c.getinfo(pycurl.HTTP_CODE)      
        totalTime =  int(self.c.getinfo(pycurl.TOTAL_TIME) * 1000)

        respContent = respContents.getvalue()
        respHeader = respHeaders.getvalue()

        

        respContents.close()
        respHeaders.close()
        # logInfo.logger.info("url: %s - method: %s - http_code: %s - total_time: %s - resp_content: %s - resp_header: %s" % (url,i_type,str(http_code),str(total_time),str(resp_content),str(resp_header)))
        
        return httpCode,totalTime,respContent,respHeader,namelookupTime,httpConnTime,httpPreTran,httpStartTran,httpTotalTime,httpSize
    