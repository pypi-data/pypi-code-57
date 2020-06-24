import time
from . import display
from . import geometry
from . import log

class _World:

    def __init__(self):

        self.cursor = None
        self.soft_target = None
        self.hard_target = None
        self.similarity = None
        self.vertical_targets = []
        self.arrows = []
        
class Experiment:

    def __init__(self,
                 duration,
                 frequency,
                 width,
                 height,
                 background,
                 similarity,
                 soft_target,
                 mediator,
                 hard_target,
                 cursor,
                 vertical_targets,
                 arrows):

        
        # frequency of display update
        self.frequency = frequency
        
        # attributes of the main window
        self.width = width
        self.height = height
        self.background = background

        # how much is the user motion (i.e. motion of the cursor)
        # similar to the hard target motion ?
        # should return a score between 0 (dissimilar) and 1 (identical)
        self._similarity = similarity
        
        # Circle is simply an holder for position,size(radius) and color
        # + an update function
        self._soft_target = display.Circle("soft_target",soft_target)
        self._hard_target = display.Circle("hard_target",hard_target)
        self._mediator = display.Circle("mediator",mediator)
        self._cursor = display.Circle("cursor",cursor)
        
        # All circles that needs management
        self._circles = [self._hard_target,
                         self._soft_target,
                         self._mediator,
                         self._cursor]
        
        # if target bars are to be used, adding them.
        # All parameters currently hard coded here
        if vertical_targets:
            self._vertical_target_left = display.VerticalLine("vertical_target_left",
                                                              vertical_targets[0])

            self._vertical_target_right = display.VerticalLine("vertical_target_right",
                                                              vertical_targets[1])
            self._vertical_bars = [self._vertical_target_left,
                                   self._vertical_target_right]

        else :
            self._vertical_bars = []

        if arrows:

            self._arrows = [ display.Arrow("arrow_"+str(index),
                                           arrow.length,
                                           arrow.width,
                                           arrow.tip_size,
                                           arrow)
                             for index,arrow in enumerate(arrows) ]

        else :

            self._arrows = []

        # time of start
        self._time_start = time.time()

        # update will throw an exception
        # once time passed
        self._duration = duration
        
        # for logging in a file on exit
        self._log = log.Log()
        
    def update(self,cursor):

        if(time.time()-self._time_start) > self._duration:
            raise TimeoutError("experiment finished")
        
        # computes the attributes of all circles
        # for an iteration

        # world is the (read only) shared memory
        # providing all info required for the update
        # of each circle and each vertical target (if any)
        world  = _World()
        world.cursor = cursor
        world.soft_target = self._soft_target.get_position()
        world.hard_target = self._hard_target.get_position()
        world.similarity = self._similarity(world.cursor,
                                            world.hard_target)
        world.vertical_targets = [vb.get_source()
                                 for vb in self._vertical_bars]
        
        # for logging in a file on exit
        self._log.set(time.time()-self._time_start,cursor,world.soft_target,
                      world.hard_target,world.similarity)
        
        # each circle calls its own update function, to
        # update position,size and color
        list ( map(lambda c: c.update(world), self._circles) )

        # each vertical target calls its own update function
        # as well
        list ( map(lambda vb: vb.update(world), self._vertical_bars) )

        # same for arrows
        list ( map(lambda a: a.update(world), self._arrows) )
        
        # returning for each circle/vertical bar an instance with attributes
        # position, size and color
        return [ circle.get()
                 for circle
                 in self._circles ], [vb.get()
                                      for vb
                                      in self._vertical_bars] , [a.get()
                                                                 for a
                                                                 in self._arrows]


    
    def save(self):

        file_path = self._log.save()
        print("saved results in",file_path)
            
