from datup.core.credentials import Credentials
from datup.core.logger import Logger

''' 
The Datup class must be instantiaded. Functions in datup library required write in a log as default.
for that reason the object instantiaded is callable  
'''
class Datup(Credentials, Logger):
    r''' 
    Parameters
    ----------
        aws_access_key_id: str, default None
            Is the AWS Access Id provided AWS
        aws_secret_access_key: str, default None
            Is the AWS Access Key provided AWS
        datalake: str, default None
            Is the datalake to use for download the data using the DataIO methods classes
        prefix_s3: str, default 's3://'
            Is the prefix used by AWS S3 for connecting with datalakes
        local_path: str, default '/tmp/'
            Is the address of the temporal folder of the server which is running the process.
        suffix_name: str, default 'my_logger_'
            Is the address of the temporal folder of the server which is running the process.

    :return: The class return an object callable class 
    :rtype: Object 

    Examples
    --------
    >>> import datup as dt
    >>> object = dt.Datup("aws_key_id","aws_key","datalake")
    '''

    def __init__(self,
        aws_access_key_id=None,
        aws_secret_access_key=None,
        datalake=None,
        prefix_s3="s3://",
        local_path="/tmp/",
        suffix_name="my_logger_"
    ):
        Credentials.__init__(
            self,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            datalake=datalake,
            prefix_s3=prefix_s3,
            local_path=local_path
        )
        Logger.__init__(
            self,
            suffix_name=suffix_name,
            local_path=local_path
        )