import inspect
import os
import shutil
import dominate
import Dominate_Layui.static 
from dominate.document import *
from dominate.tags import *

COUNTS = 0
def __getVarName(variable):
    callers_local_vars = inspect.currentframe().f_back.f_locals.items()
    return [var_name for var_name, var_val in callers_local_vars if var_val is variable]

class HTMLDocument(document):
    pass

def linkInit(doc:HTMLDocument) ->None:
    """To initialize layui, you need to pass in a document object"""
    doc.head+=script(src="static/layui/layui.all.js")
    doc.head+=script(src="static/layui/init.js")
    doc.head+=link(href="static/layui/css/layui.css",rel="stylesheet")
    doc.head+=link(href="static/layui/css/layui.mobile.css",rel="stylesheet")
def FuncBtnAdd(doc:HTMLDocument,title:str,color:str="primary",radius:str="null",fluid:str="none",size:str="nr",onClick:str=None):
    """color:primary,normal,None,warm,danger
        radius:'null'/'radius'
        fluid:'none'/'fluid'
        size:lg,nr,sm,xs"""
    l=[doc,title,color,radius,fluid,size,onClick]
    front_attribute="layui-btn-"
    attribute="layui-btn"
    for i in l:
        if type(i)==type(None):
            l.remove(i)
    if not onClick:
        for i in l:
            #print(__getVarName(i))
            if __getVarName(i)[1]!="doc":
                if __getVarName(i)[1]!="title":
                    if i=="null" or i=="none":
                        continue
                    else:
                        attribute+=" "
                        attribute+=front_attribute+str(i)
                else:
                    continue
        doc.body.add(button(title,Class=attribute))
    else:
        for i in l:
            if __getVarName(i)[1]!="onClick":
                if __getVarName(i)[1]!="doc":
                    if __getVarName(i)[1]!="title":
                        if i=="null" or i=="none":
                            continue
                        else:
                            attribute+=" "
                            attribute+=front_attribute+str(i)
                    else:
                        continue
            else:
                continue
        doc.body.add(button(title,Class=attribute,onclick=onClick))
    return

def LinkBtnAdd(doc:HTMLDocument,title:str,color:str="primary",radius:str="null",fluid:str="none",size:str="nr",href:str=None):
    """color:primary,normal,None,warm,danger
        radius:'null'/'radius'
        fluid:'none'/'fluid'
        size:lg,nr,sm,xs"""
    l=[doc,title,color,radius,fluid,size,href]
    front_attribute="layui-btn-"
    attribute="layui-btn"
    for i in l:
        if type(i)==type(None):
            l.remove(i)
    for i in l:
        #print(__getVarName(i))
        if __getVarName(i)[1]!="href":
            if __getVarName(i)[1]!="doc":
                if __getVarName(i)[1]!="title":
                    if i=="null" or i=="none":
                        continue
                    else:
                        attribute+=" "
                        attribute+=front_attribute+str(i)
                else:
                    continue
    link=a(href=href)
    link.add(button(title,Class=attribute))
    doc.body.add(link)
    return
def htmlbr(doc:HTMLDocument):
    '''Just a Tag<br>.'''
    doc.add(br(doc))
def render(doc:HTMLDocument,DocName:str):
    """Copy the static resources, Doc renders them
into strings and writes them to the specified file"""
    __StaticGot()
    file=open(DocName,"w",encoding="utf-8")
    file.write(str(doc))
    file.close()
    return (doc,DocName,len(str(doc)))

def __copyFiles(sourceDir,targetDir):
    global COUNTS
    for f in os.listdir(sourceDir):
        sourceF = os.path.join(sourceDir, f)
        targetF = os.path.join(targetDir, f)
        if os.path.isfile(sourceF):
            if not os.path.exists(targetDir):
                os.makedirs(targetDir)
                COUNTS += 1
            if not os.path.exists(targetF) or (os.path.exists(targetF) and (os.path.getsize(targetF) != os.path.getsize(sourceF))):
                open(targetF, "wb").write(open(sourceF, "rb").read())
        else:
            if os.path.isdir(sourceF):
               __copyFiles(sourceF, targetF)
    COUNTS=0
    
def __StaticGot():
    """Copy all static resources to the current directory"""
    path=os.path.dirname(Dominate_Layui.static.__file__)
    __copyFiles(path,"static")
    os.remove("static/__init__.py")
    shutil.rmtree("static/__pycache__")
if "__main__"==__name__:
    Test=HTMLDocument()
    linkInit(Test)
    FuncBtnAdd(Test,title="Hello World",radius="radius",color="danger",onClick=("AlertBox('HEYSS')"))
    print(Test)
    __StaticGot()
