from ipywidgets_game_wolf_goat_cabbage.Field import Field

def test__init():
    field=Field()
    assert field.boat.side, "Problem init 1"
    assert field.rows==5, "Problem init 2"
    assert field.columns==10, "Problem init 3"
    assert field.leftCoast.goat, "Problem init 4"
    assert field.leftCoast.cabbage, "Problem init 5"
    assert field.leftCoast.wolf, "Problem init 6"
    assert field.rightCoast.goat==False, "Problem init 7"
    assert field.rightCoast.cabbage==False, "Problem init 8"
    assert field.rightCoast.wolf==False, "Problem init 9"
    
def test__board():
    field=Field()
    a,b,c=field.board('Goat')
    assert a, "Problem board 1"
    assert b, "Problem board 2"
    assert c, "Problem board 3"
    d,e,f=field.board('Wolf')
    assert d, "Problem board 4"
    assert e, "Problem board 5"
    assert f==False, "Problem board 6"
    g,h,i=field.board('Cabbage')
    assert g==False, "Problem board 7"
    assert h, "Problem board 8"
    assert i==False, "Problem board 9"
    
def test__unboard():
    field=Field()
    a,b,c,d=field.unboard('Goat')
    assert not a, "Problem unboard 1"
    assert not b, "Problem unboard 2"
    assert not c, "Problem unboard 3"
    assert not d, "Problem unboard 4"
    field.board('Wolf')
    e,f,g,h=field.unboard('Wolf')
    assert e, "Problem unboard 5"
    assert f, "Problem unboard 6"
    assert g, "Problem unboard 7"
    assert not h, "Problem unboard 8"
    
def test__cross():
    field=Field()
    assert field.cross(),"Problem cross 1"
    field2=Field()
    field2.board('Goat')
    assert not field2.cross(), "Problem cross 2"
    
    
    