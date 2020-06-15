# pip3 install awscli --upgrade --user
# aws configure

import boto3

ec2 = boto3.resource ('ec2')
ec2cli = boto3.client ('ec2')
elb = boto3.client('elb')
cw = boto3.client('cloudwatch')
elb2 = boto3.client('elbv2')
autoscaling = boto3.client('autoscaling')
rt53 = boto3.client('route53')