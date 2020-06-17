from ..Jugs import Jugs

def CRUCHES(capacite1=None, capacite2=None, UI=False):
    """
        CRUCHES permet de créer et afficher une interface français pour le jeu des cruches.
        
        Paramètres
        -----------
        capacite1 : (valeur par défaut = None) (type=int) capacité de la cruche de gauche
        capacite2 : (valeur par défaut = None) (type=int) capacité de la cruche de droite
        UI : (valeur par défaut = False) (type=boolean) True permet d'afficher une interface utilisateur et d'exécuter des actions à l'aide de boutons
        
        Fonctions disponibles
        ----------
        remplir(c)
        verser(c)
        vider(c)
        valides()
        
        Exemples d'utilisation
        -----------
        >> CRUCHES()
        >> CRUCHES(5,4,True)
    
    """
    global cruches
    cruches = Jugs(capacity1=capacite1, capacity2=capacite2, UI=UI, lang='fr_FR')
    return cruches
    
def remplir(c):
    """
        Permet de remplir la cruche n°c (c=0 ou c=1)
        
        Paramètre
        ---------
        c : (type=int) (valeur = 0 ou 1) Numéro de la cruche
        
        Exemple d'utilisation
        -----------
        >> remplir(0)
    """
    cruches.fill(c)

def verser(c):
    """
        Verse le contenu de la cruche n°c dans la seconde cruche.  (c=0 ou c=1)
        
        Paramètre
        ---------
        c : (type=int) (valeur = 0 ou 1) Numéro de la cruche
        
        Exemple d'utilisation
        -----------
        >> verser(1)
        
    """
    cruches.pour(c)

def vider(c):
    """
        Vide le contenu de la cruche n°c  (c=0 ou c=1)
        
        Paramètre
        ---------
        c : (type=int) (valeur = 0 ou 1) Numéro de la cruche
        
        Exemple d'utilisation
        -----------
        >> vider(0)
        
    """
    cruches.empty(c)

def nouvelles_capacites(c1,c2):
    """
        Modifie les capacités des deux cruches.
        
        Paramètres
        ---------
        c1 : (type=int) Nouvelle capacité de la cruche de gauche
        c2 : (type=int) Nouvelle capacité de la cruche de droite       
        
        Exemple d'utilisation
        -----------
        >> nouvelles_capacites(6,3)
    
    """
    cruches.set_volumes(c1,c2)

def valides():
    """
        Renvoie un tableau de booléens. La ièm case du tableau est à True si un volume égal à i litres a déjà été obtenu.
        
        Exemple d'utilisation
        -----------
        >> valides()
        
    """
    return cruches.obtained

def pause():
    """
        Force l'arrêt du player
        
        Exemple d'utilisation
        -----------
        >> pause()
    """
    cruches.player.player.pause()
