"""module containong StructuredData class"""

from .author import Author
from .game import Game

"""
{
    "@context": "https:\/\/schema.org",
    "@type": "CreativeWork",
    "author": {
        "@type": "Person",
        "name": "Santyx",
        "url": "https:\/\/gamebanana.com\/members\/1728386"
    },
    "isPartOf": {
        "@type": "VideoGame",
        "operatingSystem": "Windows",
        "gamePlatform": "PC",
        "applicationCategory": "Game",
        "name": "Half-Life",
        "url": "https:\/\/gamebanana.com\/games\/34"
    },
    "name": "scientists in alpha style clothing",
    "additionalType": "Request",
    "datePublished": "2020-06-09T00:02:47+0000",
    "dateModified": "2020-06-09T00:02:47+0000",
    "thumbnailUrl": "https:\/\/gamebanana.com\/requests\/embeddables\/14422?type=sdt_image",
    "image": "https:\/\/statics.gamebanana.com\/static\/img\/DefaultEmbeddables\/Request.jpg",
    "description": "",
    "commentCount": 0
}
"""

class StructuredData:
	"""
		Internal basic StructuredData class.
		The BaseSubmission class inherits from this.
	"""
	def __init__(self, src):
		if not isinstance(src, dict):
			raise TypeError(
				f"from StructuredData: "
				f"src must be `dict`, not {type(raw)}!"
			)
		#self.src = src
		
		self.author = Author(src['author'])
		self.partOf = self.game = Game(src['isPartOf'])
		
		self.name = src['name']
		self.type = src['additionalType']
		self.image = src['image']
		self.thumbnail = src['thumbnailUrl']