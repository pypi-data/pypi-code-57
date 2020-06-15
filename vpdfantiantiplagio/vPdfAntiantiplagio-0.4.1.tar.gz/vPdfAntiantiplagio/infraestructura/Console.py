#!/usr/bin/env python
import argparse
from .Controller import Controller
class Console(object):
    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self.args = None
    
    def argumentParse(self):
        self.parser.add_argument("--cli", help="Modo consola",action="store_true",default=False)
        self.parser.add_argument("-i","--input",help="Archivo pdf de entrada", nargs="?", type=str)
        self.parser.add_argument("-o","--out",help="Archivo pdf de salida", nargs="?", type=str)
        self.args = self.parser.parse_args()
    
    def iniciar(self):
        self.argumentParse()
        if self.args.cli:
            controller = Controller("console")
            controller.setInputFile(self.args.input)
            controller.setOutFile(self.args.out)
            print(controller.getInfoPDF())
            print("¿Cuales paginas deseas convertir?")
            print("Escrbir numero separado por ,")
            print("Si deseas convertir todas solo pulsa enter")
            paginas = input("")
            if(paginas != ""):
                paginas = paginas.split(",")
            controller.setPaginas(paginas)
            #controller.getPaginas()
            controller.save_output()
        else:
            controller = Controller("gui")
