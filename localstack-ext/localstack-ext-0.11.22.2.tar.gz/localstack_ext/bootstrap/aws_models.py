from localstack.utils.aws import aws_models
YeUxl=super
YeUxM=None
YeUxC=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  YeUxl(LambdaLayer,self).__init__(arn)
  self.cwd=YeUxM
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class RDSDatabase(aws_models.Component):
 def __init__(self,YeUxC,env=YeUxM):
  YeUxl(RDSDatabase,self).__init__(YeUxC,env=env)
 def name(self):
  return self.YeUxC.split(':')[-1]
# Created by pyminifier (https://github.com/liftoff/pyminifier)
