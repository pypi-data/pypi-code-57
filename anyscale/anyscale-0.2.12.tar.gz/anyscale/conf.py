import os
from typing import Optional

AWS_PROFILE = None

ANYSCALE_PRODUCTION_NAME = "anyscale.dev"

if "ANYSCALE_HOST" in os.environ:
    ANYSCALE_HOST = os.environ["ANYSCALE_HOST"]
else:
    # The production server.
    ANYSCALE_HOST = "https://" + ANYSCALE_PRODUCTION_NAME

# Global variable that contains the server session token.
CLI_TOKEN: Optional[str] = None

# Restic snapshot repo
TEST_MODE = False
SNAPSHOT_REPO = "s3:s3.amazonaws.com/anyscale-snapshots/internal"
TEST_V2 = False

SNAPSHOT_REPO_PASSWORD = "program_the_cloud"
