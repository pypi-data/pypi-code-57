import datetime
import pysftp
from typing import List, Any, Optional


def convert_dt_to_ns_time_str(datetime_obj: datetime.date) -> str:
    """Converts a datetime object to iso format string for Netsuite"""
    if isinstance(datetime_obj, datetime.date):
        ns_dt = datetime_obj.strftime('%Y-%m-%dT%H:%M:%S.000Z')

        return ns_dt
    else:
        raise Exception('Not datetime object')


def sftp_vdp_list_dir(host: str, username: str, password: str, port: int = 22, directory_loc: str = '/') -> List:
    """
    Function makes a sftp connection and lists all files and folders in specified directory
    :param: str host
    :param: str username
    :param: str possword
    :param: str port, default is 22
    :param: str directory_loc, directory location to list all files/folders
    :return: list all files and folders in specified directory
    """

    print(f'!!!!!!!!!!port {port}')
    print(f'!!!!!!!!!!vpd_directory_loc {directory_loc}')

    with pysftp.Connection(host=host, username=username, password=password, port=port) as sftp:
        with sftp.cd(directory_loc):
            dir_list = sftp.listdir()
            return dir_list


def sftp_vdp_put_assets(host: str, username: str, password: str, port: int = 22, vpd_directory_loc: str = '/',
                        folder: str = None, file: str = None) -> None:
    """
    Function makes a sftp connection and puts a file onto the directory specified
    :param: str host
    :param: str username
    :param: str possword
    :param: str port, default is 22
    :param: str vpd_directory_loc, main directory location
    :param: str folder within main directory
    :param: str file to be copied
    :return: None
    """

    print(f'sftp_vdp_put_assets!!!!!!!!!!port {port}')
    print(f'sftp_vdp_put_assets!!!!!!!!!!vpd_directory_loc {vpd_directory_loc}')

    with pysftp.Connection(host=host, username=username, password=password, port=port) as sftp:
        if not sftp.exists(vpd_directory_loc):
            sftp.mkdir(vpd_directory_loc)
        with sftp.cd(vpd_directory_loc):
            if folder:
                if not sftp.exists(folder):
                    sftp.mkdir(folder)
                with sftp.cd(folder):
                    sftp.put(file)
            else:
                sftp.put(file)


def get_last_two_months_val(date_obj: Optional[datetime.date] = None) -> str:
    """
    Utility function that takes an optional datetime.date object and returns the YYYY-MM str that is 60 days from date.
    Default is today is no argument is specified

    :return: YYYY-MM str
    """
    if date_obj:
        if isinstance(date_obj, datetime.date):
            prev_month_val = date_obj - datetime.timedelta(days=60)
        else:
            raise TypeError
    else:
        prev_month_val = datetime.datetime.now() - datetime.timedelta(days=60)

    prev_month = prev_month_val.strftime('%Y-%m')

    return prev_month


def get_last_three_months_val(date_obj: Optional[datetime.date] = None) -> str:
    """
    Utility function that takes an optional datetime.date object and returns the YYYY-MM str that is 90 days from date.
    Default is today is no argument is specified

    :return: YYYY-MM str
    """
    if date_obj:
        if isinstance(date_obj, datetime.date):
            prev_month_val = date_obj - datetime.timedelta(days=90)
        else:
            raise TypeError
    else:
        prev_month_val = datetime.datetime.now() - datetime.timedelta(days=90)

    prev_month = prev_month_val.strftime('%Y-%m')

    return prev_month

