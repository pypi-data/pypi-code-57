from localstack.utils.aws import aws_models
jlrfd=super
jlrfS=None
jlrfK=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  jlrfd(LambdaLayer,self).__init__(arn)
  self.cwd=jlrfS
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class RDSDatabase(aws_models.Component):
 def __init__(self,jlrfK,env=jlrfS):
  jlrfd(RDSDatabase,self).__init__(jlrfK,env=env)
 def name(self):
  return self.jlrfK.split(':')[-1]
# Created by pyminifier (https://github.com/liftoff/pyminifier)
