#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import sys
import re
import string
import os.path
from os import path
from graphviz import Digraph
import rdf2html

    
aux_path = os.path.abspath(rdf2html.__file__).split('/')
print(aux_path.pop())
pathi = ''
i=0
for line in aux_path:
    if(i!=0):
        pathi = pathi + '/' + line
    i=i+1
install_local = pathi
print(install_local)
# HTML to be used in the output

# Function to verify if we found a new type of data to parse or if we still maintain the previous
    # 0 - General info about the ontologie
    # 1 - Annotations general
    # 2 - DataTypes
    # 3 - Object Properties
    # 4 - Data Properties
    # 5 - Classes
    # 6 - Individuals
    # 7 - Annotations specific
def verifier (line,controller) :
    if("Annotation properties" in line):
        return 1
    if("Datatypes" in line):
        return 2
    if("Object Properties" in line):
        return 3
    if("Data properties" in line):
        return 4
    if("Classes" in line):
        return 5
    if("Individuals" in line):
        return 6
    if("Annotations" in line):
        return 7
    return controller

# Global variable to control the parse of objects_about that have nested properties
current = ''

############################ General Info #################################################
## Function to deal with general data from the ontologie, the case where controller == 0
def general_info(lines):
    infos=dict()
    for line in lines:
        key_aux = line.split(' ')
        key_aux1 = key_aux[0].split(':')
        key=''
        value = ''
        ## here we have all infos refered in this section
        if(len(key_aux1)>1):
            key = key_aux1[1]
            key = re.sub(r">[A-Z|a-z|0-9|-]*"," ",key)

        ## here we have all the value refered by these infos
        info_aux = line.split('>')
        if(len(info_aux)>2):
            info_aux1=info_aux[1].split("<")
            value = info_aux1[0]
        else:
            resource_aux = info_aux[0].split("resource=")
            if(len(resource_aux)>1):
                value = resource_aux[1]
        ## About needs a specific case
        if("rdf:about=" in line):
            key = "about"
            resource_aux = info_aux[0].split("about=")
            if(len(resource_aux)>1):
                value = resource_aux[1]

        ## here is where we store the collected data into our data structure - dictionary
        if(value!='' and key != ''):
            if (infos.get(key)):
                value= re.sub('\"', '',value)
                lista = infos.get(key)
                lista.append(value)
                infos.update({key:lista})
            else:
                lista=[]
                value= re.sub('\"', '',value)
                lista.append(value)
                infos.update({key:lista})

    ## here is where we print to the html file the values
    fd = open('output/index.html', "w")
    header_file = open(install_local + "/html/header.html", "r")
    header = header_file.read()
    fd.write(header)
    info_file = open(install_local + "/html/info.html", "r")
    info = info_file.read()
    fd.write(info)
    for key in infos:
       fd.write("<p><strong>" + key +" : </strong>")
       for value in infos[key]:
          fd.write(value + " ") 
       fd.write(".</p>\n")
    fd.write("      </div>\n" + "    </div>")

############################ Datatypes #################################################
def datatypes_info (lines):

    datatypes=dict()
    value = ''
    key = ''
    for line in lines:
    ## About needs a specific case
        info_aux = line.split('>')
        if("rdf:about=" in line):
            key = "about"
            resource_aux = info_aux[0].split("about=")
            if(len(resource_aux)>1):
                value_aux = resource_aux[1]
                value = value_aux.split('#')[1]
                ## used to clean unwanted characters
                value = re.sub(r"[^a-z|A-Z]"," ",value)
                ## here is where we store the collected data into our data structure - dictionary
                if(value!='' and key != ''):
                    if (datatypes.get(key)):
                        lista = datatypes.get(key)
                        lista.append(value)
                        datatypes.update({key:lista})
                    else:
                        lista=[]
                        lista.append(value)
                        datatypes.update({key:lista})

    fd = open('output/index.html', "a")
    datatype_file = open(install_local + "/html/datatypes.html", "r")
    datatype = datatype_file.read()
    fd.write(datatype)
    for key in datatypes:
       for value in datatypes[key]:
          fd.write("<p>" + value + "\n") 
          fd.write(".</p>\n")
    fd.write("      </div>\n" + "    </div>")

############################ Object Properties #################################################

def object_info (lines):

    #objects_about stores for each entry in Object Properties, as a key we have the object name and then all the informations associated to it
    objects_about=dict()
    objects = dict()
    value = ''
    key = ''
    ## when we find a empty line then we finished the information about that element
    for line in lines:
        if(len(line)==0):
            current = ''
        ## ignore this case
        if( not ("<!-- " in line) ):
            ## About needs a specific case
            info_aux = line.split('>')
            if("rdf:about=" in line):
                key = "about"
                resource_aux = info_aux[0].split("about=")
                if(len(resource_aux)>1):
                    value_aux = resource_aux[1]
                    value_aux1 = value_aux.split('#')
                    ## case we have # as a sperator
                    if(len(value_aux1)>1):
                        value= value_aux1[1]
                        value = re.sub(r"[^a-z|A-Z]"," ",value)
                    # case we have / as separator it depends on the iri
                    else:
                        value_aux2 = value_aux1[0].split('/')
                        value = value_aux2[len(value_aux2)-1]
                    ## used to clean unwanted characters
                        value = re.sub(r"[^a-z|A-Z]"," ",value)
                ## here is where we store the collected data into our data structure - dictionary
                if(value!='' and key != ''):
                    if (objects_about.get(key)):
                        lista=objects_about.get(key)
                        lista.append(value)
                        objects_about.update({key:lista})
                    else:
                        lista=[]
                        lista.append(value)
                        objects_about.update({key:lista})
                    ## here we update the current value when we encounter a about that marks the beggining of a new block
                    if(current == ''):
                        current = value.strip(' ')

            ## in here we deal with the object properties values
            else:
                key_aux = line.split(' ')
                key_aux1 = key_aux[0].split(':')
                key=''
                value = ''
                ## here we have all infos refered in this section
                if(len(key_aux1)>1):
                    key = key_aux1[1].strip(' ').replace(' ','_')
                    key = re.sub(r">[<|A-Z|a-z|0-9|-|/]*"," ",key)

                ## here we have all the value refered by these infos
                info_aux = line.split('>')
                if(len(info_aux)>2):
                    info_aux1=info_aux[1].split("<")
                    value = info_aux1[0]
                    if(objects.get(current)):
                        objects[current][key] = value
                    else:
                         objects.update({current:{key:value}})

                else:
                    resource_aux = info_aux[0].split("resource=")
                    if(len(resource_aux)>1):
                        value = resource_aux[1]
                        if(objects.get(current)):
                            objects[current][key] = value
                        else:
                            objects.update({current:{key:value}})
        value = ''
        key   = ''
    ## Dot graph with the information about domains, ranges and inverseOf for better understanding of the ontologie
    dot_general = Digraph(comment='Object Properties',format='png')
    ## Html append the information
    fd = open('output/index.html', "a")
    datatype_file = open(install_local + "/html/object.html", "r")
    datatype = datatype_file.read()
    fd.write(datatype)
    for p_id, p_info in objects.items():
        fd.write("<h2>"+ p_id+"</h2>")
        ## in here we create an individual graph for each property
        dot = Digraph(comment=p_id,format='png')
        dot.node(p_id,p_id)
        dot_general.node(p_id,p_id)
        for key in p_info:
            value_aux1 = p_info[key].split('#')
        ### Needed to clean the IRI ###
            ## case we have # as a sperator
            if(len(value_aux1)>1):
                p_info[key] = value_aux1[1]
                p_info[key] = re.sub(r"[^a-z|A-Z]"," ",p_info[key])
            else:
                value_aux2 = p_info[key].split('/')
                if(len(value_aux2)==1):
                    p_info[key] = value_aux2[0]
                if(len(value_aux2)>1):
                    if(value_aux2[len(value_aux2)-1]!= ''):
                        p_info[key] = value_aux2[len(value_aux2)-1]
                    else:
                        #isDefined by has a different pattern
                        if(key == 'isDefinedBy'):
                            p_info[key] = value_aux2[len(value_aux2)-3].replace("\"","")
                        else:
                            p_info[key] = value_aux2[len(value_aux2)-2].replace("\"","")
            fd.write("<p>" + key + ":" + p_info[key]+ "\n")
            fd.write(".</p>\n")
            if(key =='domain'):
                dot.node(p_info[key],p_info[key])
                dot.edge(p_info[key],p_id,key)
                dot_general.node(p_info[key],p_info[key])
                dot_general.edge(p_info[key],p_id,key)
            if(key =='inverseOf'):
                dot.node(p_info[key],p_info[key])
                dot.edge(p_id,p_info[key],key)
                dot_general.node(p_info[key],p_info[key])
                dot_general.edge(p_info[key],p_id,key)
            if(key =='range'):
                dot.node(p_info[key],p_info[key])
                dot.edge(p_id,p_info[key],key)
                dot_general.node(p_info[key],p_info[key])
                dot_general.edge(p_info[key],p_id,key)
        path = p_id.replace(" ","_")
        dot.render('dot/'+path, view=False)
        fd.write('<img src=../dot/'+ path +'.png alt="dot">')
    
    
    dot_general.render('dot/object_properties', view=False)
    
    fd.write('<h2>General Overview</h2><p><a href="../dot/object_properties.png">See Graph</a></p> ')
    fd.write('<button type="button"><a href="#">Back Top</a></button>')
    fd.write("      </div>\n" + "    </div>")


############################ Data Properties #################################################

def data_prop_info (lines):

    #objects_about stores for each entry in Object Properties, as a key we have the object name and then all the informations associated to it
    objects_about=dict()
    objects = dict()
    value = ''
    key = ''
    ## when we find a empty line then we finished the information about that element
    for line in lines:
        if(len(line)==0):
            current = ''
        ## ignore this case
        if( not ("<!-- " in line) ):
            ## About needs a specific case
            info_aux = line.split('>')
            if("rdf:about=" in line):
                key = "about"
                resource_aux = info_aux[0].split("about=")
                if(len(resource_aux)>1):
                    value_aux = resource_aux[1]
                    value_aux1 = value_aux.split('#')
                    ## case we have # as a sperator
                    if(len(value_aux1)>1):
                        value= value_aux1[1]
                        value = re.sub(r"[^a-z|A-Z]"," ",value)
                    # case we have / as separator it depends on the iri
                    else:
                        value_aux2 = value_aux1[0].split('/')
                        value = value_aux2[len(value_aux2)-1]
                    ## used to clean unwanted characters
                        value = re.sub(r"[^a-z|A-Z]"," ",value)
                ## here is where we store the collected data into our data structure - dictionary
                if(value!='' and key != ''):
                    if (objects_about.get(key)):
                        lista=objects_about.get(key)
                        lista.append(value)
                        objects_about.update({key:lista})
                    else:
                        lista=[]
                        lista.append(value)
                        objects_about.update({key:lista})
                    ## here we update the current value when we encounter a about that marks the beggining of a new block
                    if(current == ''):
                        current = value.strip(' ')

            ## in here we deal with the object properties values
            else:
                key_aux = line.split(' ')
                key_aux1 = key_aux[0].split(':')
                key=''
                value = ''
                ## here we have all infos refered in this section
                if(len(key_aux1)>1):
                    key = key_aux1[1].strip(' ').replace(' ','_')
                    key = re.sub(r">[<|A-Z|a-z|0-9|-|/]*"," ",key)

                ## here we have all the value refered by these infos
                info_aux = line.split('>')
                if(len(info_aux)>2):
                    info_aux1=info_aux[1].split("<")
                    value = info_aux1[0]
                    if(objects.get(current)):
                        objects[current][key] = value
                    else:
                         objects.update({current:{key:value}})

                else:
                    resource_aux = info_aux[0].split("resource=")
                    if(len(resource_aux)>1):
                        value = resource_aux[1]
                        if(objects.get(current)):
                            objects[current][key] = value
                        else:
                            objects.update({current:{key:value}})
        value = ''
        key   = ''
    ## Dot graph with the information about domains, ranges and inverseOf for better understanding of the ontologie
    dot_general = Digraph(comment='Object Properties',format='png')
    ## Html append the information
    fd = open('output/index.html', "a")
    datatype_file = open(install_local + "/html/data_props.html", "r")
    datatype = datatype_file.read()
    fd.write(datatype)
    for p_id, p_info in objects.items():
        fd.write("<h2>"+ p_id+"</h2>")
        ## in here we create an individual graph for each property
        dot = Digraph(comment=p_id,format='png')
        dot.node(p_id,p_id)
        dot_general.node(p_id,p_id)
        for key in p_info:
            value_aux1 = p_info[key].split('#')
            
        ### Needed to clean the IRI ###
            ## case we have # as a sperator
            if(len(value_aux1)>1):
                p_info[key] = value_aux1[1]
                p_info[key] = re.sub(r"[^a-z|A-Z]"," ",p_info[key])
            else:
                value_aux2 = p_info[key].split('/')
                if(len(value_aux2)==1):
                    p_info[key] = value_aux2[0]
                if(len(value_aux2)>1):
                    if(value_aux2[len(value_aux2)-1]!= ''):
                        p_info[key] = value_aux2[len(value_aux2)-1]
                    else:
                        #isDefined by has a different pattern
                        if(key == 'isDefinedBy'):
                            p_info[key] = value_aux2[len(value_aux2)-3].replace("\"","")
                        else:
                            p_info[key] = value_aux2[len(value_aux2)-2].replace("\"","")
            fd.write("<p>" + key + ":" + p_info[key]+ "\n")
            fd.write(".</p>\n")
            if(key =='domain'):
                dot.node(p_info[key],p_info[key])
                dot.edge(p_info[key],p_id,key)
                dot_general.node(p_info[key],p_info[key])
                dot_general.edge(p_info[key],p_id,key)
            if(key =='inverseOf'):
                dot.node(p_info[key],p_info[key])
                dot.edge(p_id,p_info[key],key)
                dot_general.node(p_info[key],p_info[key])
                dot_general.edge(p_info[key],p_id,key)
            if(key =='range'):
                dot.node(p_info[key],p_info[key])
                dot.edge(p_id,p_info[key],key)
                dot_general.node(p_info[key],p_info[key])
                dot_general.edge(p_info[key],p_id,key)
        path = p_id.replace(" ","_")
        if(path):
            dot.render('dot/'+path, view=False)
            fd.write('<img src=../dot/'+ path +'.png alt="dot">')
    dot_general.render('dot/data_properties', view=False)

    fd.write('<h2>General Overview</h2><p><a href="../dot/data_properties.png">See Graph</a></p> ')
    fd.write('<button type="button"><a href="#">Back Top</a></button>')
    fd.write("      </div>\n" + "    </div>")

############################ Classes #################################################

def class_info (lines):

    #objects_about stores for each entry in Object Properties, as a key we have the object name and then all the informations associated to it
    objects_about=dict()
    objects = dict()
    value = ''
    key = ''
    ## when we find a empty line then we finished the information about that element
    for line in lines:
        if(len(line)==0):
            current = ''
        ## ignore this case
        if( not ("<!-- " in line) ):
            ## About needs a specific case
            info_aux = line.split('>')
            if("rdf:about=" in line):
                key = "about"
                resource_aux = info_aux[0].split("about=")
                if(len(resource_aux)>1):
                    value_aux = resource_aux[1]
                    value_aux1 = value_aux.split('#')
                    ## case we have # as a sperator
                    if(len(value_aux1)>1):
                        value= value_aux1[1]
                        value = re.sub(r"[^a-z|A-Z]"," ",value)
                    # case we have / as separator it depends on the iri
                    else:
                        value_aux2 = value_aux1[0].split('/')
                        value = value_aux2[len(value_aux2)-1]
                    ## used to clean unwanted characters
                        value = re.sub(r"[^a-z|A-Z]"," ",value)
                ## here is where we store the collected data into our data structure - dictionary
                if(value!='' and key != ''):
                    if (objects_about.get(key)):
                        lista=objects_about.get(key)
                        lista.append(value)
                        objects_about.update({key:lista})
                    else:
                        lista=[]
                        lista.append(value)
                        objects_about.update({key:lista})
                    ## here we update the current value when we encounter a about that marks the beggining of a new block
                    if(current == ''):
                        current = value.strip(' ')

            ## in here we deal with the object properties values
            else:
                key_aux = line.split(' ')
                key_aux1 = key_aux[0].split(':')
                key=''
                value = ''
                ## here we have all infos refered in this section
                if(len(key_aux1)>1):
                    key = key_aux1[1].strip(' ').replace(' ','_')
                    key = re.sub(r">[<|A-Z|a-z|0-9|-|/]*"," ",key)

                ## here we have all the value refered by these infos
                info_aux = line.split('>')
                if(len(info_aux)>2):
                    info_aux1=info_aux[1].split("<")
                    value = info_aux1[0]
                    if(objects.get(current)):
                        objects[current][key] = value
                    else:
                         objects.update({current:{key:value}})

                else:
                    resource_aux = info_aux[0].split("resource=")
                    if(len(resource_aux)>1):
                        value = resource_aux[1]
                        if(objects.get(current)):
                            objects[current][key] = value
                        else:
                            objects.update({current:{key:value}})
        value = ''
        key   = ''
    ## Dot graph with the information about domains, ranges and inverseOf for better understanding of the ontologie
    dot_general = Digraph(comment='Object Properties',format='png')
    ## Html append the information
    fd = open('output/index.html', "a")
    datatype_file = open(install_local + "/html/datatypes.html", "r")
    datatype = datatype_file.read()
    fd.write(datatype)
    for p_id, p_info in objects.items():
        fd.write("<h2>"+ p_id+"</h2>")
        ## in here we create an individual graph for each property
        dot = Digraph(comment=p_id,format='png')
        dot.node(p_id,p_id)
        dot_general.node(p_id,p_id)
        for key in p_info:
            value_aux1 = p_info[key].split('#')
            
        ### Needed to clean the IRI ###
            ## case we have # as a sperator
            if(len(value_aux1)>1):
                p_info[key] = value_aux1[1]
                p_info[key] = re.sub(r"[^a-z|A-Z]"," ",p_info[key])
            else:
                value_aux2 = p_info[key].split('/')
                if(len(value_aux2)==1):
                    p_info[key] = value_aux2[0]
                if(len(value_aux2)>1):
                    if(value_aux2[len(value_aux2)-1]!= ''):
                        p_info[key] = value_aux2[len(value_aux2)-1]
                    else:
                        #isDefined by has a different pattern
                        if(key == 'isDefinedBy'):
                            p_info[key] = value_aux2[len(value_aux2)-3].replace("\"","")
                        else:
                            p_info[key] = value_aux2[len(value_aux2)-2].replace("\"","")
            fd.write("<p>" + key + ":" + p_info[key]+ "\n")
            fd.write(".</p>\n")
            if(key =='subClassOf'):
                dot.node(p_info[key],p_info[key])
                dot.edge(p_info[key],p_id,key)
                dot_general.node(p_info[key],p_info[key])
                dot_general.edge(p_info[key],p_id,key)
        path = p_id.replace(" ","_")
        if(path):
            dot.render('dot/'+path, view=False)
            fd.write('<img src=../dot/'+ path +'.png alt="dot">')
    dot_general.render('dot/classes', view=False)

    fd.write('<h2>General Overview</h2><p><a href="../dot/classes.png">See Graph</a></p> ')
    fd.write('<button type="button"><a href="#">Back Top</a></button>')
    fd.write("      </div>\n" + "    </div>")

############################ Individuals #################################################

def individuals_info (lines):

    #objects_about stores for each entry in Object Properties, as a key we have the object name and then all the informations associated to it
    objects_about=dict()
    objects = dict()
    value = ''
    key = ''
    ## when we find a empty line then we finished the information about that element
    for line in lines:
        if(len(line)==0):
            current = ''
        ## ignore this case
        if( not ("<!-- " in line) ):
            ## About needs a specific case
            info_aux = line.split('>')
            if("rdf:about=" in line):
                key = "about"
                resource_aux = info_aux[0].split("about=")
                if(len(resource_aux)>1):
                    value_aux = resource_aux[1]
                    value_aux1 = value_aux.split('#')
                    ## case we have # as a sperator
                    if(len(value_aux1)>1):
                        value= value_aux1[1]
                        value = re.sub(r"[^a-z|A-Z]"," ",value)
                    # case we have / as separator it depends on the iri
                    else:
                        value_aux2 = value_aux1[0].split('/')
                        value = value_aux2[len(value_aux2)-1]
                    ## used to clean unwanted characters
                        value = re.sub(r"[^a-z|A-Z]"," ",value)
                ## here is where we store the collected data into our data structure - dictionary
                if(value!='' and key != ''):
                    if (objects_about.get(key)):
                        lista=objects_about.get(key)
                        lista.append(value)
                        objects_about.update({key:lista})
                    else:
                        lista=[]
                        lista.append(value)
                        objects_about.update({key:lista})
                    ## here we update the current value when we encounter a about that marks the beggining of a new block
                    if(current == ''):
                        current = value.strip(' ')

            ## in here we deal with the object properties values
            else:
                key_aux = line.split(' ')
                key_aux1 = key_aux[0].split(':')
                key=''
                value = ''
                ## here we have all infos refered in this section
                if(len(key_aux1)>1):
                    key = key_aux1[1].strip(' ').replace(' ','_')
                    key = re.sub(r">[<|A-Z|a-z|0-9|-|/]*"," ",key)

                ## here we have all the value refered by these infos
                info_aux = line.split('>')
                if(len(info_aux)>2):
                    info_aux1=info_aux[1].split("<")
                    value = info_aux1[0]
                    if(objects.get(current)):
                        objects[current][key] = value
                    else:
                         objects.update({current:{key:value}})

                else:
                    resource_aux = info_aux[0].split("resource=")
                    if(len(resource_aux)>1):
                        value = resource_aux[1]
                        if(objects.get(current)):
                            objects[current][key] = value
                        else:
                            objects.update({current:{key:value}})
        value = ''
        key   = ''
    ## Dot graph with the information about domains, ranges and inverseOf for better understanding of the ontologie
    dot_general = Digraph(comment='Object Properties',format='png')
    ## Html append the information
    fd = open('output/index.html', "a")
    datatype_file = open(install_local + "/html/individuals.html", "r")
    datatype = datatype_file.read()
    fd.write(datatype)
    for p_id, p_info in objects.items():
        dot_general.node(p_id,p_id)
        for key in p_info:
            value_aux1 = p_info[key].split('#')
        ### Needed to clean the IRI ###
            ## case we have # as a sperator
            if(len(value_aux1)>1):
                p_info[key] = value_aux1[1]
                p_info[key] = re.sub(r"[^a-z|A-Z]"," ",p_info[key])
            else:
                value_aux2 = p_info[key].split('/')
                if(len(value_aux2)==1):
                    p_info[key] = value_aux2[0]
                if(len(value_aux2)>1):
                    if(value_aux2[len(value_aux2)-1]!= ''):
                        p_info[key] = value_aux2[len(value_aux2)-1]
                    else:
                        #isDefined by has a different pattern
                        if(key == 'isDefinedBy'):
                            p_info[key] = value_aux2[len(value_aux2)-3].replace("\"","")
                        else:
                            p_info[key] = value_aux2[len(value_aux2)-2].replace("\"","")
            if(key =='type'):
                dot_general.node(p_info[key],p_info[key])
                dot_general.edge(p_id,p_info[key],key)
    dot_general.render('dot/individuals', view=False)

    fd.write('<h2>General Overview</h2><p><a href="../dot/individuals.png">See Graph</a></p> ')
    fd.write('<button type="button"><a href="#">Back Top</a></button>')
    fd.write("      </div>\n" + "    </div>")

############################ Function that writes the footer ###############################

def footer():
     fd = open('output/index.html', "a")
     fd.write('<footer class="w3-center w3-light-grey w3-padding-48 w3-large"><p>Powered by <a href="https://github.com/sir-onze" title="Tiago Baptista" target="_blank" class="w3-hover-text-green">Tiago Baptista</a></p></footer>')


############################ Main Function for functional use #################################################

def exec(argv):
    # Variable to control the datatype we are parsing
    controller      = 0
    general         = []
    datatypes       = []
    objects_about   = []
    data_props      = []
    classes         = []
    individuals     = []
    if not (path.exists('output')):
        os.mkdir('output')
    # Check if the file exists and has the correct extension
    if path.exists(argv[0]) and (".rdf" in argv[0]) :
        with open(argv[0],'rt',encoding="utf-8") as f:
            for line in f:
                controller = verifier(line,controller)
                if(controller == 0):
                    general.append(line.strip())
                if(controller == 2):
                    datatypes.append(line.strip())
                if(controller == 3):
                    objects_about.append(line.strip())
                if(controller == 4):
                    data_props.append(line.strip())
                if(controller == 5):
                    classes.append(line.strip())
                if(controller == 6):
                    individuals.append(line.strip())
        ## Now we have all the information in arrays ready to be parsed and extract information
        general_info(general)
        datatypes_info(datatypes)
        object_info(objects_about)
        data_prop_info(data_props)
        class_info(classes)
        individuals_info(individuals)
        footer()
    else:
        print ( " Error : Please insert a file with .rdf extension")



############################ Main Function #################################################

def main():
# verify if the output path exists
    if not os.path.exists('output'):
        os.makedirs('output')

    # Variable to control the datatype we are parsing
    controller      = 0
    general         = []
    datatypes       = []
    objects_about   = []
    data_props      = []
    classes         = []
    individuals     = []
    # Check if the file exists and has the correct extension
    if path.exists(sys.argv[1]) and (".rdf" in sys.argv[1]) :
        with open(sys.argv[1],'rt',encoding="utf-8") as f:
            for line in f:
                controller = verifier(line,controller)
                if(controller == 0):
                    general.append(line.strip())
                if(controller == 2):
                    datatypes.append(line.strip())
                if(controller == 3):
                    objects_about.append(line.strip())
                if(controller == 4):
                    data_props.append(line.strip())
                if(controller == 5):
                    classes.append(line.strip())
                if(controller == 6):
                    individuals.append(line.strip())
        ## Now we have all the information in arrays ready to be parsed and extract information
        general_info(general)
        datatypes_info(datatypes)
        object_info(objects_about)
        data_prop_info(data_props)
        class_info(classes)
        individuals_info(individuals)
        footer()
    else:
        print ( " Error : Please insert a file with .rdf extension")


if __name__ == "__main__":
    main()
