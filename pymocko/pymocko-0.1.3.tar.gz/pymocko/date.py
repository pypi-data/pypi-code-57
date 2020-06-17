import random as r
from datetime import datetime, timedelta

def mock(f=datetime(1900,1,1), t=datetime.today()):
    if f is None:
        f = datetime(1900,1,1)
    if t is None:
        t = datetime.today()

    diff = abs(t-f).days + 1
        
    return f + timedelta(days=int(r.uniform(0,diff)))