import os
from jamboree import Jamboree
REDIS_HOST = os.getenv("REDIS_HOST", "0.0.0.0")
REDIS_PORT = int(os.getenv("REDIS_PORT", "3979"))


def setup_jamboree():
    return Jamboree(REDIS_HOST=REDIS_HOST, REDIS_PORT=REDIS_PORT)