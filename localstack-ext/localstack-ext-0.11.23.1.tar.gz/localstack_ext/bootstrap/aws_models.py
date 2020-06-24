from localstack.utils.aws import aws_models
pQKlx=super
pQKlX=None
pQKlH=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  pQKlx(LambdaLayer,self).__init__(arn)
  self.cwd=pQKlX
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class RDSDatabase(aws_models.Component):
 def __init__(self,pQKlH,env=pQKlX):
  pQKlx(RDSDatabase,self).__init__(pQKlH,env=env)
 def name(self):
  return self.pQKlH.split(':')[-1]
# Created by pyminifier (https://github.com/liftoff/pyminifier)
