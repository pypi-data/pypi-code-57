'''Helper tool'''

__version__ = "0.9.5"

from .main import link

if __name__ == '__main__':
    import pypungi
    
    pp = pypungi.link()
    pp.stash('hi')
    pp.getStash()
    