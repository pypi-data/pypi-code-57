import subprocess


class CommandLineUtils(object):
	"""
	A class used to run bash commands.

	...

	Methods
	-------
	run_bash_command(command)
		Runs a bash command and returns its output and error
	"""

	@staticmethod
	def run_bash_command(command):
		"""Static method for executing a bash command.

		Parameters
		----------
		command : str
			The bash command to run

		"""

		process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
		output, error = process.communicate()
		return output, error
