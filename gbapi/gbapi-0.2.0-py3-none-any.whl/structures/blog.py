"""module containing Blog class"""

from gbapi.api.base_submission import BaseSubmission

class Blog(BaseSubmission):
	"""
		Represents a blog on GameBanana.
		Since blogs don't have any additional info, this is just a renamed BaseSubmission.
	"""
	pass