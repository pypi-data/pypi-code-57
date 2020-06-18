#!/usr/bin/env python
from .infraestructura import Console
from .infraestructura import Server

application = Server("vPdfAntiAntiPlagio").app
def main():
    c = Console()
    c.iniciar()