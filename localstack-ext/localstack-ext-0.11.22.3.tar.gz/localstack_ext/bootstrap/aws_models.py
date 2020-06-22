from localstack.utils.aws import aws_models
HBUVs=super
HBUVI=None
HBUVp=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  HBUVs(LambdaLayer,self).__init__(arn)
  self.cwd=HBUVI
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class RDSDatabase(aws_models.Component):
 def __init__(self,HBUVp,env=HBUVI):
  HBUVs(RDSDatabase,self).__init__(HBUVp,env=env)
 def name(self):
  return self.HBUVp.split(':')[-1]
# Created by pyminifier (https://github.com/liftoff/pyminifier)
