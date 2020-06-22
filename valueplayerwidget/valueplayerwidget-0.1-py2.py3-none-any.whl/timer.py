from threading import Timer,Thread,Event

__version__ = '0.1'

class PerpetualTimer():
    """
        A timer 
    """
    def __init__(self,fps,tick):
        """
            Initialization of the PerpetualTimer
            
            Parameters
            ----------
            fps : (type=int) Frame Per Second
            tick : Player's tick
            
        """
        self.fps=fps
        self.tick = tick
        self.thread = None #Timer(self.t,self.handle_function)
        self.isrunning=False
        self.run()
        
    def handle_function(self):
        """"
            Controls the time (start, stop, how long to wait, cancel, restart...)
        """
        assert self.thread is not None
        assert self.isrunning 
        self.tick()
        self.thread.cancel()
        self.thread = Timer(1/self.fps,self.handle_function)
        self.thread.start()

    def set_fps(self,fps):
        """
            Convert fps to second
        """
        self.fps=fps    
        if self.isrunning:
            self.cancel()
            self.start()
   
    def run(self):
        """
            Start the timer
        """
        if (self.isrunning):
            return 
        self.thread = Timer(1/self.fps,self.handle_function)
        self.thread.start()
        self.isrunning=True   

    def running(self):
        """
            Return whether the timer is running or not
        """
        return self.isrunning
    
    def start(self):
        """
            Starts the timer
        """
        if (self.isrunning):
            return 
        self.thread = Timer(1/self.fps,self.handle_function)
        self.thread.start()
        self.isrunning=True

    def cancel(self):
        """
            Stops the timer
        """
        if self.isrunning:
            self.thread.cancel()
            self.thread=None
            self.isrunning=False

