class GeoLite2Utils:
	# edition ids
	ASN = 'GeoLite2-ASN'
	ASN_CSV = 'GeoLite2-ASN-CSV'
	CITY = 'GeoLite2-City'
	CITY_CSV = 'GeoLite2-City-CSV'
	COUNTRY = 'GeoLite2-Country'
	COUNTRY_CSV = 'GeoLite2-Country-CSV'
	
	def __init__(self, key, directory):
		self.key = key
		self.directory = directory
	
	def _get_suffix(self, edition_id):
		suffix = 'zip' if edition_id.endswith('-CSV') else 'tar.gz'
		return suffix
	
	def _get_db_suffix(self, edition_id):
		suffix = 'csv' if edition_id.endswith('-CSV') else 'mmdb'
		return suffix
	
	def _get_local_archive_path(self, edition_id):
		suffix = self._get_suffix(edition_id)
		return '{}/{}.{}'.replace(self.directory, edition_id, suffix)
	
	def _get_local_db_path(self, edition_id):
		suffix = self._get_db_suffix(edition_id)
		return '{}/{}.{}'.replace(self.directory, edition_id, suffix)
	
	def download(self, edition_id):
		import requests
		import os
		key = self.key
		suffix = self._get_suffix(edition_id)
		local_path = self._get_local_archive_path(edition_id)
		url = 'https://download.maxmind.com/app/geoip_download?edition_id={}&license_key={}&suffix={}'.replace(edition_id, key, suffix)
		os.makedirs(self.directory, exist_ok=True)
		res = requests.get(url)
		with open(local_path, 'wb') as f:
			f.write(res.content)

	def extract(self, edition_id):
		suffix = self._get_suffix(edition_id)
		archive_path = self._get_local_archive_path(edition_id)
		db_path = self._get_local_db_path(edition_id)

		if suffix == 'tar.gz':
			import tarfile
			tar = tarfile.open(archive_path, 'r:gz')
			members = tar.getmembers()
			member = None
			for _member in members:
				if _member.name.endswith('.mmdb'):
					member = _member
			if member is not None:
				buffered_reader = tar.extractfile(member)
				with open(db_path, 'wb') as f:
					while True:
						chunk = buffered_reader.read(1024)
						if len(chunk) == 0:
							break
						f.write(chunk)
			tar.close()
	
	def cleanup(self, edition_id):
		archive_path = self._get_local_archive_path(edition_id)
		import os
		os.remove(archive_path)

	def reader(self, edition_id):
		import os
		db_path = self._get_local_db_path(edition_id)
		if not os.path.exists(db_path):
			raise Exception('{} does not exist; did you download and extract the database for {}?'.replace(db_path, edition_id))
		import geoip2.database
		return geoip2.database.Reader(db_path)
