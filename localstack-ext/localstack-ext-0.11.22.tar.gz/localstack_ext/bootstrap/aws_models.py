from localstack.utils.aws import aws_models
RbcFe=super
RbcFj=None
RbcFz=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  RbcFe(LambdaLayer,self).__init__(arn)
  self.cwd=RbcFj
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class RDSDatabase(aws_models.Component):
 def __init__(self,RbcFz,env=RbcFj):
  RbcFe(RDSDatabase,self).__init__(RbcFz,env=env)
 def name(self):
  return self.RbcFz.split(':')[-1]
# Created by pyminifier (https://github.com/liftoff/pyminifier)
