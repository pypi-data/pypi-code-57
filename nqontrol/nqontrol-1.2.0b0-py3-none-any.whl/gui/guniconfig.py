"""gunicorn config file"""

from nqontrol.general.settings import HOST, PORT

workers = 1
bind = f"{HOST}:{PORT}"
timeout = 30
worker_class = "sync"
threads = 1
debug = True
spew = False
preload_app = True  # incompatible with reload feature
reload = False
