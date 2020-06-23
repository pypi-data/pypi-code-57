import os
import json
import asyncio
import datetime


class Database():
    """
        Database class to handle access to data
        and access to file io.

        Example:
        ```
        db = Database()
        db.insert(Host('localhost', db))
        ```

        The Database supports async read and write
        from/to memory, and will persist to disk
        every 5 seconds.

        Default mode is 'verbose', which will log
        all events in append mode to the csv log.
        
        You may wish to change to 'status' mode,
        to just get one entry, the latest log message
        foreach tracked Host in the csv file.
    """

    def __init__(self, mode = 'verbose'):
        self.__hosts = []
        self.__errors = []
        self.__last_errors = []
        self.__add_header = True
        self.__file_locked = False
        self.__errors_locked = False
        self.__log_file = 'aiocheck_log.csv'
        self.__persist_file = '.aiocheck_persist.json'

        valid_modes = ['verbose', 'status']
        if mode in valid_modes:
            self.__mode = mode
        else:
            self.__mode = 'verbose'
        
        try:
            with open(self.__persist_file, 'r') as f:
                self.__errors = json.load(f)

            for item in self.__errors:
                item['timestamp'] = datetime.datetime.strptime(item['timestamp'], '%Y-%m-%d %H:%M:%S.%f')
        except Exception:
            pass

        asyncio.ensure_future(self.__persist_loop())
    
    def insert(self, host):
        """
            Insert host into database

            Example:
            ```
            db.insert(Host('localhost', db))
            ```
        """

        self.__hosts.append(host)

    def select(self, addr = None):
        """
            Read host from database

            Example:
            ```
            print(db.select())
            ```

            Supplied with addr, the host with that
            addr will be returned.

            Supplied with no addr, all hosts will
            be returned.

            if no hosts were found, None will be
            returned.
        """

        if addr is None:
            return self.__hosts
        
        for i in range(len(self.__hosts)):
            if self.__hosts[i].get_addr() == addr:
                return self.__hosts[i]
        return None
    
    def insert_error(self, host_as_json):
        """
            Insert error into database

            Example:
            ```
            db.insert_error(Host('localhost', db).get_json())
            ```

            Data is in json format, and is used to persist the
            database.
        """

        try:
            if self.__errors_locked:
                return
            
            self.__errors_locked = True

            if host_as_json in self.__errors:
                self.__errors_locked = False
                return

            match = False
            for i in range(len(self.__errors)):
                if self.__errors[i]['addr'] == host_as_json['addr']:
                    self.__errors[i] = host_as_json
                    match = True

            if not match:
                self.__errors.append(host_as_json)
            
            self.__errors = sorted(self.__errors, key = lambda i: i['timestamp'], reverse=True)
        except Exception as e:
            print(e)
        finally:
            self.__errors_locked = False

    def select_error(self, addr = None):
        """
            Read error from database

            Example:
            ```
            print(db.select_error())
            ```

            Supplied with addr, the error with that
            addr will be returned.

            Supplied with no addr, all error will
            be returned.

            if no error were found, {} will be
            returned.
        """

        if self.__errors_locked:
            return {}
        
        if addr is None:
            return self.__errors

        for error in self.__errors:
            if error['addr'] == addr:
                return error
        return {}

    def select_newest_errors(self):
        """
            Read newest errors from database

            Example:
            ```
            print(db.select_newest_errors())
            ```

            if no error were found, [] will be
            returned.
        """

        if self.__errors_locked:
            return []

        result = []
        check_addr = []
        for error in self.__errors:
            if error['addr'] not in check_addr:
                check_addr.append(error['addr'])
                result.append(error)
        return result

    def __error_equal(self, first, second):
        if first['addr'] != second['addr']:
            return False
        if first['alive'] != second['alive']:
            return False
        if first['timestamp'] != second['timestamp']:
            return False
        return True

    def __errors_equal(self):
        for new in self.__errors:
            for old in self.__last_errors:
                if new['addr'] == old['addr']:
                    if not self.__error_equal(new, old):
                        return False
        return True

    async def __persist_loop(self):
        while True:
            asyncio.ensure_future(self.__export())
            await asyncio.sleep(5)
    
    async def __export(self):
        try:
            if self.__file_locked:
                return

            if self.__errors_equal():
                self.__last_errors = self.__errors
                return

            self.__file_locked = True

            if (len(self.__errors) > 0) and (self.__mode == 'status'):
                with open(self.__persist_file, 'w') as f:
                    json.dump(self.__errors, f, indent=4, default=str)

            header = 'address, alive, timestamp\n'

            result = ''
            if self.__mode == 'status':
                result = header

            if (self.__mode == 'verbose') and (self.__add_header):
                try:
                    with open(self.__log_file, 'r') as f:
                        log_file = f.read()
                    if log_file.split('\n')[0] != header.replace('\n', ''):
                        result = header
                        target = open(self.__log_file, 'w')
                        target.close()
                except Exception:
                    pass
                    result = header
                finally:
                    self.__add_header = False

            for error in self.__errors:
                result += f"{error['addr']}, {error['alive']}, {error['timestamp']}\n"

            if self.__mode == 'status':
                file_mode = 'w'
            if self.__mode == 'verbose':
                file_mode = 'a'

            if len(result) > 0:
                with open(self.__log_file, file_mode) as f:
                    f.write(result)

            self.__last_errors = self.__errors
        except PermissionError:
            pass
        except Exception as e:
            print(e)
        finally:
            self.__file_locked = False
