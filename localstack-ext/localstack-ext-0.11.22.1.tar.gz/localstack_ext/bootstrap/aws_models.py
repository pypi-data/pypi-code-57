from localstack.utils.aws import aws_models
liAze=super
liAzr=None
liAza=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  liAze(LambdaLayer,self).__init__(arn)
  self.cwd=liAzr
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class RDSDatabase(aws_models.Component):
 def __init__(self,liAza,env=liAzr):
  liAze(RDSDatabase,self).__init__(liAza,env=env)
 def name(self):
  return self.liAza.split(':')[-1]
# Created by pyminifier (https://github.com/liftoff/pyminifier)
