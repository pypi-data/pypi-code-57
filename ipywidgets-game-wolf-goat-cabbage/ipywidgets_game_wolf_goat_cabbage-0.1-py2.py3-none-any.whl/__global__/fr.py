from ipywidgets_game_wolf_goat_cabbage.Grid import Grid
__version__ = '0.1'
global traduction
traduction={'Chèvre':'Goat','Loup':'Wolf','Chou':'Cabbage'}


def JEUX(UI=True):
    """
        Lance et affiche le jeux Chou-Chèvre-Loup.
        
        Paramètre
        ----------
        UI : (valeur par défaut=True) (type=boolean) True pour afficher les boutons 
        
        Fonctions
        ----------
        monter()
        descendre()
        reset()
        traverser()
        
        Exemple d'utilisation
        ------------
        >> JEUX(UI=False)
        
    """
    global jeux
    jeux=Grid(UI=UI,lang='fr_FR')
    return jeux
    
def monter(element):
    """
        Faire monter un element sur le bâteau
        
        Paramètre
        ----------
        element : (type=string) element à faire monter sur le bâteau
        
        Exemple d'utilisation
        ------------
        >> monter('Chèvre')
         
    """
    if element in traduction:
        jeux.board(traduction[element])
    else:
        print(element+" n'existe pas. Choisir parmis: \n'Chèvre'\n'Loup'\nChou")
    
def descendre(element):
    """
        Faire descendre un élément du bâteau
        
        Paramètre
        ----------
        element : (type=string) element à faire descendre du bâteau
        
        Exemple d'utilisation
        ------------
        >> descendre('Loup')
        
    """
    if element in traduction:
        jeux.unboard(traduction[element])
    else:
        print(element+" n'existe pas. Choisir parmis: \n'Chèvre'\n'Loup'\nChou")
    
def reset():
    """
        Recommencer le jeux
        
        Exemple d'utilisation
        ------------
        >> reset()
        
    """
    jeux.reset()    
    
def traverser():
    """
        Faire traverser la rivière au bâteau
        
        Exemple d'utilisation
        ------------
        >> traverser()
        
    """
    jeux.cross()    
    