import ipaddress
import validators as val

def isIp(value):
    try:
        ipaddress.ip_address(value)
        return True
    except:
        return False

def isURL(value):
    return val.url(value)
