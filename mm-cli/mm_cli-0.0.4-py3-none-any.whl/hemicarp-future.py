
# def _functionFabric(func_name, argList, oargs, oargNames, password):
#     """Function fabric for Session class"""

#     def functionHandler(self, *args, **kwargs):
#         call_args = {}

#         pos = 0
#         for value in args:
#             if (pos < len(argList)):
#                 call_args[argList[pos]] = value
#                 pos += 1
#             elif (pos < len(argList) + len(oargNames)):
#                 call_args[oargNames[pos - len(argList)]] = value
#             else:
#                 print("warning: extraneous argument passed to function",func_name,value)

#         for (key, value) in kwargs.items():
#             if key not in oargs:
#                 if key in argList:
#                     # this is a positional argument, given a keyword name
#                     # that happens in python.
#                     # TODO: we can't handle this along with unnamed positional args.
#                     pos = argList.index(key)
#                     call_args[argList[pos]] = value
#                     continue
#                 else:
#                     print("warning: not an argument to this function",func_name,key)
#                     print(oargs)
#             else:
#                 # TODO: check oargs[key] type matches value
#                 # warn, if doesn't
#                 call_args[key] = value

#         return _callFunc(self, func_name, password, call_args)

#     functionHandler.__name__ = func_name
#     return functionHandler

######################
# # Get the functions and make the object
# page = 0
# availableFunctions = {}
# while True:
#     sock.send(
#         'd1:q24:Admin_availableFunctions4:argsd4:pagei' +
#         str(page) + 'eee')
#     data = sock.recv(BUFFER_SIZE)
#     benc = bdecode(data)
#     for func in benc['availableFunctions']:
#         availableFunctions[func] = benc['availableFunctions'][func]
#     if (not 'more' in benc):
#         break
#     page = page+1

# funcArgs = {}
# funcOargs = {}

# for (i, func) in availableFunctions.items():
#     items = func.items()

#     # required args
#     argList = []
#     # optional args
#     oargs = {}
#     # order of optional args for python-style calling
#     oargNames = []

#     for (arg,atts) in items:
#         if atts['required']:
#             argList.append(arg)
#         else:
#             oargs[arg] = atts['type']
#             oargNames.append(arg)

#     setattr(Session, i, _functionFabric(
#         i, argList, oargs, oargNames, password))

#     funcArgs[i] = argList
#     funcOargs[i] = oargs

# session = Session(sock)
##################################
# funcOargs_c = {}
#     for func in funcOargs:
#         funcOargs_c[func] = list(
#             [key + "=" + str(value)
#                 for (key, value) in funcOargs[func].items()])

#     for func in availableFunctions:
#         session._functions += (
#             func + "(" + ', '.join(funcArgs[func] + funcOargs_c[func]) + ")\n")
# return session..

class Hemicarp:
  """
  Admin API accessible with tcp or unix socket
    - admin_endpoint=("127.0.0.2", 3959)
    - admin_endpoint="/pirates/microprovision/remote-ygg.sock"
  """

  def __init__(self, name, admin_endpoint):
    self.name = name
    self.admin_endpoint = admin_endpoint
    self.list = self.yggCaller(json.dumps({"request":"list"}))
    self.nodeinfo = self.yggCaller(json.dumps({"request":"getself"}))['response']['self']
    self.ipv6 = list(self.nodeinfo.keys())[0]
    self.build_version = self.nodeinfo[self.ipv6]['build_version']
    self.box_pub_key = self.nodeinfo[self.ipv6]['box_pub_key']
    self.coords = self.nodeinfo[self.ipv6]['coords']
    self.subnet = self.nodeinfo[self.ipv6]['subnet']
  # /init

  def allowSource(self, subnet):
    return self.yggCaller(json.dumps({"request":"addlocalsubnet", "subnet": subnet}))

  def addRoute(self, subnet, pubkey):
    return self.yggCaller(json.dumps({"request":"addremotesubnet", "subnet": subnet, "box_pub_key": pubkey}))

  def addPeer(self, uri):
    return self.yggCaller(json.dumps({"request":"addpeer", "uri": uri}))

  def getPeers(self):
    return self.yggCaller(json.dumps({"request":"getpeers"}))['response']['peers']

  def enableTunnel(self):
    return self.yggCaller(json.dumps({"request":"settunnelrouting", "enabled": True}))['response']['enabled']

  def disableTunnel(self):
    return self.yggCaller(json.dumps({"request":"settunnelrouting", "enabled": False}))['response']['enabled']


  def yggCaller(self, pqrs):
    try:
      if (type(self.admin_endpoint) == str):
        s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
      elif (type(self.admin_endpoint) == tuple):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      else:
        print ('unknown yggdrasil endpoint type', type(self.admin_endpoint))
      s.connect(self.admin_endpoint)
      s.send(pqrs.encode('utf-8'))
      f = s.makefile('r')

    except PermissionError as e:
      print('error:: Permission Error AF_UNIX: ' + self.admin_endpoint)
      print('        Try: chown root:$(whoami) ' + self.admin_endpoint)
      exit()


    while True:
      data = f.read();
      if (data == ""):
        break
      else:
        try:
          gatos += data
        except NameError as e:
          gatos = data

    s.close()

    try:
      return json.loads(gatos)
    except:
      return {"status": "error"}
  #<!-- end caller-->
