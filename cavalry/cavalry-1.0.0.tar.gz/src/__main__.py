import os, json, argparse

def main():

	path = os.path.dirname(__file__) + "/.secrets.json"

	parser = argparse.ArgumentParser(description="Utility to load environment variables. To persist the variables into your scope, run 'source cav [options]' or '. cav [options]'")
	parser.add_argument("-s", "--secrets", metavar="FILE", default=path, help="specify an alternate secrets file")# SECRETS should be set to wherever .secrets.json is located.

	subparsers = parser.add_subparsers(dest="action")
	store = subparsers.add_parser("store", help="store variables")
	delete = subparsers.add_parser("delete", help="delete variables")
	load = subparsers.add_parser("load", help="load variables")

	store.add_argument("project", help="project to load")
	store.add_argument("key", help="variable name")
	store.add_argument("value", help="secret data")
	delete.add_argument("project", help="project to load")
	delete.add_argument("key", help="variable name")

	load.add_argument("project", help="project to load")
	load.add_argument("-v", "--var", default=None, help="load a specific variable")

	args = parser.parse_args()

	# Initialize .secrets.json
	if not os.path.exists(args.secrets):
		with open(args.secrets, 'w') as f:
			f.write(json.dumps({}))

	# Load .secrets.json
	with open(args.secrets, 'r') as f:
		secrets = json.loads(f.read())

	if args.action == "store":
		if not args.project in secrets:
			secrets[args.project] = {args.key: args.value}
		else:
			secrets[args.project][args.key] = args.value

	elif args.action == "delete":
		secrets[args.project].pop(args.key)

	elif args.action == "load":
		if args.var:
			print(f"export {args.var}={secrets[args.project][args.var]}")
		data = []
		for k, v in secrets[args.project].items():
			data.append(f"{k}={json.dumps(v)}")# make sure v is valid as a single value

		print(f"export {' '.join(data)}")

	# Save changes
	with open(args.secrets, 'w') as f:
		f.write(json.dumps(secrets))

if __name__ == "__main__":
	main()
