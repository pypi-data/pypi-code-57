import requests


def isSessionUp(sessionUrl):
    try:
        requests.get(sessionUrl)
        return True
    except Exception as error:
        print(error)
        return False


class SessionManager:
    pass


if __name__ == '__main__':
    print(isSessionUp('http://192.168.0.188:52419/wd/hub'))
