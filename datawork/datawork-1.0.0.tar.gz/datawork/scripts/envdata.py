import multiprocessing
import re
import json
from pathlib import Path
from networktools.environment import get_env_variable
from networktools.library import check_type
"""
Variables de ambiente para datawork
"""
class EnvData:
    def __init__(self,*args,**kwargs):
        self.LOG_PATH=get_env_variable("LOG_PATH")
        self.NPROC = multiprocessing.cpu_count()        
        self.DW_DIR=Path(__file__).parent.parent.parent.resolve()
        self.DATAWORK_EST_X_PROC=get_env_variable("DATAWORK_EST_X_PROC")
        self.DATAWORK_TSLEEP=get_env_variable("DATAWORK_TSLEEP")
        self.DATAWORK_WORKERS=int(get_env_variable("DATAWORK_WORKERS"))
        self.DW_STATUS=get_env_variable("DW_STATUS")
        self.DW_GROUP=get_env_variable("DW_GROUP")
        self.SELECT_GROUP=get_env_variable("SELECT_GROUP")
        self.COLLECTOR_SOCKET_IP=get_env_variable("COLLECTOR_SOCKET_IP")
        self.COLLECTOR_SOCKET_PORT=get_env_variable("COLLECTOR_SOCKET_PORT")
        self.DATAWORK_SOCKET_IP=get_env_variable("DATAWORK_SOCKET_IP")
        self.DATAWORK_SOCKET_PORT=get_env_variable("DATAWORK_SOCKET_PORT")
        
        self.RDB_SOURCE_HOST=get_env_variable("RDB_SOURCE_HOST")
        self.RDB_SOURCE_PORT=get_env_variable("RDB_SOURCE_PORT")        
        self.RDB_ENU_HOST=get_env_variable("RDB_ENU_HOST")
        self.RDB_ENU_PORT=get_env_variable("RDB_ENU_PORT")

        self.MQ_HOST=get_env_variable("MQ_HOST")
        # Es la dirección ip on url del host dónde se ubica el servicio
        self.MQ_NAME=get_env_variable("MQ_NAME")
        # Es el nombre de usuario que accede a la cola
        self.MQ_PASS=get_env_variable("MQ_PASS")
        # Es el la password asociada
        self.MQ_VHOST=get_env_variable("MQ_VHOST")
        # Es el nombre del host virtual de la cola
        self.MQ_CODE=get_env_variable("MQ_CODE")
        # Es el nombre en código de la cola
        self.MQ_QUEUE_NAME=get_env_variable("MQ_QUEUE_NAME")

        
    
    def show(self):
        [print("export %s=%s"%(k,v)) for k,v in vars(self).items()]

    @property
    def json(self):
        return {k:str(v) for k,v in vars(self).items()}

    def save_json(self, name):
         json_file = re.compile("\.json$")
         if json_file.search(name):
             with open(name,"w") as f:
                 json.dump(self.json, f, indent=2)
                 f.write("\n")
         else:
             print("El nombre de archivo no es json, no se genera")


if __name__ == "__main__":
    envdata = EnvData()
    envdata.save_json("ejemplo_datawork.json")
