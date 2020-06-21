from .core.model import Model, Joint

class rollingJoint(Joint):
    def __init__(self, client, orientation, id):
        self.objectName = "rollingJoint_" + orientation + id
        super().__init__(client, self.objectName)

class Youbot(Model):
    def __init__(self, client, id = ""):
        self.objectName = "youBot" + id
        super().__init__(client, self.objectName)
        self.id = id

        self.rollingJoint_fl = rollingJoint(client, "fl", id)
        self.rollingJoint_fr = rollingJoint(client, "fr", id)
        self.rollingJoint_rl = rollingJoint(client, "rl", id)
        self.rollingJoint_rr = rollingJoint(client, "rr", id)

        self.wheel_radius = 0.05 
        return

    def actuate(self, forwBackVel, leftRightVel, rotVel):    #set four wheel speed according to vx,vy,w
        v0 = (-forwBackVel + leftRightVel + 0.38655 * rotVel) / self.wheel_radius
        v1 = (-forwBackVel - leftRightVel + 0.38655 * rotVel) / self.wheel_radius
        v2 = (-forwBackVel + leftRightVel - 0.38655 * rotVel) / self.wheel_radius
        v3 = (-forwBackVel - leftRightVel - 0.38655 * rotVel) / self.wheel_radius

        self.rollingJoint_fl.set_velocity(v0)
        self.rollingJoint_rl.set_velocity(v1)
        self.rollingJoint_rr.set_velocity(v2)
        self.rollingJoint_fr.set_velocity(v3)
    