import re
from orm_collector import load_protocol
from orm_collector import load_dbdata
from orm_collector import load_dbtype
from orm_collector import load_server
from orm_collector import load_network
from orm_collector import load_station
from pathlib import Path
from collections import OrderedDict 
import click
from orm_collector.scripts.create_db import get_session, get_json2dbdata
import ujson as json

def load_data(session, conf_files):
    operations = OrderedDict([
            ("protocol",load_protocol),
            ("dbtype",load_dbtype),        
            ("dbdata",load_dbdata),
            ("network", load_network),
            ("server", load_server),
            ("station",load_station)]
        )
    files = {key_op:conf_files.get(key_op) for key_op in operations.keys()}
    final_ops = {key_op:operations.get(key_op)(session, value) for key_op, value in files.items()}
    session.close()

 
       

@click.command()
@click.option("--name", default="collector", show_default=True, help="Nombre del esquema a conectarse {collector, datawork}")
@click.option("--env/--no-env", default=True, show_default=True,  type=bool, required=True,help="Si obtener los datos de ambiente o cargarlos de un json o data entregada")
@click.option("--conf", default="dbdata.json",  show_default=True, help="Archivo json con los parámetros de database, debe contener las llaves {user, passw, dbname, hostname, port}")
@click.option("--path", default='./fixtures',  show_default=True, help="Ruta a los archivos csv, con nombres {protocol, dbdata, dbtype, server, station}")
@click.option("--filenames", default="filenames.json",  show_default=True, help="Archivo json con las llaves y nombres de archivo (en caso que no sean los definidos por defecto)")
def load_data_orm(name, env, conf, path, filenames):
    """
    Define files to load
    """
    conf_files = {}
    group_path = Path(path)
    data_files = {}
    if group_path.exists():
        cf_path = Path(filenames)
        if cf_path.exists():
            file_json = open(cf_path)           
            data_files = json.load(file_json)
            file_json.close()
        else:
            cf_path_default = Path(__file__).parent/"filenames.json"
            if cf_path_default.exists():
                with open(cf_path_default,"r") as f:                       
                    data_files = json.load(f)
    conf_files_check = dict(filter(lambda k_f: (group_path/Path(k_f[1])).exists(), data_files.items()))
    conf_files = {key: group_path/data_files.get(key) for key in conf_files_check}
    print("Files selected (que existen y se leerán)")
    [print("%s -> %s" %(k,v)) for k,v in conf_files.items()]     
    if conf_files:
        dbdata = {}
        if not env:
            dbdata = get_json2dbdata(conf)
        schema = name.upper()
        dbparams =  dict(dbuser='%s_DBUSER' %schema,
                        dbpass='%s_DBPASS' %schema,
                        dbname='%s_DBNAME' %schema,
                        dbhost='%s_DBHOST' %schema,
                        dbport='%s_DBPORT' %schema)                
        session = get_session(name, env, dbdata, dbparams)
        if session:
            print("Cargando los siguientes archivos con datos a la database")
            [print("%s -> %s"%(k,v)) for k,v in conf_files.items()]
            load_data(session, conf_files)
    else:
        print("Debes entregar una ruta que contenga los archivos con datos .csv, \n"+
              "o bien una ruta a un json con los datos de los archivos \n"+
              "o bien la ruta de los archivos que deseas cargar")

if __name__=='__main__':
    load_data_orm()

