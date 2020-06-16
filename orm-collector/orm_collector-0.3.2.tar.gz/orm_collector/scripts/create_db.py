import click
from orm_collector import SessionCollector
from orm_collector import create_collector
from orm_collector import create_datawork
from sqlalchemy import create_engine
from networktools.environment import get_env_variable
from orm_collector import Base
import ujson as json



def get_session(name, env, dbdata, dbparams):
    if env:
        dbdata.update(dbuser=get_env_variable(dbparams.get("dbuser")),
                    dbpass=get_env_variable(dbparams.get("dbpass")),
                    dbname=get_env_variable(dbparams.get("dbname")),
                    dbhost=get_env_variable(dbparams.get("dbhost")),
                    dbport=get_env_variable(dbparams.get("dbport")))
        if not all(filter(lambda v:len(v)>0, dbdata.values())):
            print("Las variables de ambiente no están todas definidas, haz una revisión")
            print("Tienes lo siguiente:")
            [print(f"export {dbparams.get(llave)}={valor}" for llave, valor in dbparams.items())]
    print("Iniciando db con")
    [print("%s -> %s"%(k,v)) for k, v in dbdata.items()]
    csession = SessionCollector(**dbdata)
    return csession
    
def crear_schema(name="collector", env=True, dbdata = {}):
    schema = name.upper()
    dbparams =  dict(dbuser='%s_DBUSER' %schema,
                    dbpass='%s_DBPASS' %schema,
                    dbname='%s_DBNAME' %schema,
                    dbhost='%s_DBHOST' %schema,
                    dbport='%s_DBPORT' %schema)    
    csession = get_session(name, env, dbdata, dbparams)
    session = csession.session
    engine = csession.engine
    opts = {"collector":create_collector,"datawork":create_datawork}    
    create_db = opts.get(name.lower(), create_collector)    
    #load schema on engine
    try:
        print("Data->", csession.data)
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
import subprocess



def show_vars(name):
    command = "env|grep DB|grep -i %s" %name.upper()
    try:
        results=subprocess.run(command, shell=True, universal_newlines=True, check=True)
    except Exception as e:
        print("Parámetros no existen para : %s en ambiente" %name.upper())


@click.command()
@click.option("--name", default="collector", show_default=True, help="Nombre del esquema paraa mostrar {collector, datawork}")
def show_envvars(name):
    show_vars(name)


def get_json2dbdata(conf):
    json_file = re.compile("\.json$")
    dbdata = {}
    if json_file.search(conf):
        file_path=Path(conf)
        if file_path.exists():
            with open(file_path,'r') as f:
                dbdata = json.load(f)
            keys = {"dbuser", "dbpass", "dbname", "dbhost", "dbport"}
            if all(filter(lambda k: k in dbdata,keys)):
                return dbdata
            else:
                print("A tu archivo le falta una llave, revisa si tiene %s" %keys)
        else:
            print("Tu archivo json no existe en la ruta especificada: %s" %file_path)
            print("Debe ser así:")
            this_path = Path(__file__).parent
            example_path = this_path/"dbdata_example.json"
            if example_path.exists():
                with open(example_path,'r') as f:
                    print("{")
                    [print(k,":",v) for k,v in json.load(f).items()]
                    print("}")
            else:
                print("El archivo de ejemplo no existe, lo siento, escribe a dpineda@uchile.cl consultando")
    else:
        print("Tu archivo json debe tener una extensión json y una ruta correcta: pusiste  <%s>" %conf)
        print("Archivo json debe ser así:")
        this_path = Path(__file__).parent
        example_path = this_path/"dbdata_example.json"
        if example_path.exists():
            with open(example_path,'r') as f:
                print("{")
                [print("    %s:\"%s\","%(k,v)) for k,v in json.load(f).items()]
                print("}")
        else:
            print("El archivo de ejemplo no existe, lo siento, escribe a dpineda@uchile.cl consultando")
    return dbdata

@click.command()
@click.option("--name", default="collector", show_default=True, help="Nombre del esquema a crear {collector, datawork}")
@click.option("--vars", default=True, show_default=True,  type=bool, help="Para mostrar el nombre de las variables de database y su valor" )
@click.option("--env/--no-env", default=True, show_default=True,  type=bool, required=True,help="Si obtener los datos de ambiente o cargarlos de un json o data entregada")
@click.option("--conf", default="JSON FILE",  show_default=True, help="Archivo json con los parámetros de database, debe contener las llaves {dbuser, dbpass, dbname, dbhost, dbport}")
def run_crear_schema(name, vars, env, conf):
    print("Env option", env, conf)
    if env and vars:
        show_vars(name)
    if env:
        crear_schema(name)
    else:
        dbdata = get_json2dbdata(conf)
        if dbdata:
            crear_schema(name, env=False, dbdata=dbdata)
        else:
            print("Parámetros insuficientes %s" %dbdata)

if __name__=='__main__':
    run_crear_schema()

    
