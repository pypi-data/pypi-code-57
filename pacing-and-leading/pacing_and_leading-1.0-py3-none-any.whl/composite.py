import copy,curses
from . import geometry

class Composite:

    def __init__(self,instances,console=False):

        self._instances = instances
        self._total_weights = float(sum([i[0] for i in instances]))

        self.console = console
        if console:
            self._screen = curses.initscr()
            curses.noecho()
            curses.curs_set(0)
            curses.start_color()
            curses.use_default_colors()
            curses.init_pair(1,curses.COLOR_GREEN,-1)
            curses.init_pair(2,curses.COLOR_BLUE,-1)

    def exit(self):
        curses.endwin()
            
    def _display(self,similarities,similarity,width=100):

        self._screen.clear()

        similarities.append((None,"total",similarity))
        
        titles = [s[1] for s in similarities]
        longer_title = max([len(t) for t in titles])
        def fix_size(s,size):
            l = len(s)
            s = s+" "*(size-l)+" "
            return s
        titles = list( map( lambda title:fix_size(title,longer_title),
                            titles ) )
        
        scores = [s[2] for s in similarities]
        weights = [s[0] for s in similarities]
        
        for weight,title,score in zip(weights,titles,scores):

            if weight!=0:
            
                score = int(score*width)
                try:
                    weight_str = "("+"%.2f" % round(weight,2)+")"
                except:
                    weight_str = "      "
                
                self._screen.addstr(title+weight_str+": "+"|"*score+"\n")

        self._screen.refresh()
            
    def __call__(self,arg1,arg2=None):

        def _none_safe(v):
            if v is None:
                return 0
            return v

        def _get_position(i):
            r = i(arg1)
            try :
                position,_,_,x_shift = r
                p = copy.deepcopy(position)
                p[0]+=x_shift
                return p
            except:
                return r[0]

        if arg2 is None:
            # for positions (vectors)
            r = self._instances[0][1](arg1)
            try:
                _,size,color = r
            except:
                _,size,color,_ = r
            weighted_vectors = [[i[0],_get_position(i[1])] for i in self._instances]
            value =  geometry.linear_combination(weighted_vectors)
            return [v/self._total_weights for v in value],size,color
        else :
            # for similarity (scalar)
            value = sum([i[0]*_none_safe(i[1](arg1,arg2)) for i in self._instances])
            value = value/self._total_weights
            
            if self.console:
                similarities = [ (i[0],
                                  i[1].__class__.__name__,
                                  _none_safe(i[1](arg1,arg2)))
                                 for i in self._instances ]
                self._display(similarities,value)

            return value
                

