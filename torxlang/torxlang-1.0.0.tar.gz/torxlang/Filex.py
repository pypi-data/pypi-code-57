'''
Filex Module is Sub-Module of rx7 library.
It contains 2 classes:  
1- files: Static method
2- File: create File object and use its methods.  
(If you are using rx7 module, don't use this and directly use rx7.files and rx7.File)
(Usually I use first one when I need a file only one time in my code  
and use 2nd one when i'm working with a file more than 1 time.)

'''

import os,shutil,subprocess



class files:
    #self.info: size-atime-mtime-hide-ronly
    '''
    (STATIC METHODS)\n
    Actions and information about files.\n
    (READ FUNCTIONS DOCSTRING)

    GET INFORMATION:
    - exists
    - size
    - abspath
    - mdftime
    - acstime
    - content (read function)
    - is file
    - is dir
    - is readonly
    - is hidden

    ACTIONS:
    - remove
    - rename
    - move
    - copy
    - hide
    - read only
    - write
    '''
    @staticmethod
    def size(path):
        '''
        return size of the file in byte(s).
        Also work on directories.
        '''
        return os.path.getsize(path)
        #rooye pooshe emtehan she
    @staticmethod
    def remove(path):
        '''
        Use this to delete a file or a directory.
        '''
        if os.path.isfile(path):
            os.remove(path)
        else:
            shutil.rmtree(path)
    @staticmethod
    def rename(old_name,new_name):
        '''Rename files with this function.'''
        os.rename(old_name,new_name)
    @staticmethod
    def abspath(path):
        '''
        return absolute path of given path.
        '''
        return os.path.abspath(path)
    @staticmethod
    def exists(path):
        '''
        Search for the file And Returns a boolean.
        if file exists: True
        else: False
        '''
        return os.path.exists(path)
    @staticmethod
    def mdftime(path):
        '''
        Get last modify time of the file.
        '''
        return os.path.getmtime(path)
    @staticmethod
    def acstime(path):    
        '''
        Get last access time of the file.
        '''
        return os.path.getatime(path)
        # change to date bayad biad
    @staticmethod
    def move(src,dst):
        '''
        Move (cut) file from crs to dst.
        '''
        shutil.move(src,dst)
        #live_path= dst
        #Baraye folder hast ya na?
    @staticmethod
    def copy(path,dst):
        '''
        Copy the file from src to destination.
        (You can use it instead of rename too.
         e.g:
            copy('D:\\Test.py','E:\\Ali.py')
            (It copies Test.py to E drive and renames it to Ali.py)
         )
        '''
        if os.path.isdir(path):
            shutil.copytree(path,dst)
        else:
            shutil.copy(path,dst)
    @staticmethod
    def hide(path,mode=True):
        '''
        Hide file or folder.
        If mode==False: makes 'not hide'
        '''
        if mode:
            os.system("attrib -h "+path)
        else:
            subprocess.check_call(["attrib","+H",path])
    @staticmethod
    def read_only(path,mode=True):
        '''
        Make file attribute read_only.
        If mode==False: makes 'not read_only'
        '''
        if type(mode)==bool:
            from stat import S_IREAD,S_IWUSR
            if mode==True:
                os.chmod(path, S_IREAD)
            elif mode==False:
                os.chmod(path, S_IWUSR)
        else:
            raise Exception('Second argumant (mode) should be boolean.')
    @staticmethod
    def read(path):
        '''
        This can help you to read your file faster.
        Example:
            read('C:\\users\\Jack\\test.txt')
            ==> "Content of 'test.txt' will be shown."
        '''
        op= open(path,mode='r')
        FileR= op.read()
        op.close()
        return FileR
    @staticmethod
    def write(file,text=None,mode='replace',start=''):
        '''
        With this method you can change content of the file.  
        file:   File you want to change its content.
        content:   Content you want to add to file.
        mode:   Type of writing method.
            'continue' for add content to end of the file. 
            'replace' for overwriting to file content.
        start: I use this when I use mode='continue'
        '''
        if mode=='replace':
            op= open(path,mode='w')
            if text==None:
                text= input('Type what you want.\n\n')
            op.write(text)
            op.close()
        elif mode=='continue':
            '''opr= open(file,mode='r')
            FileR= opr.read()
            op= open(file,mode='w')'''
            op=open(path,'a')
            if text==None:
                text= input('Type what you want to add in the end of the file.\n\n')
            op.write(start+text)
            op.close() 
        else:
            raise ValueError('mode can only be: replace(default) or continue Not "{0}"'.format(mode))
    @staticmethod
    def isdir(path):
        return os.path.isdir(path)
    @staticmethod
    def isfile(path):
        return os.path.isfile(path)
    @staticmethod
    def is_readonly(path):
        '''
        Return True if path is readonly else False.
        (May Not Work in Linux)
        '''
        return subprocess.getoutput(f'dir /ar {path} >nul 2>nul && echo True || echo False')
    @staticmethod
    def is_hidden(path):
        """
        Check whether a file is presumed hidden, either because
        the pathname starts with dot or because the platform
        indicates such.
        Return True if File or Directory is hidden.
        (Work on both Linux and Windows)
        """
        import platform
        full_path = os.path.abspath(path)
        name = os.path.basename(full_path)
        def no(path):
        	return False
        platform_hidden = globals().get('is_hidden_' + platform.system(), no)
        return name.startswith('.') or platform_hidden(full_path)
    @staticmethod
    def is_hidden_Windows(path):
        import ctypes
        res = ctypes.windll.kernel32.GetFileAttributesW(path)
        assert res != -1
        return bool(res & 2)


class File:
    '''
    (CLASS METHODS)
    Actions and Information about files and directories.
    (READ METHODS DOCSTRING)
     if path exists:
         --  self.size - self.abspath - self.acstime - self.mdftime
     if path type is file:
         --  self.content
     if path type is directory:
         --  self.file_list - self.files - self.all_files - self.all_files_sep
     METHODS: 
     - copy
     - move
     - rename
     - hide
     - delete
     - read_only
    '''
    def __init__(self,path):
        self.path=    path
        self.live_path= path
        self.size=    None
        self.abspath= None
        self.acstime= None
        self.mdftime= None
        #self.content= None
        if files.exists(path):
            self.size= files.size(path)
            self.abspath= files.abspath(path)
            self.acstime= files.acstime(path)
            self.mdftime= files.mdftime(path)
            if __import__('platform').system()=='Windows':
             self.hidden= files.is_hidden(path)
            if os.path.isfile(path):
             self.type= 'file'
             self.content= files.read(path)
             if __import__('platform').system()=='Windows':
              self.readonly= files.is_readonly(path)
             else: self.readonly= 'UNKNOWN'
            if os.path.isdir(path):
             self.type='dir'                
             walk= os.walk(path)
             self.MEMBERS_all_sep= []  
             for i in walk: self.MEMBERS_all_sep.append(i)
             self.MEMBERS_files= self.MEMBERS_all_sep[0][2]   # only files in exact folder
             # All files of folder in ONE list:
             self.MEMBERS_files_all=[val for sublist in [[os.path.join(i[0], j) for j in i[2]] for i in os.walk(path)] for val in sublist]
             # All files of folder but SEPRATED in lists
             self.MEMBERS_files_all_sep=[[os.path.join(i[0], j) for j in i[2]] for i in os.walk(path)]

    def delete(self):
        '''
        Use this to delete a file or a directory.\n
        FOR STATIC USAGE USE 'remove()'
        '''
        files.remove(self.path)            
    def rename(self,new_name):
        '''
        Rename files with this function.\n
        FOR STATIC USAGE USE 'chname()'
        '''
        os.rename(self.path,new_name)
    def move(self,dst):
        '''
        Move (cut) file from crs to dst.
        '''
        shutil.move(self.path,dst)
        #self.live_path= dst
        #Baraye folder hast ya na?
    def copy(self,dst):
        '''
        Copy the file from src to destination.
        (You can use it instead of rename too.
         e.g:
            copy('D:\\Test.py','E:\\Ali.py')
            (It copies Test.py to E drive and renames it to Ali.py)
         )
        '''
        files.copy(self.path,dst)
    def hide(self,mode=True):
        '''
        Hide file or folder.
        If mode==False: makes 'not hide'
        '''
        files.hide(self.path,mode)
    def read_only(self,mode=True):
        '''
        Make file attribute read_only.
        If mode==False: makes 'not read_only'
        '''
        files.read_only(self.path,mode)


    #####
    # ext of file - 
    #####
