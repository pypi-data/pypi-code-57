import pandas as pd
import s3fs
import os
import boto3
from pandas_profiling import ProfileReport
from statsmodels.tsa.statespace.exponential_smoothing import ExponentialSmoothingResults

def download_excel(
    self,
    stage=None, 
    filename=None,
    sheet_name=None
):
    '''
    THIS METHOD HAS BE TESTED

    Parameters
    ----------
        self: Datup
            It is the object type Datup necessary to download using aws credentials and write the log. The 
            default folder for log is /tmp/
        stage: str, default None
            It is the set of folders after the datalake to the file that is required to download 
        filename: str, default None
            Is the name of the filename to download without xlsx suffix
        sheet_name: str, default None
            Is the name of the excel worksheet to download

    :rtype: DataFrame
    :return: A DataFrame is return as two-dimensional data structure
        
    Examples
    --------
    >>> import datup as dt    
    >>> dt.download_excel(object,stage='stage',filename='filename',sheet_name='sheet')  
    '''
    try:
        complete_path = str(os.path.join(self.prefix_s3, self.datalake,stage,filename+".xlsx")).replace("\\","/")
        df = pd.read_excel(
            self.aws_credentials_s3fs.open(complete_path),
            sheet_name=sheet_name
        )
    except FileNotFoundError as error:
        self.logger.exception(f"Exception found: {error}") 
        raise
    except ValueError as error:
        self.logger.exception(f'Exception found: {error}') 
    return df

def download_csv(
    self,
    stage=None, 
    filename=None,
    datecols=False, 
    sep=",", 
    encoding="ISO-8859-1",
    infer_datetime_format=True,
    low_memory=False,
    indexcol=None,
    ts_csv = False,
    freq=None,
    key_complete=False,
    freq_offset=False
):
    r"""
    Return a dataframe downloaded from a specified datalake.
    This function takes the aws credentials from DataIO class and use it for download 
    the required data.

    THIS METHOD HAS BE TESTED

    Parameters
    ----------
        self: Datup
            It is the object type Datup necessary to download using aws credentials and write the log. The 
            default folder for log is /tmp/
        stage: str, default None
            It is the set of folders after the datalake to the file that is required to download 
        filename: str, default None
            Is the name of the filename to download without csv suffix
        datecols: bool or list of int or names or list of lists or dict, default False
            Took it from Pandas read_csv parse_dates description
            The behavior is as follows:
                * boolean. If True -> try parsing the index.
                * list of int or names. e.g. If [1, 2, 3] -> try parsing columns 1, 2, 3 each as a separate date column.
                * list of lists. e.g. If [[1, 3]] -> combine columns 1 and 3 and parse as a single date column.
                * dict, e.g. {‘foo’ : [1, 3]} -> parse columns 1, 3 as date and call result ‘foo’
                If a column or index cannot be represented as an array of datetimes, say because of an unparseable value
                or a mixture of timezones, the column or index will be returned unaltered as an object data type. For
                non-standard datetime parsing, use pd.to_datetime after pd.read_csv. To parse an index or column with
                a mixture of timezones, specify date_parser to be a partially-applied pandas.to_datetime() with
                utc=True. See Parsing a CSV with mixed timezones for more.
                Note: A fast-path exists for iso8601-formatted dates.
        sep: str, default ‘,’
            Took it from Pandas read_csv sep description
            Delimiter to use. If sep is None, the C engine cannot automatically detect the separator, but the Python
            parsing engine can, meaning the latter will be used and automatically detect the separator by Python’s
            builtin sniffer tool, csv.Sniffer. In addition, separators longer than 1 character and different from '\s+'
            will be interpreted as regular expressions and will also force the use of the Python parsing engine. Note
            that regex delimiters are prone to ignoring quoted data. Regex example: '\r\t'.
        encoding: str, default ‘ISO-8859-1’
            Took it from Pandas read_csv encoding description
            Encoding to use for UTF when reading/writing (ex. ‘utf-8’).
        infer_datetime_format: bool, default True
            Took it from Pandas read_csv infer_datetime_format description
            If True and parse_dates is enabled, pandas will attempt to infer the format of the datetime strings in the
            columns, and if it can be inferred, switch to a faster method of parsing them. In some cases this can
            increase the parsing speed by 5-10x.
        low_memory: bool, default True
            Took it from Pandas read_csv low_memory description
            Internally process the file in chunks, resulting in lower memory use while parsing, but possibly mixed
            type inference. To ensure no mixed types either set False, or specify the type with the dtype parameter.
            Note that the entire file is read into a single DataFrame regardless, use the chunksize or iterator
            parameter to return the data in chunks. (Only valid with C parser).
        indexcol: int, str, sequence of int / str, or False, default None
                Took it from Pandas read_csv index_col description
                Column(s) to use as the row labels of the DataFrame, either given as string name or column index. If a
                sequence of int / str is given, a MultiIndex is used. 
                Note: index_col=False can be used to force pandas to not use the first column as the index, e.g. when
                you have a malformed file with delimiters at the end of each line.
        ts_csv: bool, default False
            If ts_csv is True then activates the ts_csv downloaded. If True, indexcol and freq, both must
            be different to None
        freq: str, default W-MON
            Is the frequency of getting data.
        key_complete: bool, default False
            If key_complete is True then the stage path of element in s3 bucket must be the full path without s3 prefix
            and datalake.
        freq_offset: bool, default False
            The freq_offset parameter defines the time frequency which dataframe would be downloaded. If True, then
            the function will execute the following command
            * df.index.freq=pd.tseries.frequencies.to_offset(freq)
            If false then
            * df.index.freq=freq

    :rtype: DataFrame
    :return: A DataFrame is return as two-dimensional data structure
        
    Examples
    --------
    >>> import datup as dt    
    >>> dt.download_csv(object,stage='stage',filename='filename') 
    """

    try:
        if key_complete:
            complete_path = str(os.path.join(self.prefix_s3,self.datalake,stage)).replace("\\","/")
            if ts_csv and indexcol is not None and freq is not None:
                df = pd.read_csv(
                    self.aws_credentials_s3fs.open(complete_path),
                    sep=sep, 
                    encoding=encoding,
                    infer_datetime_format=infer_datetime_format,
                    low_memory=low_memory, 
                    index_col=indexcol
                )
                df.index = pd.to_datetime(df.index)
                if freq_offset:
                    df.index.freq=pd.tseries.frequencies.to_offset(freq)
                else: 
                    df.index.freq=freq
            elif ts_csv and indexcol is None and freq is not None:
                print("Is necessary an indexcol value")
            elif ts_csv and indexcol is not None and freq is None:
                print("Is necessary a freq value")            
            else:                
                df = pd.read_csv(
                    self.aws_credentials_s3fs.open(complete_path),
                    sep = sep,
                    encoding= encoding, 
                    infer_datetime_format = infer_datetime_format,
                    low_memory=low_memory, 
                    parse_dates=datecols
                )     
        else:
            complete_path = str(os.path.join(self.prefix_s3, self.datalake,stage,filename+".csv")).replace("\\","/")
            if ts_csv and indexcol is not None and freq is not None:
                df = pd.read_csv(
                    self.aws_credentials_s3fs.open(complete_path),
                    sep=sep, 
                    encoding=encoding,
                    infer_datetime_format=infer_datetime_format,
                    low_memory=low_memory, 
                    index_col=indexcol
                )
                df.index = pd.to_datetime(df.index)
                if freq_offset:
                    df.index.freq=pd.tseries.frequencies.to_offset(freq)
                else: 
                    df.index.freq=freq
            elif ts_csv and indexcol is None and freq is not None:
                print("Is necessary an indexcol value")
            elif ts_csv and indexcol is not None and freq is None:
                print("Is necessary a freq value")            
            else:                
                df = pd.read_csv(
                    self.aws_credentials_s3fs.open(complete_path),
                    sep = sep,
                    encoding= encoding, 
                    infer_datetime_format = infer_datetime_format,
                    low_memory=low_memory, 
                    parse_dates=datecols
                )        
    except FileNotFoundError as error:
        self.logger.exception(f"Exception found: {error}") 
        raise
    return df

def download_csvm(
    self,
    uris
):
    r"""
    Return a set of dataframes downloaded from a specified datalake in a list.
    This function takes the aws credentials from DataIO class and use it for download 
    the required data through download_csv method.

    THIS METHOD HAS BE TESTED
    
    Parameters
    ----------
        self: Datup
            It is the object type Datup necessary to download using aws credentials and write the log. The 
            default folder for log is /tmp/
        uris: dict
            Is the dictionary with all parameters necessary for the download_csv method
        
    :rtype: List of DataFrames
    :return: A list of DataFrames are returned
    :rtype: List of DataFrames Names
    :return: A list of DataFrames Names are return in string type
        
    Examples
    --------
    >>> import datup as dt    
    >>> uris = {
            "uri_1":{
                "stage":"stage",
                "filename":"filename",
                "datecols":False,
                "sep":";",
                "encoding":"ISO-8859-1"
            },
            "uri_2":{
                "stage":"stage",
                "filename":"filename",
                "datecols":False,
                "sep":";",
                "encoding":"ISO-8859-1"
            }
        }
    >>> dt.download_csvm(object,uris=dict(uris)) 
    """

    try:
        dataframes = []
        dataframes_names = []
        for k,v in uris.items():  
            exec("df_{} = download_csv(self=self, stage='{}',filename='{}',sep='{}',encoding='{}', datecols={})".format(k,v["stage"],v["filename"],v["sep"],v["encoding"],v["datecols"]))
            exec("dataframes.append(df_{})".format(k))
            exec("dataframes_names.append('df_{}')".format(k))
    except AttributeError as error:
        self.logger.exception(f"Exception found: {error}")  
        raise
    return dataframes, dataframes_names

def upload_csv(
    self,
    df,
    stage=None,
    filename=None,
    index=False,
    header=True,
    date_format="%Y-%m-%d",
    ts_csv=False
):  
    r"""
    Return a uri where the dataframes was uploaded in csv format.
    This function takes the aws credentials from DataIO class and use it for upload
    the required data.
    
    THIS METHOD HAS BE TESTED

    Parameters
    ----------
        self: Datup
            It is the object type Datup necessary to upload using aws credentials and write the log. The 
            default folder for log is /tmp/
        df: DataFrame
            Is the DataFrame for uploading to S3 datalake
        stage: str, default None
            It is the set of folders after the datalake to the file that is required to upload 
        filename: str, default None
            Is the name of the filename to upload without csv suffix
        index: bool, default False
            Took it from Pandas to_csv index description
            Write row names (index).
        header: bool or list of str, default True
            Took it from Pandas to_csv index description
            Write out the column names. If a list of strings is given it is assumed to be aliases for
            the column names.
        date_format: str, default %Y-%m-%d
            Took it from Pandas to_csv index description
            Format string for datetime objects.
        ts_csv: bool, default False
            If ts_csv is True then activates the ts_csv upload. If True, index must be different to False
        
    :rtype: Str
    :return: The uri where DataFrame was uploaded into S3
                
    Examples
    --------
    >>> import datup as dt
    >>> dt.upload_csv(object,df,stage="stage",filename="filename")        
    """

    try:
        complete_s3_path = str(os.path.join(self.prefix_s3, self.datalake,stage,filename,filename+".csv")).replace("\\","/")
        complete_local_path = str(os.path.join(self.local_path,filename+".csv")).replace("\\","/")
        medium_s3_path = str(os.path.join(stage, filename, filename+'.csv').replace("\\","/"))
        if ts_csv and index:
            df.to_csv(complete_local_path, index=index, header=header, date_format=date_format)
            self.aws_credentials_s3.Bucket(self.datalake).upload_file(complete_local_path, medium_s3_path)
        if ts_csv and not index:
            print("Is necessary use index True for ts_csv mode")
        if index and not ts_csv:
            print("Is necessary use ts_csv True")
        else:
            df.to_csv(complete_local_path, index=index, header=header, date_format=date_format)
            self.aws_credentials_s3.Bucket(self.datalake).upload_file(complete_local_path, medium_s3_path)                
        upload_path = complete_s3_path
    except FileNotFoundError as error:
        self.logger.exception(f"Exception found: {error}") 
        raise    
    return upload_path

def profiling_report(
    self,
    df,
    stage=None,
    filename=None,
    save=False,
    minimal=True
):
    r"""
    Return a html embbeded with the DataFrame profiling data or save it into a S3 datalake .
    This function takes the aws credentials from DataIO class and use it for upload
    the required data, after this, the method can save or not the result by the save flag.

    THIS METHOD HAS BE TESTED

    Parameters
    ----------
        self: Datup
            It is the object type Datup necessary to upload using aws credentials and write the log. The 
            default folder for log is /tmp/
        df: DataFrame
            Is the DataFrame for profiling the data
        stage: str, default None
            It is the set of folders after the datalake to the file that is required to upload,
            this method just apply if save parameter is True 
        filename: str, default None
            Is the name of the filename to upload without html suffix, 
            this method just apply if save parameter is True
        save: bool, default False
            If save is False, the html was embedded in the worksheet if True, the html will be saved into a 
            S3 datalake
        minimal: bool, default True
            If minimal is True the method disables expensive computations (such as correlations and dynamic binning)
        
    :rtype: Html
    :return: A Html is returned by the method
                
    Examples
    --------
    >>> import datup as dt
    >>> dt.generate_profiling(object,df)        
    """

    try:
        profile = ProfileReport(df, minimal=minimal)
        if save: 
            complete_s3_path = str(os.path.join(self.prefix_s3, self.datalake,stage,filename,"{}.html".format(filename))).replace("\\","/")         
            medium_s3_path = str(os.path.join(stage, filename,"{}.html".format(filename))).replace("\\","/")
            profile.to_file("{}{}.html".format(self.local_path,filename))
            self.aws_credentials_s3.Bucket(self.datalake).upload_file("{}{}.html".format(self.local_path,filename), medium_s3_path)
            return complete_s3_path
        else:
            return profile.to_notebook_iframe()
    except:
        self.logger.exception(f"Exception found: ")  
        raise
    
def upload_model(
    self,
    model,
    stage=None,
    item=None,
    filename=None
):
    r"""
    The upload_model save a pkl model and return the S3 datalake path where saved.

    THIS METHOD HAS BE TESTED

    Parameters
    ----------
        self: Datup
            It is the object type Datup necessary to upload using aws credentials and write the log. The 
            default folder for log is /tmp/
        model: str
            Is the pkl model
        stage: str, default None
            It is the set of folders after the datalake to the file that is required to upload,
        filename: str, default None
            Is the name of the filename to upload without pkl suffix, 
        item: str, default None
            Is the name of item for a model. This method is used by upload_best_model in ExponetialSmoothing class

    :rtype: Str
    :return: The path where model saved is returned
                
    Examples
    --------
    >>> import datup as dt
    >>> dt.upload_model(object,model,stage="stage",item="item_id",filename="filename")        
    """

    try:        
        complete_s3_path = str(os.path.join(self.prefix_s3, self.datalake, stage, item, "{}.pkl".format(filename))).replace("\\","/")
        route_model = str(os.path.join(self.local_path,"{}.pkl".format(filename))).replace("\\","/") 
        medium_s3_path = str(os.path.join(stage, item, "{}.pkl".format(filename))).replace("\\","/")
        model.save(route_model)
        self.aws_credentials_s3.Bucket(self.datalake).upload_file(route_model, medium_s3_path)
    except FileNotFoundError as error:
        self.logger.exception(f"Exception found: {error}")  
        raise    
    return complete_s3_path

def upload_log(
    self,
    logfile,
    stage=None
):
    r"""
    The upload_log save the log of process and return the S3 datalake path where saved.

    THIS METHOD HAS BE TESTED

    Parameters
    ----------
        self: Datup
            It is the object type Datup necessary to upload using aws credentials and write the log. The 
            default folder for log is /tmp/
        logfile: str
            Is the log model
        stage: str, default None
            It is the set of folders after the datalake to the file that is required to upload
                
    :rtype: Str
    :return: The path where log saved is returned
                
    Examples
    --------
    >>> import datup as dt
    >>> dt.upload_log(object,logfile, stage="stage")        
    """

    try:      
        complete_s3_path = str(os.path.join(self.prefix_s3, self.datalake, stage, logfile)).replace("\\","/")
        route_logfile = str(os.path.join(self.local_path, logfile)).replace("\\","/")
        medium_s3_path = str(os.path.join(stage, logfile)).replace("\\","/")
        self.aws_credentials_s3.Bucket(self.datalake).upload_file(route_logfile, medium_s3_path)
    except FileNotFoundError as error:
        self.logger.exception(f"Exception found: {error}") 
        raise    
    return complete_s3_path

def list_items(
    self,
    stage
):
    """
    Return list of items files stored in the datalake
    
    THIS METHOD HAS BE TESTED

    Parameters
    ----------
        self: Datup
            It is the object type Datup necessary to upload using aws credentials and write the log. The 
            default folder for log is /tmp/
        stage: str
            It is the set of folders after the datalake to the files that is required to download
                
    :rtype: List
    :return: The list of items queried in the dataframe
                
    Examples
    --------
    >>> import datup as dt
    >>> dt.list_items(object,stage="stage") 
    """
    try: 
        items = [e['Key'][:] for p in self.aws_client_s3.get_paginator('list_objects_v2').paginate(Bucket=self.datalake, Prefix=stage) for e in p['Contents']]
    except IOError as error:
        self.logger.exception(f"Exception found: {error}") 
        raise
    return items

def delete_items(
    self,
    stage,
    item_id
):
    """
    Return a boolean flag indicating success for items deletion in the datalake
    
    THIS METHOD HAS BE TESTED

    Parameters
    ----------
        self: Datup
            It is the object type Datup necessary to upload using aws credentials and write the log. The 
            default folder for log is /tmp/
        stage: str,
            It is the set of folders after the datalake to the files that is required to download
        item_id: str,
            Is the all path of item to delete    
                
    :rtype: Bool
    :return: A True or False flag indicating success for deletion
                
    Examples
    --------
    >>> import datup as dt
    >>> dt.delete_items(object,stage="stage",item_id="item_id")    
    """
    try:
        for it in self.aws_client_s3.get_paginator('list_objects_v2').paginate(Bucket=self.datalake, Prefix=os.path.join(stage, item_id).replace("\\","/")):
            key_counts = it.get('KeyCount')
        if key_counts > 0:
            keys = [e['Key'][:] for p in self.aws_client_s3.get_paginator('list_objects_v2').paginate(Bucket=self.datalake, Prefix=os.path.join(stage, item_id).replace("\\","/")) for e in p['Contents'][-1:]]
            for key in keys:            
                kwargs = {'Bucket':self.datalake, 'Key':key}
                response = self.aws_client_s3.delete_object(**kwargs)
                response = response.get('DeleteMarker')
        else: 
            response = True
    except IOError as error:
        self.logger.exception(f"Exception found: {error}") 
        raise
    return response

def get_model_name(
    self,
    stage,
    item_id
):
    """
    Return list of models' names stored in the datalake
    
    THIS METHOD HAS BE TESTED

    Parameters
    ----------
        self: Datup
            It is the object type Datup necessary to upload using aws credentials and write the log. The 
            default folder for log is /tmp/
        stage: str,
            It is the set of folders after the datalake to the files that is required to download
        item_id: str,
            Is the all path of item to delete    
                
    :rtype: List
    :return: A list of model names per items
                
    Examples
    --------
    >>> import datup as dt
    >>> dt.get_model_name(object,stage="stage",item_id="item_id") 
    """
    try: 
        item = [e['Key'][-10:-4] for p in self.aws_client_s3.get_paginator('list_objects_v2').paginate(Bucket=self.datalake, Prefix=os.path.join(stage, item_id).replace("\\","/")) for e in p['Contents'][-1:]]
    except IOError as error:
        self.logger.exception(f"Exception found: {error}")
        raise
    return item

def download_model(
    self,
    stage,
    item_id,
    filename
):
    """
    Return a pkl model from a S3 Bucket
    
    THIS METHOD HAS BE TESTED

    Parameters
    ----------
        self: Datup
            It is the object type Datup necessary to upload using aws credentials and write the log. The 
            default folder for log is /tmp/
        stage: str,
            It is the set of folders after the datalake to the files that is required to download
        item_id: str,
            Is the all path of item to delete    
        filename: str,
            Is the name of file inside of the item_id path which contains the pkl model
                
    :rtype: Object
    :return: The ExponentialSmoothingResults object
                
    Examples
    --------
    >>> import datup as dt
    >>> dt.download_model(object,stage="stage",item_id="item_id",filename="filename")    
    """
    try:
        file_pickle = os.path.join(self.local_path, '{}.pkl'.format(filename)).replace("\\","/")
        s3_route_picke = os.path.join(stage, item_id, '{}.pkl'.format(filename)).replace("\\","/")
        self.aws_credentials_s3.Bucket(self.datalake).download_file(s3_route_picke, file_pickle)        
        model = ExponentialSmoothingResults.load(file_pickle)
    except FileNotFoundError as error:
        self.logger.exception(f"Exception found: {error}")
        raise
    return model


