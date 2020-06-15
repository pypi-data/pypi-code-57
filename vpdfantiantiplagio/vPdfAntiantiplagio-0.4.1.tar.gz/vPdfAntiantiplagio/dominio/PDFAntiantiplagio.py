#!/bin/python
class PDFAntiantiplagio():
    def __init__(self):
        self.numPaginas = 0
        self.paginasSeleccionadas = []
        self.metodo = 'default'
    
    def getInfo(self):
        return {"numero de Paginas":self.numPaginas,"paginas Seleccionadas":self.paginasSeleccionadas}

    def setNumPaginas(self, num):
        self.numPaginas = num
    
    def setPaginasSeleccionadas(self, listSelect):
        if(listSelect != ""):
            self.paginasSeleccionadas = listSelect
            return True
        else:
            return self.seleccionarTodasLasPaginas()
    
    def setMetodo(self, metodoTxt):
        self.metodo = metodoTxt
    
    def getNumPaginas(self):
        return self.numPaginas
    
    def getPaginasSeleccionadas(self):
        return self.paginasSeleccionadas

    def comprobarPaginas(self, listSelect):
        for pagina in listSelect:
            if pagina > numPaginas:
                raise ErrorNumeroPaginas
        return True
    
    def seleccionarPaginas(self, listSelect):
        try:
            if self.comprobarPaginas(listSelect):
                self.setPaginasSeleccionadas(listSelect)
            return True
        except:
            print("Error en la seleccion de paginas")
    
    def seleccionarTodasLasPaginas(self):
        if(self.getNumPaginas() > 0):
            for numPagina in range(self.getNumPaginas()):
                self.paginasSeleccionadas.append(numPagina)
            return True
        else:
            raise ErrorNumeroPaginas

    def procesarPDF(self):
        return self.getNumPaginas() > 0 and len(self.getPaginasSeleccionadas()) > 0

class ErrorNumeroPaginas(Exception):
    def __init__(self):
        pass