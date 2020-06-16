import re

from pyramid.response import Response
from pyramid.authentication import AuthTktCookieHelper
from pyramid.settings import asbool
from pyramid.renderers import render_to_response

from ..constants import Conf
from ..models import PPSsuser,PPSsgroup,PPSspermission
from ..ppss_auth_utils import checkPassword

from pyramid.view import view_config,forbidden_view_config
from pyramid.httpexceptions import HTTPFound, HTTPNotFound
from beaker.cache import cache_region



import os,datetime,logging
l = logging.getLogger('ppssauth')


from pyramid.security import (
    Everyone, Authenticated,
    remember,forget,
    Allow,Deny,
    Everyone,ALL_PERMISSIONS
    )


def getPrincipals(uid,request):
    groups = request.session.get('principals',[])
    l.debug("####  usergroups:{g}".format(g=groups))
    return groups


class ACLBuilder(object):
    def __init__(self,baseACL,dbsession):
        self.baseACL = baseACL
        self.session  = dbsession

    @cache_region('short_term', 'ACLpermissions')
    def buildACL(self):
        groups = self.session.query(PPSsgroup).filter(PPSsgroup.enabled==1).all()
        acl = [] 
        for group in groups:
            acl.append( (Allow,
                    str("g:"+group.name),
                    tuple([str(p.name) for p in group.permissions])  
            ) )
        acl = self.baseACL + acl
        l.debug("acl built: {acl}".format(acl = acl))
        return acl



class ACLRoot(object):
    baseACL=[(Allow, Authenticated, 'view'),
        (Allow, 'g:superadmin', ALL_PERMISSIONS),
        (Deny,  'g:sysadmin', 'deleteadmin'),
        (Allow, 'g:sysadmin', ALL_PERMISSIONS)
        ]

    lastupdateACL = datetime.datetime.now()
    __acl__ = [
        (Allow, 'g:superadmin', ALL_PERMISSIONS),
        (Allow, 'g:sysadmin', ALL_PERMISSIONS),
    ]


    @classmethod
    @cache_region('short_term', 'ACLpermissions')
    def buildACL(cls,dbsession):
        groups = dbsession.query(PPSsgroup).filter(PPSsgroup.enabled==1).all()
        acl = [] 
        for group in groups:
            acl.append( (Allow,
                    str("g:"+group.name),
                    tuple([str(p.name) for p in group.permissions])  
            ) )
        ACLRoot.__acl__ = ACLRoot.baseACL + acl
        l.debug("built ACL:{acl}".format(acl=repr(ACLRoot.__acl__)) )


    def __init__(self, request):
        self.request = request
        aclb = ACLBuilder(ACLRoot.baseACL,request.dbsession)
        ACLRoot.__acl__ = aclb.buildACL()


class AuthController():

    def getUserById(self,userid):
        if userid<0:
            user = PPSsuser()
        else:
            user = PPSsuser.byId(userid,self.request.dbsession)
        return user

    def __init__(self,request):
        self.request = request
        self.user = None
        activemenu = ""
        activeaction = ""
        ##request.bt = Conf['bootstrapclasses']

        try:
            mr = self.request.matched_route.name.split(":")
            if len(mr) == 3:
                activemenu = mr[1]
                activeaction = mr[2]
        except:
            pass

        #for all ops on users, get the target user
        self.userid = int(self.request.matchdict.get("elementid",
            self.request.session[Conf.sessionuser]['id'] if Conf.sessionuser in self.request.session else -1 ) )
        self.user = self.getUserById(self.userid)
        

        self.retdict = {
            'midtpl':Conf.sectiontemplateinherit,
            'supertpl':Conf.mastertemplateinherit,
            'botplinherit':Conf.botemplateinherit,
            'activemenu' : activemenu,
            'activeaction' : activeaction,
            'bc': Conf.bootstrapClasses,
            'ppsauthconf':Conf,
            'msg':""
        }

    @view_config(route_name='ppsslogin',renderer=Conf.logintemplate)
    def login(self):
        r = self.request
        postloginpage = self.request.referer if (self.request.referer and self.request.referer!=self.request.route_url("ppsslogin")) else r.route_url(Conf.postloginroute)
        l.info("plp = {},referer = {}, loginurl = {}, plr = {}, is true? {}".format(
            postloginpage, 
            self.request.referer, 
            self.request.route_url("ppsslogin"),
            r.route_url(Conf.postloginroute), (self.request.referer and self.request.referer!=self.request.route_url("ppsslogin")) )   )
        self.request.session['postloginpage'] = postloginpage
        if self.user and self.user.passwordExpired():
                return HTTPFound(r.route_url("ppss:user:changepassword"))
        if r.POST:
            username = r.params.get("username",u"")
            password = r.params.get("password",u"")
            superuser = False
            res = None
            l.info("Login attempt: u={username}".format(username=username))
            if username == Conf.adminname:
                superuser =True
                if Conf.adminpass and password == Conf.adminpass:
                    u = PPSsuser.byField('username',username,r.dbsession)
                    if u:
                        res = u[0]
                    else:
                        self.retdict["msg"] = 'something went wrong with your login. Please check your informations'
                        return self.retdict
            if res is None:
                res = PPSsuser.checkLogin(username,password,r.dbsession)
            if res:
                res.lastlogin = datetime.datetime.now()  #TODO: don't commit lastlogin because the item get expunged
                
                if superuser:
                    l.info("{username} logged in as superuser".format(username=username) )
                    r.session['admin'] = True
                    r.session['principals'] = ["g:admin","g:superadmin"]
                else:
                    l.debug("{username} logged in as normal user".format(username=username) )
                    r.session['principals'] = res.getPrincipals(res.passwordExpired()) 
                    r.session['admin'] = False
                #r.userid=res.id
                r.dbsession.expunge(res)
                r.session[Conf.sessionuser] = {'id':res.id,'name':username,'user':res}
                headers = remember(r, res.id)
                return HTTPFound(postloginpage,headers=headers)
            self.request.dbsession.query(PPSsuser).filter()
            l.warn("Login attempt failed for user {user}".format(user=username))    
            self.retdict.update({'logintpl': Conf.publictemplateinherit ,'msg':'something went wrong with your login. Please check your informations'})
            return self.retdict
        self.retdict.update({'logintpl': Conf.publictemplateinherit , 'msg':''})
        return self.retdict

    @view_config(route_name='ppsslogout')
    def logout(self):
        l.debug("logout")
        l.debug("principals = {pr}".format(pr=self.request.session.get('principals',[])  ))

        headers = forget(self.request)
        self.request.session.pop('admin',None)
        self.request.session.pop(Conf.sessionuser,None)
        self.request.session.pop('principals',None)
        
        return HTTPFound(self.request.route_url(Conf.postlogoutroute),headers=headers)

    def oauthCallBack(self):
        return Response("OK")

    def registernewuser(self):
        retdict = self.retdict
        retdict["link"] = ["",""]
        if self.request.POST:
            cancreate = True
            username = self.request.params.get("username","")
            password = self.request.params.get("password","")
            confirmnewpassword = self.request.params.get("confirmnewpassword","")
            if not username:
                retdict["msg"] +="Username can not be empty."
                cancreate = False
            if not password:
                retdict["msg"] +="Password can not be empty."
                cancreate = False
            if password != confirmnewpassword:
                retdict["msg"] +="Password check doesn't match the password."
                cancreate = False
            if not checkPassword(PPSsuser(),password):
                retdict["msg"] +="Password doesn't respect minimum constraints."
                cancreate = False
            if cancreate:
                user = PPSsuser(username = username)
                user.setPassword(password)
                for g in Conf.newusergroups:
                    group = PPSsgroup.byName(g,self.request.dbsession)
                    if group:
                        user.groups.append(group)
                self.request.dbsession.add(user)
                retdict['msg'] = "User created, please go to login page."
                retdict["link"] = ["login",self.request.route_url("ppsslogin")]

            
            HTTPFound(self.request.route_url("ppsslogin"))
        return retdict
        
    @view_config(route_name="ppss:user:changepassword",renderer=Conf.changepasswordtemplate,permission='login')
    def ppsschangepassword(self):
        l.debug("change password")
        if not Conf.sessionuser in self.request.session:
            return HTTPFound(self.request.route_url("ppsslogin"))
        message = ""
        if self.user.passwordExpired():
            message = Conf.passwordexpiredmessage
        
        retdict = {'logintpl': Conf.publictemplateinherit,'msg':message,'res':True}
        retdict.update(self.retdict)
        if self.request.POST:
            oldpassword = self.request.params.get("oldpassword")
            newpassword = self.request.params.get("newpassword")
            username = self.request.session.get(Conf.sessionuser).get("name")
            res = PPSsuser.checkLogin(username,oldpassword,self.request.dbsession)     
            if res:
                res.password = newpassword       
                
            else:
                retdict['res']=False
                retdict['msg']='password is wrong'
        return retdict
        
    def listUser(self):
        elements = self.request.dbsession.query(PPSsuser).all()
        retdict = {'elements':elements}
        retdict.update(self.retdict)
        return retdict

    def editUser(self):
        l.info("edit user")
        userid = self.userid
        user = self.user
        if self.request.matched_route.name == 'ppss:user:editself':
            userid = self.request.session[Conf.sessionuser]['id']
            user = self.getUserById(userid)
            self.userid = userid
            self.user = user
        l.debug("***{id} -> {user}".format(user=user,id=userid))
        retdict = dict(self.retdict,**{'msg':"",'res':True,'userid':userid} )
        if not user:
            retdict['res'] = False
            retdict['msg'] = "user not found"

        editablegroups = []
        logged_id = self.request.session[Conf.sessionuser]['id']
        logged_user = self.getUserById(logged_id)

        
        if logged_user.isSuperUser():
            editablegroups = PPSsgroup.all(self.request.dbsession)
        if logged_user.hasPermission('edituser'):
            editablegroups =  logged_user.groups


        retdict.update({"user" : user, 'allgroups':editablegroups })

        if self.request.POST:
            if userid<0:
                self.request.dbsession.add(user)
            if not user:
                return retdict
            newpassword = self.request.params.get("password","")
            if newpassword:
                l.info("*****changing password for {}".format(user.username) )
                l.info("checkPassword result = {res}".format(res = checkPassword(user,newpassword) ))
                user.setPassword(newpassword)
            user.username = self.request.params.get("username",user.username)
            user.enabled = 1 if self.request.params.get("enabled")=="1" else 0
            
            groups=map(int,self.request.params.getall("allgroups"))
            l.debug("group={groups}".format(groups=groups ))
            usergroups = [PPSsgroup.byId(groupid,self.request.dbsession) for groupid in groups]
            user.groups = usergroups
            self.request.dbsession.flush()
            return HTTPFound(self.request.route_url('ppss:user:edit',elementid = user.id) )
            #return retdict

        return retdict

    def checkPassword(self):
        newpassword = self.request.get("newpassword","")
        if self.request.session[Conf.sessionuser]['id'] != self.userid and not self.request.session['admin']: 
            return {"res":False,"message":"Utente non autorizzato"}
            #TODO: log the incident
        if not self.user:
            return {"res":False,"message":"Utente non trovato"}
        
        res = checkPassword(self.user,newpassword)
        if res: 
            return {"res":res,"message":"ok"}
        else:
            return {"res":res,"message":Conf.passwordwrongmessage}


    def listGroup(self):
        elements = self.request.dbsession.query(PPSsgroup).all()
        return dict(self.retdict,**{'elements':elements}) 

    def editGroup(self):
        groupid = int(self.request.matchdict.get("elementid","-1"))
        retdict = dict(self.retdict,**{'msg':"",'res':True,'groupid':groupid} )
        if groupid<0:
            group = PPSsgroup()
        else:
            group = PPSsgroup.byId(groupid,self.request.dbsession)
            if not group:
                return HTTPFound(self.request.route_url('ppss:group:list'))
        retdict.update({'group':group})

        if self.request.POST:  #editing group
            if groupid<0:
                self.request.dbsession.add(group)
            group.name = self.request.params.get("name")
            group.enabled = 1 if self.request.params.get("enablecheck")=="1" else 0
            l.debug("paratri: {p}".format(p=self.request.params ) )
            l.debug("group.name={name},  group.enabled={enabled}".format(name=group.name,enabled=group.enabled))
            elements = self.request.dbsession.query(PPSsgroup).all()
            return dict(retdict,**{'elements':elements})

        elif group:
            allperm = self.request.dbsession.query(PPSspermission).all()
            users = self.request.dbsession.query(PPSsuser).all()
            return render_to_response(  Conf.editgrouptemplate,
                dict(retdict,**{'group':group,'allperm':allperm, 'users': users, 'msg':""}),
                self.request )
        #return HTTPFound(self.request.route_url("ppss:group:list") )

    def listPerm(self):
        elements = self.request.dbsession.query(PPSspermission).all()
        return dict(self.retdict,**{'elements':elements})

    def editPerm(self):
        pid = int(self.request.matchdict.get('elementid',-1) )
        if pid<0:
            perm = PPSspermission(id=pid)
        else:
            perm = PPSspermission.byId(pid,self.request.dbsession)

        if self.request.POST:
            elements = self.request.dbsession.query(PPSspermission).all()
            name = self.request.params.get("name","")
            if pid<0:
                self.request.dbsession.add(PPSspermission(name=name))
            elif perm.permtype!=1:
                perm.name = name
            else:
                res = {'res':False,'msg':"Impossibile modificare il permesso"}
                return dict(self.retdict,dict(res,**{'elements':elements}) )
            res = {'res':True,'msg':"Permesso modificato"}
            return dict(self.retdict,**dict(res,**{'elements':elements}) )
        elif perm:
            return render_to_response(  Conf.editpermtemplate,dict(self.retdict,**{'perm':perm}),self.request )
        return HTTPFound(self.request.route_url("ppss:perm:list") )

    def deletePerm(self):
        perm = PPSspermission.byId(int(self.request.matchdict.get('elementid',-1)))

        if perm and perm.permtype != 1:
            self.request.dbsession.delete(perm)
            res = {'res':True,'msg':"permesso cancellato"}
        else:
            res = {'res':False,'msg':"Impossibile cancellare il permesso"}
        elements = self.request.dbsession.query(PPSspermission).all()
        return dict(self.retdict,**dict(res,**{'elements':elements}) ) 



    def addPerm2Group(self):
        perm = PPSspermission.byId(int(self.request.matchdict.get('targetid',-1)),self.request.dbsession)
        group = PPSsgroup.byId(int(self.request.matchdict.get('elementid',-1)),self.request.dbsession)
        if not perm or not group:
            return {'res':False,"msg":"error in ids"}
        for i in group.permissions:
            if i.id == perm.id:
                return {'res':False,"msg":"already present"}
        group.permissions.append(perm)
        l.info(u"adding {perm} to {group}".format(perm=perm,group=group))
        return {'res':True,"msg":"change_perm", "groupperm":group.permdict()}

    def removePerm2Group(self):
        perm = PPSspermission.byId(int(self.request.matchdict.get('targetid',-1)),self.request.dbsession)
        group = PPSsgroup.byId(int(self.request.matchdict.get('elementid',-1)),self.request.dbsession)
        
        if perm and (perm.permtype != 'y'):  #TODO add superadmin capability to do this
            for i,p in enumerate(group.permissions):
                l.info("check {} {}".format(p.id,perm.id) )
                if p.id == perm.id:
                    l.info("match")
                    group.permissions.pop(i)
                    return {'res':True,"msg":"change_perm", "groupperm":group.permdict()}
                else:
                    l.info("no match")


        return {'res':False,'msg':"Impossibile rimuovere il permesso"}


    def addUser2Group(self):
        user  = PPSsuser.byId(int(self.request.matchdict.get('targetid',-1)),self.request.dbsession)
        group = PPSsgroup.byId(int(self.request.matchdict.get('elementid',-1)),self.request.dbsession)
        if not user or not group:
            return {'res':False,"msg":"error in ids"}
        for i in group.users:
            if i.id == user.id:
                return {'res':False,"msg":"already present"}
        group.users.append(user)
        l.info(u"adding {user} to {group}".format(user=user,group=group))
        return {'res':True,"msg":"change_user", "elements":group.userdict()}


    def removUser2Group(self):
        user  = PPSsuser.byId(int(self.request.matchdict.get('targetid',-1)),self.request.dbsession)
        group = PPSsgroup.byId(int(self.request.matchdict.get('elementid',-1)),self.request.dbsession)
        if user:  #TODO add superadmin capability to do this
            for i,p in enumerate(group.users):
                if p.id == user.id:
                    group.users.pop(i)
                    return {'res':True,"msg":"change_user", "elements":group.userdict()}
        return {'res':False,'msg':"Impossibile rimuovere il permesso"}

    def parseqstring(self,qparam):
        if qparam == "" or qparam is None:
            return ""
        qparam = " " + qparam + " "
        qparam = re.sub("[%]+", "\\%", qparam)
        qparam = re.sub("[ ]+", "%", qparam)
        return qparam




    @view_config(route_name='ppss:user:search',permission='listuser',renderer="json")
    def searchUser(self):
        qparam = self.parseqstring(self.request.params.get('q',''))
        l.debug("qparam = {qp}".format(qp=qparam))
        users = self.request.dbsession.query(PPSsuser).filter(PPSsuser.enabled==1).filter(PPSsuser.username.like(qparam)).all()
        return {'res':True,'elements':[u.todict() for u in  users]}

    @view_config(route_name='ppss:group:search',permission='listuser',renderer="json")
    def searchGroup(self):
        qparam = self.parseqstring(self.request.params.get('q',''))
        users = self.request.dbsession.query(PPSsgroup).filter(PPSsgroup.enabled==1).filter(PPSsgroup.name.like(qparam)).all()
        return {'res':True,'elements':[u.todict() for u in  users]}

    @view_config(route_name='ppss:perm:search',permission='listuser',renderer="json")
    def searchParam(self):
        qparam = self.parseqstring(self.request.params.get('q',''))
        users = self.request.dbsession.query(PPSspermission).filter(PPSspermission.name.like(qparam)).all()
        return {'res':True,'elements':[u.todict() for u in  users]}

    @view_config(route_name='test:test',permission='listuser',renderer=Conf.logintemplate)
    def testroute(self):
        return {}
