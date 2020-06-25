import uuid
import re
import socket
import psutil
import platform
from urllib.parse import urljoin
import tempfile

# Get temporary folder
TEMP_DIR = tempfile.gettempdir()

# Set API Base url
BASE_URL = 'https://epione-demo.inria.fr/fedbionet/'

# Set urls
ME_URL = urljoin(BASE_URL, 'me/')
CLIENTS_URL = urljoin(BASE_URL, 'clients/')
MODELS_URL = urljoin(BASE_URL, 'model/')
JOBS_URL = urljoin(BASE_URL, 'job/')
SUBMISSIONS_URL = urljoin(BASE_URL, 'submission/')
DATA_URL = urljoin(BASE_URL, 'data/')


# Get system info
def system_info():
    info = {'platform': platform.system(),
            'platform-release': platform.release(),
            'platform-version': platform.version(),
            'architecture': platform.machine(),
            'hostname': socket.gethostname(),
            'ip-address': socket.gethostbyname(socket.gethostname()),
            'mac-address': ':'.join(re.findall('..', '%012x' % uuid.getnode())),
            'processor': platform.processor(),
            'ram': str(round(psutil.virtual_memory().total / (1024.0 ** 3))) + " GB"}
    return info
