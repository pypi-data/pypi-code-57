#!/usr/bin/env python
import argparse
import logging
from .Controller import Controller
from .Server import Server

logging.basicConfig(level=logging.DEBUG)
class Console(object):
    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self.args = None
    
    def argumentParse(self):
        self.parser.add_argument("--cli", help="Modo consola",action="store_true",default=False)
        self.parser.add_argument("--ws", help="Modo Web Service",action="store_true",default=False)
        self.parser.add_argument("-i","--input",help="Archivo pdf de entrada", nargs="?", type=str)
        self.parser.add_argument("-o","--out",help="Archivo pdf de salida", nargs="?", type=str)
        self.parser.add_argument('--host','-H',nargs='?',type=str,default='0.0.0.0',help='recibe el host con el cual estara escuchando el servidor, 0.0.0.0 para todas las ip')
        self.parser.add_argument('--port','-P',nargs='?',type=int,default=8001,help='Recibe el puerto en el cual estara escuchado el servidor')
        self.parser.add_argument('--debug',default=True, action="store_true", help='modo debug')
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
            controller.save_output()
        elif self.args.ws:
            server = Server("vPdfAntiAntiPlagio")
            server.app.run(host=self.args.host,port=self.args.port,debug=self.args.debug)
        else:
            controller = Controller("gui")
