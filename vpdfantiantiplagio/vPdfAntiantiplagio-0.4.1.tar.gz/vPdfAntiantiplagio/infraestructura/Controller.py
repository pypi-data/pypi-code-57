#!/usr/bin/env python
from pdf2image import convert_from_path, convert_from_bytes
from pdf2image.exceptions import (
    PDFInfoNotInstalledError,
    PDFPageCountError,
    PDFSyntaxError
)
from PyPDF2 import PdfFileReader
from ..aplicacion import Aplicacion

class Controller():
    def __init__(self,ui_type):
        app = None
        pdf = None
        ui_type = ui_type
        out = ""
        images = None
    
    def setOutFile(self, outFile):
        self.out = outFile

    def setInputFile(self, inputFile):
        self.pdf = PdfFileReader(open(inputFile,'rb'))
        self.app = Aplicacion()
        numPaginas = self.pdf.getNumPages()
        self.app.setPDFaProcesar(inputFile, numPaginas)

    def setPaginas(self, paginas):
        if self.app.setPaginasAProcesar(paginas):
            print("paginas seleccionada de forma correcta")

    
    def getInfoPDF(self):
        return self.app.getInfo()


    def getPaginas(self):
        self.images = self.getImages()
        paginas = self.app.getPaginasAProcesar()
        paginas_imagenes = []
        for pagina in paginas:
            paginas_imagenes.append(self.images[int(pagina)])
        return paginas_imagenes
    
    def save_output(self):
        paginas_imagenes = self.getPaginas()
        self.images[0].save(self.out, save_all=True, append_images=paginas_imagenes)
        print("Proceso Exitoso")

    def getImages(self):
        images = convert_from_path(self.app.getPdfAProcesar())
        return images
        images[0].save(self.out, save_all=True, append_images=images[1:])