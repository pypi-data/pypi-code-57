
from python_freeipa.exceptions import DuplicateEntry, NotFound
import logging

def safe_run(func):
	_log = logging.getLogger('ipa-connector')
	def func_wrapper(*args, **kwargs):
		try:
			return func(*args, **kwargs)
		except (NotFound, DuplicateEntry) as e:
			_log.error(e)
			_log.warning("Minor error occured, continue...")
			return None
	return func_wrapper

class LoggingClass(object):
	_log = logging.getLogger('ipa-connector')

class TranslatedObject:
	def _translate(self, input_data: dict):
		"""
		Get rid of nasty newValue keys from input json file.
		Also workaround to set None values on non-provided, mandatory fields
		"""
		trans = dict()
		for key in input_data.keys():
			try:
				trans[key] = input_data[key]['newValue']
			except KeyError:
				trans[key] = None
		return trans
class User(TranslatedObject, LoggingClass):
	def __init__(self, input_data: dict):
		user_info = self._translate(input_data)
		self.login = user_info['login']
		self.first_name= user_info.get('firstname')
		self.name = user_info.get('name')
		self.full_name = " ".join([str(i) for i in [self.first_name ,self.name] if i != None])
		self.email = user_info.get('email')
		self.homedir = f"/data0/{self.login}/"
		self.gecos = f"FR/C//BYTEL/{self.full_name}"
		self.org = user_info.get('company')

	def __repr__(self):
		return f"{self.login}|{self.full_name}|{self.email}"

	@safe_run
	def add(self, client):
		"""
		Performs actual operation towards IPA server.
		client: ipa client instance
		"""
		self._log.info(f"Adding user {self.login}")
		self._log.debug(f"User info: {self.login} \n "\
				"Full name {self.full_name} \n"\
				"First name {self.first_name} \n"\
				"Last name {self.name} \n"\
				"Homedir {self.homedir} \n"\
				"Email {self.email} \n"\
				"GECOS {self.gecos} \n"\
				"ORG {self.org} \n"\
				)
		client.user_add(self.login,
		self.first_name,
		self.name,
		self.full_name,
		o_homedirectory=self.homedir,
		o_mail=self.email,
		o_gecos=self.gecos,
		o_ou=self.org)

	@safe_run
	def delete(self, client):
		"""
		Deletes user from IPA
		"""
		self._log.info(f"Deleting user {self.login}")
		client.user_del(self.login)


class Group(TranslatedObject, LoggingClass):
	def __init__(self, input_data: dict):
		group_info = self._translate_group(input_data)
		try:
			self.name = group_info['name']
		except KeyError:
			self.name = input_data['primaryKey']['name']
		self.members = group_info['members']
		self.description = group_info.get('description')


	def _translate_group(self, input_data):
		translated = self._translate(input_data)
		try:
			translated['members'] = input_data['members']
		except KeyError:
			translated['members'] = {"add": []}
		return translated

	@safe_run
	def add(self, client):
		"""
		Adds group to IPA
		"""
		self._log.info(f"Adding Group: {self.name}")
		self._log.debug(f"Adding Group: {self.name} \n Description: {self.description} \n Members: {self.members['add']}")
		client.group_add(self.name, o_description=self.description)
		for member in self.members['add']:
			self._change_membership('add', member, client)

	@safe_run
	def delete(self, client):
		"""
		Deletes Group from IPA
		"""
		client.group_del(self.name)

	def update_members(self, client):
		for member in self.members['add']:
			self._change_membership('add', member, client)
		for member in self.members['remove']:
			self._change_membership('remove', member, client)

	@safe_run
	def _change_membership(self, action, member, client):
		if action == 'add':
			func=client.group_add_member
		elif action == 'remove':
			func=client.group_remove_member
		self._log.info(f"{action} {member} to/from group {self.name}")
		func(self.name, o_user=member)

