""" ddp - data printer """

import sys
from colored import fore, back, style


SCHEME_DEFAULT = dict(
    bool = fore.LIGHT_BLUE,
    none = fore.LIGHT_BLUE,
    int = fore.LIGHT_YELLOW,
    float = fore.LIGHT_YELLOW,
    str = fore.LIGHT_GREEN,
    bytes = fore.LIGHT_MAGENTA,
    object = fore.LIGHT_RED,
    key = fore.LIGHT_CYAN,
    ref = fore.RED,
    punct = fore.WHITE,
)


class SchemeColors:
    ''' Схема цветов '''
    def __init__(self, **kw):
        x = dict(**SCHEME_DEFAULT)
        for k in kw:
            x[k]    # тест на профпригодность
            x[k] = kw[k]
        for k in x:
            setattr(self, k, x[k])
            

class DDP:
    def __init__(self, color):
        self.ref = {}   # memaddr => pathaddr
        self._idents = []
        self.s = []
        self.path = [] # pathaddr
        self.color = SchemeColors(**color) if isinstance(color, dict) else (color if isinstance(color, SchemeColors) else SchemeColors())
        self.is_color = bool(color)
        
    
    def echo(self, x, c):
        if self.is_color:
            self.s.append(c)
        self.s.append(x)
    
        
    def ident(self, n):
        ''' Кеширует отступы '''
        i = self._idents
        
        if n == len(i):
            i.append(' ' * (n*2))
        return i[n]


    def el_dict(self, e):
        ''' Распечатывает элемент словаря '''
        k, v = e

        self.path[-1] = str(k)
        self.np(k)
        self.echo(": ", self.color.punct)
        self.np(v)


    def el_object(self, e):
        ''' Распечатывает элемент объекта '''
        k, v = e
        self.path[-1] = str(k)
        self.echo(k, self.color.key)
        self.echo("=", self.color.punct)
        self.np(v)


    def el_list(self, e):
        ''' Распечатывает элемент объекта '''
        k, v = e
        self.path[-1] = str(k)
        self.echo('[%d] ' % k, self.color.punct)
        self.np(v)

    def struct(self, fill, iterator, sk1, sk2, elem_fn):
        ''' Структура '''
        space = self.ident(len(self.path))
        self.path.append(None)
        spaces = self.ident(len(self.path))
        self.echo(sk1, self.color.punct)
        if fill:
            self.echo("\n", style.RESET)
            for e in iterator:
                self.echo(spaces, '')
                elem_fn(e)
                self.echo(",\n", self.color.punct)
            self.echo(space, '')
        self.echo(sk2, self.color.punct)
        self.path.pop()


    def np(self, p):
        """ Распечатывает данные в список """
        
        if isinstance(p, (dict, list, tuple)) or isinstance(p, object) and hasattr(p, '__dict__'):
        
            addr = id(p)
            if addr in self.ref:
                self.echo("<%s at %s>" % (type(p), '.'.join(self.ref[addr]) or '<root>'), self.color.ref)
                return
            
            self.ref[addr] = self.path[:]
        
            if isinstance(p, object) and hasattr(p, '__dict__'):
                self.echo(
                    p.__class__.__name__+
                    (' '+p.__name__ if hasattr(p, '__name__') else '')+
                    (' of '+p.__self__.__class__.__name__ if hasattr(p, '__self__') else '')
                , self.color.object)
                self.struct(
                    fill=bool(p.__dict__),
                    iterator=p.__dict__.items(),
                    sk1="(",
                    sk2=")",
                    elem_fn=self.el_object,
                )

            if isinstance(p, dict):
                self.struct(
                    fill=bool(p),
                    iterator=p.items(),
                    sk1="{",
                    sk2="}",
                    elem_fn=self.el_dict,
                )
            elif isinstance(p, list):
                self.struct(
                    fill=bool(p),
                    iterator=enumerate(p),
                    sk1="[",
                    sk2="]",
                    elem_fn=self.el_list,
                )
            elif isinstance(p, tuple):
                self.struct(
                    fill=bool(p),
                    iterator=enumerate(p),
                    sk1="(",
                    sk2=")",
                    elem_fn=self.el_list,
                )
            
                
        
        elif isinstance(p, str):
            self.echo(repr(p), self.color.str)
        elif isinstance(p, bool):
            self.echo(repr(p), self.color.bool)
        elif isinstance(p, int):
            self.echo(repr(p), self.color.int)
        elif isinstance(p, float):
            self.echo(repr(p), self.color.float)
        elif isinstance(p, bytes):
            self.echo(repr(p), self.color.bytes)
        else:
            self.echo(repr(p), self.color.none)



def np(p, color=False):
    x = DDP(color)
    x.np(p)
    x.echo('\n', style.RESET)
    return "".join(x.s)



class DDPFile(DDP):
    def __init__(self, file, color):
        super().__init__(color)
        self.file=file


    def echo(self, x, c):
        if self.is_color:
            self.file.write(c)
        self.file.write(x)



def p(data, file=sys.stdout, color=True):
    x = DDPFile(file, color)
    x.np(data)
    x.echo('\n', style.RESET)
