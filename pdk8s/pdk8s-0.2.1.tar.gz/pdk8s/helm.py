import subprocess

import yaml

class Helm:
    def __init__(self, namespace=None):
        self.bin = "helm"
        self.namespace = namespace
    
    def get(self, resource_type, *args):
        pass

    def exec(self, *args):
        cmd = [self.bin] + list(args) + ["-o", "yaml"]
        if self.namespace:
            cmd += ['-n', self.namespace]
        
        data = subprocess.check_output(cmd)
        return yaml.safe_load(data)

    def install(self):
        pass

    def upgrade(self):
        pass
1461

helm = Helm()

upgrade = helm.upgrade
install = helm.install