import requests,random
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from bane.payloads import ua
def wpadmin(u,username,password,path='/xmlrpc.php',timeout=10,proxy=None):
 '''
   this function is to check the wordpress given logins using the xmlrpc.php file. if they are correct it returns True, else False
'''
 if proxy:
  proxy={'http':'http://'+proxy}
 if u[len(u)-1]=='/':
  u=u[0:len(u)-1]
 s=False
 u+=path
 post ="""<methodCall>
<methodName>wp.getUsersBlogs</methodName>
<params>
<param><value>{}</value></param>
<param><value>{}</value></param>
</params>
</methodCall>""".format(username,password)
 try:
  r = requests.post(u, data=post,headers = {'User-Agent': random.choice(ua)},proxies=proxy,timeout=timeout, verify=False)
  if "isAdmin" in r.text:
   s=True
 except:
  pass
 return s
def wp_users_list(u,path='/wp-json/wp/v2/users',timeout=10,boolean=False,link=False,content=True,proxy=None):
 '''
   this function is to get WP users
'''
 if proxy:
  proxy={'http':'http://'+proxy}
 if u[len(u)-1]=='/':
  u=u[0:len(u)-1]
 s=''
 c=''
 b=False
 u+=path
 try:
  r=requests.get(u, headers = {'User-Agent': random.choice(ua)},proxies=proxy,timeout=timeout, verify=False)
  if ('{"id":'in r.text) and('"name":"' in r.text):
   s+=u
   b=True
   c=r.text
 except Exception as e:
  pass
 if link==True:
  return s
 if boolean==True:
  return b
 if content==True:
  return c
def wp_user(u,path='/wp-json/wp/v2/users/',user=1,timeout=10,boolean=False,link=False,content=True,proxy=None):
 '''
   this function is to return all informations about a WP user with a given index integer
'''
 if proxy:
  proxy={'http':'http://'+proxy}
 if u[len(u)-1]=='/':
  u=u[0:len(u)-1]
 s=''
 c=''
 b=False
 u+=path+str(user)
 try:
  r=requests.get(u, headers = {'User-Agent': random.choice(ua)},proxies=proxy,timeout=timeout, verify=False)
  if ('{"id":'in r.text) and('"name":"' in r.text):
   s+=u
   b=True
   c+=r.text
 except Exception as e:
  pass
 if link==True:
  return s
 if boolean==True:
  return b
 if content==True:
  return c
def wp_posts_list(u,path='/wp-json/wp/v2/posts',timeout=10,boolean=False,link=False,content=True,proxy=None):
 '''
   this function is to get WP posts
'''
 if proxy:
  proxy={'http':'http://'+proxy}
 if u[len(u)-1]=='/':
  u=u[0:len(u)-1]
 s=''
 c=''
 b=False
 u+=path
 try:
  r=requests.get(u, headers = {'User-Agent': random.choice(ua)},proxies=proxy,timeout=timeout, verify=False)
  if ('{"id":'in r.text) and('"date":"' in r.text):
   s+=u
   b=True
   c+=r.text
 except Exception as e:
  pass
 if link==True:
  return s
 if boolean==True:
  return b
 if content==True:
  return c
def wp_post(u,path='/wp-json/wp/v2/posts/',post=1,timeout=10,boolean=False,link=False,content=True,proxy=None):
 '''
   this function is to return all informations about a WP post with a given index integer
'''
 if proxy:
  proxy={'http':'http://'+proxy}
 if u[len(u)-1]=='/':
  u=u[0:len(u)-1]
 s=''
 c=''
 b=False
 u+=path+str(post)
 try:
  r=requests.get(u, headers = {'User-Agent': random.choice(ua)},proxies=proxy,timeout=timeout, verify=False)
  if ('{"id":'in r.text) and('"date":"' in r.text):
   s+=u
   b=True
   c+=r.text
 except Exception as e:
  pass
 if link==True:
  return s
 if boolean==True:
  return b
 if content==True:
  return c
def wp_users_enumeration(u,path='/',timeout=15,proxy=None,start=1,end=20,logs=True,returning=False):
 d=u.split('://')[1].split("/")[0]
 u=u.split(d)[0]+d
 if proxy:
  proxy={'http':'http://'+proxy}
 l=[]
 for x in range(start,end+1):
  try:
      r=requests.get(u+path+"?author="+str(x),headers = {'User-Agent': random.choice(ua)},proxies=proxy,timeout=timeout, verify=False).text
      a=r.split('<meta property="og:title" content="')[1].split('>')[0]
      if ',' in a:
       a=a.split(',')[0]
       l.append((x,a))
       if logs==True:
          print("[+]Username found: {} | ID: {}".format(a,x))
  except KeyboardInterrupt:
      break
  except:
      pass
 if returning==True:
     return l
def wp_version(u,timeout=15,proxy=None):
 if proxy:
  proxy={'http':'http://'+proxy}
 try:
  r=requests.get(u,headers = {'User-Agent': random.choice(ua)},proxies=proxy,timeout=timeout, verify=False).text
  return r.split('<meta name="generator" content="')[1].split('"')[0].strip()
 except:
  pass
