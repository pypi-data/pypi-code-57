from ipywidgets_game_wolf_goat_cabbage.Coast import Coast

def test__init():
    coast=Coast(True)
    assert coast.goat, "Problem init 1"
    assert coast.wolf, "Problem init 2"
    assert coast.cabbage, "Problem init 3"
    coast2=Coast(False)
    assert coast2.goat==False, "Problem init 4"
    assert coast2.wolf==False, "Problem init 5"
    assert coast2.cabbage==False, "Problem init 6"
    
def test__check():
    coast=Coast(True)
    assert coast.check()==-1, "Problem check 1"
    coast2=Coast(False)
    assert coast2.check()==1, "Problem check 2"
    
def test__win():
    coast=Coast(True)
    assert coast.win(), "Problem win 1"
    coast2=Coast(False)
    assert coast2.win()==False, "Problem win 2"
    
def test__board():
    coast=Coast(True)
    assert coast.board('Goat'), "Problem board 1"
    assert coast.goat==False, "Problem board 2"
    assert coast.board('Cabbage'), "Problem board 3"
    assert coast.cabbage==False, "Problem board 4"
    assert coast.board('Wolf'), "Problem board 5"
    assert coast.wolf==False, "Problem board 6"
    
def test__unboard():
    coast=Coast(False)
    coast.unboard('Goat')
    coast.unboard('Cabbage')
    coast.unboard('Wolf')
    assert coast.goat, "Problem unboard 1"
    assert coast.wolf, "Problem unboard 2"
    assert coast.cabbage, "Problem unboard 3"












    