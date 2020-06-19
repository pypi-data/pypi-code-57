from python_freeipa import ClientMeta
from python_freeipa.exceptions import Unauthorized
from ipaconnector.kerberos import Kerberos
from ipaconnector.klass import User, Group
import json
from typing import List
import logging


class IpaConnector:
	def __init__(self, host):
		self._log = logging.getLogger('ipa-connector')
		self._log.info(f"IPA SERVER: {host}")
		self.client = ClientMeta(host=host, verify_ssl=False, dns_discovery=False)
	
	def connect(self, user=None, password=None, kerberos=False):
		if kerberos:
			self._log.info("Authenticating via kerberos")
			self._connect_kerberos()
			return
		if not user and not password:
			raise RuntimeError("Credentials not provided")
		self._log.info("Authenticating via credentials")
		self.client.login(user, password)


	def _connect_kerberos(self):
		"""
		Make connection to IPA server
		"""
		self._log.info("Connecting to IPA")
		try:
			self.client.login_kerberos()
		except Unauthorized:
			self._log.debug("Unauthorized, acquiring TGT...")
			Kerberos().acquire_tgt()
			self._log.debug("Retrying login")
			self.client.login_kerberos()

	def _open_as_json(self, path: str) -> dict:
		"""
		path: full or relative path to input file
		Usually given via command line - see scripts/
		"""
		with open(path, 'r') as _file:
			content = json.load(_file)
		return content

	def run(self, path: str):
		"""
		Runs everything.
		"""
		to_add, to_update, to_delete = self.read_input(path)

		self.make_add(to_add)
		self.make_update(to_update)
		self.make_delete(to_delete)
	def read_input(self, path: dict) -> list:
		"""
		path: path to input json file
		return: list of actions required
		"""
		self._log.info(f"Reading file {path}")
		input_data = self._open_as_json(path)
		to_add = input_data['CREATIONS']
		to_delete = input_data['DELETIONS']
		to_update = input_data['UPDATES']
		return to_add, to_update, to_delete

	def make_add(self, to_add):
		self._log.info("Adding HumanUsers")
		if to_add.get('HumanUser'):
			[User(user_data).add(self.client) for user_data in to_add['HumanUser']]
		self._log.info("Adding UserGroup")
		if to_add.get('UserGroup'):
			[Group(group_data).add(self.client) for group_data in to_add['UserGroup']]

	def make_delete(self, to_delete):
		self._log.info("Deleting Users")
		if  to_delete.get('HumanUser'):
			[User(user_data).delete(self.client) for user_data in to_delete['HumanUser']]
		self._log.info("Deleting UserGroups")
		if  to_delete.get('UserGroup'):
			[Group(group_data).delete(self.client) for group_data in to_delete['UserGroup']]

	def make_update(self, to_update):
		self._log.info("Updating UserGroups")
		if to_update.get('UserGroup'):
			[Group(group_data).update_members(self.client) for group_data in to_update['UserGroup']]




