# get the general noisetagging framework
from noisetag import Noisetag
from utopiaclient import TimeStampClock

# graphic library
import pyglet
isi=1/60
drawrate=0 # rate at which draw is called


class Screen:
    '''Screen abstract-class which draws stuff on the screen until finished'''
    def __init__(self,window):
        self.window=window
    def draw(self,t):
        '''draw the display, N.B. NOT including flip!'''
        pass
    def is_done(self):
        '''test if this screen wants to quit'''
        return False


class InstructionScreen(Screen):
    '''Screen which shows a textual instruction for duration or until key-pressed'''
    def __init__(self,window,text,duration=5000,waitKey=True):
        super().__init__(window)
        self.tsc=None # timer for the duration
        self.duration=duration
        self.waitKey=waitKey
        self.isRunning=False
        self.clearScreen=True
        # initialize the instructions screen
        self.instructLabel=pyglet.text.Label(x=window.width//2,y=window.height//2,anchor_x='center',anchor_y='center',font_size=24,color=(255,255,255,255),multiline=True,width=int(window.width*.8))
        self.set_text(text)
        print("Instruct (%dms): %s"%(duration,text))

    def set_text(self,text):
        '''set/update the text to show in the instruction screen'''
        if type(text) is list:
            text = "\n".join(text)
        self.instructLabel.begin_update()
        self.instructLabel.text=text
        self.instructLabel.end_update()

    def is_done(self):
        # check termination conditions
        isDone=False
        if not self.isRunning :
            return False
        if self.waitKey :
            global last_key_press
            if last_key_press :
                self.key_press=last_key_press
                isDone=True
                last_key_press=None
        if self.tsc.getTime() > self.duration :
            isDone=True
        return isDone
        
    def draw(self,t):
        '''Show a block of text to the user for a given duration on a blank screen'''
        if not self.isRunning :
            self.tsc=TimeStampClock()
            self.isRunning=True # mark that we're running
        if self.clearScreen:
            self.window.clear()
        self.instructLabel.draw()
