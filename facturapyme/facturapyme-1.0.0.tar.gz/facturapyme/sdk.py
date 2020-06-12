#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests


class FacturaPyme:

    def __init__(self, host, api_key, version='v1'):
        self.headers = {'User-Agent': 'SDK FacturaPyme Python',
                        'Cache-Control': 'no-cache',
                        'Authorization': api_key}
        self.host = host + '/api/' + version + '/'
        self.use_ssl = True

    def ssl(self, ssl):
        self.use_ssl = ssl

    def get(self, endPoint):
        return self.processResponse(requests.get(self.host + endPoint,
                                    verify = self.use_ssl,
                                    headers = self.headers))

    def post(self, endPoint, data):
        return self.processResponse(requests.post(self.host + endPoint,
                                    data,
                                    verify = self.use_ssl,
                                    headers = self.headers))

    def pdf(self, tipoDte, folio):
        return self.get('dte/pdf/' + str(tipoDte) + '/' + str(folio))

    def xml(self, tipoDte, folio):
        return self.get('dte/xml/' + str(tipoDte) + '/' + str(folio))

    def enviaDTE(self, documento):
        return self.post('dte', documento)

    def estadoDTE(self, id):
        return self.get('dte/' + str(id))

    def processResponse(self, response):
        body = response.content
        if response.headers.get('content-type') == 'application/json':
            body = response.json()

        if response.status_code > 400:
            raise Exception('error:[' + str(response.status_code) + '] '
                             + body['error'])

        return body
