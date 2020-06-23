#
# This entity denotes a secure RESTServer, an extension of
# RESTserver.
#
# copyright (c) 2020 cisco Systems Inc., ALl righhts reseerved
# @author rks@cisco.com
#

from dnac.utils.RESTServer import RESTServer
#from dnac.exception import DnacException
#from dnac.exception import InvalidCriterionException

# copyright (c) 2019 cisco Systems Inc., ALl righhts reseerved

class SecureRESTServer(RESTServer):
	def __init__(self,service_address, service_port = 443):
		super().__init__(self, service_address, service_port)

	@property
	def protocol(self):
		return 'https'
