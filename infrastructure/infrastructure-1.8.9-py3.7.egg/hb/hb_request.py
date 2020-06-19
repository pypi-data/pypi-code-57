# -*- coding: utf-8 -*-
# @Author: yongfanmao
# @Date:   2020-06-10 14:43:59
# @E-mail: maoyongfan@163.com
# @Last Modified by:   yongfanmao
# @Last Modified time: 2020-06-16 16:06:39
from infrastructure.http_agent.http_request import HttpRequest

class HBRequest(object):
	def __init__(self,coverageLog=""):
		self.coverageLog = coverageLog

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

	def ticketGit(self,team,service_name,cookie,user_agent):
		"""
			申请git权限
		"""
		url = "https://ticket-inner.hellobike.cn/api/v1/work/workorder"
		data = {
			"template":100002740,
			"application_args":{
				"username":"maoyongfan10020",
				"projects":{
					"team":{
						"value":team,
						"label":team
					},
					"name":service_name,
					"access":{
						"value":30,
						"label":"开发"
					}
				}
			}
		}

		headers = {'content-type': "application/json;charset=UTF-8",
			'cookie': cookie,
			'User-Agent': user_agent}

		response = HttpRequest.post(url,headers=headers,data=data)
		if response['code'] == 201:

			if self.coverageLog:
				self.logs(operationType="成功申请权限",
					message=str(response),
					typeInfo="申请git权限",
					remark="")

		else:
			if self.coverageLog:
				self.logs(operationType="申请权限失败",
					message=str(response),
					typeInfo="申请git权限",
					remark="")

			raise Exception("等待git审批")

			

	def openServerAuth(self,server,token,cookie,user_agent):
		"""
		先获取服务器挂载app,再去请求开通权限
		"""
		addECSUserURL = "https://ticket-inner.hellobike.cn/api/v1/work/workorder"
		appsTemp = ""
		if server.apps:
			appsTemp = server.apps
		else:
			searchDetail = self.searchEcsDetail(server,token,cookie,user_agent)
			if not searchDetail:
				# 获取服务器详细信息失败，无法开通服务访问权限
				raise Exception("获取服务器详细信息失败，无法开通服务访问权限")
			else:			 
				for app in searchDetail['apps']:
					appsTemp += app["app__name"]+","
				if appsTemp[-1] == ",":
					appsTemp = appsTemp[:-1]
				server.apps = appsTemp
				server.save()

		data = {
			"template":100003005,
			"application_args":
				{"ip":"{}".format(server.ip.intranet),
				"team_name":"{}".format(server.team),
				"name":"{}".format(server.name),
				"env":"{}".format(server.env),
				"apps":"{}".format(appsTemp)}
		}

		headers = {'token': token,
			'cookie': cookie,
			'User-Agent': user_agent}	

		response = HttpRequest.post(addECSUserURL,headers=headers,data=data)
		if response['code'] == 201:
			if self.coverageLog:
				self.logs(operationType="申请服务器权限成功",
					message=str(response),
					typeInfo="申请服务器权限成功",
					remark="")
			return True
		else:
			logs = LogMonitorUserOperateLogsSerializer(data=
				{
					"operationType":"job",
					"message": "开通该{}服务器 {} 访问权限,失败,无法分析该服务器日志!"
					.format(server.name,server.env),
					"typeInfo": "获取服务器挂载app信息失败,请分析",
					"status":10
			})
			if self.coverageLog:
				self.logs(operationType="申请服务器权限时失败",
					message=str(response),
					typeInfo="申请服务器权限失败",
					remark="")
			raise Exception("无法开通服务器访问权限")		

	def searchEcsDetail(self,server,token,cookie,user_agent):
		searchEcsDetailURL = "http://10.111.90.230:20001/api/v1/ecs/{}/".format(server.server_id)
		# print (self.searchEcsDetailURL)
		response = HttpRequest.get(searchEcsDetailURL,headers={'token': token,
			'cookie': cookie,
			'User-Agent': user_agent})
		if response['code'] == 200:
			detailData = response['result']['data']
			return detailData
		else:
			if self.coverageLog:
				self.logs(operationType="获取服务器挂载app信息失败,请分析",
					message=str(response),
					typeInfo="申请服务器权限失败",
					remark="获取该{}服务器 {} 挂载app信息,失败"
					.format(server.name,server.env))

			return False






