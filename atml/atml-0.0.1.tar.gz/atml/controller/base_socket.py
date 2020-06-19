from sklearn.pipeline import Pipeline

from logzero import logger


class SocketBase(object):
    def __init__(self, with_default=False):
        self._with_default = with_default
        self.plugs = []
        
    def register(self, plug):
        clazz = type(plug)
        
        if self._plug_index(clazz) > -1:
            logger.warning("Already exists: plug {0} in Socket {1}".format(clazz, self.__class__.__name__))
            return
        
        weight = 100 if len(self.plugs) == 0 else self.plugs[-1][0] - 1 
        self.plugs.append((weight, plug))
        
        self.plugs.sort(reverse=True)
        
        logger.info('Registered plug {0} in Socket {1}'.format(clazz, self.__class__.__name__))
    
    def register_with_weight(self, tuple_plug):
        weight, plug = tuple_plug
        clazz = type(plug)
        
        if self._plug_index(clazz) > -1:
            logger.info("Already exists: plug {0} in Socket {1}".format(clazz, self.__class__.__name__))
            return
        
        self.plugs.append((weight, plug))
        self.plugs.sort(reverse=True)
        
        logger.info('Registered plug {0} in Socket {1}'.format(clazz, self.__class__.__name__))
    
    def _plug_index(self, clazz):
        
        for ind, (_, plug) in enumerate(self.plugs):
            if type(plug) == clazz:
                return ind
    
        return -1
        
    def unregister(self, plug):
        clazz = type(plug)
        ind = self._plug_index(clazz)
        if ind > -1:
            del self.plugs[ind]
            logger.info('Unregistered plug {0} in Socket {1}'.format(clazz, self.__class__.__name__))
            
    
    def _plugs_to_pipe(self):     
        steps = []
        for _, instance in self.plugs:
            steps.append((instance.__class__.__name__, instance))
        
        return Pipeline(steps)