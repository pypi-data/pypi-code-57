from ipywidgets_game_wolf_goat_cabbage.Boat import Boat

def test__init():
    boat=Boat()
    assert boat.first==None, "Problem init 1"
    assert boat.second==None, "Problem init 2"
    assert boat.side==True, "Problem init 3"
    
def test__board():
    boat=Boat()
    boat.board('Goat')
    boat.board('Wolf')
    assert boat.first=='Goat', "Problem board 1"
    assert boat.second=='Wolf', "Problem board 2"

    
def test__unboard():
    boat=Boat()
    boat.board('Goat')
    boat.board('Cabbage')
    boat.unboard('Cabbage')
    boat.unboard('Goat')
    assert boat.first==None, "Problem unboard 1"
    assert boat.second==None, "Problem unboard 2"
    
def test__cross():
    boat=Boat()
    boat.cross()
    assert boat.side==False, "Problem cross"
    