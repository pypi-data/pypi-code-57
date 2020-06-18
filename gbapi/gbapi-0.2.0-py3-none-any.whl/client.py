import aiohttp

from .api.url_factory		import URLFactory
from .structures.all		import *

__all__ = ['gbApi']

class gbApi:
	def __init__(self):
		self._url = URLFactory("https://gamebanana.com")
		self._session = aiohttp.ClientSession()
		self._open = True

	async def _get(self, url):
		if not self._open:
			raise RuntimeError(
				"from gbApi: "
				"Session is not open! Create a new instance!"
			)
	
		async with self._session.get(url) as r:
			if r.status != 200:
				raise RuntimeError(
					"from gbApi: "
					f"Server returned non-200 code: {r.status}"
				)
			
			try:
				return await r.json()
			except Exception as e:
				raise RuntimeError(
					"from gbApi: "
					"Error while parsing JSON response"
				) from e

	async def _init_simple(self, url, obj):
		sdata_url = self._url.make(url, "StructuredDataModule")
		stats_url = self._url.make(url, "StatsModule")
		
		sdata = await self._get(sdata_url)
		stats = await self._get(stats_url)
		
		return obj(stats, sdata)
		
	async def _init_ssat(self, url, obj):
		sdata_url = self._url.make(url, "StructuredDataModule")
		attrb_url = self._url.make(url, "AttrbutesModule")
		stats_url = self._url.make(url, "StatsModule")
		
		sdata = await self._get(sdata_url)
		attrb = await self._get(attrb_url)
		stats = await self._get(stats_url)
		
		return obj(sdata, stats, attrb)
		
	async def _init_ssatai(self, url, obj):
		sdata_url = self._url.make(url, "StructuredDataModule")
		attrb_url = self._url.make(url, "AttrbutesModule")
		ainfo_url = self._url.make(url, "AdditionalInfoModule")
		stats_url = self._url.make(url, "StatsModule")
		
		print(sdata_url)
		print(attrb_url)
		print(ainfo_url)
		print(stats_url)
		
		sdata = await self._get(sdata_url)
		attrb = await self._get(attrb_url)
		ainfo = await self._get(ainfo_url)
		stats = await self._get(stats_url)
		
		return obj(stats, sdata, ainfo, attrb)
		
	async def _init_ssai(self, url, obj):
		sdata_url = self._url.make(url, "StructuredDataModule")
		ainfo_url = self._url.make(url, "AdditionalInfoModule")
		stats_url = self._url.make(url, "StatsModule")
		
		sdata = await self._get(sdata_url)
		ainfo = await self._get(ainfo_url)
		stats = await self._get(stats_url)
	
		return obj(stats, sdata, ainfo)

	async def get_blog(self, id):
		return await self._init_simple(f"blogs/{id}", Blog)

	async def get_castaway(self, id):
		return await self._init_simple(f"castaways/{id}", Castaway)
	
	async def get_concept(self, id):
		return await self._init_simple(f"concepts/{id}", Concept)
	
	async def get_effect(self, id):
		return await self._init_simple(f"effects/{id}", Effect)

	async def get_gamefile(self, id):
		return await self._init_simple(f"gamefiles/{id}", Gamefile)

	async def get_gui(self, id):
		return await self._init_simple(f"guis/{id}", GUI)
	
	async def get_map(self, id):
		return await self._init_ssai(f"maps/{id}", Map)
	
	async def get_prefab(self, id):
		return await self._init_simple(f"prefabs/{id}", Prefab)
	
	async def get_project(self, id):
		return await self._init_ssai(f"projects/{id}", Project)
	
	async def get_question(self, id):
		return await self._init_simple(f"questions/{id}", Question)
	
	async def get_request(self, id):
		return await self._init_ssai(f"requests/{id}", Request)
	
	async def get_script(self, id):
		return await self._init_simple(f"scripts/{id}", Script)
	
	async def get_skin(self, id):
		return await self._init_simple(f"skins/{id}", Skin)
	
	async def get_sound(self, id):
		return await self._init_simple(f"sounds/{id}", Sound)
	
	async def get_spray(self, id):
		return await self._init_simple(f"sprays/{id}", Spray)
	
	async def get_texture(self, id):
		return await self._init_simple(f"textures/{id}", Texture)
	
	async def get_thread(self, id):
		return await self._init_simple(f"threads/{id}", Thread)
	
	async def get_tool(self, id):
		return await self._init_ssai(f"tools/{id}", Tool)
	
	async def get_tutorial(self, id):
		return await self._init_ssai(f"tuts/{id}", Tutorial)
	
	async def get_ware(self, id):
		return await self._init_ssai(f"wares/{id}", Ware)
	
	async def get_wip(self, id):
		return await self._init_ssai(f"wips/{id}", WiP)

	async def close(self):
		await self._session.close()
		self._open = False