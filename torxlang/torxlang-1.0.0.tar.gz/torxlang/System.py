'''
This is 'System' module.  No difference between this and 'system' class.  
So I recommend to use rx.system but no difference.
'''

class system:
    '''
    Some system actions and information.
    - Information about ram, ip, terminal, etc.
    - Some System Actions like Shutdown and Restart
    '''
    @staticmethod
    def accname():
        '''
        return account username you have logged in.
        '''
        return os.getlogin()
    @staticmethod
    def pid():
        '''
        Get pid number of terminal and return it.
        '''
        return os.getpid()
    '''@staticmethod
    def disk_usage(path):
        ####
        return shutil.disk_usage(path)'''
    @staticmethod
    def chdir(path):
        '''
        Change directory of terminal.
        '''
        os.chdir(path)
    @staticmethod
    def SHUT_DOWN():
        '''
        Shut down the PC.
        '''
        os.system("shutdown /s /t 1")
    @staticmethod
    def RESTART():
        '''
        Restart the PC.
        '''
        os.system("shutdown /r /t 1")
    @staticmethod
    def terminal_size() -> tuple:
        '''
        Return terminal size in tuple (columns,rows)
        '''
        #return os.get_terminal_size()
        return shutil.get_terminal_size()
    @staticmethod
    def cwd():
        '''
        Return a unicode string representing the current working directory.
        '''
        return os.getcwd()
    @staticmethod
    def ip_global():
        """
        Return ip with by http://ipinfo.io/ip api.
        returns global ip as string
        """
        try:
            new_session = requests.session()
            response = new_session.get("http://ipinfo.io/ip")
            ip_list = re.findall(r"(?:[0-9]{1,3}\.){3}[0-9]{1,3}", response.text)
            new_session.close()
            return ip_list[0]
        except:
            class ConnectionError(requests.exceptions.ConnectionError):
                def __init__(self, message): super().__init__(message)
            raise ConnectionError('No Internet Connection')
    @staticmethod
    def ip_local():
        """
        Return local ip of computer in windows by socket module
        and in unix with hostname command in shell.
        """
        import platform
        class NetworkError(Exception):
            def __init__(self, message): super().__init__(message)
        try:
            ip = socket.gethostbyname(socket.gethostname())
            if ip != "127.0.0.1":
                return ip
            elif platform.system() != "Windows":
                command = sub.Popen(["hostname", "-I"],stdout=sub.PIPE,stderr=sub.PIPE,stdin=sub.PIPE,shell=False)
                response = list(command.communicate())
                if len(response[0]) > 0:
                    return str(response[0])[2:-4]
                raise NetworkError('No Network Connection')
            raise NetworkError('No Network Connection')
        except:
            raise
        #return [l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1], [[(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) if l][0][0]
    @staticmethod
    def ram_total(convert=True):
        """
        Return total ram of board as string
        parameter convert: flag for convert mode (using of convert_byte function)
        """
        response = list(psutil.virtual_memory())
        if convert:
            return convert_bytes(int(response[0]))
        return str(response[0])
    @staticmethod
    def ram_used(convert=True):
        """
        Return how much ram is using.
        parameter convert: flag for convert mode (convert with convert_byte function)
        """
        response = list(psutil.virtual_memory())
        if convert:
            return convert_bytes(int(response[3]))
        return str(response[3])
    @staticmethod
    def ram_free(convert=True):
        """
        Return how much ram is available.
        parameter convert: flag for convert mode (convert with convert_byte function)
        """
        response = list(psutil.virtual_memory())
        if convert:
            return convert_bytes(int(response[1]))
        return str(response[1])
    @staticmethod
    def ram_percent(ONLY_NOM=False):
        """
        Return available ram percentage as an integer if ONLY_NOM, as string with % if not ONLY_NOM
        Parameter ONLY_NOM: flag for return type and value.
        """
        response = list(psutil.virtual_memory())
        if ONLY_NOM:
            return response[2]    
        return str(response[2]) + " %"
    @staticmethod
    def boot_time():
        '''
        Return the system boot time expressed in seconds since the epoch.
        '''
        return psutil.boot_time()
