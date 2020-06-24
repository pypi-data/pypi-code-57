import ipywidgets as widgets
import os
import time
from IPython.display import display
from .Field import Field
import traitlets
from .value_player_widget import ValuePlayerWidget
from .Visualisation import Visualisation
__version__ = '0.1'
global translation
translation={'en_EN':{'Board':'Board','Unboard':'Unboard','Cross':'Cross','Reset':'Reset', 'Goat':'Goat','Cabbage':'Cabbage','Wolf':'Wolf','Win':'images/win.jpg','Lost':'images/lost.png'},
            'fr_FR':{'Board':'Monter','Unboard':'Descendre','Cross':'Traverser','Reset':'Reset', 'Goat':'Chèvre','Cabbage':'Chou','Wolf':'Loup','Win':'images/gagne.jpg','Lost':'images/lost.png'}}

def mkImageWidget(file_name, im_format,w=50,h=50):
    assert isinstance(file_name, str), "file_name has to be a string"
    assert isinstance(im_format, str), "im_format has to be a string"
    file=open(os.path.dirname(__file__)+"/"+file_name,"rb")
    image=file.read()
    return widgets.Image(
            value=image,
            format=im_format,
            width=w,
            height=h,
            layout=widgets.Layout(border="none", margin="0px", padding="0 px")
        )

class Grid(widgets.VBox):
    """
        Visualisation of the game Goat-Wolf-Cabbage
    """
    value =traitlets.List()
    def __init__(self, UI=True, lang='en_EN'):
        """
            Initialization of the visualisation
            
            Parameter
            ----------
            lang : (default value='en_EN') (type=string) game's language
            
            Tests
            -----------
            >>> grid=Grid()
            >>> grid.field.boat.side
            True
            >>> grid.field.leftCoast.goat
            True
            >>> grid.field.rightCoast.goat
            False
            >>> grid.field.leftCoast.wolf
            True
            >>> grid.field.rightCoast.wolf
            False
            >>> grid.field.leftCoast.cabbage
            True
            >>> grid.field.rightCoast.cabbage
            False
            >>> c1=mkImageWidget('images/goat.jpg','jpg')
            >>> grid.map[1][1].value==c1.value
            True
            >>> c2=mkImageWidget('images/wolf.png','png')
            >>> grid.map[1][2].value==c2.value
            True
            >>> c3=mkImageWidget('images/cabbage.jpg','jpg')
            >>> grid.map[1][3].value==c3.value
            True
            >>> grid.value
            ['Left', (1, 1), (1, 2), (1, 3), None]
            >>> grid.player.player.pause()
            
        """
        #Initialisation: creation d un nouvwater field et creation de la map graphique
        if lang in translation:
            self.__language=lang
        else:
            self.__language='en_EN'
        self.__lost=False
        self.__lCoastLoc={"Goat":(1,1),"Wolf":(1,2),"Cabbage":(1,3)}
        self.__rCoastLoc={"Goat":(8,1),"Wolf":(8,2),"Cabbage":(8,3)}
        self.__boatLocation={"Left":{"First":(2,2),"Second":(3,2)},"Right":{"First":(6,2),"Second":(7,2)}}
        self.__data={"Goat":("images/goat.jpg","jpg"),
              "Cabbage":("images/cabbage.jpg","jpg"),
              "Wolf":("images/wolf.png","png"),
              "Water":("images/water.jpg","jpg"),
              "Ground":("images/ground.jpg","jpg"),
              "Wood":("images/wood.jpg","jpg")
          }
        self.__field=Field()
        self.__map=self.mkMap()
        self.__message=mkImageWidget("images/blank.jpg", "jpg",180,60)
        self.__action=widgets.Label(value='',layout=widgets.Layout(justify_content="center", margin='10px'))
        #self.__continue=True
        
        # Display
        myCol=[None for j in range (0,self.__field.columns)]
        for i in range (0, self.__field.columns):
            myCol[i]=widgets.VBox(self.__map[i],layout=widgets.Layout(border="none", margin="0px", padding="0px"))
        game=widgets.HBox(myCol,layout=widgets.Layout(border="none", margin="0px", padding="0px"))
        message_box=widgets.VBox([self.__action,self.__message],layout=widgets.Layout(justify_content="center", margin='10px'))
        screen= [game,message_box]
        self.__value=self.mk_value()
        self.__visualisation=Visualisation(screen, self.mk_value())
        traitlets.link([self,'value'],[self.__visualisation,'value'])
        self.__player=ValuePlayerWidget(self.__visualisation,self.__language)
        self.__player.player.reset(self.mk_value())
        if UI:
            widgets.VBox.__init__(self,[self.__player,self.mk_button_box()])
        else:
            widgets.VBox.__init__(self,[self.__player])
    
    
    @traitlets.observe('value')
    def _observe_value(self, change):
    # when self.__value is modified, the visualisation has to change
        self.update_display(change['new'])
    
    @property
    def player(self): return self.__player
    
    @property
    def field(self): return self.__field
    
    @property
    def map(self) : return self.__map
    
    def mk_value(self, action=None):
        """
            Returns the updated value of Grid
            
            Parameter
            ----------
            action : (type=string) the last action made
            
            Tests
            -----------
            >>> grid=Grid()
            >>> grid.value
            ['Left', (1, 1), (1, 2), (1, 3), None]
            >>> grid.board('Goat')
            >>> grid.cross()
            >>> grid.mk_value('Cross')
            ['Right', (6, 2), (1, 2), (1, 3), 'Cross']
            >>> grid.player.player.pause()
            
        """
        t=[]
        # Boat
        if self.__field.boat.side: #True==Left side
            t.append('Left')
        else:
            t.append('Right')
        # Goat
        if self.__field.leftCoast.goat==True:
            t.append(self.__lCoastLoc['Goat'])
        elif self.__field.rightCoast.goat==True:
            t.append(self.__rCoastLoc['Goat'])
        elif self.__field.boat.first=='Goat':
            t.append(self.__boatLocation[t[0]]['First'])
        elif self.__field.boat.second=='Goat':
            t.append(self.__boatLocation[t[0]]['Second'])
        # Wolf
        if self.__field.leftCoast.wolf==True:
            t.append(self.__lCoastLoc['Wolf'])
        elif self.__field.rightCoast.wolf==True:
            t.append(self.__rCoastLoc['Wolf'])
        elif self.__field.boat.first=='Wolf':
            t.append(self.__boatLocation[t[0]]['First'])
        elif self.__field.boat.second=='Wolf':
            t.append(self.__boatLocation[t[0]]['Second'])
        # Cabbage
        if self.__field.leftCoast.cabbage==True:
            t.append(self.__lCoastLoc['Cabbage'])
        elif self.__field.rightCoast.cabbage==True:
            t.append(self.__rCoastLoc['Cabbage'])
        elif self.__field.boat.first=='Cabbage':
            t.append(self.__boatLocation[t[0]]['First'])
        elif self.__field.boat.second=='Cabbage':
            t.append(self.__boatLocation[t[0]]['Second'])
        # Action
        t.append(action)
        return t
    
    def update_display(self,change):
        """
            Update the visualisation when self.__value has changed
            
            Parameter
            ----------
            change : (type=list) the value describing the state of the field
            
        """
        # Display Boat
        if change[0]=='Left':
            side='Right'
        else:
            side='Left'
        self.update_image(self.__boatLocation[change[0]]['First'][0],self.__boatLocation[change[0]]['First'][1],self.__data['Wood'][0],self.__data['Wood'][1])
        self.update_image(self.__boatLocation[change[0]]['Second'][0],self.__boatLocation[change[0]]['Second'][1],self.__data['Wood'][0],self.__data['Wood'][1])
        self.update_image(self.__boatLocation[side]['First'][0],self.__boatLocation[side]['First'][1],self.__data['Water'][0],self.__data['Water'][1])
        self.update_image(self.__boatLocation[side]['Second'][0],self.__boatLocation[side]['Second'][1],self.__data['Water'][0],self.__data['Water'][1])
        # All Grass
        for p in self.__lCoastLoc:
            self.update_image(self.__lCoastLoc[p][0],self.__lCoastLoc[p][1],self.__data['Ground'][0],self.__data['Ground'][1])
        for p in self.__rCoastLoc:
            self.update_image(self.__rCoastLoc[p][0],self.__rCoastLoc[p][1],self.__data['Ground'][0],self.__data['Ground'][1])
        
        # Goat
        self.update_image(change[1][0],change[1][1],self.__data['Goat'][0],self.__data['Goat'][1])
        # Wolf
        self.update_image(change[2][0],change[2][1],self.__data['Wolf'][0],self.__data['Wolf'][1])
        # Cabbage
        self.update_image(change[3][0],change[3][1],self.__data['Cabbage'][0],self.__data['Cabbage'][1])
        # Action
        if isinstance(change[4],str) and change[4]!=None:
            self.__action.value='Action : '+change[4]
        else:
            self.__action.value=""
        
        # Message
        if change[1:4]==[self.__rCoastLoc['Goat'],self.__rCoastLoc['Wolf'],self.__rCoastLoc['Cabbage']]:
            self.win()
        # Goat + Wolf
        elif (change[0]=='Right' and change[1]==self.__lCoastLoc['Goat'] and change[2]==self.__lCoastLoc['Wolf']) or (change[0]=='Left' and change[1]==self.__rCoastLoc['Goat'] and change[2]==self.__rCoastLoc['Wolf']):
            self.win(False)
        # Goat + Cabbage
        elif (change[0]=='Right' and change[1]==self.__lCoastLoc['Goat'] and change[3]==self.__lCoastLoc['Cabbage']) or (change[0]=='Left' and change[1]==self.__rCoastLoc['Goat'] and change[3]==self.__rCoastLoc['Cabbage']):
            self.win(False)
        else:
            file=open(os.path.dirname(__file__)+"/"+"images/blank.jpg","rb")
            image=file.read()
            self.__message.format="jpg"
            self.__message.value=image
        
        
    
    def update_image(self,c,r,file_name,file_format):
        """
            Update the widget Image line r column c
            
            Parameters
            -----------
            c : (type=int) column
            r : (type=int) row
            file_name : (type=string) the file's name
            file_format : (type=string) the file's format
            
            Tests
            -----------
            >>> grid=Grid()
            >>> c1=mkImageWidget('images/ground.jpg','jpg')
            >>> c2=mkImageWidget('images/goat.jpg','jpg')
            >>> grid.map[0][0].value==c1.value
            True
            >>> grid.update_image(0,0,'images/goat.jpg','jpg')
            >>> grid.map[0][0].value==c1.value
            False
            >>> grid.map[0][0].value==c2.value
            True
            >>> grid.player.player.pause()
            
        """
        file=open(os.path.dirname(__file__)+"/"+file_name,"rb")
        image=file.read()
        self.__map[c][r].format=file_format
        self.__map[c][r].value=image
    
    def reset(self):
        """
            Reset the game
            
            Tests
            -----------
            >>> grid=Grid()
            >>> grid.board('Cabbage')
            >>> grid.board('Wolf')
            >>> grid.cross()
            >>> grid.unboard('Wolf')
            >>> grid.reset()
            >>> grid.value==['Left', (1, 1), (1, 2), (1, 3), None]
            True
            >>> c1=mkImageWidget('images/ground.jpg','jpg')
            >>> c2=mkImageWidget('images/goat.jpg','jpg')
            >>> grid.map[8][1].value==c1.value
            True
            >>> grid.map[1][1].value==c2.value
            True
            >>> grid.field.boat.side
            True
            >>> grid.field.leftCoast.goat
            True
            >>> grid.field.rightCoast.goat
            False
            >>> grid.field.leftCoast.wolf
            True
            >>> grid.field.rightCoast.wolf
            False
            >>> grid.field.leftCoast.cabbage
            True
            >>> grid.field.rightCoast.cabbage
            False
            >>> grid.player.player.pause()
            
        """
        self.__lost=False
        self.__field.__init__()
        #self.__continue=True
        ## update_image self.__message
        file=open(os.path.dirname(__file__)+"/"+"images/blank.jpg","rb")
        image=file.read()
        self.__message.format="jpg"
        self.__message.value=image
        ## update_image self.__map
        ##   coast droite vide
        for i in self.__rCoastLoc:
            self.update_image(self.__rCoastLoc[i][0],self.__rCoastLoc[i][1],self.__data["Ground"][0],self.__data["Ground"][1])
        ##   Animaux sur la coast gauche
        for i in self.__lCoastLoc:
            c=self.__lCoastLoc[i][0]
            r=self.__lCoastLoc[i][1]
            self.update_image(c,r,self.__data[i][0],self.__data[i][1])
        ## boat sur la coast gauche 
        ##  Faire disparaitre boat a droite
        i="Water"
        self.update_image(6,2,self.__data[i][0],self.__data[i][1])
        self.update_image(7,2,self.__data[i][0],self.__data[i][1])
        ##  Faire apparaitre boat a gauche
        i="Wood"
        self.update_image(2,2,self.__data[i][0],self.__data[i][1])
        self.update_image(3,2,self.__data[i][0],self.__data[i][1])
        self.__player.player.reset(self.mk_value())
        
    def mkElem(self, name=None):
        """
            Get the data linked to name and give it as parameters to mkImageWidget
            
            Parameter
            ----------
            name : (type=string) the element to display
            
        """
        if name!=None:
            return mkImageWidget(self.__data[name][0], self.__data[name][1])
        

    def mkMap(self):
        """
            Create a map containing all the widgets Image
            
            Tests
            -----------
            >>> grid=Grid()
            >>> c1=mkImageWidget('images/ground.jpg','jpg')
            >>> c2=mkImageWidget('images/wood.jpg','jpg')
            >>> c3=mkImageWidget('images/water.jpg','jpg')
            >>> c4=mkImageWidget('images/goat.jpg','jpg')
            >>> c5=mkImageWidget('images/cabbage.jpg','jpg')
            >>> c6=mkImageWidget('images/wolf.png','png')
            >>> map=grid.mkMap()
            >>> map[0][0].value==c1.value
            True
            >>> map[1][1].value==c4.value
            True
            >>> map[1][2].value==c6.value
            True
            >>> map[1][3].value==c5.value
            True
            >>> map[2][2].value==c2.value
            True
            >>> map[3][2].value==c2.value
            True
            >>> grid.player.player.pause()
            
        """
        #Cree une map de widget afin d afficher l etat du field 
        items=[[None for r in range (0,self.__field.rows)] for c in range (0, self.__field.columns)]
        ##On place les animaux sur les coasts
        #On verifie quels animaux sont sur la coast gauche
        if self.__field.leftCoast.goat:
            items[1][1]=self.mkElem("Goat")
        if self.__field.leftCoast.wolf:
            items[1][2]=self.mkElem("Wolf")
        if self.__field.leftCoast.cabbage:
            items[1][3]=self.mkElem("Cabbage")
            
        #On verifie quels animaux sont sur la coast droite
        if self.__field.rightCoast.goat:
            items[8][1]=self.mkElem("Goat")
        if self.__field.rightCoast.wolf:
            items[8][2]=self.mkElem("Wolf")
        if self.__field.rightCoast.cabbage:
            items[8][3]=self.mkElem("Cabbage")

        ##On place les animaux dans le boat ou le boat vide
        #On verifie a quelle coast le boat est acoste
        i1, i2=0 ,0
        if self.__field.boat.side: #coast gauche
            i1=2
            i2=3
        else:
            i1=6
            i2=7
            
        if self.__field.boat.first!=None: #il y a quelque chose dans la premiere case du boat
            items[i1][2]=self.mkElem(self.__field.boat.first)
        else: #l emplacement du boat est vide
            items[i1][2]=self.mkElem("Wood")
        if self.__field.boat.second!=None: #il y a quelque chose dans la seconde case du boat
            items[i2][2]=self.mkElem(self.__field.boat.second)
        else:
            items[i2][2]=self.mkElem("Wood")
        
        #on remplie toutes les cases restees vides par du ground ou de la mer
        for r in range (0, self.__field.rows):
            for c in [0,1,8,9]:
                if items[c][r]==None:
                    items[c][r]=self.mkElem("Ground")
            for c in range (2,8):
                if items[c][r]==None:
                    items[c][r]=self.mkElem("Water")
        return items
    
    def mk_button(self, action, character=""):
        """
            Create a button executing the function action (potentially on the element character)
            
            Parameters
            -----------
            action : (type=string) the action to execute
            character : (default value='') (type=string) the character to execute the action on
            
        """
        if character!="":
            button = widgets.Button(description=translation[self.__language][action]+" "+translation[self.__language][character])
        else:
            button = widgets.Button(description=translation[self.__language][action])
        output = widgets.Output()

        def on_button_clicked(b):
            with output:
                if action=="Board" and self.__lost==False:
                    self.board(character)
                elif action =="Unboard" and self.__lost==False:
                    self.unboard(character)
                elif action == "Cross" and self.__lost==False:
                    self.cross()
                elif action == "Reset":
                    self.reset()

        button.on_click(on_button_clicked)
        return button
    
    def win(self, win=True):
        """
            Display a winning or a loosing message
            
            Parameter
            ----------
            win : (default value=True) (type=boolean) True to display a winning message, False otherwise
            
        """
        #self.__message
        if win==True:
            file=open(os.path.dirname(__file__)+"/"+translation[self.__language]['Win'],"rb")
            image=file.read()
            self.__message.format="jpg"
        else:
            file=open(os.path.dirname(__file__)+"/"+translation[self.__language]['Lost'],"rb")
            image=file.read()
            self.__message.format="png"
        self.__message.value=image
        
    
    def mk_button_box(self):
        """
            Create an HBox containing all the buttons
        """
        goat_box = widgets.VBox([self.mk_button("Board","Goat"),self.mk_button("Unboard","Goat")])
        cabbage_box = widgets.VBox([self.mk_button("Board","Cabbage"),self.mk_button("Unboard","Cabbage")])
        wolf_box = widgets.VBox([self.mk_button("Board","Wolf"),self.mk_button("Unboard","Wolf")])
        cross_box = widgets.VBox([self.mk_button("Cross"),self.mk_button("Reset")])
        return widgets.HBox([goat_box, cabbage_box, wolf_box, cross_box])

    
    def board(self, name):
        """
            Board the element name
            
            Parameter
            ----------
            name : (type=string) the element to board
            
            Tests
            -----------
            >>> grid=Grid()
            >>> c1=mkImageWidget('images/ground.jpg','jpg')
            >>> c2=mkImageWidget('images/wood.jpg','jpg')
            >>> c3=mkImageWidget('images/water.jpg','jpg')
            >>> c4=mkImageWidget('images/goat.jpg','jpg')
            >>> c5=mkImageWidget('images/cabbage.jpg','jpg')
            >>> c6=mkImageWidget('images/wolf.png','png')
            >>> grid.board('Goat')
            >>> grid.map[1][1].value==c1.value
            True
            >>> grid.map[2][2].value==c4.value
            True
            >>> grid.field.leftCoast.goat
            False
            >>> grid.field.boat.first
            'Goat'
            >>> grid.player.player.pause()
            
        """
        assert isinstance (name,str),"name has to be a string"
        done,coast,side=self.__field.board(name)
        #side=""
        if side: #first case de boat
            boat_side="First"
        else:
            boat_side="Second"
        if done: #il est effectivement possible de faire board l animal
            if coast: #mise a jour de la coast gauche
                coast_side="Left"
                loc=self.__lCoastLoc[name]
            else:
                coast_side="Right"
                loc=self.__rCoastLoc[name]
            #faire disparaitre l animal sur la coast
            im_info=self.__data["Ground"]
            self.update_image(loc[0],loc[1],im_info[0],im_info[1])
            #faire apparaitre l animal dans le boat
            loc2=self.__boatLocation[coast_side][boat_side]
            im_info2=self.__data[name]
            self.update_image(loc2[0],loc2[1],im_info2[0],im_info2[1])
            self.__player.set_value(self.mk_value(translation[self.__language]['Board']+' '+translation[self.__language][name]))
    

    def unboard(self, name):
        """
            Unboard the element name
            
            Parameter
            ----------
            name : (type=string) the element to unboard
            
            Tests
            -----------
            >>> grid=Grid()
            >>> c2=mkImageWidget('images/wood.jpg','jpg')
            >>> c6=mkImageWidget('images/wolf.png','png')
            >>> grid.board('Wolf')
            >>> grid.cross()
            >>> grid.unboard('Wolf')
            >>> grid.map[8][2].value==c6.value
            True
            >>> grid.map[6][2].value==c2.value
            True
            >>> grid.player.player.pause()
            
        """
        assert isinstance (name,str),"name has to be a string"
        done, coast, side, win=self.__field.unboard(name)
        #print(win)
        if side: #premiere case du boat concernee
            boat_side="First"
        else:
            boat_side="Second"
        if done: #Changement fait, mettre a jour l affichage
            if coast: #mise a jour de la coast gauche
                coast_side="Left"
                loc=self.__lCoastLoc[name]
            else:
                coast_side="Right"
                loc=self.__rCoastLoc[name]
            #faire disparaitre l animal du boat
            loc2=self.__boatLocation[coast_side][boat_side]
            im_info2=self.__data["Wood"]
            self.update_image(loc2[0],loc2[1],im_info2[0],im_info2[1])
                
            #faire apparaitre l animal sur la coast
            im_info=self.__data[name]
            self.update_image(loc[0],loc[1],im_info[0],im_info[1])
            self.__player.set_value(self.mk_value(translation[self.__language]['Unboard']+' '+translation[self.__language][name]))
        
        if win==True:
            self.win()
            

    def cross(self):
        """
            Make the boat cross the river
            
            Tests
            -----------
            >>> grid=Grid()
            >>> c2=mkImageWidget('images/wood.jpg','jpg')
            >>> c3=mkImageWidget('images/water.jpg','jpg')
            >>> grid.cross()
            >>> grid.map[2][2].value==c3.value
            True
            >>> grid.map[3][2].value==c3.value
            True
            >>> grid.map[6][2].value==c2.value
            True
            >>> grid.map[7][2].value==c2.value
            True
            >>> grid.field.boat.side
            False
            >>> grid.player.player.pause()
            
        """
        self.__lost=self.__field.cross()
        if self.__lost==True:
            self.win(False)
        if self.__field.boat.first!=None:
            case1=self.__data[self.__field.boat.first]
        else:
            case1=self.__data["Wood"]
        if self.__field.boat.second!=None:
            case2=self.__data[self.__field.boat.second]
        else:
            case2=self.__data["Wood"]
        replace=self.__data["Water"]
        if self.__field.boat.side: #coast droite vers coast gauche
            for j in range (0,4):
                i=7-j
                #case2 devient la mer
                self.update_image(i,2,replace[0],replace[1])
                #case1 devient case2
                self.update_image(i-1,2,case2[0],case2[1])
                #la mer devient case1
                self.update_image(i-2,2,case1[0],case1[1])
                time.sleep(0.2)
        else:#coast gauche vers coast droite
            for i in range (2,6):
                #case1 devient la mer
                self.update_image(i,2,replace[0],replace[1])
                #case2 devient case1
                self.update_image(i+1,2,case1[0],case1[1])
                #la mer devient case2
                self.update_image(i+2,2,case2[0],case2[1])
                time.sleep(0.2)
        self.__player.set_value(self.mk_value(translation[self.__language]['Cross']))
