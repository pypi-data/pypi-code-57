import multiprocessing
import json

from networktools.environment import get_env_variable

class EnvData:
    def __init__(self,*args,**kwargs):
        schema = "COLLECTOR"
        self.CLLGROUP = get_env_variable("CLL_GROUP")
        try:
            self.CLL_GROUP = json.loads(self.CLLGROUP)
        except Exception as ex:
            raise ex
        self.NPROC = multiprocessing.cpu_count()
        self.EST_BY_PROC = int(get_env_variable("COLLECTOR_EST_X_PROC"))
        self.COLLECTOR_TSLEPP = int(get_env_variable("COLLECTOR_TSLEEP"))
        self.COLLECTOR_WORKERS = int(get_env_variable("COLLECTOR_WORKERS"))
        self.GSOF_TIMEOUT = int(get_env_variable("GSOF_TIMEOUT"))

        if self.COLLECTOR_WORKERS > self.NPROC:
            self.COLLECTOR_WORKERS = self.NPROC

            # RETHINK SETTINGS:
        self.RDB_HOST = get_env_variable("RDB_HOST")
        self.RDB_PORT = get_env_variable("RDB_PORT")


        self.CLL_STATUS = get_env_variable("CLL_STATUS")

        self.COLLECTOR_SOCKET_IP = get_env_variable("COLLECTOR_SOCKET_IP")
        self.COLLECTOR_SOCKET_PORT = get_env_variable("COLLECTOR_SOCKET_PORT")
        self.LOG_PATH = get_env_variable("LOG_PATH")


        self.DBDATA =  dict(
            dbuser=get_env_variable('%s_DBUSER' %schema),
            dbpass=get_env_variable('%s_DBPASS' %schema),
            dbname=get_env_variable('%s_DBNAME' %schema),
            dbhost=get_env_variable('%s_DBHOST' %schema),
            dbport=get_env_variable('%s_DBPORT' %schema))

        self.SERVER_NAME=get_env_variable('SERVER_NAME')
    
    def show(self):
        [print("export %s=%s"%(k,v if not isinstance(v, tuple) else v[0])) for k,v in vars(self).items()]

    @property
    def json(self):
        return {k:v if not isinstance(v, tuple) else v[0] for k,v in vars(self).items()}

