import json
import asyncio
import platform
import datetime


class Host():
    """
        Class to represent a Host to be pinged.

        Example:
        ```
        Host('localhost', db)
        ```

        db is optional, but without it
        database functionallity will not
        function.
    """

    def __init__(self, addr, db = None):
        self.__db = db
        self.__addr = addr
        self.__alive = False
        self.__timestamp = datetime.datetime.utcnow()
        self.__errors = {}
        self.__data = None

        asyncio.ensure_future(self.__ping_loop())

    def __str__(self):
        return json.dumps(self.get_json(), indent=4, default=str)

    def __eq__(self, other):
        if self.get_addr() != other.get_addr():
            return False
        if self.is_alive() != other.is_alive():
            return False
        if self.get_timestamp() != other.get_timestamp():
            return False

        return True
    
    def get_csv(self):
        """
            Return Host as a string of csv

            Example:
            ```
            print(Host('localhost', db).get_csv())
            ```
        """
        
        return f"{self.__addr}, {self.__alive}, {self.__timestamp}\n"
    
    def get_json(self):
        """
            Return Host as a dict of json data

            Example:
            ```
            print(Host('localhost', db).get_json())
            ```
        """

        return {
            'addr': self.__addr,
            'alive': self.__alive,
            'timestamp': self.__timestamp,
            'errors': self.__errors,
            'data': self.__data,
        }

    def get_timestamp(self):
        return self.__timestamp

    def get_addr(self):
        return self.__addr

    def is_alive(self):
        return self.__alive

    def __check_error(self, errors, query, message):
        if self.__data.find(query) != -1:
            errors.append(message)

    async def __ping_loop(self):
        while True:
            asyncio.ensure_future(self.ping())
            await asyncio.sleep(1)

    async def ping(self):
        """
            Ping the provided self.
            
            Example:
            ```
            print(ping('localhost', db))
            ```
        """

        param = '-c'
        if platform.system().lower() == 'windows':
            param = '-n'

        proc = await asyncio.subprocess.create_subprocess_exec(
            'ping',
            '-w', '1',
            param, '1',
            self.__addr,
            stdout=asyncio.subprocess.PIPE,
        )
        proc_data = await proc.communicate()
        self.__data = proc_data[0].decode()

        errors = []
        self.__check_error(errors, '100%', 'host_packet_loss')
        self.__check_error(errors, 'Request timed out', 'host_timed_out')
        self.__check_error(errors, 'Name or service not known', 'host_name_not_found')
        self.__check_error(errors, 'Destination host unreachable', 'host_unreachable')
        self.__check_error(errors, 'Ping request could not find host', 'host_not_found')

        if len(errors) == 0:
            self.__alive = True
        else:
            self.__alive = False
            self.__db.insert_error(self.get_json())
        
        for error in errors:
            self.__errors[error] = True

        self.__timestamp = datetime.datetime.utcnow()
