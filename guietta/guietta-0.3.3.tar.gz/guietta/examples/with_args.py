# -*- coding: utf-8 -*-

from guietta import _, ___, Gui, HS
        
gui = Gui(
    
  [  HS('slider'),  ___ , ___   ],
  [  'num'       ,   _  ,  _    ],
)



with gui.slider as value:
    print(value)
    gui.num = gui.slider*2
     
gui.run()
