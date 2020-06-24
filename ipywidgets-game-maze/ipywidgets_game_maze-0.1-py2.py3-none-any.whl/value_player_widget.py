from enum import Enum
import ipywidgets
from functools import partial 
from ipywidgets import HBox, VBox ,Layout
PlayDirection = Enum('PlayDirection','Forward Backward None')
from threading import *
from .timer import PerpetualTimer
from traitlets import *
import locale

__version__ = '0.1'

global translation
translation = {'fr_FR':{'time':'Temps :', 'speed':'Vitesse :'},'en_EN':{'time':'Time :', 'speed':'Speed :'}}

class Player(HasTraits) :
        time=Int()

        def run(self):
            self.timer.run()
        
        def update(self):
            self.slider_time.value=self.time
            self.view.value= self.history[self.time]
        def get_value(self):
            
            return self.history[len(self.history)-1]
        
        def set_value(self,value): 
            if (len(self.history) > 10000):
                raise RuntimeError("Votre programme a pris plus de 1000 étapes")
            self.history.append(value)
            self.slider_time.max=len(self.history)-1
            if ( not self.timer.running() and self.time == len(self.history) -2):
                self.time=self.time+1
                self.update()
        
        def tick(self):
            if(self.play_direction == PlayDirection.Forward ):  
                self.step_forward()
            else:
                self.step_backward()
        
        def reset(self,value):      
                self.time=0
                self.history=[value]
                self.slider_time.max=len(self.history)-1
                self.update()
        
        def begin(self):
            self.time=0
            
            self.update()
        
        def end(self):
            self.time= len(self.history)-1  
            self.update()

        def step_backward(self):
            if( self.time >0):
                self.time=self.time-1
                self.update()
        def step_forward(self):
            if( self.time <len(self.history)-1):  
                self.time=self.time+1
                self.update()        
        def backward (self):
            self.play_direction = PlayDirection.Backward # a check
            self.timer.set_fps(self.play_fps)
        
        def play(self):
            self. play_direction = PlayDirection.Forward # a check
            self.timer.set_fps(self.play_fps)
            self.timer.run()

        def pause(self):
            self.play_direction=None
            self.timer.cancel()
            #self.timer.set_fps(0)
        
        def set_fps(self,fps):
            self.play_fps=fps
            if(self.play_direction != None):
                self.timer.set_fps(fps)
        
        def won(self):
            return self.history[len(self.history)-1].won()

        def set_time(self,tps):  
            self.time=tps
            

        def __init__(self, _view, language=None):
            if not(language in translation):
                self.language=locale.getdefaultlocale()[0]
            else:
                self.language=language
            self.view = _view
            self.original_value=self.view.value
            self.play_direction=PlayDirection.Forward
            self.play_fps=1
            
            self.timer =PerpetualTimer( self.play_fps,self.tick )
            self.history=[]
            self.time=0
           
            
            
            self.slider_time=ipywidgets.IntSlider(
                value=self.time,
                min=0,
                max=0,#len(self.history),
                step=1,
                description=translation[self.language]['time']
            )
            self.reset(self.original_value)
                
            
            def on_value_change(change):
                self.time=change['new']
                self.update()
            self.slider_time.observe(on_value_change,names='value')
            #@observe('value')
            #def _value_changed(self,change):
            #    self.set_value(change)

class PlayerView(VBox):
    #link((slider_time,'value'),(player,'time'))
    #link trailest.link
    #player_trait=Instance(Player)
    #time = Delegate('player_trait')

    # def _time_changed (self,old,new):
    #     self.slider_time.value=self.time

    def set_value(self,value):
        self.player.set_value(value)
    def __init__(self,player):
        
        self.widget=ipywidgets.HTML(
        value="",
        placeholder='',
        description='',
        )
        output = ipywidgets.Output()
        self.player=player
        

        def fast_backward_clicked(b):
            with output:
                self.player.begin()
                self.player.pause()
            
        def backward_clicked(b):
            with output:
                self.player.backward()
        def step_backward_clicked(b):
            with output: 
                self.player.pause()
                self.player.step_backward()
        def pause_clicked(b):
            with output:
                self.player.pause()
        def step_forward_clicked(b):
            with output:
                self.player.pause()
                self.player.step_forward()

        def play_clicked(b):
            with output:
                self.player.play()
        def fast_forward_clicked(b):
            with output:
                self.player.pause()
                self.player.end()
                            
        # self.slider_time=ipywidgets.IntSlider(
        # value=0,
        # min=0,
        # max=len(self.player.history),
        # step=1,
        #     description="time:"
        # )

        

        slider=ipywidgets.FloatSlider(
        value=1.0,
        min=0.0,
        max=6.0,
        step=1,
            description=translation[self.player.language]['speed']
        )
        # 2puissance speed affiché ou alors nous affiché juste la valeur et pas "speed " 2** = puissance 
        def on_value_change(change):
            value=int (change['new'])
            self.player.set_fps(2**value)
        
        slider.observe(on_value_change, names='value')

        play= ipywidgets.Button(description="",icon='play',layout=Layout(width='35px'))
        fast_backward= ipywidgets.Button(description="",icon='fast-backward',layout=Layout(width='35px'))
        backward= ipywidgets.Button(description="",icon='backward',layout=Layout(width='35px'))
        step_backward= ipywidgets.Button(description="",icon='step-backward',layout=Layout(width='35px'))
        pause= ipywidgets.Button(description="",icon='pause',layout=Layout(width='35px'))
        step_forward= ipywidgets.Button(description="",icon='step-forward',layout=Layout(width='35px'))
        fast_forward= ipywidgets.Button(description="",icon='fast-forward',layout=Layout(width='35px'))

        play.on_click(play_clicked)
        fast_backward.on_click(fast_backward_clicked)
        backward.on_click(backward_clicked)
        step_backward.on_click(step_backward_clicked)
        pause.on_click(pause_clicked)
        step_forward.on_click(step_forward_clicked)
        fast_forward.on_click(fast_forward_clicked)

        self.affichage=ipywidgets.HBox([fast_backward,backward,step_backward,pause,step_forward,play,fast_forward,slider])
        VBox.__init__(self,[self.player.view,self.player.slider_time,self.affichage])
        #link((self.slider_time,'value'),(self.player,'time'))

        #self.widget_affichage=VBox([self.player.view,self.slider_time,self.affichage])
        #self.player.time=0
        self.player=player
    
def ValuePlayerWidget(visualisation, language=None):
    player=Player(visualisation,language)
    app=PlayerView(player) 
  
    return app