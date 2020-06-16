import pickle
import argparse
import sys
import os

import numpy as np
import pandas as pd
import sqlalchemy as sa

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.automap import classname_for_table
from sqlalchemy import Column, Integer, String, Date, Float
from sqlalchemy import create_engine, exists
from sqlalchemy.sql import select, literal_column
from sqlalchemy.orm import sessionmaker
from sqlalchemy import inspect

try:
    from . import su_trace
except Exception:
    import su_trace

"""
Connexion to the postgreSQL database called : affiliere
port : 5432 #default port (may be 5433)
user : flux_user or affiliere_user
pass : steep2019 (flux) or steep2017 (aff)
"""


################################
### model of database tables ###
################################

# modeling the table
affiliere = declarative_base() #inherit Base (simplify database table definitions)

#Define table structure inside our database
#### The database named ProtoBDD has to exist in the PostgreSQL server ###
class ResultList(affiliere):
    __tablename__ = 'ResultLists'
    id = Column(Integer, primary_key=True)
    id_int = Column(Integer)
    model_name = Column(String)
    region = Column(String)
    table = Column(String)
    produit = Column(String)
    secteur = Column(String)
    origine = Column(String)
    destination = Column(String)
    valeur_in = Column(Float)
    sigma_in = Column(Float)
    sigma_in_p = Column(Float)
    min_in = Column(Float)
    max_in = Column(Float)
    valeur_out = Column(Float)
    nb_sigmas = Column(Float)
    Ai = Column(String)
    free_min_Ai = Column(Integer)
    free_max_Ai = Column(Integer)
    rref_python1_classif = Column(String)
    MC_mu_in = Column(Integer)
    MC_std_in = Column(Integer)
    MC_mu = Column(Integer)
    MC_std = Column(Integer)
    MC_min = Column(Integer)
    MC_max = Column(Integer)
    MC_p0 = Column(Integer)
    MC_p5 = Column(Integer)
    MC_p10 = Column(Integer)
    MC_p20 = Column(Integer)
    MC_p30 = Column(Integer)
    MC_p40 = Column(Integer)
    MC_p50 = Column(Integer)
    MC_p60 = Column(Integer)
    MC_p70 = Column(Integer)
    MC_p80 = Column(Integer)
    MC_p90 = Column(Integer)
    MC_p95 = Column(Integer)
    MC_p100 = Column(Integer)
    MC_hist0 = Column(Integer)
    MC_hist1 = Column(Integer)
    MC_hist2 = Column(Integer)
    MC_hist3 = Column(Integer)
    MC_hist4 = Column(Integer)
    MC_hist5 = Column(Integer)
    MC_hist6 = Column(Integer)
    MC_hist7 = Column(Integer)
    MC_hist8 = Column(Integer)
    MC_hist9 = Column(Integer)

    #def __repr__(self): #To print personal output when controling table contents
    #    return "<ProtoBDD(product='{}', sector='{}', origin='{}', dest='{}', date='{}')>"\
    #        .format(self.product, self.sector, self.reg_origin, self.reg_destin, self.reccord_date)

class Data(affiliere):
    __tablename__ = "Datas"
    id = Column(Integer, primary_key=True)
    model_name = Column(String)
    Periode = Column(String)
    Region = Column(String)
    Table = Column(String)
    Origine = Column(String)
    Destination = Column(String)
    Valeur = Column(Float)
    Incertitude_p = Column(Float)
    Contrainte_Sym_p = Column(Float)
    Quantity = Column(Float)
    Unit = Column(String)
    Factor = Column(Float)
    Source = Column(String)

class MinMax(affiliere):
    __tablename__ = "MinMaxs"
    id = Column(Integer, primary_key=True)
    model_name = Column(String)
    Periode = Column(String)
    Region = Column(String)
    Table = Column(String)
    Origine = Column(String)
    Destination = Column(String)
    Min = Column(Float)
    Max = Column(Float)
    Min_Unit = Column(String)
    Max_Unit = Column(String)
    Unit = Column(String)
    Factor = Column(Float)
    Source = Column(String)

class Geographic(affiliere):
    __tablename__ = "Geographics"
    id = Column(Integer, primary_key=True)
    model_name = Column(String)
    id_int = Column(String)
    geotype = Column(Integer)
    Code_Insee = Column(String)
    Nom = Column(String)
    Code_Parents = Column(String)
    Code_Enfants = Column(String)
     
class Proxy(affiliere):
    __tablename__ = "Proxys"
    id = Column(Integer, primary_key=True)
    model_name = Column(String)
    Proxy_name = Column(String)
    Code_geo = Column(String)
    Geographic = Column(String)
    Percent = Column(Float)
    Quantity = Column(Float)
    Source = Column(String)

class Proxytype(affiliere):
    __tablename__ = "Proxytypes"
    id = Column(Integer, primary_key=True)
    model_name = Column(String)
    Proxy_name = Column(String)
    Type = Column(String)
    Sector = Column(String)
    TableER = Column(String)
    Origin = Column(String)
    Destination = Column(String)

class Product(affiliere):
    __tablename__ = "Products"
    id = Column(Integer, primary_key=True)
    model_name = Column(String)
    Level = Column(Integer)
    Prod_name = Column(String)
    Bilan = Column(Integer)
    Transport = Column(Integer)
    Poids_conso = Column(Integer)
    Table_conso = Column(Integer)
    Sankey = Column(Integer)

class Sector(affiliere):
    __tablename__ = "Sectors"
    id = Column(Integer, primary_key=True)
    model_name = Column(String)
    Level = Column(Integer)
    Sect_name = Column(String)
    Bilan = Column(Integer)
    Transport = Column(Integer)
    Poids_conso = Column(Integer)
    Table_conso = Column(Integer)
    Sankey = Column(Integer)

class Flux(affiliere):
    __tablename__ = "Fluxs"
    id = Column(Integer, primary_key=True)
    model_name = Column(String)
    Table = Column(String)
    Origine = Column(String)
    Destination = Column(String)
    Valeur = Column(Integer)

class Constraint(affiliere):
    __tablename__ = "Constraints"
    id = Column(Integer, primary_key=True)
    model_name = Column(String)
    id_interne = Column(Integer)
    Periode = Column(String)
    Region = Column(String)
    Table = Column(String)
    Origine = Column(String)
    Destination = Column(String)
    Equality = Column(Float)
    Eq_lower = Column(Float)
    Eq_upper = Column(Float)
    Coef_inv = Column(Float)
    Coefficient = Column(Float)

class Param(affiliere):
    __tablename__ = "Params"
    id = Column(Integer, primary_key=True)
    model_name = Column(String)
    Parametre = Column(String)
    Valeur = Column(String)
    Description = Column(String)


def check_db(pgadm, pgadmpass, pghost, pgport, pguser, pgpass, pgdb):
    #Access generic database as generic super user
    DB_URI = f'postgresql://{pgadm}:{pgadmpass}@{pghost}:{pgport}/postgres'
    engi = create_engine(DB_URI)
    try:
        conn = engi.connect()
    except BaseException as exc:
        su_trace.logger.error(exc)
        return False
    conn.execute("commit")
    try:
        susercreate = f'create user {pguser} with password \'{pgpass}\''
        conn.execute(susercreate)
    except Exception as exc:
        #if pgcode = 42710 this user already exists
        if exc.orig.pgcode != '42710': # pylint: disable=maybe-no-member
            su_trace.logger.error(exc)
            return False
    conn.execute("commit")
    try:
        sdbcreate = f"create database {pgdb} with owner = {pguser}"
        conn.execute(sdbcreate)
    except Exception as exc:
        #if pgcode = 42P04 this database already exists
        if exc.orig.pgcode != '42P04': # pylint: disable=maybe-no-member
            su_trace.logger.error(exc)
            return False
    conn.execute("commit")
    conn.close()
    return True

def connect_aff(db_type):
    #Establishing the connection to PostgreSQL
    #Note : the connection information can be retrieved by using psycopg2
    #Scheme: "postgres+psycopg2://<USERNAME>:<PASSWORD>@<IP_ADDRESS>:<PORT>/<DATABASE_NAME>"
    #DATABASE_URI = 'postgres+psycopg2://flux_user:steep2019@localhost:5432/ProtoBDD'
    if not (db_type in [0, 1]): #db_type == 99
        #Working without database
        return sessionmaker()
    if db_type == 0: #Developpement mode
        #Dev database URI
        suser = 'flux_user'
        spass = 'steep2019'
        sserv = 'localhost'
        sport = '5432'
        sdb = 'affiliere'
        #DATABASE_URI = 'postgresql://flux_user:steep2019@localhost/affiliere'
    if db_type == 1: #Production mode
        #Prod database URI
        suser = 'affiliere_user'
        spass = 'steep2017'
        sserv = 'greel-761.postgres.pythonanywhere-services.com'
        sport = '10761'
        sdb = 'affiliere'
        #DATABASE_URI = 'postgresql://affiliere_user:steep2017@greel-761.postgres.\
        #    pythonanywhere-services.com:10761/affiliere'
    #if check_db('postgres', 'postgres', sserv, sport, 'pipo', 'pipopass', 'test'):
    if check_db('postgres', 'postgres', sserv, sport, suser, spass, sdb):
        DATABASE_URI = f'postgresql://{suser}:{spass}@{sserv}:{sport}/{sdb}'
        #DATABASE_URI = f'postgresql://pipo:pipopass@localhost:5432/test'
        engine = create_engine(DATABASE_URI)
        #Creating and openning a session
        session = sessionmaker()
        session.configure(bind=engine)
        sess = session()
        #Creation of the table
        affiliere.metadata.create_all(engine)
        #return session openned
        return sess
    else:
        su_trace.logger.error('Problème d\'acces ou de connection à la base de donnée : \
tentative d\'exécution du programme sans bdd.')
        return sessionmaker()

def get_class_by_tablename(base, tablename):
    """Return class reference mapped to table.
    :param tablename: String with name of table.
    :return: Class reference or None.
    """
    for _class in base._decl_class_registry.values():
        if hasattr( _class, '__tablename__') and  _class  .__tablename__ == tablename:
            return  _class
    return None

def table_list():
    return affiliere.metadata.tables.keys()

def check_table_exist(myobject):
    li_ta = table_list()
    resu = any(myobject == val for val in li_ta)
    return resu

def check_rec_exist(act_ses,tabname,colname,myval):
    res = False
    resu = act_ses.query(tabname).filter(tabname.colname == myval).first()
    if resu != None:
        res = True
    return res

def clean_mod(tab_mod, mod_nam, act_ses, col_clean = '', val_clean = ['']):
    #Cleaning database is required before copying new data
    resu = None
    li_col = [col.key for col in tab_mod.__table__.columns]
    if ((col_clean != '') and not (col_clean in li_col)):
        su_trace.logger.critical(f'Column {col_clean} is not in table {tab_mod} ' + str(li_col))
        sys.exit()
    if col_clean != '':
        resu = act_ses.query(tab_mod).filter(tab_mod.model_name == mod_nam, \
            getattr(tab_mod, col_clean).in_(val_clean)).first()
    else:
        resu = act_ses.query(tab_mod).filter(tab_mod.model_name == mod_nam).first()
    if resu != None:
        #need to clean the table
        if col_clean != '':
            resdel = tab_mod.__table__.delete().where((tab_mod.model_name == mod_nam) and \
                (getattr(tab_mod, col_clean).in_(val_clean)))
        else:
            resdel = tab_mod.__table__.delete().where(tab_mod.model_name == mod_nam)        
        act_ses.execute(resdel)
        act_ses.commit()

def save_results(file_dat, active_ses, bdd_clean_mode, modname, downscale):
    if bdd_clean_mode == 1:
        #Cleaning database is required before copying new data
        clean_mod(ResultList, modname, active_ses)
    #Get data from .dat file
    with open(file_dat, 'rb') as fi:
        scmfa = pickle.load(fi)
    #Select appropriate subset of data
    savmfa = scmfa.mfa
    savlsys = scmfa.lin_sys

    qres = None
    if bdd_clean_mode in [2, 3]:
        qres = active_ses.query(ResultList).filter(ResultList.model_name == modname)
    #Filling ResultList table
    for i in range(savmfa.size):
        name = savmfa.name_of(i)
        qfind = False
        qmodif = False
        #if ((bdd_clean in [2, 3]) and (len(resu) > 0)):
        if ((qres != None) and (qres.first() != None)): #Means bdd_clean is in [2, 3]
            litest = ['U','E','u','e']
            if name['t'] not in litest:
                litest = ['S','R','s','r']
            for qresin in qres:
                regtest = True
                if downscale:
                    if qresin.region != name['r']:
                        regtest = False
                if ((qresin.id_int == i) and (regtest == True) and \
                        (qresin.table in litest) and (qresin.produit in name['p']) and \
                        (qresin.secteur == name['s']) and (qresin.origine == name['o']) and \
                        (qresin.destination == name['d'])):
                    #This reccord already exists in the db
                    qfind = True
                    if (qresin.valeur_out != scmfa.solved_vector[i]):
                        #The value of this reccord has changed
                        qmodif = True
                    break
            if qfind == True:
                if ((bdd_clean_mode == 2) or (qmodif == False)):
                    #Not necessary to go further in these cases
                    continue
        if qmodif == True:
            #Modify existing reccord
            res = qresin
        else:
            #Add a new reccord
            res = ResultList()
        res.model_name = modname
        res.id_int = i
        name = savmfa.name_of(i)
        if downscale:
            res.region = name['r']
        res.table = name['t']
        res.produit = name['p']
        res.secteur = name['s']
        res.origine = name['o']
        res.destination = name['d']
        if savmfa.measured[i]:
            res.valeur_in = savmfa.vector[i]
            res.sigma_in = savmfa.sigmas[i]
            res.sigma_in_p = 2*savmfa.sigmas[i]/savmfa.vector[i]
            #From write_out routine
            delta = scmfa.solved_vector[i] - savmfa.vector[i]
            res.nb_sigmas = delta / savmfa.sigmas[i]
            #From montecarlo_result routine
            res.MC_mu_in = round(scmfa.mc_result['measured']['mu in'][i])
            res.MC_std_in = round(scmfa.mc_result['measured']['std in'][i])
        if savmfa.cons['lb'][i] > 0:
            res.min_in = savmfa.cons['lb'][i]
        if savmfa.cons['ub'][i] != savmfa.max:
            res.max_in = savmfa.cons['ub'][i]
        #From write_out routine
        res.valeur_out = scmfa.solved_vector[i]
        res.rref_python1_classif = savlsys.vars_type[i]
        for v in {'Ai': savlsys.vars_occ_Ai}.values():
            constraints = ''
            if i in v.keys():
                for j in v[i].keys():
                    constraints += str(j) + ' - '
            res.Ai = constraints
        #if i in savlsys.vars_type_dict[savmfa.main_classif]['free vars']:
        if i in savlsys.vars_type_dict['free vars']:
            for m in ['Ai']:
                res.free_min_Ai = round(savlsys.intervals[m][i][0])
                res.free_max_Ai = round(savlsys.intervals[m][i][1])
        #From montecarlo_result routine
        res.MC_mu = round(scmfa.mc_result['determinable']['mu'][i])
        res.MC_std = round(scmfa.mc_result['determinable']['std'][i])
        if i in savlsys.vars_type_dict['free vars']:
            classi = 'free'
            le_min, le_max = round(scmfa.mc_result['free'][5][i]), \
                round(scmfa.mc_result['free'][95][i])
        else:
            classi = 'determinable'
            le_min, le_max = round(scmfa.mc_result['determinable'][2.5][i]), \
                round(scmfa.mc_result['determinable'][97.5][i])
        res.MC_p0 = round(scmfa.mc_result[classi][0][i])
        res.MC_p5 = round(scmfa.mc_result[classi][5][i])
        res.MC_p10 = round(scmfa.mc_result[classi][10][i])
        res.MC_p20 = round(scmfa.mc_result[classi][20][i])
        res.MC_p30 = round(scmfa.mc_result[classi][30][i])
        res.MC_p40 = round(scmfa.mc_result[classi][40][i])
        res.MC_p50 = round(scmfa.mc_result[classi][50][i])
        res.MC_p60 = round(scmfa.mc_result[classi][60][i])
        res.MC_p70 = round(scmfa.mc_result[classi][70][i])
        res.MC_p80 = round(scmfa.mc_result[classi][80][i])
        res.MC_p90 = round(scmfa.mc_result[classi][90][i])
        res.MC_p95 = round(scmfa.mc_result[classi][95][i])
        res.MC_p100 = round(scmfa.mc_result[classi][100][i])            
        res.MC_hist0 = int(round(scmfa.mc_result[classi]['hist'][i][0][0]))
        res.MC_hist1 = int(round(scmfa.mc_result[classi]['hist'][i][0][1]))
        res.MC_hist2 = int(round(scmfa.mc_result[classi]['hist'][i][0][2]))
        res.MC_hist3 = int(round(scmfa.mc_result[classi]['hist'][i][0][3]))
        res.MC_hist4 = int(round(scmfa.mc_result[classi]['hist'][i][0][4]))
        res.MC_hist5 = int(round(scmfa.mc_result[classi]['hist'][i][0][5]))
        res.MC_hist6 = int(round(scmfa.mc_result[classi]['hist'][i][0][6]))
        res.MC_hist7 = int(round(scmfa.mc_result[classi]['hist'][i][0][7]))
        res.MC_hist8 = int(round(scmfa.mc_result[classi]['hist'][i][0][8]))
        res.MC_hist9 = int(round(scmfa.mc_result[classi]['hist'][i][0][9]))
        res.MC_min = le_min
        res.MC_max = le_max
        if qmodif == False:
            active_ses.add(res)
    active_ses.commit()

def save_input_param(mydat, act_ses, bdd_clean, modna):
    if bdd_clean == 1:
        #Cleaning database is required before copying new data
        clean_mod(Param, modna, act_ses)
    qres = None
    if bdd_clean in [2, 3]:
        qres = act_ses.query(Param).filter(Param.model_name == modna)
    # Initialisation (move to the right record)
    for ssli in mydat:
        if len(ssli) > 0:
            qfind = False
            qmodif = False
            if ((qres != None) and (qres.first() != None)): #bdd_clean is in [2, 3]
                for qresin in qres:
                    if qresin.Parametre == ssli[0]:
                        qfind = True #This reccord already exists in the db
                        if qresin.Valeur != ssli[1]:
                            qmodif = True #The value of this reccord has changed
                            break
                if qfind == True:
                    if ((bdd_clean == 2) or (qmodif == False)):
                        continue #Not necessary to go further in these cases
            if qmodif == True:                
                res = qresin #Modify existing reccord
            else:
                res = Param() #Add a new reccord
            #Filling Param table
            res.model_name = modna
            res.Parametre = ssli[0]
            res.Valeur = ssli[1]
            res.Description = ssli[2]
            #Add new reccord if needed
            if qmodif == False:
                act_ses.add(res)
    act_ses.commit()
    
def save_input_product(mydat, act_ses, bdd_clean, modna):
    if bdd_clean == 1:
        #Cleaning database is required before copying new data
        clean_mod(Product, modna, act_ses)
    qres = None
    if bdd_clean in [2, 3]:
        qres = act_ses.query(Product).filter(Product.model_name == modna)
    # Initialisation (move to the right record)
    for ssli in mydat:
        if len(ssli) > 0:
            qfind = False
            qmodif = False
            if ((qres != None) and (qres.first() != None)): #bdd_clean is in [2, 3]
                litest = ['U','E','u','e']
                if ssli[5] not in litest:
                    litest = ['S','R','s','r']
                for qresin in qres:
                    if qresin.Prod_name == ssli[1]:
                        qfind = True #This reccord already exists in the db
                        if ((qresin.Level != ssli[0]) or (qresin.Bilan != ssli[2]) or 
                                (qresin.Transport != ssli[3]) or 
                                (qresin.Poids_conso != ssli[4]) or
                                (qresin.Table_conso in litest) or 
                                (qresin.Sankey != ssli[6])):
                            qmodif = True #The value of this reccord has changed
                            break
                if qfind == True:
                    if ((bdd_clean == 2) or (qmodif == False)):
                        continue #Not necessary to go further in these cases
            if qmodif == True:                
                res = qresin #Modify existing reccord
            else:
                res = Product() #Add a new reccord
            #Filling Param table
            res.model_name = modna
            res.Level = ssli[0]
            res.Prod_name = ssli[1]
            res.Bilan = ssli[2]
            res.Transport = ssli[3]
            res.Poids_conso = ssli[4]
            res.Table_conso = ssli[5]
            res.Sankey = ssli[6]
            #Add new reccord if needed
            if qmodif == False:
                act_ses.add(res)
    act_ses.commit()

def save_input_sector(mydat, act_ses, bdd_clean, modna):
    if bdd_clean == 1:
        #Cleaning database is required before copying new data
        clean_mod(Sector, modna, act_ses)
    qres = None
    if bdd_clean in [2, 3]:
        qres = act_ses.query(Sector).filter(Sector.model_name == modna)
    # Initialisation (move to the right record)
    for ssli in mydat:
        if len(ssli) > 0:
            qfind = False
            qmodif = False
            if ((qres != None) and (qres.first() != None)): #bdd_clean is in [2, 3]
                litest = ['U','E','u','e']
                if ssli[5] not in litest:
                    litest = ['S','R','s','r']
                for qresin in qres:
                    if qresin.Sect_name == ssli[1]:
                        qfind = True #This reccord already exists in the db
                        if ((qresin.Level != ssli[0]) or (qresin.Bilan != ssli[2]) or 
                                (qresin.Transport != ssli[3]) or 
                                (qresin.Poids_conso != ssli[4]) or
                                (qresin.Table_conso in litest) or 
                                (qresin.Sankey != ssli[6])):
                            qmodif = True #The value of this reccord has changed
                            break
                if qfind == True:
                    if ((bdd_clean == 2) or (qmodif == False)):
                        continue #Not necessary to go further in these cases
            if qmodif == True:                
                res = qresin #Modify existing reccord
            else:
                res = Sector() #Add a new reccord
            #Filling Param table
            res.model_name = modna
            res.Level = ssli[0]
            res.Sect_name = ssli[1]
            res.Bilan = ssli[2]
            res.Transport = ssli[3]
            res.Poids_conso = ssli[4]
            res.Table_conso = ssli[5]
            res.Sankey = ssli[6]
            #Add new reccord if needed
            if qmodif == False:
                act_ses.add(res)
    act_ses.commit()

def save_input_flux(mydat, act_ses, bdd_clean, modna):
    if bdd_clean == 1:
        #Cleaning database is required before copying new data
        clean_mod(Flux, modna, act_ses)
    qres = None
    if bdd_clean in [2, 3]:
        qres = act_ses.query(Flux).filter(Flux.model_name == modna)
    # Initialisation (move to the right record)
    for ssli in mydat:
        if len(ssli) > 0:
            qfind = False
            qmodif = False
            if ((qres != None) and (qres.first() != None)): #bdd_clean is in [2, 3]
                litest = ['U','E','u','e']
                if ssli[0] not in litest:
                    litest = ['S','R','s','r']
                for qresin in qres:
                    if ((qresin.Table in litest) and (qresin.Origine == ssli[1]) and
                            (qresin.Destination == ssli[2])):
                        qfind = True #This reccord already exists in the db
                        if qresin.Valeur != ssli[3]:
                            qmodif = True #The value of this reccord has changed
                            break
                if qfind == True:
                    if ((bdd_clean == 2) or (qmodif == False)):
                        continue #Not necessary to go further in these cases
            if qmodif == True:                
                res = qresin #Modify existing reccord
            else:
                res = Flux() #Add a new reccord
            #Filling Param table
            res.model_name = modna
            res.Table = ssli[0]
            res.Origine = ssli[1]
            res.Destination = ssli[2]
            res.Valeur = ssli[3]
            #Add new reccord if needed
            if qmodif == False:
                act_ses.add(res)
    act_ses.commit()

def save_inputs_data(mydat, act_ses, bdd_clean, modna):
    if (bdd_clean == 1):
        #Cleaning database is required before copying new data
        clean_mod(Data, modna, act_ses)
    qres = None
    if bdd_clean in [2, 3]:
        qres = act_ses.query(Data).filter(Data.model_name == modna)
    #Filling Data table
    for ssli in mydat:
        if len(ssli) > 0:
            qfind = False
            qmodif = False
            #if ((bdd_clean in [2, 3]) and (len(resu) > 0)):
            if ((qres != None) and (qres.first() != None)): #Means bdd_clean is in [2, 3]
                litest = ['U','E','u','e']
                if ssli[2] not in litest:
                    litest = ['S','R','s','r']
                for qresin in qres:
                    if ((qresin.Periode == ssli[0]) and \
                            (qresin.Region == ssli[1]) and (qresin.Table in litest) and \
                            (qresin.Origine == ssli[3]) and (qresin.Destination == ssli[4])):
                        #This reccord already exists in the db
                        qfind = True
                        if qresin.Valeur != ssli[5]:
                            #The value of this reccord has changed
                            qmodif = True
                        break
                if qfind == True:
                    if ((bdd_clean == 2) or (qmodif == False)):
                        #Not necessary to go further in these cases
                        continue
            if qmodif == True:
                #Modify existing reccord
                res = qresin
            else:
                #Add a new reccord
                res = Data()
            res.model_name = modna
            res.Periode = ssli[0]
            res.Region = ssli[1]
            res.Table = ssli[2]
            res.Origine = ssli[3]
            res.Destination = ssli[4]
            res.Valeur = None
            if ssli[5] not in ['', None]:
                res.Valeur = float(ssli[5])
            res.Incertitude_p = None
            if ssli[6] not in ['', None]:
                res.Incertitude_p = float(ssli[6])
            if ssli[7] not in ['', None]:
                res.Contrainte_Sym_p = float(ssli[7])
            res.Quantity = None
            if ssli[8] not in ['', None]:
                res.Quantity = float(ssli[8])
            res.Unit = ssli[9]
            res.Factor = None
            if ssli[10] not in ['', None]:
                res.Factor = float(ssli[10])
            res.Source = ssli[11]
            if qmodif == False:
                act_ses.add(res)
    act_ses.commit()

def save_inputs_mima(mydat, act_ses, bdd_clean, modna):
    if bdd_clean == 1:
        #Cleaning database is required before copying new data
        clean_mod(MinMax, modna, act_ses)
    qres = None
    if bdd_clean in [2, 3]:
        qres = act_ses.query(MinMax).filter(MinMax.model_name == modna)
    #Filling MinMax table
    for ssli in mydat:
        if len(ssli) > 0:
            qfind = False
            qmodif = False
            #if ((bdd_clean in [2, 3]) and (len(resu) > 0)):
            if ((qres != None) and (qres.first() != None)): #Means bdd_clean is in [2, 3]
                litest = ['U','E','u','e']
                if ssli[2] not in litest:
                    litest = ['S','R','s','r']
                for qresin in qres:
                    if ((qresin.Periode == ssli[0]) and \
                            (qresin.Region == ssli[1]) and (qresin.Table in litest) and \
                            (qresin.Origine == ssli[3]) and (qresin.Destination == ssli[4])):
                        #This reccord already exists in the db
                        qfind = True
                        if ((qresin.Min != ssli[5]) or (qresin.Max != ssli[6])):
                            #The value of this reccord has changed
                            qmodif = True
                        break
                if qfind == True:
                    if ((bdd_clean == 2) or (qmodif == False)):
                        #Not necessary to go further in these cases
                        continue
            if qmodif == True:
                #Modify existing reccord
                res = qresin
            else:
                #Add a new reccord
                res = MinMax()
            res.model_name = modna
            res.Periode = ssli[0]
            res.Region = ssli[1]
            res.Table = ssli[2]
            res.Origine = ssli[3]
            res.Destination = ssli[4]
            res.Min = float(ssli[5])
            res.Max = float(ssli[6])
            res.Min_Unit = ssli[7]
            res.Max_Unit = ssli[8]
            res.Unit = ssli[9]
            res.Factor = float(ssli[10])
            res.Source = ssli[11]
            if qmodif == False:
                act_ses.add(res)
    act_ses.commit()

def save_input_constraint(mydat, act_ses, bdd_clean, modna):
    if bdd_clean == 1:
        #Cleaning database is required before copying new data
        clean_mod(Constraint, modna, act_ses)
    qres = None
    if bdd_clean in [2, 3]:
        qres = act_ses.query(Constraint).filter(Constraint.model_name == modna)
    # Initialisation (move to the right record)
    for ssli in mydat:
        if len(ssli) > 0:
            qfind = False
            qmodif = False
            if ((qres != None) and (qres.first() != None)): #bdd_clean is in [2, 3]
                litest = ['U','E','u','e']
                if ssli[3] not in litest:
                    litest = ['S','R','s','r']
                for qresin in qres:
                    if ((qresin.id_interne == ssli[0]) and (qresin.Periode == ssli[1]) and
                            (qresin.Region == ssli[2]) and (qresin.Table in litest) and
                            (qresin.Origine == ssli[4]) and (qresin.Destination == ssli[5])):
                        qfind = True #This reccord already exists in the db
                        if ((qresin.Equality != ssli[6]) or (qresin.Eq_lower != ssli[7]) or
                                (qresin.Eq_upper != ssli[8]) or (qresin.Coef_inv != ssli[9])
                                or (qresin.Coefficient != ssli[10])):
                            qmodif = True #The value of this reccord has changed
                            break
                if qfind == True:
                    if ((bdd_clean == 2) or (qmodif == False)):
                        continue #Not necessary to go further in these cases
            if qmodif == True:                
                res = qresin #Modify existing reccord
            else:
                res = Constraint() #Add a new reccord
            #Filling Param table
            res.model_name = modna
            res.id_interne = ssli[0]
            res.Periode = ssli[1]
            res.Region = ssli[2]
            res.Table = ssli[3]
            res.Origine = ssli[4]
            res.Destination = ssli[5]
            res.Equality = ssli[6]
            res.Eq_lower = ssli[7]
            res.Eq_upper = ssli[8]
            res.Coef_inv = ssli[9]
            res.Coefficient = ssli[10]
            #Add new reccord if needed
            if qmodif == False:
                act_ses.add(res)
    act_ses.commit()

def save_inputs_proxy(mydat, act_ses, bdd_clean, modna, proxlist=['']):
    if bdd_clean == 1:
        #Cleaning database is required before copying new data
        clean_mod(Proxy, modna, act_ses, 'Proxy_name', proxlist)
    qres = None
    if bdd_clean in [2, 3]:
        qres = act_ses.query(Proxy).filter(Proxy.model_name == modna)
    #Filling MinMax table
    for ssli in mydat:
        if len(ssli) > 0:
            qfind = False
            qmodif = False
            #if ((bdd_clean in [2, 3]) and (len(resu) > 0)):
            if ((qres != None) and (qres.first() != None)): #Means bdd_clean is in [2, 3]
                for qresin in qres:
                    if ((qresin.Proxy_name == ssli[0]) and \
                            (qresin.Code_geo == ssli[1]) and (qresin.Geographic == ssli[2])):
                        #This reccord already exists in the db
                        qfind = True
                        if ((qresin.Percent != ssli[3]) or (qresin.Quantity != ssli[4])):
                            #The value of this reccord has changed
                            qmodif = True
                        break
                if qfind == True:
                    if ((bdd_clean == 2) or (qmodif == False)):
                        #Not necessary to go further in these cases
                        continue
            if qmodif == True:
                #Modify existing reccord
                res = qresin
            else:
                #Add a new reccord
                res = Proxy()
            res.model_name = modna
            res.Proxy_name = ssli[0]
            res.Code_geo = ssli[1]
            res.Geographic = ssli[2]
            res.Percent = float(ssli[3])
            res.Quantity = float(ssli[4])
            res.Source = ssli[5]
            if qmodif == False:
                act_ses.add(res)
    act_ses.commit()

def save_inputs_proxytype(mydat, act_ses, bdd_clean, modna):
    if bdd_clean == 1:
        #Cleaning database is required before copying new data
        clean_mod(Proxytype, modna, act_ses)
    qres = None
    if bdd_clean in [2, 3]:
        qres = act_ses.query(Proxytype).filter(Proxy.model_name == modna)
    #Filling ProxyType table
    for ssli in mydat:
        if len(ssli) > 0:
            qfind = False
            qmodif = False
            #if ((bdd_clean in [2, 3]) and (len(resu) > 0)):
            if ((qres != None) and (qres.first() != None)): #Means bdd_clean is in [2, 3]
                for qresin in qres:
                    if qresin.Type == ssli[4]:
                        if ssli[4] == 'flow':
                            if qresin.Proxy_name == ssli[3]:
                                qfind = True
                                if ((qresin.TableER != ssli[0]) or (qresin.Origin != ssli[1]) or \
                                        (qresin.Destination != ssli[2])):
                                    #The value of this reccord has changed
                                    qmodif = True
                                break
                        else: #ssli[4] == 'sector'
                            if qresin.Proxy_name == ssli[1]:
                                qfind = True
                                if (qresin.Sector != ssli[0]):
                                    #The value of this reccord has changed
                                    qmodif = True
                                break
                if qfind == True:
                    if ((bdd_clean == 2) or (qmodif == False)):
                        #Not necessary to go further in these cases
                        continue
            if qmodif == True:
                #Modify existing reccord
                res = qresin
            else:
                #Add a new reccord
                res = Proxytype()
            res.model_name = modna
            res.Type = ssli[4]
            if ssli[4] == 'flow':
                res.Proxy_name = ssli[3]
                res.Sector = ''
                res.TableER = ssli[0]
                res.Origin = ssli[1]
                res.Destination = ssli[2]
            else: #ssli[4] == 'sector'
                res.Proxy_name = ssli[1]
                res.Sector = ssli[0]
                res.TableER = ''
                res.Origin = ''
                res.Destination = ''
            if qmodif == False:
                act_ses.add(res)
    act_ses.commit()

def save_inputs_geo(mydat, act_ses, bdd_clean, modna):
    if bdd_clean == 1:
        #Cleaning database is required before copying new data
        clean_mod(Geographic, modna, act_ses)
    qres = None
    if bdd_clean in [2, 3]:
        qres = act_ses.query(Geographic).filter(Geographic.model_name == modna)
    #Filling Geographic table
    for ssli in mydat:
        if len(ssli) > 0:
            qfind = False
            qmodif = False
            #if ((bdd_clean in [2, 3]) and (len(resu) > 0)):
            if ((qres != None) and (qres.first() != None)): #Means bdd_clean is in [2, 3]
                for qresin in qres:
                    if ((qresin.id_int == ssli[0]) and (qresin.geotype == ssli[1])):
                        #This reccord already exists in the db
                        qfind = True
                        if ((qresin.Code_Insee != ssli[2]) or (qresin.Nom != ssli[3]) or \
                                (qresin.Code_Parents != ssli[4]) or \
                                (qresin.Code_Enfants != ssli[5])):
                            #The value of this reccord has changed
                            qmodif = True
                        break
                if qfind == True:
                    if ((bdd_clean == 2) or (qmodif == False)):
                        #Not necessary to go further in these cases
                        continue
            if qmodif == True:
                #Modify existing reccord
                res = qresin
            else:
                #Add a new reccord
                res = Geographic()
            res.model_name = modna
            res.id_int = ssli[0]
            res.geotype = ssli[1]
            res.Code_Insee = ssli[2]
            res.Nom = ssli[3]
            res.Code_Parents = ssli[4]
            res.Code_Enfants = ssli[5]
            if qmodif == False:
                act_ses.add(res)
    act_ses.commit()

def save_inputs(
    js_di, # output JSON dictionary
    active_ses : str,
    bdd_clean_mode : int,
    modname : str, 
    li_add=['']
):
    li_entry = ['param', 'dim_products', 'dim_sectors', 'ter_base', 'data', 
            'min_max', 'constraints', 'proxy', 'proxytype', 'geographic']
    for myent in li_entry:
        if myent in js_di.keys():
            #Filling Param table
            if myent == 'param' and len(js_di['param']) > 0:
                save_input_param(js_di['param'], active_ses, bdd_clean_mode, modname)
            #Filling Product table
            if myent == 'dim_product' and len(js_di['dim_product']) > 0:
                save_input_product(js_di['dim_product'], active_ses, bdd_clean_mode, modname)
            #Filling Sector table
            if myent == 'dim_sector' and len(js_di['dim_sector']) > 0:
                save_input_sector(js_di['dim_sector'], active_ses, bdd_clean_mode, modname)
            #Filling Flux table
            if myent == 'ter_base' and len(js_di['ter_base']) > 0:
                save_input_flux(js_di['ter_base'], active_ses, bdd_clean_mode, modname)
            #Filling Data table
            elif myent == 'data' and len(js_di['data']) > 0:
                save_inputs_data(js_di['data'], active_ses, bdd_clean_mode, modname)
            #Filling Min_Max table
            elif myent == 'min_max' and len(js_di['min_max']) > 0:
                save_inputs_mima(js_di['min_max'], active_ses, bdd_clean_mode, modname)
            #Filling Constraint table
            if myent == 'constraints' and len(js_di['constraints']) > 0:
                save_input_constraint(js_di['constraints'], active_ses, bdd_clean_mode, modname)
            #Filling Proxys table
            elif myent == 'proxy' and len(js_di['proxy']) > 0:
                save_inputs_proxy(js_di['proxy'], active_ses, bdd_clean_mode, modname, li_add)
            #Filling Proxytypes table
            elif myent == 'proxytype' and len(js_di['proxytype']) > 0:
                save_inputs_proxytype(js_di['proxytype'], active_ses, bdd_clean_mode, modname)
            #Filling geographic table
            elif myent == 'geographic' and len(js_di['geographic']) > 0:
                save_inputs_geo(js_di['geographic'], active_ses, bdd_clean_mode, modname)
            else:
                pass
    
def read_inputs(tab_name, act_ses, modname, param1, param2, col1='', col2=''):
    my_js = []
    if tab_name.__tablename__ == 'Geographics':
        resu = act_ses.query(tab_name).filter((tab_name.model_name == modname) & \
(tab_name.id_int == param1)).first()
        if resu != None:
            li_enf = [getattr(resu, col.name) for col in resu.__table__.columns if \
                col.name == 'Code_Enfants']
            li_enf = li_enf[0].split(', ')
            my_row = [getattr(resu, col.name) for col in resu.__table__.columns if \
                    col.name in ['id_int', 'Nom', 'Code_Parents']]
        else:
            su_trace.logger.critical(f'No entry with geotype {param1} was found')
            sys.exit()
        resu = act_ses.query(tab_name).filter((tab_name.model_name == modname) & \
(tab_name.geotype == param2)).all()
        if resu != None:
            my_out = []
            my_js.append(my_row) #The first line is the "parent" line
            for rs in resu:
                my_row = [getattr(rs, col.name) for col in rs.__table__.columns if \
                    col.name in ['id_int', 'Nom', 'Code_Parents']]
                li_par = my_row[2].split(', ')
                codep = my_row[0][:2]
                if codep.isdigit() and (not codep in li_par):
                    li_par.append(codep)
                    rs.Code_Parents = ', '.join(li_par)
                    act_ses.commit()
                if not set(li_par).isdisjoint(li_enf):
                    my_js.append(my_row)
                else:
                    my_out.append(my_row) #non utile pour l'instant (à virer ?)
        else:
            su_trace.logger.critical(f'No entry with geotype {param2} was found')
            sys.exit()
        resu = None
    else:
        if col2 != '':
            resu = act_ses.query(tab_name).filter((tab_name.model_name == modname) & \
(tab_name.__table__.columns[col1] == param1) & (tab_name.__table__.columns[col2] == param2))
        else:
            if col1 != '':
                resu = act_ses.query(tab_name).filter((tab_name.model_name == modname) & \
(tab_name.__table__.columns[col1] == param1))
            else:
                resu = act_ses.query(tab_name).filter(tab_name.model_name == modname).all()
    if resu != None:
        for rs in resu:
            my_row = [getattr(rs, col.name) for col in rs.__table__.columns if \
                col.name not in ['id', 'model_name']]
            my_js.append(my_row)
    return my_js

def database_proxy_to_json(
    act_ses, #session name
    model_name : str,
    main_mod_name : str,
    proxy_geo : list, #list of 2 lists
):
    proxy_input = {}
    geo_max = proxy_geo[0] # string
    geo_min = proxy_geo[1] # list of string
    # Should try if query routine in read_input can support 'in' argument instead of '==' for
    # param1 and param2 ==> could suppress following double for loop
    data_geo = []
    for geo_min in proxy_geo[1]:
        data_g = read_inputs(Geographic, act_ses, model_name, geo_max, geo_min)
        if len(data_geo) == 0:
            proxy_input['main_reg'] = data_g[0][1]
        del data_g[0]
        data_geo.extend(data_g)
    # Extraction of main region data
    data_add = np.array(read_inputs(Data, act_ses, main_mod_name, 
            proxy_input['main_reg'], '', 'Region'))
    proxy_input['years'] = [data_add[0,0]]
    proxy_input['data'] = data_add
    np_flows = np.array(read_inputs(Proxytype, act_ses, model_name, 
            'flow', '', 'Type'))
    proxy_input['proxis_flows'] = np_flows[:,[3, 4, 5, 0]]
    np_sectors = np.array(read_inputs(Proxytype, act_ses, model_name, 
            'sector', '', 'Type'))
    proxy_input['proxis_sectors'] = np_sectors[:,[2,0]]
    proxy_input['regions'] = [r[0] for r in data_geo] #using id (r[1] for the name)
    proxis = np.array(read_inputs(Proxy, act_ses, model_name, '', ''))
    proxy_input['proxis'] = proxis[:, [0, 1, 3]] #using id ([0, 2, 3] for the name)
    # build data_ps (used for proxis sectors)
    # data = np.array(read_inputs(Data, act_ses, model_name, '', ''))
    data_ps = np.append(data_add[:,0:1].astype(str),data_add[:,1:], axis=1)
    # build data_ps (used for proxis sectors)
    ps = np.array(()).reshape((0,2))
    for r in data_add:
        if r[2] in ['R', 'r', 'S', 's']:
            ps = np.append(ps, np.array([[r[4],r[3]]]), axis=0)
        else:
            ps = np.append(ps, np.array([[r[3], r[4]]]), axis=0)
    proxy_input['data_ps'] = np.append(data_ps, ps, axis=1)
    proxy_input['headers'] = ['period', 'region', 'table', 'origin', 'destination', 'value',
            'uncert', 'constraint', 'quantity', 'unit', 'factor', 'source','product', 'sector']
    return proxy_input

def write_proxy_output_in_db(
    act_ses, #session name
    model_name : str,
    proxy_output # array with proxy output results
):
    try:
        js_di = {}
        js_di['data'] = proxy_output
        #model_name = model_name + '_terri'
        if len(js_di) > 0:
            save_inputs(js_di, act_ses, 1, model_name, '')
        return True
    except:
        return False
