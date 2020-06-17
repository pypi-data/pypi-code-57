import numpy as np
from . import btypes

ID_COUNTER = 1



def new_vector(radius=1., theta=0., phi=0.):
        x = lambda r, t, p: r*np.sin(t)*np.cos(p)
        y = lambda r, t, p: r*np.sin(t)*np.sin(p)
        z = lambda r, t, p: r*np.cos(t)
        vect = np.array([x(radius, theta, phi),
                         y(radius, theta, phi),
                         z(radius, theta, phi)])
        return vect


def new_t_obj(position, frame, label):
    """ get a bayesiantracker object from an observation """
    global ID_COUNTER
    obj = btypes.PyTrackObject()
    obj.ID = ID_COUNTER
    obj.x = position[0]
    obj.y = position[1]
    obj.z = position[2]
    obj.t = frame
    obj.dummy = False
    obj.label = label
    obj.probability = np.zeros((5,),dtype='float')
    ID_COUNTER+=1
    return obj


class AgentManager(object):
    def __init__(self,
                 num_agents=100,
                 periodic_boundary=False,
                 noise=0.01,
                 box=1024):

        self.num_agents = num_agents
        self.periodic_boundary = periodic_boundary
        self.noise = noise
        self.box = box

        self.__current_ID = 0

        self.agents = []


    def simulate(self, num_frames):
        """ run the simulation """
        agents = [Agent(ID=self.get_new_ID(),
                  noise=self.noise,
                  periodic_boundary=self.periodic_boundary,
                  position=(512.,512.,512.),
                  frame=0,
                  box=self.box) for a in range(self.num_agents)]

        to_add = []

        # iterate over the frames
        for i in range(num_frames):

            for agent in agents:
                ret = agent.update()
                if ret == 2:
                    to_add = self.mitosis(agent)

            # append any new agents here
            while to_add:
                agents.append(to_add.pop(0))

        self.agents = agents


    def mitosis(self, agent):
        """ perform a mitosis """
        current_pos = agent.position
        r = np.random.randint(5,20)
        theta = np.random.randn()*np.pi
        phi = np.random.randn()*np.pi
        v = new_vector(radius=r, theta=theta, phi=phi)

        frame = agent.frames[-1]+1

        new_pos = [current_pos-v, current_pos+v]
        new_agents = [Agent(ID=self.get_new_ID(),
                            noise=self.noise,
                            periodic_boundary=self.periodic_boundary,
                            frame=frame+1,
                            position=p.tolist(),
                            box=self.box) for p in new_pos]

        print("Mitosis {}->{},{}".format(agent.ID, new_agents[0].ID, new_agents[1].ID,))

        return new_agents


    def get_new_ID(self):
        """ get a new ID """
        self.__current_ID+=1
        return self.__current_ID


    def get_data(self):
        """ get all of the data """
        data = []
        for agent in self.agents:
            data += agent.get_objects()
        return data

class Agent(object):
    """ Agent

    An Agent class that can be used to simulate a moving object in a field of
    view.

    Args:
        noise: normally distributed noise in speed and angle(s)
        periodic_boundary: a bool which causes agents to wrap around edges of
            bounding box
        box: size of initialisation/bounding box
        speed: agent speed

    """
    def __init__(self,
                 ID=0,
                 noise=.1,
                 periodic_boundary=False,
                 position=[],
                 frame=0,
                 box=1024):

        self.ID = ID

        self.box = box
        self.periodic_boundary = periodic_boundary

        if not position:
            self.position = np.random.randint(0,high=self.box, size=(3,))
        else:
            self.position = np.array(position)

        self.theta = np.random.randn(2,)*np.pi # az and elev
        self.speed = 1.
        self.noise = noise

        self.frame = frame

        # position, label=3 (anaphase for starting track)
        self.trajectory = [self.position]
        self.labels = [3]
        self.frames = [frame]

        self.predicted = None

        # sampling noise
        self.sample_noise = 0.1
        self.sample_iter = 0

        # active track?
        self.active = True

        # division?
        self.division_time = 300


    @property
    def division_clock(self):
        return self.frames[-1]-self.frames[0]

    def update(self):
        if not self.active:
            return None

        t = self.theta + np.random.randn(2,)*self.noise
        s = max(self.speed + np.random.randn()*self.noise, 0.)
        # v = [np.cos(t[0])*np.cos(t[1]), np.sin(t[0])*np.cos(t[1]), np.sin(t[1])]
        v = new_vector(radius=s, theta=t[0], phi=t[1])
        v[-1] = 0.
        self.position = self.position + v

        if self.periodic_boundary:
            self.position = np.mod(self.position, self.box)

        if self.divide():
            label = 2 # metaphase
        else:
            label = 0 # interphase

        self.frames.append(self.frames[-1]+1)
        self.trajectory.append(self.position)
        self.labels.append(label)
        self.theta = t

        return label



    def divide(self):
        if self.division_clock >= self.division_time+np.random.randn()*1:
            self.active = False
            return True
        return False


    def get_objects(self):
        objects = []
        for i in range(len(self)):
            o = new_t_obj(self.trajectory[i],
                          self.frames[i],
                          self.labels[i])
            objects.append(o)
        return objects


    def __len__(self): return len(self.trajectory)


    @property
    def x(self): return self.coords(0)
    @property
    def y(self): return self.coords(1)
    @property
    def z(self): return self.coords(2)

    def coords(self, axis=0):
        return [self.trajectory[i][axis] for i in range(len(self.trajectory))]


if __name__ == "__main__":
    pass
