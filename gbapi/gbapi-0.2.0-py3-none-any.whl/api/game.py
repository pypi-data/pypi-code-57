"""module containing Game class"""

"""
(from structured_data.py)
	"isPartOf": {
        "@type": "VideoGame",
        "operatingSystem": "Windows",
        "gamePlatform": "PC",
        "applicationCategory": "Game",
        "name": "Half-Life",
        "url": "https:\/\/gamebanana.com\/games\/34"
    }
"""

class Game:
	"""
		Internal Game class.
		Represents a game on GameBanana.
	"""
	def __init__(self, src):
		if not isinstance(src, dict):
			raise TypeError(
				f"from Game: "
				f"src must be `dict`, not {type(raw)}!"
			)
		self.src = src
		
		self.name = src['name']
		self.url = src['url']
		self.platform = src['gamePlatform']
		self.os = self.system = src['operatingSystem']