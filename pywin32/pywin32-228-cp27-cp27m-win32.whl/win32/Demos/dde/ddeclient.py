# 'Request' example added jjk  11/20/98

import win32ui
import dde

server = dde.CreateServer()
server.Create("TestClient")

conversation = dde.CreateConversation(server)

conversation.ConnectTo("RunAny", "RunAnyCommand")
conversation.Exec("DoSomething")
conversation.Exec("DoSomethingElse")

conversation.ConnectTo("RunAny", "ComputeStringLength")
s = 'abcdefghi'
sl = conversation.Request(s)
print 'length of "%s" is %s'%(s,sl)

