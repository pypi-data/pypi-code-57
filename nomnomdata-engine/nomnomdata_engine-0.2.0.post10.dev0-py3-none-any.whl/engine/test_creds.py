import json
import os.path

if "NOMIGEN_TEST_CREDENTIALS" in os.environ:
    creds_dir = os.environ["NOMIGEN_TEST_CREDENTIALS"]
else:
    creds_dir = "/nomnom/test_config"

if "CI" in os.environ:
    creds_path = os.environ["ENGINE_TEST_CREDS"]
else:
    creds_path = os.path.join(creds_dir, "nomigen_test_credentials.json")
if os.path.exists(creds_path):
    credentials = json.load(open(creds_path))
else:
    credentials = {}


def update_creds(new_creds):
    credentials = new_creds
    with open(creds_path, "w") as outfile:
        outfile.write(json.dumps(credentials, indent=4))


key_fp = os.path.join(creds_dir, "dummy_key.rsa")
private_key = None
if os.path.exists(key_fp):
    private_key = open(key_fp).read()
