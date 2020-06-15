import requests
URL      = 'https://data.ivanstanojevic.me/api/tle/43554'


def position_data():
    """ I wish I could tell you what this number is ... position of something up there!
    :return: float
    """
    r = requests.get(URL)
    return float(r.json()['line2'].split(' ')[8])



if __name__=="__main__":
    print(position_data())