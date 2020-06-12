import re
from orm_collector import load_protocol
from orm_collector import load_dbdata
from orm_collector import load_dbtype
from orm_collector import load_server
from orm_collector import load_station
from pathlib import Path
from collections import OrderedDict 
import click


def load_data(dbdata, conf_files):
    session = SessionCollector(**dbdata)    
    operations = OrderedDict([
            ("protocol",load_protocol),
            ("dbtype",load_dbtype),        
            ("dbdata",load_dbdata),
            ("station",load_station)]
        )
    files = {key_op:conf_files.get(key_op) for key_op in operations.keys()}
    final_ops = {key_op:operations.get(key)(session, value) for key_op, value in files}
    session.close()



@click.command()
@click.option("--name", default="collector", show_default=True, help="Nombre del esquema a conectarse {collector, datawork}")
@click.option("--env/--no-env", default=True, show_default=True,  type=bool, required=True,help="Si obtener los datos de ambiente o cargarlos de un json o data entregada")
@click.option("--conf", default="dbdata.json",  show_default=True, help="Archivo json con los parámetros de database, debe contener las llaves {user, passw, dbname, hostname, port}")
@click.option("--dbuser", default="collector",  show_default=True, help="Nombre de usuario de la database, por defecto collector")
@click.option("--dbpass", default="xxxxxxxx",  show_default=True, help="Password para el usuario de la database, obligatoria si no se toma de env o json file")
@click.option("--dbname", default='collector',   show_default=True, help="Nombre de la database, por defecto {collector}")
@click.option("--dbhost", default='localhost',  show_default=True, help="Host o ip de la base de datos, por defecto localhost")
@click.option("--dbport", default='5432',  show_default=True, help="Puerto de database, por defecto de postgresql 5432")
@click.option("--path", default='./fixtures',  show_default=True, help="Ruta a los archivos csv, con nombres {protocol, dbdata, dbtype, server, station}")
@click.option("--filenames", default="filenames.json",  show_default=True, help="Archivo json con las llaves y nombres de archivo (en caso que no sean los definidos por defecto)")
@click.option("--protocol", default="protocol.csv",  show_default=True, help="Ruta al archivo csv con datos de la tabla protocol")
@click.option("--dbtype", default='dbtype.csv',  show_default=True, help="Ruta al archivo csv con datos de la tabla dbtype")
@click.option("--dbdata", default='dbdata.csv',   show_default=True, help="Ruta al archivo csv con datos de la tabla dbdata")
@click.option("--server", default='server.csv',  show_default=True, help="Ruta al archivo csv con datos de la tabla station_instance")
@click.option("--station", default='station.csv',  show_default=True, help="Ruta a los archivos csv con datos de la tabla station ")
def load_data_orm(name, env, conf, dbuser, dbpass, dbname, dbhost, dbport,
                  path, filenames, protocol, dbdata, dbtype, server, station):
    """
    Define files to load
    """
    conf_files = {}
    group_path = Path(path)
    if group_path.exists():
        cf_path = Path(filenames)
        if cf_path.exists():
            data_files = json.load(cf_path)
        else:
            cf_path_default = Path(__file__).parent/"filenames.json"            
            data_files = json.load(cf_path_default)
    else:
        data_files = dict(
            protocol_file=Path(protocol),
            dbdata_file=Path(dbdata),
            dbtype_file=Path(dbtype),
            server_file=Path(server),
            station_file=Path(station))        
    conf_files_check = dict(filter(lambda k_f: k_f[1].exists(), data_files.items()))
    conf_files = {key: data_files.get(key) for key in conf_files_check}    
    schema = name.upper()
    dbdata = {}
    dbparams = {}
    keys = {"user", "passw", "dbname", "hostname","port"}
    if conf_files:
        if env:    
            dbparams.update(user='%s_DBUSER' %schema,
                            passw='%s_DBPASS' %schema,
                            dbname='%s_DBNAME' %schema,
                            hostname='%s_DBHOST' %schema,
                            port='%s_PORT' %schema)
            dbdata.update(user=get_env_variable(dbparams.get("user")),
                        passw=get_env_variable(dbparams.get("passw")),
                        dbname=get_env_variable(dbparams.get("dbname")),
                        hostname=get_env_variable(dbparams.get("hostname")),
                        port=get_env_variable(dbparams.get("port")))
        elif json_file.search(conf):
            file_path=Path(conf)
            if file_path.exists():
                dbdata = json.load(file_path)
                if all(filter(lambda k: k in dbdata,keys)):
                    load_data(dbdata, conf_files)
                else:
                    print("A tu archivo le falta una llave, revisa si tiene %s" %keys)
            else:
                print("No existe el archivo con los datos para acceder a la db")
        else:
            print("Si no desea acceder a los datos cargados en ambiente de la db entregue la ruta a un json con las llaves %s" %keys)                
    else:
        print("Debes entregar una ruta que contenga los archivos con datos .csv, \n"+
              "o bien una ruta a un json con los datos de los archivos \n"+
              "o bien la ruta de los archivos que deseas cargar")

