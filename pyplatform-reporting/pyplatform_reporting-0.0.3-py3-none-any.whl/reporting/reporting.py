import os
import json
import logging
import datetime
import pytz

import tableauserverclient as TSC
from tableauhyperapi import TableName
import pantab


def get_tableau_server_credentials(**kwargs):
    """ infers and/or updates defaults for tableau server
    defaults comes from credentials.json filepath set as environment 'TABLEAU_SERVER_CREDENTIALS'
    providing below Keyword Arguments over rides defaults

    Keyword Arguments:
        serverUrl {str} - e.g. 'https://server.company.com'
        contentUrl {str} - siteName
        username {str} - userid
        password {str} 
        project {str} - tableau server folder/project ,defaults to 'Default' project
    

    Returns:
    {dict} - credential dictionary

    {'serverUrl': 'https://server.company.com' \
        , 'contentUrl': 'siteName' \
        , 'username' : 'userid' \
        , 'password': '***' \
        , 'project': 'Default'} 
    
    """
    default_credpath =  os.environ.get('TABLEAU_SERVER_CREDENTIALS')
    
    if default_credpath:
        with open(default_credpath, 'r') as file:
            credentials = json.load(file)
    else:
        logging.warning('default credentials path does not exit, no defaults set for tableau server authentication')
        credentials = {}
    
    if 'serverUrl' in kwargs:
        credentials['serverUrl'] = kwargs['serverUrl']
    
    if 'contentUrl' in kwargs:
        credentials['contentUrl'] = kwargs['contentUrl']
        
    if 'username' in kwargs:
        credentials['username'] = kwargs['username']
        
    if 'password' in kwargs:
        credentials['password'] = kwargs['password']
    
    if 'project' in kwargs:
        credentials['project'] = kwargs['project']
        
    return credentials

def upload_hyper_tableau_server(hyper_file, **kwargs):
    """ publishes local extract.hyper file to tableau server

    Arguments:
        hyper_file {str} -- filepath of extract.hyper or .tde to be published

    Keyword Arguments:
        project {str} -- tableau prep folder/project (Defaults: {Defaults})
        mode {str} -- CreateNew|Overwrite|Append (Defaults: Overwrite)
        embed {bool} -- if True, embeds credentails in data source (Defaults: True)
        name {str} -- name of extract file on server to be replaced or appended to
        ``serverUrl`` , ``contentUrl`` ,``username``, ``password``  can also be provide to override defaults for Tableau server authentication
    
    Returns:
        str -- datasource_name on the server
    """

    credentials = get_tableau_server_credentials(**kwargs)
    tableau_auth = __tableau_auth(credentials)
    server = TSC.Server(credentials.get('serverUrl'))
    project = credentials.get('project')


    logging.debug(f'supplied keyword args: {kwargs}')
    with server.auth.sign_in(tableau_auth):
        assert server.is_signed_in() == True

        all_project_items, pagination_item = server.projects.get()
        try:
            project_id = [
                item.id for item in all_project_items if item.name == project][0]
        except:
            project_id = [
                item.id for item in all_project_items if item.name == 'Default'][0]

        logging.debug(f'selected {project} with id {project_id}')

        if os.path.isfile(hyper_file):
            name = os.path.basename(hyper_file)
            hyper_filepath = hyper_file
        else:  # when only filename is passed which is in curren working directory folder
            name = hyper_file
            hyper_filepath = os.path.join(os.path.curdir, name)

        if 'name' in kwargs.keys() and kwargs.get('name') != None:
            name = kwargs.get('name')
        else:
            name = name.split('.')[0]

        if 'mode' in kwargs.keys():
            mode = kwargs.get('mode').title()
            if mode == 'Createnew':
                mode = 'CreateNew'

            if mode == 'Append':
                all_datasources, pagination_item = server.datasources.get()

                try:
                    datasource_id = [
                        datasource.id for datasource in all_datasources if datasource.name == name][0]
                    data_source_item = server.datasources.get_by_id(
                        datasource_id)
                    logging.debug(f"appending {hyper_filepath} to {name}")
                except:
                    mode = 'CreateNew'
                    data_source_item = TSC.DatasourceItem(
                        project_id=project_id, name=name)
                    logging.warning(
                        f'could not find {name} on server, publishing  {hyper_file} a new datasource')
            else:
                data_source_item = TSC.DatasourceItem(
                    project_id=project_id, name=name)
                logging.debug(
                    f"publishing {hyper_filepath} as {name} in {mode} mode")

        else:
            mode = 'Overwrite'
            data_source_item = TSC.DatasourceItem(
                project_id=project_id, name=name)
            logging.debug(f"publishing {name} in {mode} mode")

        if 'embed' in kwargs.keys():
            embedded_credential = TSC.ConnectionCredentials(
                username, password, embed=embed, oauth=False)
            server.datasources.publish(
                data_source_item, hyper_filepath, mode, connection_credentials=embedded_credential)
        else:
            server.datasources.publish(
                data_source_item, hyper_filepath, mode)
    logging.info(
        f'{hyper_filepath} was successfully published in {mode} mode to {project} project!')
    # TODO datasource_id or datasource_name not included in url at this time
    # url = __make_datasource_url(datasource_id, serverUrl=serverUrl, contentUrl=contentUrl)

    return name

def download_hyper_tableau_server(datasource_name, filepath=None, output_option='hyper', **credentials):
    """ downloads tdsx/hyper datasources from tableau server

    Arguments:
        datasource_name {str} -- datasource name without file extention

    Keyword Arguments:
        filepath {str} -- filepath for downloaded datasource (default: {None})
        output_option {str} -- to download ``tdsx``, set output_ouption = None (default: {'hyper'})
        kwargs for over-riding default credentials

    Returns:
        str -- filepath of downloaded data source in hyper ot tdsx format
    """
    credentials = get_tableau_server_credentials(**credentials)
    tableau_auth = __tableau_auth(credentials)
    datasource_id = __find_datasource_id_by_name(name = datasource_name)
    server = TSC.Server(credentials.get('serverUrl'))

    with server.auth.sign_in(tableau_auth):
            assert server.is_signed_in() == True
            data_source_item = server.datasources.get_by_id(datasource_id)
            filepath = server.datasources.download(datasource_id, filepath=filepath)

    if output_option == 'hyper':
        tdsx_path = filepath
        filepath = unzip_tdsx(filepath, hyper_filepath=None)
        os.remove(tdsx_path)
        
    return filepath

def df_to_hyper(df, filepath=None, table_name=None):
    """converts dataframe to hyper format on local drive, gcs, azure storage, tableau server, pass cred/clients?

    Arguments:
        df {pandas.DataFrame}
    Keyword Arguments:
        filepath {str} -- filename or filepath for hyper output (default: {extract_timestamp.hyper})
        table_name {tableauhyperapi.TableName} (default: {TableName('Extract', 'Extract')})

    Returns:
        str -- filepath of created hyper file
    """
    if not table_name:
        table_name = TableName('Extract', 'Extract')
        
    if not filepath:
        timezone = pytz.timezone("America/New_York")
        utc_now = pytz.utc.localize(datetime.datetime.utcnow())
        est_now_str = utc_now.astimezone(pytz.timezone(
            "America/New_York")).strftime("%Y%m%d_%H%M%S_EST")
        filepath = 'extract_' + est_now_str + '.hyper'
    else:
        filepath = filepath.split('.')[0] + '.hyper'
        
    pantab.frame_to_hyper(df, filepath, table=table_name)
    return filepath

def hyper_to_df(hyper_filepath, table_name=None):
    """ creates pandas.DataFrame form hyper

    Arguments:
        hyper_filepath {str} -- filepath of hyper file

    Keyword Arguments:
        table_name {tableauhyperapi.TableName} (default: {TableName('Extract', 'Extract')})

    Returns:
        pandas.DataFrame
    """
    if not table_name:
        table_name = TableName('Extract', 'Extract')
    return pantab.frame_from_hyper(hyper_filepath, table=table_name)

def __tableau_auth(credentials):
    """ instantiates tableau auth
    
    credentials {dict}
    """
    server_address = credentials.get('serverUrl')
    username = credentials.get('username')
    password = credentials.get('password')
    logging.info(f"singing into {server_address} as {username}")

    
    tableau_auth = TSC.TableauAuth(
        username, password, credentials.get('contentUrl'))
    return tableau_auth

def __find_datasource_id_by_name(name='extract.hyper', output_option=None, **kwargs):
    """ finds datasource_id on tableau server

    Keyword Arguments:
        name {str} -- datasource name (default: {'extract.hyper'})
        output_option {str} -- change output, if output_option = DICT returns dictionary of all datasource with name: id
                                if output_option = LIST returns list of all datasource attributes  (default: {None})

    Returns:
        str, dict, list
    """
    credentials = None
    if not credentials:
        credentials = get_tableau_server_credentials()
    tableau_auth = __tableau_auth(credentials)
    server = TSC.Server(credentials.get('serverUrl'))
    with server.auth.sign_in(tableau_auth):
        assert server.is_signed_in() == True
        
        all_datasources, pagination_item = server.datasources.get()
    
        if output_option == 'DICT':
            datasource_id = {datasource.name: datasource.id for datasource in all_datasources}
            return datasource_id
        elif output_option == 'LIST':
            datasource_id = [{'name' : datasource.name, 'id': datasource.id, 'project_name': datasource.project_name,'owner_id': datasource.owner_id, 'updated_at': datasource.updated_at , 'content_url': datasource.content_url} for datasource in all_datasources]
            return datasource_id

        else:
            datasource_id = [datasource.id for datasource in all_datasources if datasource.name == name]
            
        if len(datasource_id) >= 1:
            return datasource_id[0]
        else:
            logging.warning('{} datasource not found. Below is all datasources name and id \n {}'.format(name, {datasource.name: datasource.id for datasource in all_datasources}))
            

def unzip_tdsx(tdsx_filepath, hyper_filepath=None):
    """ extracts extract.hyper from tdsx

    Arguments:
        tdsx_filepath {str} -- filepath for tdsx

    Keyword Arguments:
        hyper_filepath {str} -- filepath for hyper (default: {tdsx_filepath})

    Returns:
        str -- filepath for hyper
    """
    import zipfile
    if not hyper_filepath:
        hyper_filepath = '.'.join(tdsx_filepath.split('.')[:-1])  + '.hyper'
        
    tdsx = zipfile.ZipFile(tdsx_filepath)
    for item in tdsx.namelist():
        if '.hyper' in item:
            f = tdsx.open(item)
            content = f.read()
            f = open(hyper_filepath, 'wb')
            f.write(content)
            f.close()
    return hyper_filepath


def __parse_datasource_url(datasource_url):
    #TODO datasource_id not part of url at this time ref: https://github.com/tableau/server-client-python/issues/268
    """ decomposes datasource url into components

    Arguments:
        datasource_url {str} -- url of extract.hyper file on tableau server e.g. 'https://server.company.com/#/site/contentUrl/project/163271/askData'

    Returns:
        tuple -- serverUrl, contentUrl, project, datasource_Id
    """
    url = datasource_url.split('/')
    serverUrl, contentUrl, project, datasource_Id = '/'.join(url[:3]), url[5], url[6] , url[7]
    return serverUrl, contentUrl, project, datasource_Id

def __make_datasource_url(datasource_id, **kwargs):
    #TODO datasource_id not part of url at this time ref https://github.com/tableau/server-client-python/issues/268
    """ creates datasource url from datasource_id
    Arguments:
        datasource_id {str}
    
    Keyword Arguments:
        serverUrl {str} - e.g. 'https://server.company.com'
        contentUrl {str} - siteName
        project {str} - tableau server folder/project ,defaults to 'Default' project

    Returns:
        url {str} -- 'https://server.company.com/#/site/contentUrl/project/163271/askData'
    """
    
    defaults_creds = get_tableau_server_credentials()
    
    if 'serverUrl' not in kwargs:
        serverUrl = defaults_creds.get('serverUrl')
    else:
        serverUrl = kwargs['serverUrl']
        
    if 'contentUrl' not in kwargs:
        contentUrl = defaults_creds.get('contentUrl')
    else:
        contentUrl = kwargs['contentUrl']
        
    if 'project' not in kwargs:
        project = defaults_creds.get('project')
    else:
        project = kwargs['project']
        
    url = serverUrl +'/#/site/' + contentUrl +'/' + project + '/' + datasource_id + '/askData'
    
    return url
