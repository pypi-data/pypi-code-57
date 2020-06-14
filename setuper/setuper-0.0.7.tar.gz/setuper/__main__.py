import argparse

import setuper

def main():
	argument_parser = argparse.ArgumentParser(description="Install the requirements of a setuptools setup.py file.")
	argument_parser.add_argument("setup_path", help="The path to setup.py.")
	argument_parser.add_argument("--pip-arguments", help="Extra arguments to pass to Pip.")
	argument_parser.add_argument("--remove-self", action="store_true", help="Remove setuper after installing requirements.")
	argument_parser.add_argument("--extras", help="Comma separated categories of extras_require extras to install.")
	arguments = argument_parser.parse_args()

	setuper.run(arguments.setup_path, pip_arguments=arguments.pip_arguments, remove_self=arguments.remove_self, extras=arguments.extras.split(","))

if __name__ == "__main__":
	main()
