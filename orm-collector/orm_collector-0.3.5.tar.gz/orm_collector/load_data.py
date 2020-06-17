from networktools.library import check_type
from orm_collector import SessionCollector
from pathlib import Path
import csv

def load_protocol(session, file_protocol):
     this_protocol = dict()
     with open(file_protocol, 'r') as rfile:
         reader = csv.DictReader(rfile, delimiter=';', quoting=csv.QUOTE_NONE)
         for row in reader:
             print(row)
             for k in row.keys():
                 row[k] = row[k].rstrip().lstrip()
             p = row['name']
             if not session.get_protocol_id(p) and p != '':
                 this_protocol[int(row['id'])] = session.protocol(**row)
     print("Protocol ok")
                 

def load_dbtype(session, file_dbtype):
    this_dbtype = dict()
    with open(file_dbtype, 'r') as rfile:
        reader = csv.DictReader(rfile, delimiter=';', quoting=csv.QUOTE_NONE)
        for row in reader:
            for k in row.keys():
                row[k] = row[k].rstrip().lstrip()
            print(row)
            p = row['name']
            if not session.get_dbtype_id(p) and p != '':
                this_dbtype[int(row['id'])] = session.dbtype(**row)
    print("DBType ok")

def load_dbdata(session, file_dbdata):
    this_dbdata = dict()

    with open(file_dbdata, 'r') as rfile:
        reader = csv.DictReader(rfile, delimiter=';', quoting=csv.QUOTE_NONE)
        for row in reader:
            for k in row.keys():
                row[k] = row[k].rstrip().lstrip()
            if not row['port'].isdigit():
                row['port'] = 0
            p = row['code']
            path = row['path']
            if path == '':
                row['path'] = None
            if not session.get_dbdata_id(p) and p != '':
                print("Saving->", row)
                this_dbdata[int(row['id'])] = session.dbdata(**row)
                print("Saved dbdata", this_dbdata[int(row['id'])])


def load_server(session, file_server):
    this_server = dict()

    with open(file_server, 'r') as rfile:
        reader = csv.DictReader(rfile, delimiter=';', quoting=csv.QUOTE_NONE)
        for row in reader:
            print(row)
            for k in row.keys():
                row[k] = row[k].rstrip().lstrip()
            hostname = row['host_name']
            row["gnsocket"] = check_type(row.get('gnsocket', 0), 'int')
            row["activated"] = check_type(row.get("activated"))
            if not session.get_protocol_id(hostname):
                this_server[int(row['id'])] = session.server(**row)

    print("This server->", this_server)
    [print(server.host_name) for server in this_server.values()]


def load_network(session, file_network):
    this_network = dict()
    with open(file_network, 'r') as rfile:
        reader = csv.DictReader(rfile, delimiter=';', quoting=csv.QUOTE_NONE)
        for row in reader:
            print(row)
            for k in row.keys():
                row[k] = row[k].rstrip().lstrip()
            this_network[int(row['id'])] = session.network(**row)
    print("This network->", this_network)
    [print(network) for network in this_network.values()]

    
def load_station(session, file_station):
    this_station = dict()

    print("Server Instances ok")

    with open(file_station, 'r') as rfile:
        reader = csv.DictReader(rfile, delimiter=';', quoting=csv.QUOTE_NONE)
        for row in reader:
            print(row)
            for k in row.keys():
                row[k] = row[k].rstrip().lstrip()
            port = row.get('port', 0)
            iport = row.get('interface_port', 0)
            p = row['code']
            if not session.get_station_id(p) and p != '':
                station_data = dict(
                    id=check_type(row.get('id'), 'int'),
                    code=row['code'],
                    name=row['name'],
                    ECEF_X=row['ECEF_X'],
                    ECEF_Y=row['ECEF_Y'],
                    ECEF_Z=row['ECEF_Z'],
                    host=row['host'],
                    port=check_type(port, 'int'),
                    interface_port=check_type(iport, 'int'),
                    db=row['db'],
                    protocol=row['protocol'],
                    protocol_host=row["protocol_host"],
                    active=check_type(row.get("active", 0)),
                    server_id=check_type(row.get('server_id', 0), 'int'),
                    network_id=row["network_id"]
                )
                this_station[int(row['id'])] = session.station(**station_data)

    print("Station ok")



if __name__=='__main__':
    pwd = Path(__file__).parent
    file_protocol = pwd/"fixtures/protocol.csv"
    file_dbdata = pwd/"fixtures/dbdata.csv"
    file_dbtype = pwd/"fixtures/dbtype.csv"
    file_server = pwd/"fixtures/server.csv"
    file_network = pwd/"fixtures/network.csv"
    file_station = pwd/"fixtures/station.csv"
    session = SessionCollector()
    load_protocol(session, file_protocol)
    load_dbdata(session, file_dbdata)
    load_dbtype(session, file_dbtype)
    load_server(session, file_server)
    load_network(session, file_network)
    load_station(session, file_station)

