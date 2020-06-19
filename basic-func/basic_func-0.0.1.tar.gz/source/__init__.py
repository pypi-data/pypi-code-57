import random as rnd

global true,false

true = True
false = False

def rand_bl():
  global true,false

  f6y = rnd.randint(0,1)
  if f6y == 1:
    return true
  else:
    return false

def rplc(z1k, p3e, y7q):
  zik.remove(p3e);
  z1k.insert(p3e,y7q);

def mns(t1d):
  return t1d * -1

def pls_abs(i8u):
  return abs(i8u)

def mns_abs(f9e):
  return mns(pls_abs(f9e))

def reset():
  global true,false

  true = True
  false = False

