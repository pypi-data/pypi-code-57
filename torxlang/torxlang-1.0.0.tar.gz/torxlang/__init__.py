'''
This Module is One to Make Your Code Shorter.
High API Will Make You Feel You're Ordering And Machine Is Doing!
Also There is Collection of most usefull function and methods from popular modules of python.
(Read Help of Functions)
Official Documention Will Be Added Soon.
'''
'''
Written By RX
Last Update: 06-01-2020
'''
__version__='2.0.0'
# rxobject - Tuple object - record.reset() - record.lap() new parameter
# files.is_readonly - files.is_hidden


#START
import os,shutil,random,time,requests,re,socket,subprocess
import psutil
from typing import Any

__all__=['p','re','rev',
         'read','write',
         'wait','cls',
         'progressbar',
         'cons_int',
         'wait_for',
         'call_later',
        #Tuples:
         'force','erase',
         'insert','replace',
        #Classes
         'rand','system',
         'file','files',
         'style','record'
         'Tuple'
         ]

#######        8888888888                         888    d8b                                   ####### 
 #####         888                                888    Y8P                                    #####  
  ###          888                                888                                            ###   
   #           8888888 888  888 88888b.   .d8888b 888888 888  .d88b.  88888b.  .d8888b            #    
   #           888     888  888 888 "88b d88P"    888    888 d88""88b 888 "88b 88K                #    
  ###          888     888  888 888  888 888      888    888 888  888 888  888 "Y8888b.          ###   
 #####         888     Y88b 888 888  888 Y88b.    Y88b.  888 Y88..88P 888  888      X88         #####  
#######        888      "Y88888 888  888  "Y8888P  "Y888 888  "Y88P"  888  888  88888P'        ####### 

                                                                 
def p(text='',end='\n'):
    '''
    p is print!
    But because we use it a lot, we\'ve decided to make it one letter.
    Example:
        p('Hello World')
        ==>Hello World
    '''
    print(text,end=end)

def repeat(function,n: int):
    '''
    Repeat function for n times
    for more info see the example below.
    Example:
        re(Func_Name, 3)
        ==> "function Func_Name will launch 3 times."
    '''
    i=1
    while i <= n:
        i+=1
        function() 

def rev(var:Any):
    '''
    This function is for reversing Strings, Lists, Tuples And also Integers.
    Example:
        b= rev('Football')
        print(b)
        ==> llabtooF
    '''
    ret=var
    if type(ret)==int or type(ret)==float:
        ret= str(ret)
        ret= ret[::-1]
        if type(var)==int:
            ret= int(ret)
        else:
            ret=float(ret)
    else:
        ret= ret[::-1]
    return ret

def read(file):
    '''
    This can help you to read your file faster.
    Example:
        read_file('C:\\users\\Jack\\test.txt')
        ==> "Content of 'test.txt' will be shown."
    '''
    op= open(file,mode='r')
    FileR= op.read()
    op.close()
    return FileR
def write(file,text='',mode='replace',start=''):
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
        op= open(file,mode='w')
        op.write(text)
        op.close()
    elif mode=='continue':
        op=open(file,'a')
        op.write(start+str(text))
        op.close() 
    else:   
        print('Error\nmode can only be: 1-replace(default)  2-continue\nNot "{0}"'.format(mode)) 

def wait(seconds):
    '''
    Use this if you want your program wait for a certain time.
    Example:
        wait(3)
        ==> "Nothing happen and there will be no calculation for 3 seconds"
    '''
    import time
    time.sleep(seconds)
#__SQ_= 'powernrxbetfromporto'
def cls():
    '''
    You can use this function if you want to clear the environment.
    '''
    os.system('clear')

def progressbar(total=100,dashes_nom=100,delay=1,dashes_shape='-',complete_shape='█',pre_text='Loading: ',
                left_port='|',right_port='|'):
    '''
    Use this function to make a custom in-app progress bar.
    Example:
        progressbar(Total=100,Dashes_Nom=10,Time=1,Dashes_Shape='-',Complete_Shape='#', Pre_Text='Loading')
        ==>   Loading|####------| 40/100
    '''
    import sys
    def Progressbar(it, prefix="", size=60, file=sys.stdout):
        count = len(it)
        def show(j):
            x = int(size*j/count)
            file.write("%s%s%s%s%s %i/%i\r" % (prefix, right_port, complete_shape*x, dashes_shape*(size-x), left_port, j, count))
            file.flush()        
        show(0)
        for i, item in enumerate(it):
            yield item
            show(i+1)
        file.write("\n")
        file.flush()
    for i in Progressbar(range(total), pre_text, dashes_nom):
        wait(delay)

def cons_int(First_Nom:int, Last_Nom:int):
    '''
    Make string from First_Nom to Last_Nom.
    string('1','12')  ==> '123456789101112
    '''
    if type(First_Nom)==int and type(First_Nom)==type(Last_Nom):
        strin=''
        i=First_Nom
        for i in range(First_Nom,Last_Nom+1):
            strin= strin+str(i)
        return strin
    else:
        TypeError('Both Args Most Have int Type')

def wait_for(button):
    '''
    If You Want to Wait For the User to Press a Key (Keyboard or Mouse) Use This Function.
    '''
    if button.lower() in ('middle','left','right','back','forward'):
        if button.lower()[:1]=='b':
            button='x'
        if button.lower()[:1]=='f':
            button='x2'
        import mouse
        mouse.wait(button)
    else:
        import keyboard
        try:
            keyboard.wait(button)
        except:
            raise ValueError('Incorrect Button Name.')

def call_later(function,*args,delay=0.001):
    '''
    Do You Want to Call Your Function Later Even Between Other Operations?
    call_later() will help you to do that!
    First arg should be your function name,
    After That (*args) you can add any args that your function need,
    And Last arg is delay for calling your function in seconds.
    '''
    import keyboard
    keyboard.call_later(function,args,delay)

def convert_bytes(num:int) -> str :
    """
    Convert num to idiomatic byte unit.
    num is the input number (bytes).
    
    >>> convert_bytes(200)
    '200.0 bytes'
    >>> convert_bytes(6000)
    '5.9 KB'
    >>> convert_bytes(80000)
    '78.1 KB'
    """
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if num < 1024.0:
            return "%3.1f %s" % (num, x)
        num /= 1024.0





    
'''
import zipfile
from typing import Iterable,Text,Optional
def extract(file:Text, path:Optional[Text]=None,members:Optional[Iterable[Text]]=None, password:Optional[Text]='') -> None: 
    zipfile.ZipFile(file, 'r').extractall(path=path,members= members,pwd=password)
'''
'''
import pyautogui
def ActiveWindowTitle():
    return pyautogui.getActiveWindowTitle()

#import pyscreeze
def screenshot(image_name='Screenshot.png')
    return pyscreeze.screenshot(image_name)
'''


#######         .d8888b.   888  888                                                         #######
 #####         d88P  Y88b  888  888                                                          ##### 
  ###          888    888  888  888                                                           ###  
   #           888         888  888   8888b.   .d8888b   .d8888b    .d88b.   .d8888b           #   
   #           888         888  888      "88b  88K       88K       d8P  Y8b  88K               #
  ###          888    888  888  888  .d888888  "Y8888b.  "Y8888b.  88888888  "Y8888b.         ###  
 #####         Y88b  d88P  888  888  888  888       X88       X88  Y8b.           X88        ##### 
#######         "Y8888P"   888  888  "Y888888   88888P'   88888P'   "Y8888    88888P'       #######


from .Filex import *
from .Tuple_tools import *
from .RX_obj import *
from .System import *
#from .Date_Time import *

class rand:
    '''
    Random Variable Generator Class.
    '''
    @staticmethod
    def choose(iterator,k: int =1,duplicate=True):
        '''
        Return a random element from a non-empty sequence.
        '''
        if k==1:
            return random.choice(iterator)
        elif k>1:
            if duplicate:
                return random.choices(iterator,k=k)
            else:
                return random.sample(iterator,k=k)
        else:
            raise ValueError('k Must Be Higher 0')
        
    @staticmethod
    def integer(first_number,last_number):
        '''
        Return random integer in range [a, b], including both end points.
        '''
        return random.randint(first_number,last_number)
    @staticmethod
    def O1(decimal_number=17):
        '''
        return x in the interval [0, 1)
        '''
        return round(random.random(),decimal_number)
    @staticmethod
    def number(first_number,last_number):
        '''
        return x in the interval [F, L]
        '''
        return random.uniform(first_number,last_number)


'''
class Math:
    def sqrt(number):
        import math
        return math.sqrt(number)
'''

class style:
    '''
    This class is for Changing text Color,BG & Style.
    - style.print  to customize your print.
    - style.switch to change terminal colors.
    - style.switch_default for making everything default.
    '''
    def __init__(self,text,color='default',BG='black'):
        from colored import fg,bg,attr
        try: color= color.lower();BG=BG.lower()#;style=style.lower()
        except:pass        
        if color=='default':
            color=7 #188
        self.text= text     
        self.content= f"{fg(color)}{bg(BG)}{text}{attr(0)}"
    def __str__(self):
        return self.content
    def __repr__(self):
        return self.content
    def __add__(self,other):
        #print(type(other))
        if type(other)!=style:
            return self.content+other
        else:
            return self.content+other.content
    def __mul__(self,nom):
        return self.content*nom
    def __getitem__(self,index):
        return self.text[index]


    @staticmethod
    def print(text='',color='default',BG='black',style='None',end='\n'):
        '''
        text(text='Hello World',color='red',BG='white')
        output ==> 'Hello World' (With red color and white BG)
        Styles: bold - underline - reverse - hidden
         *bold and underline may not work. (Depends on terminal and OS)
        '''
        from colored import fg,bg,attr
        try: color= color.lower();BG=BG.lower();style=style.lower()
        except:pass
        if color=='default':
            color=7 #188
        if style=='none':
            style=0
        if text=='':
            print('%s%s%s' % (attr(style),bg(BG),fg(color)),end=end)
        else:
            print('%s%s%s%s%s' % (attr(style),bg(BG),fg(color),text,attr(0)),end=end)
    @staticmethod
    def switch(color='default',BG='black',style='None'):
        '''
        Change color,BG and style untill you call it again and change them.
        '''
        try: color= color.lower();BG=BG.lower();style=style.lower()
        except:pass        
        if style=='none':
            style=0
        if color=='default':
            color=7
        from colored import fg,bg,attr
        print('%s%s%s' % (attr(style),bg(BG),fg(color)),end='')
    @staticmethod
    def switch_default():
        '''Switch Terminal Attributes to its defaults'''
        from colored import attr
        print('%s' % (attr(0)),end='')


class record:
    '''
    Use this method to record an action time in second.
    Usage:
        Start= record()
        #Some codes here...
        Finnish= Start.lap()
        print(Finnish) ==> 0.25486741
        #Some more codes here...
        Finnish= Start.lap() ==> 0.4502586
        Start.laps -->  [0.25486741, 0.4502586]
    Use Start.stop() to finnish recording and save memory.
    (after self.stop() using self.lap will cause error.)
    '''
    def __init__(self):
        self.__start= time.time()
        self.__end__=False
        self.laps=[]
    def __str__(self):
        if not self.__end__:
            running=True
        else:
            running=False
        return f'Running={str(running)} \nLaps: {self.laps}'
    def __repr__(self):
        if not self.__end__:
            running=True
        else:
            running=False
        return f'Running={str(running)} \nLaps: {self.laps}'

    class EndError(Exception):
        def __init__(self, message='Recording Has Been Finnished. Can Not Add a Lap.'):
            super().__init__(message)
    def lap(self,save=True):
        '''
        Return time passed from creating time of self.
        (Read 'record' Doc String)
        If save is True, time will be added to self.laps
        '''        
        if not self.__end__:
            lp= time.time()-self.__start
            if save:
                self.laps.append(lp)
            return lp
        else:
            raise self.EndError
    def stop(self):
        self.__end__=True
        '''del self
        return self.laps'''
    def reset(self,reset_start= False):
        '''
        This will erase self.laps 
        If reset_start is True, start time will reset too.
        '''
        self.laps= []
        if reset_start: self.__start= time.time()

#END
