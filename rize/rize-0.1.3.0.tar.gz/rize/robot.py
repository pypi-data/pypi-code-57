import nep
import threading
import time
import signal
import sys, os

class robot:
    
    def __init__(self, robot_name, middleware = "ZMQ", debug = False):
        """ Define a new robot

            Parameters
            ----------

            robot_name : string
                Node or robot name which identify the robot
        """

        self.robot_name = robot_name
        self.debug = debug
        self.middleware = middleware
        self.currentActionID = "0"
        self.node = nep.node(robot_name, self.middleware, True)
        self.rize = self.node.new_pub("rize_event", "json")
        self.sharo = self.node.new_pub("action_state", "json")
        print ("ROBOT NODE using: "  + self.middleware)
        self.sub_action = self.node.new_callback("robot_action", "json", self.callback_action)
        time.sleep(.5)
    
        self.state = "idle" # state can only be idle, busy or wait
        self.result = "inactive" # result can only be success or failure.
        self.action2do = {"active":False, "bt":{}}

        # Give feedback to the rize interface
        self.robot_actions = {}
        self.robot_cancel_actions = {}

        self.isCanceled = False
        self.inActionExecution = False
        self.running = True

        # ------------------------- Action thread ------------------------------------
        self.action_thread = threading.Thread(target = self.onActionLoop)
        self.action_thread.start()
        time.sleep(.1)
        
        # ------------------------- Stop thread ------------------------------------
        self.cancel_thread = threading.Thread(target = self.onCancelLoop)
        self.cancel_thread.start()
        time.sleep(.1)

    def onConnectSuccess(self):
        self.rize.publish({"robot":"ready", "name": self.robot_name})


    def onConnectError(self):
        self.rize.publish({"robot":"connection_error", "name": self.robot_name})

    def onExecutionError(self):
        self.rize.publish({"robot":"execution_error", "name": self.robot_name})

    def onActionLoop(self):
        print("Action loop started")

        while self.running:  # While in execution  
            if self.action2do["active"] == True:                                                # If there is an action to be executed
                if self.action2do["bt"]["state"] == "idle":                                     # If that action was idle
                    self.inActionExecution = True #TODO: lock                                   # There is an action in execution
                    print ("Action with id: " + self.action2do["bt"]["id"] +" started")
                    self.runAction(self.action2do["bt"])                                        # Run the action
                    print ("Action with id: " + self.action2do["bt"]["id"] +" finished\n")
                    self.inActionExecution = False #TODO: lock                                  # No more action in execution
                    self.action2do["bt"]["state"] = "success"                                   # Return success
                    self.action2do["active"] == False                                           # Desactivate this action
                    self.sharo.publish(self.action2do["bt"])                                    # Public new action state
                time.sleep(.001)

                if self.action2do["bt"]["state"] == "success":                                  # Delete current action2do if state is success
                    self.action2do["bt"] = {"state": "finished"}                                                              # Clear action
            else:
                time.sleep(.001)
                
    def onCancelLoop(self):
        print("Cancel loop started")
        while self.running:
            if self.isCanceled:
                print ("Action with id: " + self.action2do["bt"]["id"] +" canceled")
                self.runAction(self.action2do["bt"], cancel = True)                            # Cancel action if possible
                self.isCanceled = False                                                        # The signal to cancel this action was send, then change flag to False                                                         
                print ("Action with id: " + self.action2do["bt"]["id"] +" was canceled")
            else:
                time.sleep(0.05)                                                               # Idle


    def setRobotActions(self,robot_actions):
        """ Set a python dictionary with all the functions which the node can execute
            Parameters
            ----------

            robot_actions : dictionary
                Dictionary of functions
            
        """
        try:
            self.robot_actions = robot_actions                                                  # Set robot actions (functions)
        except Exception as e:
            nep.logError(e)
            print ("Error setting actions, exit...")
            self.onConnectError()                                                               # Send error message to RIZE
            time.sleep(.1)                                                                      # Wait to see the message 
            os.system('kill %d' % os.getpid())                                                  # Kill this process
            sys.exit(0)                                                                         # Close this process
            
    def setCancelActions(self,actions):
        """ Set a python dictionary with all the functions which the node can execute
            Parameters
            ----------

            robot_actions : dictionary
                Dictionary of functions
            
        """
        try:
            self.robot_cancel_actions = actions                                                 # Set robot actions (functions) that cancel the current actions
        except Exception as e:
            nep.logError(e)
            print ("Error setting cancel actions")
            self.onConnectError()                                                               # Send error message to RIZE
            time.sleep(.1)                                                                      # Wait to see the message 
            os.system('kill %d' % os.getpid())                                                  # Kill this process
            sys.exit(0)                                                                         # Close this process
    
    def wait(self, input_ = 0,  parameters = {}, parallel = False ):                            # Wait universal primitive
        """ Generic wait primitive
            Parameters
            ----------

            input : float
                Seconds to wait
            
        """
        try:
            value = float(input_)
            time.sleep(value)
        except Exception as e:
            nep.logError(e)
            return False
            pass
        return True


    def isValidRequest(self, action_request):
        try:
            if 'robots' in action_request:                                          # Chech if the request specify that this robot need to do the action
                if  (type(action_request['robots']) is list):                       # Is a list of robots
                    if self.robot_name in action_request['robots']:                 # Is this robot in the list
                        return  True
                    else:
                        if self.debug:
                            print("Ignored request for " + str(action_request['robots']) + ". Current robot name: *" + self.robot_name + "*")
                        return  False
                else:                                                               # Is this robot in the same that the string value "robots"
                    if self.robot_name == action_request['robots']: 
                        return  True
                    else:
                        if self.debug:
                            print("Ignored request for " + str(action_request['robots']) + ". Current robot name: *" + self.robot_name + "*")
                        return  False
        except Exception as e:
            nep.logError(e)
            print ("action_request is " + str(type(action_request)))
            return False

    def getPrimitivesList(self,primitives):
        lista = []
        for primitive in primitives:
            lista.append(primitive["primitive"])
        return lista




    def callback_action(self, action_request):

        try: 
            if self.debug:
                print("")
                print("--- New request--- ")
                lista = self.getPrimitivesList(action_request["primitives"])
                print ("ID: " + action_request["id"])
                print ("Primitives: " + str(lista))
                print ("Robots: " + str(action_request["robots"]))
            
            valid_request = self.isValidRequest(action_request)                                                 # Check if this action must be executed by this robot
            
            if self.debug:
                print ("valid: " + str(valid_request))

            if valid_request:
                if action_request["node"] == "cancel":                                                          # Cancel all actions is requested
                    self.isCanceled = True
                else: 
                        
                    listPrimitives = []
                    primitives = action_request["primitives"]
                    for p in primitives:
                        listPrimitives.append(p["primitive"]) 

                    
                    # If an action is in execution
                    if self.inActionExecution:                                                                  # Then cancel current action and update bt with idle
                        new_action = self.isNewAction(action_request["id"])
                        if new_action:
                            action_request["state"] = "idle" 
                            print ("new action - cancel")
                            self.isCanceled = True 
                            self.sharo.publish(action_request)
                    else:
                            self.setAction(action_request)
                    # Set new action to execute
        except:
            print("Error processing primitive")
            
                

    def isNewAction(self,id_):
        if id_ == self.currentActionID:
            return False
        else:
            return True
        
    def setAction(self,action_request):
        self.currentActionID = action_request["id"]
        self.action2do["bt"] = action_request
        self.action2do["active"] = True

    

    def runAction(self, message, cancel = False):
        """ Run an action
            
            Parameters
            ----------

            message : dictionary
                Use the Action description
            cancel : bool
                Use the Cancel action description

        """
            
        action = message["primitives"]                                                                                         # Get list of concatenated primitives
        n_primitives = len(action)                                                                                             # How many actions are?
        in_parallel = True                                                                                                     # Start variable                                                                                                     
                
        # Perform all the actions in parallel
        for i in range(n_primitives):                                                                                          # Run primitives in parallel until the last one
                    
            # Except the last one
            if (i == n_primitives-1):
                in_parallel = False
                
            primitive = action[i]                                                                                              # Get parameters 
            primitive_name = primitive["primitive"] #Name of the primitive
            input_ = primitive["input"]
            options = primitive["options"]

            if primitive_name in self.robot_actions:
                # Execute function
                if cancel:                                                                                                     # Cancel each action
                    try:
                        self.robot_cancel_actions[primitive_name]()
                    except Exception as e:
                        nep.logError(e)
                        pass
                else:                                                                                                          # Run each action
                    try:
                        self.robot_actions[primitive_name](input_, options, in_parallel)                                       # Execute robot action
                    except Exception as e:
                        nep.logError(e)
                        nep.printError(" primitive " + str(primitive_name) + " was not executed")
            else:
                nep.printError(" primitive " + str(primitive_name) + " is not registered")

