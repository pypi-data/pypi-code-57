"""

Haystack client.
Includes session and session management and basic get/put operations.


"""

import json
#import logging
from cxhs.val import HStr
from cxhs.session import HSession
from cxhs.core import Storage
from cxhs.io import ZincReader, ZincWriter
from cxhs.grid import HGridBuilder
class HClient(object):
	""" Haystack client.

	This client uses json payload.

	Examples:
		>>> from hs.client import HClient
		>>> client = HClient("http://localhost:1225/haystack")
		>>> client.about()
		>>> client.readAll("point")
		>>> client.hisRead("@D-AHU1-DTemp", "yesterday")

		>>> import hs.client
		>>> client = hs.client.HClient("http://localhost:1225/haystack")
		>>> client.about()
		>>> client.readById("@11-CurrentTemperature")


	"""
	def __init__(self, url, username = None, password = None, basic = True):
		self.session = HSession(url, username, password, basic)
		self.url = url

	@property
	def contentType(self):
		return self.session.contentType

	@contentType.setter
	def contentType(self, value):
		self.session.contentType = value

	def _parseResponse(self, res):
		if self.contentType == "json":
			ret = Storage(json.loads(res))
		else:
			ret = ZincReader(res).readGrid()
		return ret

	def about(self):
		"""Perform about operation.
		"""
		print("ABOUT:","%s/about" % self.url)
		res = self.session.get("%s/about" % self.url)
		#print(res #res.status_code, res.content)
		return self._parseResponse(res)

	def readById(self, nid):
		"""Read node by id.

		Args:
			nid: node id
		"""
		res = self.session.get("%s/read?id=%s" % (self.url, nid))
		return self._parseResponse(res)

	def readAll(self, filt):
		"""Read all points as given filter spec.
		Args:
			filt: filter
		"""
		res = self.session.get("%s/read?filter=%s" % (self.url, filt))
		return self._parseResponse(res)

	def read(self, filt):
		res = self.session.get("%s/read?filter=%s&limit=1" % (self.url, filt))
		return Storage(json.loads(res))

	def pointWrite(self, nid, val, level=1):
		'''
		Write the value to the point at the given priority level.

		Args:
			nid   - node id (stored as 'haystackHis')
			val   - value to write
			level - priority level to write
		'''
		if not nid.startswith("@"):
			nid = '@' + nid
		u = '%s/pointWrite?id=%s&val=%s&level=%s&who=%s' % (self.url, nid, val, level, self.session.session.auth[0])
		res = self.session.get(u)
		return self._parseResponse(res)

	def hisRead(self, nid, hrange):
		"""Read history for a given point.

		Args:
			nid: node id
			hrange: history range in haystack format
		"""
		hrange = hrange.replace(' ', '%20')
		res = self.session.get('%s/hisRead?id=%s&range="%s"' % (self.url, nid, hrange))
		return self._parseResponse(res)

	def eval(self, expr):
		"""Eval .

		Args:
			expr: eval expression
		"""
		b = HGridBuilder()
		b.addCol("expr")
		b.addRow([HStr.make(expr)])
		grid = b.toGrid()
		data = ZincWriter.gridToString(grid)
		print("request to %s" % '%s/eval' % self.url)
		res = self.session.post('%s/eval' % self.url, data)
		print(res)
		return self._parseResponse(res)

	def nav(self, navId=None):
		"""Perform nav command.
		Args:
			navId: navigation id (optional)
		"""
		if navId:
			url = "%s/nav?navId=%s" % (self.url, navId)
		else:
			url = "%s/nav" % self.url
		res = self.session.get(url)
		return self._parseResponse(res)


