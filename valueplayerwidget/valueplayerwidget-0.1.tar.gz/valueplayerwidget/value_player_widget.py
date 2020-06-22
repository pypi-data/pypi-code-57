from enum import Enum
import ipywidgets
from functools import partial 
from ipywidgets import HBox, VBox ,Layout, Label
PlayDirection = Enum('PlayDirection','Forward Backward None')
from threading import *
from .timer import PerpetualTimer
from traitlets import *
import locale

global translation
translation = {'fr_FR':{'time':'Temps :', 'speed':'Vitesse :'},'en_EN':{'time':'Time :', 'speed':'Speed :'}}

__version__ = '0.1'

class Player(HasTraits) :
    """
        A Player keep an history of the _view values so the user may check the steps leading to a final result
    """
    time=Int()
    action=traitlets.Unicode()
        
    def __init__(self, _view, language=None):
        """
            The Player's initialization
            
            Parameters
            ----------
            _view : (type: traitlets) the visualisation to display and control
            language : (default value=None) the labels'language
            
            Tests
            ----------
            >>> from ipywidgets import IntSlider
            >>> slider=IntSlider(value=24)
            >>> player=Player(slider)
            >>> player.view==slider
            True
            >>> player.original_value
            24
            >>> player.play_fps
            1
            >>> player.history
            [24]
            >>> player.actionHistory
            ['']
            >>> player.time
            0
            >>> player.playing
            True
            >>> player.pause()
            
        """
        ## If no language is specified, we set it to the system's language
        self.language='en_EN'
        if not(language in translation):
            if locale.getdefaultlocale()[0] in translation:
                self.language=locale.getdefaultlocale()[0]
        else:
            self.language=language
            
        self.view = _view
        self.original_value=self.view.value
        self.play_direction=PlayDirection.Forward
        self.play_fps=1
        
        self.timer =PerpetualTimer( self.play_fps,self.tick )
        self.history=[]
        self.actionHistory=[]
        self.time=0
        self.playing=True
                   
        style = {'description_width': 'initial'}    
        self.slider_time=ipywidgets.IntSlider(
            value=self.time,
            min=0,
            max=0,#len(self.history),
            step=1,
            description=translation[self.language]['time'],
            style=style
        )
        self.reset(self.original_value)
            
        # Slider to control which step to display
        def on_value_change(change):
            self.time=change['new']
            self.update()
        self.slider_time.observe(on_value_change,names='value')
    
    def run(self):
        """
            Run the timer
            
            Tests
            ----------
            >>> from ipywidgets import IntSlider
            >>> slider=IntSlider(value=24)
            >>> player=Player(slider)
            >>> player.pause()
            >>> player.timer.isrunning
            False
            >>> player.run()
            >>> player.timer.isrunning
            True
            >>> player.pause()
            
        """
        self.timer.run()
    
    def update(self):
        """
            Update the Player's value and action according to self.time
            
            Tests
            ----------
            >>> from ipywidgets import IntSlider
            >>> slider=IntSlider(value=24)
            >>> player=Player(slider)
            >>> player.set_value(12)
            >>> slider.value
            24
            >>> player.set_value(78)
            >>> player.time = 2
            >>> player.update()
            >>> slider.value
            78
            >>> player.pause()
            
        """
        self.slider_time.value=self.time
        self.view.value= self.history[self.time]
        if len(self.actionHistory)>self.time:
            self.action=self.actionHistory[self.time]
    
    def get_value(self):
        """
            Get the last value in the history
            
            Tests
            ----------
            >>> from ipywidgets import IntSlider
            >>> slider=IntSlider(value=24)
            >>> player=Player(slider)
            >>> player.get_value()
            24
            >>> player.pause()
            
        """
        return self.history[len(self.history)-1]
    
    def set_action(self,newAction):
        """
            Add a new action to the history
            
            Tests
            ----------
            >>> from ipywidgets import IntSlider
            >>> slider=IntSlider(value=24)
            >>> player=Player(slider)
            >>> player.set_action("New action done")
            >>> player.action
            'New action done'
            >>> player.actionHistory
            ['', 'New action done']
            >>> player.pause()
            
        """
        if (len(self.actionHistory) > 10000):
            raise RuntimeError("Votre programme a pris plus de 1000 étapes")
        self.action=newAction
        self.actionHistory.append(newAction)
    
    def set_value(self,value): 
        """
            Add a new value to the history
            
            Tests
            ----------
            >>> from ipywidgets import IntSlider
            >>> slider=IntSlider(value=24)
            >>> player=Player(slider)
            >>> t=player.slider_time.max
            >>> player.time
            0
            >>> player.set_value(45)
            >>> player.history
            [24, 45]
            >>> player.slider_time.max == t+1
            True
            >>> player.pause()
            
        """
        if (len(self.history) > 10000):
            raise RuntimeError("Votre programme a pris plus de 1000 étapes")
        self.history.append(value)
        self.slider_time.max=len(self.history)-1
        if ( not self.timer.running() and self.time == len(self.history) -2):
            self.time=self.time+1
            self.update()
    
    
    def tick(self):
        """
            Make the timer either increase or decrease
            
            Tests
            ----------
            >>> from ipywidgets import IntSlider
            >>> slider=IntSlider(value=24)
            >>> player=Player(slider)
            >>> player.set_value(23)
            >>> player.time
            0
            >>> player.tick()
            >>> player.time
            1
            >>> player.pause()
            
        """
        if(self.play_direction == PlayDirection.Forward ):  
            self.step_forward()
        else:
            self.step_backward()
    
    def reset(self,value):    
        """
            Reset the Player and set its first value to 'value'
            
            Parameter
            -----------
            value : (type=any) first value in the history
            
            Tests
            ----------
            >>> from ipywidgets import IntSlider
            >>> slider=IntSlider(value=24)
            >>> player=Player(slider)
            >>> player.set_value(46)
            >>> player.set_value(74)
            >>> player.reset(0)
            >>> player.time
            0
            >>> player.history
            [0]
            >>> player.actionHistory
            ['']
            >>> player.slider_time.max
            0
            >>> slider.value
            0
            >>> player.pause()
            
        """
        self.time=0
        self.history=[value]
        self.actionHistory=['']
        self.slider_time.max=len(self.history)-1
        self.update()
    
    def begin(self):
        """
            Set the Player to the first step
            
            Tests
            ----------
            >>> from ipywidgets import IntSlider
            >>> slider=IntSlider(value=24)
            >>> player=Player(slider)
            >>> player.set_value(13)
            >>> player.set_value(47)
            >>> player.tick()
            >>> player.tick()
            >>> player.update()
            >>> slider.value
            47
            >>> player.time
            2
            >>> player.begin()
            >>> slider.value
            24
            >>> player.time
            0
            >>> player.pause()
            
        """
        self.time=0
        self.update()
    
    def end(self):
        """
            Set the Player to the last step
            
             Tests
            ----------
            >>> from ipywidgets import IntSlider
            >>> slider=IntSlider(value=24)
            >>> player=Player(slider)
            >>> player.set_value(13)
            >>> player.set_value(47)
            >>> player.time
            0
            >>> slider.value
            24
            >>> player.end()
            >>> slider.value
            47
            >>> player.time
            2
            >>> player.pause()
            
        """
        self.time= len(self.history)-1  
        self.update()

    def step_backward(self):
        """
            Set the Player to the previous step
            
             Tests
            ----------
            >>> from ipywidgets import IntSlider
            >>> slider=IntSlider(value=24)
            >>> player=Player(slider)
            >>> player.set_value(13)
            >>> player.set_value(47)
            >>> player.step_backward()
            >>> player.time
            0
            >>> slider.value
            24
            >>> player.end()
            >>> player.step_backward()
            >>> slider.value
            13
            >>> player.time
            1
            >>> player.pause()
            
        """
        if( self.time >0):
            self.time=self.time-1
            self.update()
            
    def step_forward(self):
        """
            Set the Player to the next step
            
             Tests
            ----------
            >>> from ipywidgets import IntSlider
            >>> slider=IntSlider(value=24)
            >>> player=Player(slider)
            >>> player.set_value(13)
            >>> player.set_value(47)
            >>> player.step_forward()
            >>> slider.value
            13
            >>> player.time
            1
            >>> player.end()
            >>> player.step_forward()
            >>> slider.value
            47
            >>> player.time
            2
            >>> player.pause()
            
        """
        if( self.time <len(self.history)-1):  
            self.time=self.time+1
            self.update()        
            
    def backward (self):
        """
            Timer's steps will decrease
        """
        self.play_direction = PlayDirection.Backward # a check
        self.timer.set_fps(self.play_fps)
        self.play()
    
    def forward(self):
        """
            Timer's step will increase
        """
        self.play_direction = PlayDirection.Forward # a check
        self.timer.set_fps(self.play_fps)
        self.play()
    
    def play(self):
        """
            Start the Player's timer
        """
        #self. play_direction = PlayDirection.Forward # a check
        self.timer.set_fps(self.play_fps)
        self.playing=True
        self.timer.run()

    def pause(self):
        """
            Stop the Player's timer
        """
        #self.play_direction=None
        self.timer.cancel()
        self.playing=False
    
    
    def set_fps(self,fps):
        """
            Set the FPS
            
            Parameter
            ----------
            fps : (type=int) new FPS value
            
        """
        self.play_fps=fps
        if(self.play_direction != None):
            self.timer.set_fps(fps)
    
    #def won(self):
    #    return self.history[len(self.history)-1].won()

    def set_time(self,tps): 
        """
            Set the Player's time
            
            Parameter
            ----------
            tps : (type=int) new time
            
             Tests
            ----------
            >>> from ipywidgets import IntSlider
            >>> slider=IntSlider(value=24)
            >>> player=Player(slider)
            >>> player.set_value(13)
            >>> player.set_value(47)
            >>> player.set_value(99)
            >>> player.set_time(3)
            >>> player.update()
            >>> slider.value
            99
            >>> player.time
            3
            >>> player.pause()
            
        """
        self.time=tps


class PlayerView(VBox):
    """
        The Player's visualisation
    """
    def __init__(self,player,buttons=[]):
        """
            Initialization of PlayerView
            
            Parameters
            ----------
            player : (type=Player) the Player we make the visualisation for
            buttons : (default value=[]) (type=list) the list of action buttons we have to make
            
        """
        self.widget=ipywidgets.HTML(
        value="",
        placeholder='',
        description='',
        )
        output = ipywidgets.Output()
        self.player=player
        
        # on_clicked functions to control the timer
        def fast_backward_clicked(b):
            with output:
                self.player.begin()
                self.player.pause()
                self.color(b)
                self.pause.icon='play'
            
        def backward_clicked(b):
            with output:
                self.slider.value=0
                self.color(b)
                self.pause.icon='pause'
                self.player.backward()
                
        def step_backward_clicked(b):
            with output: 
                self.player.pause()
                self.player.step_backward()
                self.color(b)
                self.pause.icon='play'

        def step_forward_clicked(b):
            with output:
                self.player.pause()
                self.player.step_forward()
                self.color(b)
                self.pause.icon='play'


        def pause_clicked(b):
            with output:
                if self.player.playing:
                    self.player.pause()
                    self.color(b)
                    b.icon='play'
                else:
                    self.player.play()
                    self.color(b)
                    b.icon='pause'
                    
        
        def fast_forward_clicked(b):
            with output:
                self.player.pause()
                self.player.end()
                self.color(b)
                self.pause.icon='play'
                
        def forward_clicked(b):
            with output:
                self.slider.value=0
                self.color(b)
                self.pause.icon='pause'
                self.player.forward()
        
        def speed_forward_clicked(b):
            with output:
                if self.player.play_direction==PlayDirection.Forward:
                    self.slider.value+=1
                else:
                    self.player.forward()
                    self.slider.value=1
                self.color(b)
                self.pause.icon='pause'
        
        def speed_backward_clicked(b):
            with output:
                if self.player.play_direction==PlayDirection.Forward:
                    self.player.backward()
                    self.slider.value=1
                else:
                    self.slider.value+=1
                self.color(b)
                self.pause.icon='pause'
                
                
        
        ## Speed slider
        style = {'description_width': 'initial'}
        self.slider=ipywidgets.FloatSlider(
        value=1.0,
        min=0.0,
        max=6.0,
        step=1,
            description=translation[self.player.language]['speed'],
        style=style
        )
        # when the slider's value changes, the fps of the timer change 
        def on_value_change(change):
            value=int (change['new'])
            self.player.set_fps(2**value)
        
        self.slider.observe(on_value_change, names='value')
        
        # Buttons for the timer
        self.speed_forward= ipywidgets.Button(description="",icon='forward',layout=Layout(width='35px'))  
        self.speed_backward= ipywidgets.Button(description="",icon='backward',layout=Layout(width='35px')) 
        
        self.forward= ipywidgets.Button(description="",icon='chevron-right',layout=Layout(width='35px')) 
        self.backward= ipywidgets.Button(description="",icon='chevron-left',layout=Layout(width='35px'))
        
        self.pause= ipywidgets.Button(description="",icon='pause',layout=Layout(width='35px'))
        
        self.fast_backward= ipywidgets.Button(description="",icon='fast-backward',layout=Layout(width='35px'))
        self.fast_forward= ipywidgets.Button(description="",icon='fast-forward',layout=Layout(width='35px'))
        
        self.step_backward= ipywidgets.Button(description="",icon='step-backward',layout=Layout(width='35px'))
        self.step_forward= ipywidgets.Button(description="",icon='step-forward',layout=Layout(width='35px'))
        
        # on_click function for the timer's buttons
        self.pause.on_click(pause_clicked)
        self.fast_backward.on_click(fast_backward_clicked)
        self.backward.on_click(backward_clicked)
        self.forward.on_click(forward_clicked)
        self.step_backward.on_click(step_backward_clicked)
        self.step_forward.on_click(step_forward_clicked)
        self.fast_forward.on_click(fast_forward_clicked)
        self.speed_forward.on_click(speed_forward_clicked)
        self.speed_backward.on_click(speed_backward_clicked)
        
        
        self.buttonList=[self.pause, self.fast_backward, self.backward, self.forward, self.step_backward, self.step_forward, self.fast_forward, self.speed_forward, self.speed_backward]
        
        for b in self.buttonList:
            b.style.button_color='WhiteSmoke'
       
        
        
        # action label
        actionHead=ipywidgets.Label(value=" Action : ")
        actionLabel=ipywidgets.Label(value=self.player.action)
        actionBox=HBox([actionHead,actionLabel])#,layout=ipywidgets.Layout(justify_content="center"))
        
        # When the player's action changes, the display is updated
        def on_action_change(change):
            actionLabel.value=change['new']
        
        traitlets.link([actionLabel, "value"], [self.player,"action"])
        
        # Action Buttons
        buttonTab=[]
        for tab in buttons :
            mytab=[]
            for act in tab:
                mytab.append(self.mk_button(*act))
            buttonTab.append(VBox(mytab))
            
        buttonBox=HBox(buttonTab)
        # Initialization as a VBox
        self.affichage=ipywidgets.HBox([self.fast_backward,self.speed_backward,self.backward,self.step_backward,self.pause,self.step_forward,self.forward,self.speed_forward,self.fast_forward,actionBox])
        upBox=HBox([self.player.slider_time,self.slider])
        VBox.__init__(self,[self.player.view,upBox,self.affichage,buttonBox])
    
    def color(self,myButton):
        for b in self.buttonList:
            if b.icon != myButton.icon:
                b.style.button_color='WhiteSmoke'
            else:
                b.style.button_color='#D3D3D3'
        #myButton.style.button_color='#D3D3D3'

    def set_value(self,value):
        """
            Set the value of the Player
            
            Parameter
            ----------
            value :(type=any) new value for Player
            
        """
        self.player.set_value(value)
    
    def pause(self):
        """
            Stop the player
        """
        self.player.pause()
    
    def mk_button(self, action, func, *args):
        """ Make an action button """
        name=action
        button = ipywidgets.Button(description=name)
        output = ipywidgets.Output()
        def on_button_clicked(b):
            with output:
                self.set_value(func(*args))
                self.player.set_action(name)
        button.on_click(on_button_clicked)
        return button

    
def ValuePlayerWidget(visualisation, actions=[], language=None):
    """
        Returns a PlayerView 
        
        Parameters
        -----------
        visualisation : (type=traitlets) the visualisation we link the player with
        buttons : (type=list) a list of lists. Each inside list is meant to be a VBox of buttons. Each element of the list has to be under the format (name, function) or (name, function, value). 'name' specifies the name of the action, 'function' is the function the buttons must execute when clicked (function must return a value for player.value), 'value' is not obligatory, it is the given value to 'function'
        language : (type=None) language for displayed labels
        
    """
    player=Player(visualisation,language)
    app=PlayerView(player, actions) 
    return app
