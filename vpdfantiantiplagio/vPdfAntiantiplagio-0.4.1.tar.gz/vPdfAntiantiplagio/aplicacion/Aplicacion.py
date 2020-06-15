#!/usr/bin/env python
from ..dominio import PDFAntiantiplagio
from os import path
class Aplicacion():
    def __init__(self):
        PDFAntiantiplagio_c = None
        self.pathName = ""
    
    def setPDFaProcesar(self, pathName, numPaginas):
        self.PDFAntiantiplagio_c = PDFAntiantiplagio()
        self.PDFAntiantiplagio_c.setNumPaginas(numPaginas)
        if path.isfile(pathName):
            self.pathName = pathName
            return True
        else:
            print(pathName)
            raise ErrorPathNamePDF

    def getInfo(self):
        info = self.PDFAntiantiplagio_c.getInfo()
        info["nombre"] = self.pathName
        return info

    def setPaginasAProcesar(self,paginas):
        return self.PDFAntiantiplagio_c.setPaginasSeleccionadas(paginas)

    def getPaginasAProcesar(self):
        return self.PDFAntiantiplagio_c.getPaginasSeleccionadas()

    def getPdfAProcesar(self):
        return self.pathName

class ErrorPathNamePDF(Exception):
    def __init__(self):
        pass    