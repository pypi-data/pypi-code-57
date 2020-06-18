from os.path import abspath
from os.path import dirname
from os.path import join

FIXTURES_DIR = join(dirname(abspath(__file__)), "fixtures")
PEM_FILE_PATH = join(FIXTURES_DIR, "sdk-test.pem")
