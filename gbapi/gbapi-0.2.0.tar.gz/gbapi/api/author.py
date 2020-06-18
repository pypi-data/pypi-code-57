"""module containing Author class"""

"""
(from structured_data.py)
	"author": {
        "@type": "Person",
        "name": "Santyx",
        "url": "https:\/\/gamebanana.com\/members\/1728386"
    }
"""

class Author:
	"""
		Internal Author class.
		Represents a GameBanana user.
	"""
	def __init__(self, src):
		if not isinstance(src, dict):
			raise TypeError(
				f"from Author: "
				f"src must be `dict`, not {type(raw)}!"
			)
		self.src = src
		
		self.name = src['name']
		self.url = src['url']