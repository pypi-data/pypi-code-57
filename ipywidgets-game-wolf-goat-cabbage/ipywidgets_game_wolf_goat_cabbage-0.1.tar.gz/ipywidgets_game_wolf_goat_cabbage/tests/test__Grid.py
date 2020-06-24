from ipywidgets_game_wolf_goat_cabbage.Grid import Grid, mkImageWidget

def test__init():
    grid=Grid()
    assert grid.field.boat.side,"Problem init 1"
    c1= mkImageWidget('./images/goat.jpg','jpg')
    c2= mkImageWidget('./images/wolf.png','png')
    c3= mkImageWidget('./images/cabbage.jpg','jpg')
    c4= mkImageWidget('./images/wood.jpg','jpg')
    c5= mkImageWidget('./images/water.jpg','jpg')
    c6= mkImageWidget('./images/ground.jpg','jpg')
    assert grid.map[1][1].value==c1.value, "Problem init 2"
    assert grid.map[1][2].value==c2.value, "Problem init 3"
    assert grid.map[1][3].value==c3.value, "Problem init 4"
    for row in range (0,grid.field.rows):
        assert grid.map[0][row].value==c6.value, "Problem init 5"
        assert grid.map[8][row].value==c6.value, "Problem init 6"
        assert grid.map[9][row].value==c6.value, "Problem init 7"
        assert grid.map[4][row].value==c5.value, "Problem init 8"
        assert grid.map[5][row].value==c5.value, "Problem init 9"
        assert grid.map[6][row].value==c5.value, "Problem init 10"
        assert grid.map[7][row].value==c5.value, "Problem init 11"
    assert grid.map[2][2].value==c4.value, "Problem init 12"
    assert grid.map[3][2].value==c4.value, "Problem init 13"
    assert grid.value==['Left', (1, 1), (1, 2), (1, 3), None], "Problem init 14"
    grid.player.player.pause()
    
def test__mk_value():
    grid=Grid()
    assert grid.mk_value()==['Left', (1, 1), (1, 2), (1, 3), None], "Problem mk_vaue 1"
    grid.board('Cabbage')
    grid.board('Wolf')
    grid.cross()
    grid.unboard('Wolf')
    assert grid.mk_value()==['Right', (1, 1), (8, 2), (6, 2), None], "Problem mk_value 2"
    grid.player.player.pause()
    
def test__reset():
    grid=Grid()
    grid.board('Cabbage')
    grid.board('Wolf')
    grid.cross()
    grid.unboard('Wolf')
    grid.reset()
    assert grid.field.boat.side,"Problem reset 1"
    c1= mkImageWidget('./images/goat.jpg','jpg')
    c2= mkImageWidget('./images/wolf.png','png')
    c3= mkImageWidget('./images/cabbage.jpg','jpg')
    c4= mkImageWidget('./images/wood.jpg','jpg')
    c5= mkImageWidget('./images/water.jpg','jpg')
    c6= mkImageWidget('./images/ground.jpg','jpg')
    assert grid.map[1][1].value==c1.value, "Problem reset 2"
    assert grid.map[1][2].value==c2.value, "Problem reset 3"
    assert grid.map[1][3].value==c3.value, "Problem reset 4"
    for row in range (0,grid.field.rows):
        assert grid.map[0][row].value==c6.value, "Problem reset 5"
        assert grid.map[8][row].value==c6.value, "Problem reset 6"
        assert grid.map[9][row].value==c6.value, "Problem reset 7"
        assert grid.map[4][row].value==c5.value, "Problem reset 8"
        assert grid.map[5][row].value==c5.value, "Problem reset 9"
        assert grid.map[6][row].value==c5.value, "Problem reset 10"
        assert grid.map[7][row].value==c5.value, "Problem reset 11"
    assert grid.map[2][2].value==c4.value, "Problem reset 12"
    assert grid.map[3][2].value==c4.value, "Problem reset 13"
    assert grid.value==['Left', (1, 1), (1, 2), (1, 3), None], "Problem reset 14"
    grid.player.player.pause()
    
    
def test__board():
    grid=Grid()
    c1=mkImageWidget('images/ground.jpg','jpg')
    c2=mkImageWidget('images/wood.jpg','jpg')
    c3=mkImageWidget('images/water.jpg','jpg')
    c4=mkImageWidget('images/goat.jpg','jpg')
    c5=mkImageWidget('images/cabbage.jpg','jpg')
    c6=mkImageWidget('images/wolf.png','png')
    grid.board('Goat')
    assert grid.map[1][1].value==c1.value, "Problem board 1"
    assert grid.map[2][2].value==c4.value, "Problem board 2"
    assert not grid.field.leftCoast.goat, "Problem board 3"
    assert grid.field.boat.first=='Goat', "Problem board 4"
    grid.player.player.pause()
    
    
def test__unboard():
    grid=Grid()
    c1=mkImageWidget('images/ground.jpg','jpg')
    c2=mkImageWidget('images/wood.jpg','jpg')
    c3=mkImageWidget('images/water.jpg','jpg')
    c4=mkImageWidget('images/goat.jpg','jpg')
    c5=mkImageWidget('images/cabbage.jpg','jpg')
    c6=mkImageWidget('images/wolf.png','png')
    grid.board('Goat')
    grid.cross()
    grid.unboard('Goat')
    assert grid.map[8][1].value==c4.value, "Problem unboard 1"
    assert grid.map[6][2].value==c2.value, "Problem unboard 2"
    grid.player.player.pause()    
    
    
def test__cross():
    grid=Grid()
    c2=mkImageWidget('images/wood.jpg','jpg')
    c3=mkImageWidget('images/water.jpg','jpg')
    grid.cross()
    assert grid.map[2][2].value==c3.value, "Problem cross 1"
    assert grid.map[3][2].value==c3.value, "Problem cross 2"
    assert grid.map[6][2].value==c2.value, "Problem cross 3"
    assert grid.map[7][2].value==c2.value, "Problem cross 4"
    assert not grid.field.boat.side, "Problem cross 5"
    grid.player.player.pause()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    