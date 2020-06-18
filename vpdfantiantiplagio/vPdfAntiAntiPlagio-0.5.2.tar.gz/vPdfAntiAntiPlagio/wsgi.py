#!/usr/bin/env python
from .main import application
from waitress import serve

def wsgi():
    serve(application, unix_socket='/run/waitress/vPdfAntiAntiPlagio.sock',unix_socket_perms='666',ident="vPdfAntiAntiPlagio",threads=20)
