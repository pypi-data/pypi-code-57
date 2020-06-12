import click
from orm_collector import CollectorSession
from orm_collector import create_collector
from orm_collector import create_datawork
from sqlalchemy import create_engine
from networktools.environment import get_env_variable
from orm_collector import Base
import ujson as json


def crear_schema(name="collector", env=True, dbdata = {}):
    schema = name.upper()
    opts = {"collector":create_collector,"datawork":create_datawork}
    create_db = opts.get(name.lower(), create_collector)
    dbparams =  dict(user='%s_DBUSER' %schema,
                    passw='%s_DBPASS' %schema,
                    dbname='%s_DBNAME' %schema,
                    hostname='%s_DBHOST' %schema,
                    port='%s_PORT' %schema)
    if env:
        dbdata.update(user=get_env_variable(dbparams.get("user")),
                    passw=get_env_variable(dbparams.get("passw")),
                    dbname=get_env_variable(dbparams.get("dbname")),
                    hostname=get_env_variable(dbparams.get("hostname")),
                    port=get_env_variable(dbparams.get("port")))
        if not all(filter(lambda v:len(v)>0, dbdata.values())):
            print("Las variables de ambiente no están todas definidas, haz una revisión")
            print("Tienes lo siguiente:")
            [print(f"export {dbparams.get(llave)}={valor}" for llave, valor in dbparams.items())]            
    csession = CollectorSession(**dbdata)
    engine = csession.engine
    #load schema on engine
    try:
        create_db(engine)
        Base.metadata.create_all(engine, checkfirst=True)
        print("Esquema creado en la base de datos %s" %dbdata.get("dbname"))
        if not env:
            print("Pon estos parámetros en tu ambiente virtual para que el %s los tome al ejecutarse")
            [print(f"export {dbparams.get(llave)}={valor}" for llave, valor in dbparams.items())]
    except Exception as e:
        print("Falla al crear esquema de tablas")
        raise e
    
import re
from pathlib import Path

@click.command()
@click.option("--name", default="collector", show_default=True, help="Nombre del esquema a crear {collector, datawork}")
@click.option("--env/--no-env", default=True, show_default=True,  type=bool, required=True,help="Si obtener los datos de ambiente o cargarlos de un json o data entregada")
@click.option("--conf", default="JSON FILE",  show_default=True, help="Archivo json con los parámetros de database, debe contener las llaves {user, passw, dbname, hostname, port}")
@click.option("--dbuser", default="collector",  show_default=True, help="Nombre de usuario de la database, por defecto collector")
@click.option("--dbpass", default="xxxxxxxx",  show_default=True, help="Password para el usuario de la database, obligatoria si no se toma de env o json file")
@click.option("--dbname", default='collector',   show_default=True, help="Nombre de la database, por defecto {collector}")
@click.option("--dbhost", default='localhost',  show_default=True, help="Host o ip de la base de datos, por defecto localhost")
@click.option("--dbport", default='5432',  show_default=True, help="Puerto de database, por defecto de postgresql 5432")
def run_crear_schema(name, env, conf, dbuser, dbpass, dbname, dbhost, dbport):
    json_file = re.compile("\.json$")
    if env:
        crear_schema(name)
    elif json_file.search(conf):
        file_path=Path(conf)
        if file_path.exists():
            dbdata = json.load(file_path)
            keys = {"user", "passw", "dbname", "hostname","port"}
            if all(filter(lambda k: k in dbdata,keys)):
                create_schema(name, env=False, dbdata=dbdata)
            else:
                print("A tu archivo le falta una llave, revisa si tiene %s" %keys)
        else:
            print("Tu archivo json no existe en la ruta especificada: %s" %file_path)
    else:
        dbdata = dict(user=dbuser,
                    passw=dbpass,
                    dbname=dbname,
                    hostname=dbhost,
                    port=dbpost)
        create_schema(name, env=False, dbdata=dbdata)         
       


if __name__=='__main__':
    run_crear_schema()

    
