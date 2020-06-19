# -*- coding: utf-8 -*-
# @Author: yongfanmao
# @Date:   2020-05-29 11:41:39
# @E-mail: maoyongfan@163.com
# @Last Modified by:   yongfanmao
# @Last Modified time: 2020-06-11 21:25:05

import os
import time
from infrastructure.variables.hb_conf import JAVA_COV
from infrastructure.parse.htmlParse import HtmlParse
class LocalServer(object):
	def __init__(self,alreadyRecord,JavaCoverageReportUrl="",coverageLog="",
		javaCoverageNolib=""):
		"""
			操作本地服务器
		"""
		self.alreadyRecord = alreadyRecord
		self.JavaCoverageReportUrl = JavaCoverageReportUrl
		self.coverageLog = coverageLog
		self.jarDir = JAVA_COV["jarDir"].format(service_name=self.alreadyRecord.service_name)
		self.copySourceDir = JAVA_COV["copySourceDir"].format(service_name=self.alreadyRecord.service_name)
		self.reportDir = JAVA_COV["reportDir"].format(service_name=self.alreadyRecord.service_name,
			recordID=self.alreadyRecord.id)
		self.serviceRepoDir = JAVA_COV["serviceRepoDir"].format(service_name=self.alreadyRecord.service_name)
		self.jacocoDir = JAVA_COV["jacocoDir"]
		self.destfile = JAVA_COV["destfile"]
		self.javaCoverageNolib = javaCoverageNolib

	def logs(self,operationType="",message="",typeInfo="",remark=""):
		record = self.coverageLog(data=
					{
						"operationType": operationType,
						"message": message,
						"typeInfo": typeInfo,
						"remark": remark,
						"status":1
					})					
		record.is_valid(raise_exception=True)
		record.save()

	def filter_local_jar(self,jar_list,command):
		"""
		过滤本服务器上的jar包名,为特殊化处理打成一个jar包的服务
		"""

		download_jar = []
		jar_name_list = eval(self.alreadyRecord.jar_name)
		for jar_name in jar_name_list:
			filter_jar_command = command.format(
				service_name=self.alreadyRecord.service_name,jarNameDir=jar_list[0].split(".j")[0],jarName=jar_name)	

			with os.popen(filter_jar_command) as temp:
				result =temp.read()

			if self.coverageLog:
				self.logs(operationType="在服务本地过滤",
					message=filter_jar_command+"\n"+result,
					typeInfo="特殊化过滤jar包",
					remark="{recordId}次覆盖率统计{service_name}".format(recordId=self.alreadyRecord.id,
							service_name=self.alreadyRecord.service_name))

			for loop in result.split('\n'):
				if not loop:
					continue
				if 'iface' in loop.lower():
					continue

				download_jar.append(loop.strip())


		if download_jar:
			self.alreadyRecord.download_jar = str(download_jar)
			self.alreadyRecord.save()
			return True
		else:
			self.alreadyRecord.status = 6
			self.alreadyRecord.mark = "在本地特殊化处理匹配jar包失败"
			self.alreadyRecord.save()
			return False


	def checkZip(self,zipPath):
		if os.path.exists(zipPath):
			command = "rm -rf {zipPath}".format(zipPath = zipPath)
			os.popen(command).read()
			if self.coverageLog:
				self.logs(operationType="删除旧的zip包",
					message=command,
					typeInfo="覆盖率解压zip包过程",
					remark="{recordId}次覆盖率统计{service_name}".format(recordId=self.alreadyRecord.id,
							service_name=self.alreadyRecord.service_name))


	def upzipJar(self,jar_list="",jarDir="",special_deal=False):
		"""
			解压下载下来的jar包(jar包已重命名)
			args:
				jar_list  为了处理特殊的服务，该服务把所有jar包融成一个jar包 该参数为了第一次解压融合jar包
				jarDir special_deal 为特殊化处理第二次解压本地融合的jar包
			1.判断/home/maoyongfan10020/jc/{service_name}/all 是否存在 不存在创建
		"""
		classFile = self.jarDir+"/all"
		os.makedirs(classFile) if not os.path.exists(classFile) else True
		if not special_deal:
			deleteAllCommand = "rm -rf " + self.jarDir + "/all/*"
			os.popen(deleteAllCommand).read()

		if not jarDir:
			jarDir = self.jarDir

		if jar_list:
			download_jar = jar_list
		else:
			download_jar = eval(self.alreadyRecord.download_jar)



		
		for jar in download_jar:
			self.checkZip(self.jarDir+'/'+jar.split('.j')[0]+'.zip')
			command = "cd " + jarDir + ";mv {download_jar} {jarToZip}".format(
				download_jar=jar,
				jarToZip=jar.split('.j')[0]+'.zip')
			os.popen(command).read()

			if self.coverageLog:
				self.logs(operationType="把jar包转为zip包命令",
					message=command,
					typeInfo="覆盖率解压zip包过程",
					remark="{recordId}次覆盖率统计{service_name}".format(recordId=self.alreadyRecord.id,
							service_name=self.alreadyRecord.service_name))

			unzip_command = "cd " + jarDir + (";unzip -o {jarToZip} -d "+self.jarDir + "/all/{jarNameDir}").format(
				jarToZip=jar.split('.j')[0]+'.zip',
				jarNameDir=jar.split('.j')[0])

			if self.coverageLog:
				self.logs(
						operationType="解压zip包命令",
						message=unzip_command,		
						typeInfo="覆盖率解压zip包过程",
						remark="{recordId}次覆盖率统计{service_name}".format(recordId=self.alreadyRecord.id,
							service_name=self.alreadyRecord.service_name)
					)		
			os.popen(unzip_command).read()

		if self.alreadyRecord.service_name == "AppHelloAnunnakiDSPService" and not special_deal:

			command = "cd /home/maoyongfan10020/jc/{service_name}/all/{jarNameDir}/BOOT-INF/lib;ls | grep {jarName}"
			self.filter_local_jar(jar_list,command)
			self.upzipJar(jarDir="/home/maoyongfan10020/jc/{service_name}/all/{jarNameDir}/BOOT-INF/lib".format(
				service_name=self.alreadyRecord.service_name,
				jarNameDir=jar_list[0].split(".j")[0]),special_deal=True)

			# 删除掉融合目录(包含了不需要的class)
			os.popen("rm -rf /home/maoyongfan10020/jc/{service_name}/all/AppHelloAnunnakiDSPService".format(
										service_name=self.alreadyRecord.service_name
										)).read()

	def copyCode(self):
		os.popen("rm -rf " + self.copySourceDir).read() if os.path.exists(self.copySourceDir) else True
		for path in eval(self.alreadyRecord.jar_dir):
			os.popen("cp -r " + path + "/src/main/java/. " + self.copySourceDir).read() if os.path.exists(path + "/src/main/java") else True

	def jacocoReport(self):
		try:
			os.makedirs(self.reportDir) if not os.path.exists(self.reportDir) else True
		except:
			if self.coverageLog:
				self.logs(
						operationType="reportDir目录下recordID目录已存在",
						message=self.reportDir,		
						typeInfo="目录已存在",
						remark="{recordId}次覆盖率统计{service_name}".format(recordId=self.alreadyRecord.id,
							service_name=self.alreadyRecord.service_name)
					)


		f = open(self.reportDir+"/jacoco.xml","w")
		f.close()

		self.copyCode()

		# 判断ip是否是多个，需merge
		if (len(eval(self.alreadyRecord.server_ip)))==1:
			if self.alreadyRecord.service_name == "AppHelloMercuryService":
				classfile = self.jarDir + "/all/mercury-service/BOOT-INF/classes"
			elif self.javaCoverageNolib.objects.filter(service_name=self.alreadyRecord.service_name):
				classfile = self.jarDir + "/all/{name}/BOOT-INF/classes".format(name=eval(self.alreadyRecord.download_jar)[0].split('.j')[0])
			else:
				classfile = self.jarDir + "/all"
			sourcefiles = self.copySourceDir

			report_command = ("cd {jacocoDir};java -jar jacococli.jar report " +\
					self.destfile + " --classfiles {classfile} --sourcefiles {sourcefiles} --html {reportDir} --xml {xml}").format(
					jacocoDir = self.jacocoDir,
					service_name=self.alreadyRecord.service_name,
					index=1,
					classfile=classfile,
					sourcefiles = sourcefiles,
					reportDir=self.reportDir,
					xml=self.reportDir+"/jacoco.xml"
					)

			if self.coverageLog:
				self.logs(operationType="覆盖率执行参数",
					message=report_command,
					typeInfo="覆盖率报告",
					remark="{recordId}次覆盖率统计{service_name}".format(recordId=self.alreadyRecord.id,
							service_name=self.alreadyRecord.service_name))

			with os.popen(report_command) as temp:
					temp.read()

			return True
		else:
			return False



	def jacocoIncrementReport(self):
		command = "source /home/maoyongfan10020/virtualEnv/rfServerEnv/bin/activate;cd {serviceCodeDir};diff-cover {xml} --compare-branch=origin/master --src-roots {sourcefiles} --html-report {incrementReport}".format(
			serviceCodeDir = self.serviceRepoDir,	
			xml=self.reportDir+"/jacoco.xml",
			sourcefiles=self.serviceRepoDir + '/*/src/main/java',			
			incrementReport=self.reportDir+"/incrementReport.html"
			)

		with os.popen(command) as gen_irmReport:
			out = gen_irmReport.read()

		if self.coverageLog:
			self.logs(operationType="覆盖率执行参数",
				message=command + "\n" + out,
				typeInfo="覆盖率增量报告",
				remark="{recordId}次覆盖率统计{service_name}".format(recordId=self.alreadyRecord.id,
						service_name=self.alreadyRecord.service_name))

		if not out:
			return False
		if "No lines" in out:
			if self.coverageLog:
				self.logs(operationType="无新增覆盖率",
					message="",
					typeInfo="覆盖率增量报告",
					remark="{recordId}次覆盖率统计{service_name}".format(recordId=self.alreadyRecord.id,
							service_name=self.alreadyRecord.service_name))
			return "无新增覆盖率"
		for loop in out.split('\n'):
			if 'Total' in loop:
				totalList = [ i for i in loop.split(' ') if (len(i)!=0) ]
				total = totalList[1]

			if 'Missing' in loop:
				missList = [ i for i in loop.split(' ') if (len(i)!=0) ]
				miss = missList[1]

			if 'Coverage' in loop:
				coverageList = [ i for i in loop.split(' ') if (len(i)!=0) ]
				coverage = coverageList[1]

		self.alreadyRecord.incrementCoverage = coverage
		self.alreadyRecord.increment_coverage_lines = str(int(total)-int(miss))
		self.alreadyRecord.increment_lines = total
		self.alreadyRecord.save()

		return True

	def parseReport(self):
		index_path = self.reportDir+"/index.html"
		if os.path.exists(index_path):
			with open(index_path) as report:
				content = report.read()
			hp = HtmlParse(content)
			tdContent = hp.getNode('table').tfoot.tr.contents
			no_coverage_lines = self.__delayStringLine((tdContent[7].contents)[0])
			total_lines = self.__delayStringLine((tdContent[8].contents)[0])

			total_coverage_lines = total_lines - no_coverage_lines
			totalCoverage = '{:.2f}%'.format(total_coverage_lines/total_lines*100)
			print (total_coverage_lines,total_lines)
			# return str(total_lines),str(total_coverage_lines),totalCoverage

			self.alreadyRecord.total_lines = str(total_lines)
			self.alreadyRecord.total_coverage_lines = str(total_coverage_lines)
			self.alreadyRecord.totalCoverage = totalCoverage
			#http://10.111.10.223:8001/report/AppHellobikeRideApiService/129/index.html
			report_html_url = ['https://fat-rfautotest.hellobike.cn/report/{}/report/{}/index.html'.format(
					self.alreadyRecord.service_name,self.alreadyRecord.id),
				'https://fat-rfautotest.hellobike.cn/report/{}/report/{}/incrementReport.html'.format(
				self.alreadyRecord.service_name,self.alreadyRecord.id)]
			for url in report_html_url:
				self.JavaCoverageReportUrl.objects.create(coverageRecord=self.alreadyRecord,reportUrl=url)

			self.alreadyRecord.status = 1
			self.alreadyRecord.save()
			return self.alreadyRecord
		else:
			if self.coverageLog:
				self.logs(operationType="无总量报告生成",
					message="",
					typeInfo="解析覆盖率总量报告",
					remark="{recordId}次覆盖率统计{service_name}".format(recordId=self.alreadyRecord.id,
							service_name=self.alreadyRecord.service_name))
		return False

	def __delayStringLine(self,line):
		'''
			line '13,401'
		'''
		if ',' in line:
			temp = line.split(',')
			return int(temp[0]+temp[1])
		else:
			return int(line)	

