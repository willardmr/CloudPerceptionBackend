from troposphere.constants import NUMBER
from troposphere import FindInMap, GetAtt, Join, Output
from troposphere import Parameter, Ref, Template
from troposphere.awslambda import Function, Code, MEMORY_VALUES
from troposphere.cloudformation import CustomResource
from troposphere.ec2 import Instance
from troposphere.ec2 import SecurityGroup
from troposphere.iam import Role, Policy

from generateResources import *

# Lets support names and arrows from the start
# UML later

'''
Code containers that want code pipelines and use languages:
These also have roles that need permissions to do what they gotta do to the resource
AWS::EC2
    Maybe autoscaling by default??
AWS::ECS
    Needs some management system kubernetes or something else idk
AWS::Lambda

Regular services:
AWS::AmazonMQ
AWS::ApiGateway
AWS::ApplicationAutoScaling
AWS::Athena
AWS::CloudFront
AWS::Cognito
AWS::DataPipeline
AWS::DynamoDB
    This should by default have autoscaling
AWS::EMR
AWS::ElastiCache
AWS::ElasticBeanstalk
AWS::Elasticsearch
AWS::Events
AWS::Glue
AWS::IoT
AWS::Kinesis
AWS::KinesisAnalytics
AWS::KinesisFirehose
AWS::Neptune
AWS::RDS
AWS::Redshift
AWS::Route53
AWS::S3
AWS::SES
AWS::SNS
AWS::SQS
AWS::SageMaker
AWS::StepFunctions

Databases should have backups

Need to include a unique id that can be used to refernce the image at the bottom of the template
'''

def convertMarkersToTemplate(markers):
    print(markers)
    t = Template()
    for marker in markers:
        if marker["id"] in normalResources:
            normalResources[marker["id"]](t)
    return t

normalResources = {
        1: generateDynamoDbTable
        }
codeContainerResources = {}

if __name__ == "__main__":
    markers = [{"x": 0.0, "y": 0.0, "id": 1}]
    print(convertMarkersToTemplate(markers).to_yaml())
