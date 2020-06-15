from hackingtools.core import Logger, Utils, Config
if Utils.amIdjango(__name__):
	from .library.core import hackingtools as ht
else:
	import hackingtools as ht
import os

from pyshorteners import Shortener

config = Config.getConfig(parentKey='modules', key='ht_urlshortener')
output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'output'))

class StartModule():

	def __init__(self):
		self._main_gui_func_ = 'createShortcut'
		self._funcArgFromFunc_ = {
			'createShortcut' : {
				'shortenerDomain' : {
					'urlshortener' : 'getShortcutDomains'
				}
			}
		}

	def help(self):
		Logger.printMessage(message=ht.getFunctionsNamesFromModule('ht_urlshortener'), debug_module=True)

	def createShortcut(self, url, fakeUrl, fakeText, shortenerDomain='tinyurl', api_key=None, user_id=None):
		try:
			shortener = Shortener(api_key=api_key, user_id=user_id)
			if shortenerDomain in shortener.available_shorteners:
				short = eval( 'shortener.{dom}'.format(dom=shortenerDomain) )
				endLink = short.short(url)
				withouthttp = endLink[7:]
				if withouthttp.startswith('/'):
					withouthttp = withouthttp[1:]
				fakeUrl = fakeUrl.replace('http://', '').replace('https://', '').replace('www.', '')
				return "https://www.{domain}-{postlink}@{withouthttp}".format(domain=fakeUrl, postlink=fakeText, withouthttp=withouthttp.replace('\n', ''))
			return ""
		except Exception as e:
			Logger.printMessage(str(e), description=shortenerDomain, is_error=True, debug_module=True)
			return ""

	def getShortcutDomains(self):
		shortener = Shortener()
		return shortener.available_shorteners