import os
import ipywidgets as widgets
from ipycanvas import Canvas, hold_canvas, MultiCanvas
from .SingleJug import SingleJug
from .Visua import Visua
import traitlets
from .value_player_widget import ValuePlayerWidget

global translation
translation={'en_EN':{'language':'english','drop1':'Capacity 1','drop2':'Capacity 2','fill':'Fill','empty':'Empty','pour':'Pour','launch':'Launch','image':os.path.dirname(__file__)+"/"+'images/win.jpg', 'locale':'en_EN'}, 
             'fr_FR':{'language':'français','drop1':'Capacité 1','drop2':'Capacité 2','fill':'Remplir','empty':'Vider','pour':'Verser','launch':'Valider','image':os.path.dirname(__file__)+"/"+'images/gagne.jpg', 'locale':'fr_FR'}}


def mkImageWidget(file_name, im_format,w=50,h=50):
    """ Return an object widget.Image displaying the image titled file_name
        
        Parameters
        ----------
        file_name : (type=string) image file name
        im_format : (type=string) format of the file
        w : (default value=50) (type=int) image width
        h : (default value=50) (type=int) image height
        
    """
    assert isinstance(file_name, str), "file_name doit être un string"
    assert isinstance(im_format, str), "im_format doit être un string"
    file=open(os.path.dirname(__file__)+"/"+file_name,"rb")
    image=file.read()
    return widgets.Image(
            value=image,
            format=im_format,
            width=w,
            height=h,
            layout=widgets.Layout(border="none", margin="0px", padding="0 px")
        )

class Jugs(widgets.VBox):
    """ This class contains both the visualisation and the SingleJug objects. You may interact with the game by using buttons or executing the class'methods. 
        
    Readable attributes
    ----------
    v1 : The Canvas and the information
    player : ValuePlayerWidget containing v1
    jugs : a list containing the two objects SingleJug of the game
    obtained : a list of boolean indicating which volumes have already been obtained
    """
    value = traitlets.List()
    
    def __init__(self, capacity1=None, capacity2=None, UI=False, lang='en_EN'):
        """ Game's initialisation : set the jugs'capacities, the language and creates the action buttons and the visualisation
        
        Parameters
        ----------
        capacity1 : (default value=None) (type=int) Set the capacity of the first jug. It has to belong to [0,10] otherwise it is set to 5
        capacity2 : (default value=None) (type=int) Set the capacity of the second jug. It has to belong to [0,10] otherwise it is set to 7
        UI : (default value=False) (type=boolean) Set wether the player may use the buttons to play (UI=True) or has to call the methods(UI=False)
        lang : (default value='en') (type=string) Set the game's language. Available languages : english ('en') and french ('fr')
        
        Tests
        ----------
        >>> jugs=Jugs()
        >>> jugs.jugs[0].capacity
        5
        >>> jugs.jugs[1].capacity
        7
        >>> jugs.obtained
        [True, False, False, False, False, False, False, False]
        >>> jugs2=Jugs(1,3)
        >>> jugs2.jugs[0].capacity
        1
        >>> jugs2.jugs[1].capacity
        3
        >>> jugs.player.player.pause()
        >>> jugs2.player.player.pause()
        
        """     
        
        assert (isinstance(capacity1, int) or capacity1==None), "capacity1 has to be an int"
        assert (isinstance(capacity2, int) or capacity2==None), "capacity1 has to be an int"
        # Translation in French and English
        #self.__translation={'en':{'language':'english','drop1':'Capacity 1','drop2':'Capacity 2','fill':'Fill','empty':'Empty','pour':'Pour','launch':'Launch','image':'images/win.jpg', 'locale':'en_EN'}, 'fr':{'language':'français','drop1':'Capacité 1','drop2':'Capacité 2','fill':'Remplir','empty':'Vider','pour':'Verser','launch':'Valider','image':'images/gagne.jpg', 'locale':'fr_FR'}}
        
        # Set the language
        if not(lang in translation) :
            print("This language isn't available yet : english by default. \n Please choose a language in the following list :")
            for l in translation:
                print(l +" : "+translation[l]['language'])
            self.__language='en'
        else:
            self.__language=lang
            
        # Set the jugs'capacities
        if capacity1==None or capacity2==None or capacity1<0 or capacity1>10 or capacity2<0 or capacity2>10:
            # Invalid capacities given in parameters or no given capacities
            self.__jugs=[SingleJug(5), SingleJug(7)]
            self.__display_dropdown=True
        else:
            self.__jugs=[SingleJug(capacity1), SingleJug(capacity2)]
            self.__display_dropdown=False
            
        # Indicate how much water the jugs contain
        self.__information=[widgets.Label(value=str(self.__jugs[0].volume)+" / "+str(self.__jugs[0].capacity)), widgets.Label(value=str(self.__jugs[1].volume)+" / "+str(self.__jugs[1].capacity))]
        
        # Hold some place for the future winning message
        self.__message=mkImageWidget("images/blanc.jpg", "jpg",380,5)
        
        # All the coordonates we need to draw the water inside de jugs
        self.__coef=25
        self.__w=120
        self.__x1=50
        self.__x2=self.__x1+self.__w+65
        self.__y2=20
        self.__y1=self.__y2 + self.__coef * (self.__jugs[1].capacity - self.__jugs[0].capacity)
        self.__width=400
        self.__height=self.__y2+self.__coef*11
        self.__left=(5,20)
        self.__right=(30,45)
        
        # The canvas has two layers : one for the edges and graduation and one for the water
        self.__canvas = MultiCanvas(2, width=self.__width, height=self.__height)
        self.__canvas[0].line_width = 3
        
        # List of the volumes we already had
        self.__obtained=[False for i in range (0,max(self.__jugs[0].capacity,self.__jugs[1].capacity)+1)]
        self.__obtained[0]=True

        # Initialize self.__obtained and self._reussiLab
        self.reset_obtained()
        
        
        # Initialize self.__value for ValuePlayerWidget
        self.__value=self.mk_value()
        
        # Indicate the action
        self.__action=widgets.Label(value="")
        self.update_action()
        
        # The visualization we give to ValuePlayerWidget
        affichage=widgets.VBox([self.__canvas, widgets.HBox(self.__information, layout=widgets.Layout(justify_content="space-around"))])
        self.__v1=Visua([affichage, widgets.VBox([self.__action,self.__message])],self.__value)
        
        # Link self.__value and self.__v1.value
        traitlets.link([self, "value"], [self.__v1,"value"])
        
        # Set ValuePlayerWidget
        self.__player=ValuePlayerWidget(self.__v1, translation[self.__language]['locale'])
        self.__player.player.reset(self.__value)
        
        # The complete visualization
        # The dropdown zone
        if self.__display_dropdown==True:
            # Dropdown to choose the jugs'capacities
            self.__dropdown1=widgets.Dropdown(options=[str(i) for i in range (1,11)],value='5',description=translation[self.__language]['drop1'],disabled=False)
            self.__dropdown1.observe(self._observe_dropdown1, names='value')
            self.__dropdown2=widgets.Dropdown(options=[str(i) for i in range (1,11)],value='7',description=translation[self.__language]['drop2'],disabled=False)
            self.__dropdown2.observe(self._observe_dropdown2, names='value')
            validBox = widgets.VBox([self.__dropdown1,self.__dropdown2])#,self.mk_valider_button()])
            
        # The action buttons zone
        if UI==True:
            c5=widgets.VBox([self.mk_button(translation[self.__language]['pour'],0), self.mk_button(translation[self.__language]['fill'],0), self.mk_button(translation[self.__language]['empty'],0)])
            c7=widgets.VBox([self.mk_button(translation[self.__language]['pour'],1), self.mk_button(translation[self.__language]['fill'],1), self.mk_button(translation[self.__language]['empty'],1)])
            buttons= widgets.HBox([c5,c7])
            
        # Run the game
        self.redraw()
        self.update_obtained(0)
        if self.__display_dropdown==True:
            if UI==True:
                widgets.VBox.__init__(self,[validBox,self.__player,buttons])
            else:
                widgets.VBox.__init__(self,[validBox,self.__player])
        else:
            if UI==True:
                widgets.VBox.__init__(self,[self.__player,buttons])
            else:
                widgets.VBox.__init__(self,[self.__player])
              
        
    
    @property
    def v1(self): return self.__v1
        
    
    @property
    def player(self): return self.__player
    
    @property
    def jugs(self): return self.__jugs
    
    @property
    def obtained(self): return self.__obtained
    
    @property
    def canvas(self): return self.__canvas
    
    @property
    def action(self): return self.__action

    
    @traitlets.observe('value')
    def _observe_value(self, change):
        """ when self.__value is modified, the visualisation has to change
            
            Parameter
            ----------
            change : (type=dictionary) List with change['new'] which gives the new value of self.__value
        """
        self.set_capacity(change['new'])
   

    def _observe_dropdown1(self,change):
        """ Called method when the value of self.__dropdown1 is modified
            
            Parameter
            ----------
            change : an object -> change.new gives the new value of the dropdown
        """
        self.set_volumes(int(change.new),int(self.__dropdown2.value))
    
    def _observe_dropdown2(self,change):
        """ Called method when the value of self.__dropdown2 is modified
            
            Parameter
            ----------
            change : an object -> change.new gives the new value of the dropdown
        """
        self.set_volumes(int(self.__dropdown1.value),int(change.new))
        

    def completed(self):
        """ Returns True if all possible voumes have been obtained, False otherwise 
        
            Tests
            ----------
            >>> jugs=Jugs(1,2)
            >>> jugs.completed()
            False
            >>> jugs.fill(0)
            >>> jugs.fill(1)
            >>> jugs.completed()
            True
            >>> jugs.player.player.pause()
            
        """
        return all(i==True for i in self.__obtained)
    
    def mk_value(self, action=None):
        """ Returns the current volumes and the obtained volumes in a list to set self.__value 
            
            Tests
            ----------
            >>> jugs=Jugs(1,3)
            >>> jugs.mk_value()
            [0, 0, True, False, False, False, None]
            >>> jugs.player.player.pause()
        """
        t=[self.__jugs[0].volume,self.__jugs[1].volume]
        for r in self.__obtained:
            t.append(r)
        t.append(action)
        return t
    
    def set_capacity(self, values):
        """ Change the visualisation without modifying self.__jugs
        
        Parameters
        ----------
        values : (type=list) it has the same format than self.__value
        
        """
        # Update information
        for i in range (0,2):
            self.__information[i].value=str(values[i])+" / "+str(self.__jugs[i].capacity)
        # Update action
        self.update_action(values[len(values)-1])
        # Canvas
        x11,x12,y11,y12= self.get_coordonates(0)
        x21,x22,y21,y22= self.get_coordonates(1)
        graduateX=x12+40
        # clear the canvas
        self.__canvas[1].clear_rect(x11+2, y11+1, x12-x11-3, y12-y11+3)
        self.__canvas[1].clear_rect(x21+2, y21+1, x22-x21-3, y22-y21+3)
        self.__canvas[0].clear_rect(graduateX,y21-10,15,self.__coef*len(self.__obtained))
        
        # draw on the canvas
        for i in range (2,2+len(self.__obtained)):
            if values[i]==True:
                self.__canvas[0].fill_text("✓", graduateX, y12-(self.__coef*(i-2)-5))
        # c1
        if values[0]>0:
            c1=values[0]
            c1dif=self.__jugs[0].capacity-c1
            self.__canvas[1].fill_rect(x11+2, y11+1+self.__coef*c1dif, x12-x11-3, self.__coef*c1-3)
        # c2
        if values[1]>0:
            c2=values[1]
            c2dif=self.__jugs[1].capacity-c2
            self.__canvas[1].fill_rect(x21+2, y21+1+self.__coef*c2dif, x22-x21-3, self.__coef*c2-3)
        
        # Tab
        #for num in range(2,len(values)):
        #    if values[num]==True:
        #        self.__obtainedLab[num-2][1].value=" X "
        #    else:
        #        self.__obtainedLab[num-2][1].value="   "
        # Update the message
        if all(i==True for i in values[2:2+len(self.__obtained)]):
            file=open(translation[self.__language]['image'],'rb')
            #file=open("images/gagne.jpg","rb")
            image=file.read()
            self.__message.format="jpg"
            self.__message.value=image
        else:
            file=open(os.path.dirname(__file__)+"/"+"images/blanc.jpg","rb")
            image=file.read()
            self.__message.format="jpg"
            self.__message.value=image
            
        
                
    def update_obtained(self, num):
        """ Switch the element number 'num' of self.__obtained from False to True
            Check the matching graduation on the canvas
            Display a winning message if they are all True
        
            Parameter
            ----------
            num : (type=int) number of the volume, has to belong to [0,max(capacity1,capacity2)]
            
            Tests
            ----------
            >>> jugs=Jugs(3,2)
            >>> jugs.obtained
            [True, False, False, False]
            >>> jugs.update_obtained(2)
            >>> jugs.obtained
            [True, False, True, False]
            >>> jugs.player.player.pause()
        
        """
        self.__obtained[num]=True
       # self.__obtainedLab[num][1].value=" X "
        if num>=0:
            #21,x22,y21,y22= self.get_coordonates(1)
            x11,x12,y11,y12= self.get_coordonates(0)
            graduateX=x12+40
            self.__canvas[0].fill_text("✓", graduateX, y12-(self.__coef*num-5))
        if all(i==True for i in self.__obtained):
            # All True : The player wins
            file=open(translation[self.__language]['image'],'rb')
            #file=open("images/gagne.jpg","rb")
            image=file.read()
            self.__message.format="jpg"
            self.__message.value=image
    
   
    def reset_obtained(self):
        """ Reset the list self.__obtained
            Set them all to False
            
            Tests
            ----------
            >>> jugs=Jugs(1,2)
            >>> jugs.obtained
            [True, False, False]
            >>> jugs.reset_obtained()
            >>> jugs.obtained
            [True, False, False]
            >>> jugs.player.player.pause()
            
        """
        self.__obtained=[False for i in range (0,max(self.__jugs[0].capacity,self.__jugs[1].capacity)+1)]
        self.__obtained[0]=True

    
    #def mk_lab(self,val):
    #    """ Return a Label with the value val
    #    """
    #    return widgets.Label(value=val)
    
    def get_coordonates(self, num):
        """ Returns coordonates to draw the water inside the first or the second jug
        
            Parameter
            ----------
            num : (type=int) number of the jug. Num has to belong to [0,1]
            
            Tests
            ----------
            >>> jugs=Jugs(2,4)
            >>> jugs.get_coordonates(0)
            (50, 170, 70, 120)
            >>> jugs.get_coordonates(1)
            (235, 355, 20, 120)
            >>> jugs.player.player.pause()
            
        """
        assert (num==0 or num==1), "Num has to belong to [0,1]"
        if num==0:
            return self.__x1, self.__x1+self.__w, self.__y1, self.__y1+self.__coef*self.__jugs[0].capacity
        else:
            return self.__x2, self.__x2+self.__w, self.__y2, self.__y2+self.__coef*self.__jugs[1].capacity
        
    def pour(self, num):
        """ Pour the water of one jug inside the other one
            
            Parameter
            ----------
            num : (type=int) number of the jug. Num has to belong to [0,1]
            
            Tests
            ----------
            >>> jugs=Jugs(2,7)
            >>> jugs.fill(1)
            >>> jugs.pour(1)
            >>> jugs.jugs[0].volume
            2
            >>> jugs.jugs[1].volume
            5
            >>> jugs.player.player.pause()
            
        """
        assert isinstance(num, int), "Num has to be an int"
        assert (num==0 or num==1), "Num has to belong to [0,1]"
        self.__jugs[num].pour(self.__jugs[(num+1)%2])
        x11,x12,y11,y12= self.get_coordonates(0)
        x21,x22,y21,y22= self.get_coordonates(1)
        # clear the canvas
        self.__canvas[1].clear_rect(x11+2, y11+1, x12-x11-3, y12-y11+3)
        self.__canvas[1].clear_rect(x21+2, y21+1, x22-x21-3, y22-y21+3)
        # Draw the news volumes obtained
        #c1
        c1=self.__jugs[0].volume
        if(c1>0):
            c1dif=self.__jugs[0].capacity-c1
            self.__canvas[1].fill_rect(x11+2, y11+1+self.__coef*c1dif, x12-x11-3, self.__coef*c1-3)
        #c2
        c2=self.__jugs[1].volume
        if c2>0:
            c2dif=self.__jugs[1].capacity-c2
            self.__canvas[1].fill_rect(x21+2, y21+1+self.__coef*c2dif, x22-x21-3, self.__coef*c2-3)
        # Information
        self.update_information()
        if self.__obtained[self.__jugs[0].volume]==False:
            self.update_obtained(self.__jugs[0].volume)
        if self.__obtained[self.__jugs[1].volume]==False:
            self.update_obtained(self.__jugs[1].volume)
        self.__player.set_value(self.mk_value(translation[self.__language]['pour']+'('+str(num)+')'))

    
    def fill(self, num):
        """ Fill a jug with water
            
            Parameter
            ----------
            num : (type=int) number of the jug. Num has to belong to [0,1]
            
            Tests
            ----------
            >>> jugs=Jugs(2,4)
            >>> jugs.fill(0)
            >>> jugs.jugs[0].volume
            2
            >>> jugs.jugs[1].volume
            0
            >>> jugs.fill(1)
            >>> jugs.jugs[1].volume
            4
            >>> jugs.player.player.pause()
            
        """
        assert isinstance(num, int), "Num has to be an int"
        assert (num==0 or num==1), "Num has to belong to [0,1]"
        self.__jugs[num].fill()
        x11,x12,y11,y12= self.get_coordonates(num)
        self.__canvas[1].fill_rect(x11+2, y11+1, x12-x11-4, y12-y11-3)
        # Information
        self.update_information()
        if self.__obtained[self.__jugs[0].volume]==False:
            self.update_obtained(self.__jugs[0].volume)
        if self.__obtained[self.__jugs[1].volume]==False:
            self.update_obtained(self.__jugs[1].volume)
        self.__player.set_value(self.mk_value(translation[self.__language]['fill']+'('+str(num)+')'))

    def empty(self,num):
        """ Empty a jug 
        
            Parameter
            ----------
            num : (type=int) number of the jug. Num has to belong to [0,1]
            
            Tests
            ----------
            >>> jugs=Jugs(5,7)
            >>> jugs.fill(0)
            >>> jugs.fill(1)
            >>> jugs.jugs[0].volume
            5
            >>> jugs.jugs[1].volume
            7
            >>> jugs.empty(0)
            >>> jugs.jugs[0].volume
            0
            >>> jugs.jugs[1].volume
            7
            >>> jugs.empty(1)
            >>> jugs.jugs[0].volume
            0
            >>> jugs.jugs[1].volume
            0
            >>> jugs.player.player.pause()
            
        """
        assert isinstance(num, int), "Num has to be an int"
        assert (num==0 or num==1), "Num has to belong to [0,1]"
        self.__jugs[num].empty()
        x11,x12,y11,y12= self.get_coordonates(num)
        self.__canvas[1].clear_rect(x11+2, y11+1, x12-x11-3, y12-y11)
        # Information
        self.update_information()
        if self.__obtained[self.__jugs[0].volume]==False:
            self.update_obtained(self.__jugs[0].volume)
        if self.__obtained[self.__jugs[1].volume]==False:
            self.update_obtained(self.__jugs[1].volume)
        self.__player.set_value(self.mk_value(translation[self.__language]['empty']+'('+str(num)+')'))

    def update_information(self):
        """ Update the volumes contained by the jugs """
        for i in range (0,2):
            self.__information[i].value=str(self.__jugs[i].volume)+" / "+str(self.__jugs[i].capacity)
    
    def update_action(self, value=None):
        """
            Update the Label on which the action is displayed
        """
        if isinstance(value,str) and value!=None :
            self.__action.value="Action : "+value
        else:
            self.__action.value=""
    
    def redraw(self):
        """ When the player modifies the jugs'capacities, their edges and graduations have to be drawn again """
        # get the coordonates
        x11,x12,y11,y12= self.get_coordonates(0)
        x21,x22,y21,y22= self.get_coordonates(1)
        
        # new canvas' height
        self.__canvas.height= max(y12,y22)+6
        
        self.__canvas[0].fill_style = 'black'
        
        #c1
        self.__canvas[0].begin_path()
        self.__canvas[0].move_to(x11, y11)
        self.__canvas[0].line_to(x11, y12)
        self.__canvas[0].line_to(x12,y12)
        self.__canvas[0].line_to(x12,y11)
        self.__canvas[0].stroke()
        self.__canvas[0].close_path()

        #c2
        
        self.__canvas[0].begin_path()
        self.__canvas[0].move_to(x21, y21)
        self.__canvas[0].line_to(x21, y22)
        self.__canvas[0].line_to(x22,y22)
        self.__canvas[0].line_to(x22,y21)
        self.__canvas[0].stroke()
        self.__canvas[0].close_path()

        self.__canvas[1].fill_style = 'blue'
        
        self.__canvas[0].font = '15px sans-serif'

        graduateX=x12+20
        for i in range (0,max(self.__jugs[0].capacity,self.__jugs[1].capacity)+1):
            self.__canvas[0].fill_text(str(i), graduateX , y22-(self.__coef*i-5))
        #self.reset_obtained()
        #self.update_obtained(0)
                


    
    def set_volumes(self, v1, v2):
        """ Set the jugs'capacities with the values v1 and v2
        
            Parameters
            ----------
            v1 : (type=int) new capacity of the first jug
            v2 : (type=int) new capacity of the second jug
            
            Tests
            ----------
            >>> jugs=Jugs(5,7)
            >>> jugs.jugs[0].capacity
            5
            >>> jugs.jugs[1].capacity
            7
            >>> jugs.set_volumes(3,2)
            >>> jugs.jugs[0].capacity
            3
            >>> jugs.jugs[1].capacity
            2
            >>> jugs.player.player.pause()
            
        """
        assert isinstance(v1,int), "v1 has to be an int"
        assert isinstance(v2,int), "v2 has to be an int"
        if int(v1)>0 and int(v1)<11 and int(v2)>0 and int(v2)<11:
            # Erase the canvas
            self.__canvas[0].clear_rect(0, 0, self.__width, self.__height)
            self.__canvas[1].clear_rect(0, 0, self.__width, self.__height)
            # Modify the jugs'capacities
            self.__jugs[0].modify(v1)
            self.__jugs[1].modify(v2)
            # Update the information
            self.update_information()
            # Eventually erase the winning message
            file=open(os.path.dirname(__file__)+"/"+"images/blanc.jpg","rb")
            image=file.read()
            self.__message.format="jpg"
            self.__message.value=image
            # Calculate the new coordonates to draw the jugs (depending on which one has the biggest capacity)
            if self.__jugs[1].capacity > self.__jugs[0].capacity :
                self.__y2=20
                self.__y1=self.__y2 + self.__coef * (self.__jugs[1].capacity - self.__jugs[0].capacity)
            else:
                self.__y1=20
                self.__y2=self.__y1 + self.__coef * (self.__jugs[0].capacity - self.__jugs[1].capacity)
            # Draw the new jugs inside the canvas
            self.redraw()
            # Reset the lists of obtained volumes
            self.reset_obtained()
            self.update_obtained(0)
            self.__player.player.reset(self.mk_value())
            if self.__display_dropdown==True:
                self.__dropdown1.value=str(v1)
                self.__dropdown2.value=str(v2)
        else:
            print("The given capacity has to belong to [0,10]")

    def mk_button(self, action, num):
        """ Make an action button : fill, pour, empty
        
            Parameters
            ----------
            action : (type=string) The action the button has to execute
            num : (type=int) The number of the jug
            
        """
        button = widgets.Button(description=action)
        output = widgets.Output()
        def on_button_clicked(b):
            with output:
                if action==translation[self.__language]['pour']:
                    self.pour(num)
                elif action==translation[self.__language]['fill']:
                    self.fill(num)
                elif action==translation[self.__language]['empty']:
                    self.empty(num)
                #self.__error.value=str(self.__value)
        button.on_click(on_button_clicked)
        return button



    

        
    
