"""
Written by Ivan Debono
mail [at] ivandebono [dot] eu


22 June 2020

PURPOSE Output the Thue-Morse sequence T_n up to the desired n

INPUT   n: length of sequence

OUTPUT  s: string representation of Thue-Morse sequence

"""    


def negation(s):
    return s.replace('1', '2').replace('0', '1').replace('2', '0')

def thuemorse(n):
    s=str(0)    
    for i in np.arange(n):
        s=str(s+negation(s))
    return s