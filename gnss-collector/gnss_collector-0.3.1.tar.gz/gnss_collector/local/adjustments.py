import multiprocessing
import ujson as json

from networktools.environment import get_env_variable


nproc = multiprocessing.cpu_count()
est_by_proc = int(get_env_variable("COLLECTOR_EST_X_PROC"))
tsleep = int(get_env_variable("COLLECTOR_TSLEEP"))
workers = int(get_env_variable("COLLECTOR_WORKERS"))
GSOF_TIMEOUT = int(get_env_variable("GSOF_TIMEOUT"))

if workers > nproc:
    workers = nproc

    # RETHINK SETTINGS:
RDB_HOST = get_env_variable("RDB_HOST")
RDB_PORT = get_env_variable("RDB_PORT")


cll_status = get_env_variable("CLL_STATUS")
CLLGROUP = get_env_variable("CLL_GROUP")

try:
    cll_group = json.loads(CLLGROUP)
except Exception as ex:
    raise ex

COLLECTOR_SOCKET_IP = get_env_variable("COLLECTOR_SOCKET_IP").split()[0]
COLLECTOR_SOCKET_PORT = get_env_variable("COLLECTOR_SOCKET_PORT")
LOG_PATH = get_env_variable("LOG_PATH")


DATADB =  dict(user=get_env_variable('%s_DBUSER' %schema)),
                passw=get_env_variable('%s_DBPASS' %schema)),
                dbname=get_env_variable('%s_DBNAME' %schema)),
                hostname=get_env_variable('%s_DBHOST' %schema)),
                port=get_env_variable('%s_DBPORT' %schema))
    
