import argparse

import setuper

def main():
	argument_parser = argparse.ArgumentParser(description="Install the requirements of a setuptools setup.py file.")
	argument_parser.add_argument("setup_path", help="The path to setup.py.")
	argument_parser.add_argument("--pip-arguments", help="Extra arguments to pass to Pip.")
	argument_parser.add_argument("--remove-self", action="store_true", help="Remove setuper after installing requirements.")
	arguments = argument_parser.parse_args()

	setuper.run(arguments.setup_path, arguments.pip_arguments, arguments.remove_self)

if __name__ == "__main__":
	main()
