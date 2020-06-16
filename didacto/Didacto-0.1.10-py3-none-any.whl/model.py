# -*- coding: utf-8 -*-

#   Didacto, un logiciel d'aide à l'organisation d'un corpus didactique
#   Copyright (C) 2020  Marco de Freitas
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.
#   If not, see <https://www.gnu.org/licenses/>.
#
#   contact:marco@sillage.ch

import os
import sys
import subprocess

from PyPDF2 import PdfFileReader
from PyPDF2 import utils


class CustomDict(dict):
    """Buit-in dict Class with à sort by key funtion added."""

    def sorted(self):
        """Sort the dictionnary by lowered key values, alphabetic order."""
        temp_dict = {}
        for item in sorted(self.keys(), key=str.lower):
            temp_dict[item] = sorted(self[item], key=lambda x: x['name'].
                                     lower())
        return temp_dict


class Model:
    def __init__(self, prefs, user_data):
        """Initialise prefs values retrieved by controller."""
        self.user_data=UserData(user_data)
        self.errors_text=''
        path = prefs['path']
        self.separator = prefs['separator']
        notation = prefs['notation_format']
        self.printo()  # test

    wordsDict = CustomDict()
    path = ''
    emptyDict = {}

    def printo(self):
        print(self.path)

# Sous-fonctions de scan_repertory()
    def get_info(self, path):
        """This function takes a pdf file path and returns pdf metadata keywords field"""
        with open(path, 'rb') as f:
            pdf = PdfFileReader(f, strict=False)
            info = pdf.getDocumentInfo()
            temp ={}
            for key in info:
                temp[key]=info[key]
            try:   
                key=str(temp["/Keywords"])
            except: # fiel is empty string ''
                key = '∅' 
            finally:
                if not key: #field is empty
                    key='∅'
        return (key)

    def get_keywords_from_field(self, field, separator):
        """This function takes a keywords field and separator, keywords values or ∅ if empty"""
        newKeywords = self.split_str(field, separator)
        if newKeywords is None:
            newKeywords = "∅"
        return newKeywords

    def split_str(self, string, separator):
        """This function takes a string and a separator and return the splitted string"""
        if string is not None:
            try:
                output = string.split(separator)
            except:
                output = None
            finally:
                return(output)

# Cette fonction parcours l'arborescence à partir du dossier sélectionné
# et récupère les mots clés
    def scan_repertory(self, path, recursive):
        '''This function scan a directory for pdf file keywords and store the results in a custom Dictionary:        
        { keyword1 : [{'name' : 'file1name.pdf', 'path' : '/file1/path'},
                      {'name' : 'file2name.pdf', 'path' : '/file2/path'},
                      {'name' : 'file3name.pdf', 'path' : '/file3/path'}]}

        Keywords and file names are sorted by alpahabetic order
        
        Good to know:
        os.walk method retrieves a generator objet, each item as the form a tuple
        ('folder path', ['subfolder1', 'subfolder2', etc.], ['file1name', 'file2name', etc.])
        '''
        keywordsDict = CustomDict()
        pdfKey = ''
        errors = []
        if recursive is True:
            for i in os.walk(path, topdown = True):
                for file_name in i[2]:
                    if file_name.endswith('.pdf'):
                        try:
                            pdfKey=self.get_info(i[0] + '/' + file_name)
                        except FileNotFoundError:
                            errors.append("File does not exist:" + i[0]+ '/'+ file_name + "\n" )
                        except :
                            errors.append("Problem with file:" + i[0] + '/' + file_name + "\n")
                            #continue
                        else:
                            keywords = (self.get_keywords_from_field(pdfKey,self.separator))
                            if keywords is not None:
                                for word in keywords:
                                    if not word in keywordsDict:
                                        keywordsDict[word] = [{"name": file_name,
                                                     "path": i[0] }] 
                                    else:
                                        keywordsDict[word].append({"name": file_name,
                                                     "path": i[0] }) 
        if recursive is False:
            for name in next(os.walk(path, topdown = True))[2]:
                if name.endswith('.pdf'):
                        try:
                            pdfKey=self.get_info(path+'/'+ name)
                        except FileNotFoundError:
                            errors.append("File does not exist:" + path +'/'+ name + "\n" )
                        except PyPDF2.utils.PdfReadError:
                            errors.append("Problem with file:" + path +'/'+ name + "\n" )
                        else:
                            keywords = (self.get_keywords_from_field(pdfKey, self.separator))
                            if keywords is not None:
                                for word in keywords:
                                    if not word in keywordsDict:
                                        keywordsDict[word] = [{"name": name,
                                                     "path": path }] 
                                    else:
                                        keywordsDict[word].append({"name": name,
                                                     "path": path })
        self.wordsDict = keywordsDict.sorted()
        self.errors_text= " ".join(iter(errors)) # lists are iterable but not iterators
        

class UserData():
    '''This Class stores user data, keyword definition and categories
    curent {'keyword1':'definition1', etc.}
    future {'keyword1':{'definition':'definition1',
                        'categories':['cat1','cat2', etc.]
                        }}
    simpler {'keyword1':'definition1',['cat1','cat2','cat3']}

    even simpler, two different dics, in two files
    or go for sql lite ???
    '''

    def __init__(self, data, ):
        self.user_data=data

    def get(self,key):
        return self.user_data[key]

    def set(self,key,data):
        self.user_data[key] = data


# new methods to handle keywords categories
    def get_categories(self,key):
        return self.user_data[key][1]

    def set_categries(self,key,cat):
        self.user_data[key][1] = cat





    def retrieve(self):
        return self.user_data
            
        
              
        
