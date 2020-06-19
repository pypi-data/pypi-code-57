import pickle
import subprocess
import os
import threading
import time

from .base_socket import SocketBase

class AutoDeploySocket(SocketBase):
    def __init__(self, with_default):
        super().__init__(with_default)

        if with_default:
            self.register(AtmLocalDeployer())
        
    def deploy(self, pipe, model):
        current_dir = os.path.dirname(__file__)
        
        self.pipe_file = os.path.join(current_dir, 'atm_pipe.pkl')
        self.model_file = os.path.join(current_dir, 'atm_model.pkl')

        pickle.dump(pipe, open(self.pipe_file, 'wb'))
        pickle.dump(model, open(self.model_file, 'wb'))

        for _, instance in self.plugs:
            yield instance.deploy()


class AtmLocalDeployer(object):
    def __init__(self, port=5000):
        self.port = port

    def deploy(self):
        print ('Inside AtmLocalDeployer with port {0}'.format(self.port))

        py_file = os.path.join(os.path.dirname(__file__), 'local_server.py')

        def create_server():
            process = subprocess.Popen(["python", py_file, str(self.port)],
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()
            print ('stdout: ', stdout)
            print ('***********')
            print ('stderr: ', stderr)

        threading.Thread(target=create_server).start()

        time.sleep(3)
        return "http://localhost:{0}".format(self.port)

