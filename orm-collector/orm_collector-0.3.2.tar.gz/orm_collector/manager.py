from sqlalchemy import update
from sqlalchemy import Table, MetaData
from sqlalchemy.sql import text
from basic_logtools.filelog import LogFile
from pathlib import Path
from orm_collector.models import (Station,
                                  Protocol,
                                  DBData,
                                  DBType,
                                  DataDestiny,
                                  ServerInstance,
                                  NetworkGroup)

from orm_collector.db_session import CollectorSession, data

import datetime

from geoalchemy2 import functions as geo_func

from sqlalchemy.sql import select
from sqlalchemy.sql import table
from sqlalchemy.sql import column
from sqlalchemy import inspect


def object_as_dict(obj):
    return {c.key: getattr(obj, c.key)
            for c in inspect(obj).mapper.column_attrs}


class SessionHandle:
    """
    A session middleware class to manage the basic elements in the database,
    has generic methods to verify the elements existence, update_ and obtain
    lists from tables
    """

    def __init__(self, *args, **kwargs):
        session = CollectorSession(**kwargs)
        self.engine = session.engine
        self.session = session.session
        self.conn = session.connection
        self.metadata = MetaData()
        self.data = kwargs
        code = kwargs.get('code', 'ORM')
        log_path = kwargs.get('log_path', './')
        print("ORM log path", log_path)
        log_level = kwargs.get('log_level', 'INFO')
        hostname = kwargs.get('hostname', 'localhost')
        self.logger = LogFile(self.class_name,
                              code,
                              hostname,
                              path=log_path,
                              base_level=log_level)
        self.path = Path(__file__).parent

    @property
    def class_name(self):
        return self.__class__.__name__

    def close(self):
        self.session.close()

    def exists_table(self, table_name, **kwargs):
        """
        Check if table_name exists on schema
        :param table_name: a table_name string
        :return: boolean {True,False}
        """
        if bool(kwargs):
            this_schema = kwargs['schema']
        else:
            this_schema = 'collector'

        return self.engine.dialect.has_table(self.engine.connect(), table_name)

    def exists_field(self, table_name, field_name, **kwargs):
        """
        Check if field exist in table
        :param table_name: table name string
        :param field_name: field name string
        :return:  bolean {True, False}
        """
        if bool(kwargs):
            this_schema = kwargs['schema']
        else:
            this_schema = 'collector'

        assert self.exists_table(table_name), 'No existe esta tabla'
        fields = Table(
            table_name,
            self.metadata,
            autoload=True,
            autoload_with=self.engine,
            schema=this_schema)
        r = [c.name for c in fields.columns]
        try:
            r.remove('id')
        except ValueError as e:
            self.logger.exception("Error al checkear campo, %s" % e)
        assert field_name in r, 'No existe este campo en tabla'
        return True

    def value_type(self, table_name, field_name, value, **kwargs):
        """
        Check if value is the same value type in field
        :param table_name: table name string
        :param field_name: field name string
        :param value:  some value
        :return: boolean {True, False, None}; None if value type doesn't exist
        on that list, because there are only the most common types.
        """
        if bool(kwargs):
            this_schema = kwargs['schema']
        else:
            this_schema = 'collector'

        # get type value
        assert self.exists_table(table_name), 'No existe esta tabla'
        fields = Table(
            table_name,
            self.metadata,
            autoload=True,
            autoload_with=self.engine,
            schema=this_schema)
        r = [c.name for c in fields.columns]
        assert self.exists_field(table_name, field_name), \
            'Campo no existe en tabla'
        this_index = r.index(field_name)
        t = [str(c.type) for c in fields.columns]
        this_type = t[this_index]
        b = False
        if this_type == 'INTEGER' or this_type == 'BigInteger':
            assert isinstance(value, int)
            b = True
        elif this_type[0:7] == 'VARCHAR' or this_type == 'TEXT' or this_type == 'STRING':
            assert isinstance(value, str)
            b = True
        elif this_type == 'BOOLEAN':
            assert isinstance(value, bool)
            b = True
        elif this_type == 'DATE':
            assert isinstance(value, datetime.date)
            b = True
        elif this_type == 'DATETIME':
            assert isinstance(value, datetime.datetime)
            b = True
        elif this_type == 'FLOAT' or this_type == 'NUMERIC':
            assert isinstance(value, float)
            b = True
        else:
            b = None

        return b
        # check

        def generic_query(self, st):
            q = text(st)
            u = self.session.execute(q)
            return(u)

    def update_table(self, table_name, instance, field_name, value, **kwargs):
        """
        Change some value in table
        :param table_name: table name class
        :param instance: instance to modify in database
        :param field: field name string
        :param value: value
        :return: void()
        """
        this_schema = kwargs.get('schema', 'collector')
        # update to database
        table = Table(
            table_name,
            self.metadata,
            autoload=True,
            autoload_with=self.engine,
            schema=this_schema
        )
        up = update(table).where(
            table.c.id == instance.id).values({field_name: value})
        self.session.execute(up)
        self.session.commit()

    # LIST ELEMENTS

    def get_list(self, model):
        """
        Get the complete list of elements in some Model Class (Table in db)

        :param model:Model Class
        :return: a query list
        """
        return self.session.query(model).all()


# Class Alias
SH = SessionHandle


class SessionCollector(SH):
    """
    An specific SessionHandler who extends database model in Collector case,
    has a Station, a Protocol and a FBData tables
    """

    # STATION TABLE

    def station(self,
                **kwargs):
        code = kwargs.get('code')
        name = kwargs.get('name')
        position_x = kwargs.get('ECEF_X')
        position_y = kwargs.get('ECEF_Y')
        position_z = kwargs.get('ECEF_Z')
        protocol_host = kwargs.get('protocol_host')
        host = kwargs.get('host')
        port = int(kwargs.get('port'))
        interface_port = int(kwargs.get('interface_port'))
        db = kwargs.get('db')
        protocol = kwargs.get('protocol')
        server_id = kwargs.get('server_id', 0)
        active = kwargs.get('active', False)
        network = kwargs.get("network_id","3g")
        instance = self.session.query(Station).filter_by(code=code).first()
        if instance:
            self.logger.info("Estación %s ya existe" % instance)
            return instance
        else:
            try:
                point = dict(X=position_x, Y=position_y, Z=position_z)
                # check if db and protocol exists
                db_e = object
                prot_e = object
                network_id = object
                if isinstance(db, int):
                    db_e = self.get_dbdata_by_id(db)
                    db_id = db_e.id
                else:
                    db_e = self.get_dbdata_id(db)
                    db_id = db_e.id
                if isinstance(protocol, int):
                    prot_e = self.get_protocol_by_id(protocol.upper())
                    prot_id = prot_e.id
                else:

                    prot_e = self.get_protocol_id(protocol)
                    prot_id = prot_e.id
                if isinstance(network, int):
                    network_e = self.get_network_by_id(network.upper())
                    network_id = network_e.id
                else:
                    network_e = self.get_network_id(network)
                    network_id = network_e.id
                if db_e and prot_e:
                    station = Station(code=code,
                                      name=name,
                                      position_x=point['X'],
                                      position_y=point['Y'],
                                      position_z=point['Z'],
                                      interface_port=interface_port,
                                      protocol_host=protocol_host,
                                      port=port,
                                      host=host,
                                      db_id=db_id,
                                      protocol_id=prot_id,
                                      active=active,
                                      server_id=server_id,
                                      network_id=network_id)
                    self.create_station(station)
                    self.logger.info("Creada nueva estación %s" % instance)
                    return station
                else:
                    return None
            except Exception as ex:
                print("Alguna falla al crear nueva station -> %s" % ex)
                raise ex

    def create_station(self, station):
        self.session.add(station)
        self.session.commit()

    def update_station(self, instance, new_dict):
        t_name = 'station'
        station = object_as_dict(instance)
        db = None
        protocol = None
        if 'db' in new_dict.keys():
            db = new_dict['db']
        if 'protocol' in new_dict.keys():
            protocol = new_dict['protocol']
        db_e = object
        prot_e = object
        if db:
            if isinstance(db, int):
                db_e = self.get_dbdata_by_id(db)
                db_id = db_e.id
            else:
                db_e = self.get_dbdata_id(db)
                db_id = db_e.id
        if protocol:
            if isinstance(protocol, int):
                prot_e = self.get_protocol_by_id(protocol)
                prot_id = prot_e.id
            else:
                prot_e = self.get_protocol_id(protocol)
                prot_id = prot_e.id
            new_dict['protocol_id'] = prot_id
            new_dict['db_id'] = db_id
        for k in new_dict.keys():
            print(k)
            if k in station.keys():
                v = new_dict[k]
                self.update_table(t_name, instance, k, v)

    def delete_station(self, station):
        self.session.delete(station)
        self.session.flush()

    def get_stations(self, server='atlas', only_active=True):
        # for sta in stations:
        new_stations = []
        if only_active:
            server = self.get_server_id(server)
            print("Server", server)
            new_stations = self.session.query(
                Station).filter_by(active=True, server_id=server.id)
        else:
            new_stations = self.get_list(Station)
        return new_stations

    def get_station_id(self, code):
        # code is a unique value
        u = self.session.query(Station).filter_by(code=code).first()
        if u:
            return u.id
        else:
            return None

    def get_station_by_id(self, pk):
        u = self.session.query(Station).filter_by(id=pk).first()
        if u:
            return u
        else:
            return None

    def get_stations_near(self, center_point, km):
        lat = center_point[0]
        lon = center_point[1]
        point = "POINT(" + str(lon) + " " + str(lat) + ")"
        Q = "ST_GeogFromText(\'%s\')" % point
        print(point)
        # u = self.session.query(Station).filter(
        #    functions.ST_DWithin(
        #        Station.position,
        #        Q, km * 1000,true))
        strq = "select * from station where ST_DWithin(ST_GeogFromText(\'" + \
            point + "\'),position," + str(km * 1000) + ",true)"
        stmt = text(strq)
        result = self.session.execute(stmt)
        return result

    def get_station_data(self, server='atlas', active="true"):
        server = self.get_server_id(server)
        file_q = open(self.path/"./sql/station_query.sql", "r")
        sql_query_tpl = file_q.read()
        sql_query = sql_query_tpl.replace("[SERVER_ID]",
                                          str(server.id)).replace("[ACTIVE]", active)
        file_q.close()
        print("Consulta--->", sql_query)
        stmt = text(sql_query)
        result = self.session.execute(stmt)
        return result

    # Network Group

    def network(self, **kwargs):
        if kwargs:
            name = kwargs.get('name', "3g").upper()
            description = kwargs.get("description", "Red de celular")
        network = self.session.query(
            NetworkGroup).filter_by(name=name).first()
        if network:
            self.logger.info("network ya exitse, %s" % network)
            return network
        else:
            network = NetworkGroup(
                name=name,
                description=description)
            self.create_network(network)
            self.logger.info("Nuevo network creado, %s" % network)
            return network

    def create_network(self, network):
        self.session.add(network)
        self.session.commit()

    def update_network(self, instance, fields, values):
        t_name = 'network_instance'
        assert len(fields) == len(values)
        for i, f in enumerate(fields):
            v = values[i]
            self.update_table(t_name, instance, f, v)

    def delete_network(self, network):
        self.session.delete(network)
        self.session.flush()

    def get_network(self):
        return self.get_list(NetworkGroup)

    def get_network_id(self, name):
        # code is a unique value
        u = self.session.query(NetworkGroup).filter_by(name=name.upper()).all()
        if u:
            return u[0]
        else:
            return None

    def get_network_by_id(self, pk):
        u = self.session.query(NetworkGroup).filter_by(id=pk).all()
        if u:
            return u[0]
        else:
            return None


    

    # Server Instance

    def server(self, **kwargs):
        if kwargs:
            host_name = kwargs.get('host_name', "atlas")
            host_ip = kwargs.get("host_ip", "10.54.217.15")
            gnsocket_port = kwargs.get("gnsocket")
            activated = kwargs.get("activated", False)
        server = self.session.query(
            ServerInstance).filter_by(host_name=host_name).first()
        if server:
            self.logger.info("server ya exite, %s" % server)
            return server
        else:
            server = ServerInstance(host_name=host_name,
                                    host_ip=host_ip,
                                    gnsocket_port=gnsocket_port,
                                    activated=activated)
            self.create_server(server)
            self.logger.info("Nuevo server creado, %s" % server)
            return server

    def create_server(self, server):
        self.session.add(server)
        self.session.commit()

    def update_server(self, instance, fields, values):
        t_name = 'server_instance'
        assert len(fields) == len(values)
        for i, f in enumerate(fields):
            v = values[i]
            self.update_table(t_name, instance, f, v)

    def active_server(self, instance):
        self.update_server(instance, ["activated"], [True])

    def deactive_server(self, instance):
        self.update_server(instance, ["activated"], [False])

    def delete_server(self, server):
        self.session.delete(server)
        self.session.flush()

    def get_server(self):
        return self.get_list(ServerInstance)

    def get_server_id(self, name):
        # code is a unique value
        u = self.session.query(ServerInstance).filter_by(host_name=name).all()
        if u:
            return u[0]
        else:
            return None

    def get_server_by_id(self, pk):
        u = self.session.query(ServerInstance).filter_by(id=pk).all()
        if u:
            return u[0]
        else:
            return None

    # PROTOCOL TABLE

    def protocol(self, **kwargs):
        if bool(kwargs):
            name = kwargs['name']
            ref = kwargs['ref']
            class_name = kwargs['class_name']
            git = kwargs['git']
        protocol = self.session.query(Protocol).filter_by(name=name).first()
        if protocol:
            self.logger.info("Protocolo ya exite, %s" % protocol)
            return protocol
        else:
            protocol = Protocol(name=name,
                                ref_url=ref,
                                class_name=class_name,
                                git_url=git)
            self.create_protocol(protocol)
            self.logger.info("Nuevo protocolo creado, %s" % protocol)
            return protocol

    def create_protocol(self, protocol):
        self.session.add(protocol)
        self.session.commit()

    def update_protocol(self, instance, fields, values):
        t_name = 'protocol'
        assert len(fields) == len(values)
        for f in fields:
            v = values[fields.index(f)]
            self.update_table(t_name, instance, f, v)

    def delete_protocol(self, protocol):
        self.session.delete(protocol)
        self.session.flush()

    def get_protocol(self):
        return self.get_list(Protocol)

    def get_protocol_id(self, name):
        # code is a unique value
        u = self.session.query(Protocol).filter_by(name=name).all()
        if len(u) > 0:
            return u[0]
        else:
            return None

    def get_protocol_by_id(self, pk):
        u = self.session.query(Protocol).filter_by(id=pk).all()
        if len(u) > 0:
            return u[0]
        else:
            return None
    # DBDATA TABLE

    def dbdata(self, **kwargs):
        try:
            code = kwargs.get('code')
            path = kwargs.get('path')
            host = kwargs.get('host')
            port = int(kwargs.get('port'))
            user = kwargs.get('user')
            passw = kwargs.get('passw')
            info = kwargs.get('info')
            dbtype = kwargs.get('dbtype')
            dbname = kwargs.get('dbname')
            if 'type_name' in kwargs:
                dbtype = kwargs.get('type_name')
            instance = self.session.query(DBData).filter_by(code=code).first()
            if instance:
                self.logger.info("DBdata existe, %s" % instance)
                return instance
            else:
                db_e = self.get_dbtype_id(dbtype)
                if db_e:
                    instance = DBData(code=code,
                                      path=path,
                                      host=host,
                                      port=port,
                                      user=user,
                                      passw=passw,
                                      info=info,
                                      dbtype_id=db_e.id,
                                      dbname=dbname)
                    self.create_dbdata(instance)
                    self.logger.info("DBdata creada, %s" % instance)
                    return instance
                else:
                    return None
        except Exception as ex:
            self.logger.exception("Error al crear new dbdata, %s" % ex)
            raise ex

    def create_dbdata(self, dbdata):
        self.session.add(dbdata)
        self.session.commit()

    def update_dbdata(self, instance, new_dict):
        t_name = 'dbdata'
        dbdata = object_as_dict(instance)
        for k in new_dict.keys():
            if k in dbdata.keys():
                v = new_dict[k]
                db_e = self.get_dbtype_by_id(dbdata)
                new_dict['dbtype_id'] = db_e.id
                if type(v) == type(dbdata[k]) and v != dbdata[k]:
                    self.update_table(t_name, instance, k, v)

    def delete_dbdata(self, dbdata):
        self.session.delete(dbdata)
        self.session.flush()

    def get_dbdatas(self):
        return self.get_list(DBData)

    def get_dbdata_id(self, code):
        # code is a unique value
        u = self.session.query(DBData).filter_by(code=code).all()
        if u:
            return u[0]
        else:
            return None

    def get_dbdata_list_by_type(self, dtype):
        # code is a unique value
        u = self.session.query(DBData).filter_by(dbtype=dtype).all()
        return u

    def get_dbdata_by_id(self, pk):
        u = self.session.query(DBData).filter_by(id=pk).all()
        if len(u) > 0:
            return u[0]
        else:
            return None

    def get_dbdata_data(self):
        file_q = open(self.path/"./sql/dbdata_query.sql", "r")
        sql_query = file_q.read()
        file_q.close()
        stmt = text(sql_query)
        result = self.session.execute(stmt)
        return result
    # DBTYPE TABLE

    def dbtype(self, **kwargs):
        if kwargs:
            typedb = kwargs['typedb']
            name = kwargs['name']
            url = kwargs['url']
            data_list = kwargs['data_list']
        instance = self.session.query(DBType).filter_by(name=name).first()
        if instance:
            self.logger.info("DBType existe, %s" % instance)
            return instance
        else:
            instance = DBType(
                typedb=typedb,
                name=name,
                url=url,
                data_list=data_list)
            self.create_dbtype(instance)
            self.logger.info("DBType creada, %s" % instance)
            return instance

    def create_dbtype(self, dbtype):
        self.session.add(dbtype)
        self.session.commit()

    def update_dbtype(self, instance, fields, values):
        t_name = 'dbtype'
        assert len(fields) == len(values)
        for f in fields:
            v = values[fields.index(f)]
            self.update_table(t_name, instance, f, v)

    def delete_dbtype(self, dbtype):
        self.session.delete(dbtype)
        self.session.flush()

    def get_dbtype(self):
        return self.get_list(DBType)

    def get_dbtype_id(self, name):
        # code is a unique value
        u = self.session.query(DBType).filter_by(name=name).all()
        if len(u) > 0:
            return u[0]
        else:
            return None

    def get_dbtype_by_id(self, db_id):
        # code is a unique value
        u = self.session.query(DBType).filter_by(id=db_id).all()
        if len(u) > 0:
            return u[0]
        else:
            return None

    def get_dbtype_list_by_type(self, dtype):
        # code is a unique value
        u = self.session.query(DBData).filter_by(typedb=dtype).all()
        return u

    # DataDestiniy section


class SessionDataWork(SessionCollector):

    def datadestiniy(self, **kwargs):
        if bool(kwargs):
            station = kwargs['station']
            destiny = kwargs['destiny']
            uri = kwargs['uri']
            port = kwargs['port']
            description = kwargs['description']
        instance = self.session.query(DataDestiny).filter_by(
            station_id=station_id,
            destiny=destiny,
            uri=uri).first()
        if instance:
            return instance
        else:
            sta_id = self.get_station_id(station)
            if sta_id:
                instance = DataDestiny(
                    station_id=sta_id,
                    destiny=destiny,
                    uri=uri,
                    port=port,
                    description=description
                )
                self.create_datadestiny(instance)
                return instance
            else:
                return None

    def create_datadestiny(self, datadestiny):
        self.session.add(datadestiny)
        self.session.commit()

    def update_datadestiny(self, instance, fields, values):
        t_name = 'datadestiny'
        assert len(fields) == len(values)
        for f in fields:
            v = values[fields.index(f)]
            self.update_table(t_name, instance, f, v, **{'schema': 'datawork'})

    def delete_datadestiny(self, datadestiny):
        self.session.delete(datadestiny)
        self.session.flush()

    def get_datadestiny(self):
        return self.get_list(DataDestiny)

    def get_datadestiny_id(self, name):
        # code is a unique value
        u = self.session.query(DataDestiny).filter_by(
            station_id=station_id,
            destiny=destiny,
            uri=uri).all()
        if len(u) > 0:
            return u[0]
        else:
            return None

    def get_datadestiny_by_id(self, db_id):
        # code is a unique value
        u = self.session.query(DataDestiny).filter_by(id=db_id).all()
        if len(u) > 0:
            return u[0]
        else:
            return None

    def get_dbtype_list_by_type(self, destiny_type):
        # code is a unique value
        u = self.session.query(DataDestiny).filter_by(
            destiny=destiny_type).all()
        return u

    def get_destiny_by_station(self, station):
        sta_id = self.get_station_id(station)
        u = self.session.query(DataDestiny).filter_by(station_id=sta_id).all()
        return u
