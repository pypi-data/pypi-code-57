'''
EnviroData QC

Quality control and assurance of
environmental data including:
- air...
'''

from envirodataqc.checkdata import checkvals

#------------------ Check All --------------------#
def persus(data):
    '''
    Returns % suspicious data
    '''
    susp = len(data[data.flags==1])
    tot = len(data[data.flags!=2])
    susp = susp/tot*100
    susp = round(susp,0)

    return susp

def checkall(data):
    '''
    A function for running all other checks at once
    Returns:
    - Flagged data
    * Does not complete wind checks due to needed two inputs on wind dir!
    '''
    #Value and behavior check
    data = checkvals(data)
    #data = checkbehavior(data)

    return data