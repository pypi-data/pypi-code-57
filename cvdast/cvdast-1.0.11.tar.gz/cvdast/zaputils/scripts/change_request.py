
def sendingRequest(msg, initiator, helper):
    global OLD_STRING;
    global NEW_STRING;

    body = msg.getRequestBody().toString();
    print(dir(msg))


def responseReceived(msg, initiator, helper):
    pass;