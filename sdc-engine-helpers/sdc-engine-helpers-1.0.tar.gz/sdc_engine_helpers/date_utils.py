"""
    Date utilities module
"""
from datetime import datetime
from datetime import timedelta

class DateUtils:
    """
        Date utilities class to perform specific date manipulation
    """

    mysql_date_format = '%Y-%m-%d %H:%M:%S'

    def get_next_time(self, *, this_time=None, frequency: int, return_type='str') -> datetime:
        """
            Perform the required maintenance on a list of campaigns

            args:
                this_time: The time to calculate with (str/datetime)
                frequency (int): A period in minutes to calculate next time with
                return_type (str): The requested return type - default string

            returns:
                next_time (datetime): The calculated next time

        """
        if this_time is None:
            this_time = datetime.now()

        if isinstance(this_time, str):
            this_time = datetime.strptime(
                this_time,
                self.mysql_date_format
            )

        next_time = this_time + timedelta(
            minutes=frequency
        )

        # If next time is less than the current time. Set next time to the current time
        # plus the frequency
        now = datetime.now()
        if next_time < now + timedelta(minutes=frequency + 1):
            next_time = now + timedelta(minutes=frequency)

        if return_type == 'str':
            next_time = datetime.strftime(
                next_time,
                self.mysql_date_format
            )

        return next_time

    def get_mysql_date_format(self) -> str:
        """
            Get the defined MySql date format

            returns:
                date_format (str): This class's Mysql date format

        """
        return self.mysql_date_format
