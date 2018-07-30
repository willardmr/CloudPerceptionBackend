from troposphere.constants import NUMBER
from troposphere import FindInMap, GetAtt, Join, Output
from troposphere import Parameter, Ref, Template
from troposphere.awslambda import Function, Code, MEMORY_VALUES
from troposphere.cloudformation import CustomResource
from troposphere.ec2 import Instance
from troposphere.ec2 import SecurityGroup
from troposphere.iam import Role, Policy

import boto3

import cloudperception.sendEMail as sendEmail

def handler(event, context):

    print(event)
    #print(createLambda())
    t = createLambda()
    with open("/tmp/template.yaml", "w+") as templateFile:
        templateFile.write(t.to_yaml())
    sendEmail.sendEmail("/tmp/template.yaml")
    return {}


def createLambda():
    t = Template()

    t.add_version("2010-09-09")

    code = [
	"var response = require('cfn-response');",
	"exports.handler = function(event, context) {",
	"   var responseData = {Value: event.ResourceProperties.List};",
	"   responseData.Value.push(event.ResourceProperties.AppendedItem);",
	"   response.send(event, context, response.SUCCESS, responseData);",
	"};",
    ]

    MemorySize = t.add_parameter(Parameter(
    'LambdaMemorySize',
    Type=NUMBER,
    Description='Amount of memory to allocate to the Lambda Function',
    Default='128',
    AllowedValues=MEMORY_VALUES))

    Timeout = t.add_parameter(Parameter(
        'LambdaTimeout',
        Type=NUMBER,
        Description='Timeout in seconds for the Lambda function',
        Default='60'))

    AppendItemToListFunction = t.add_resource(Function(
        "AppendItemToListFunction",
        Code=Code(
            ZipFile=Join("", code)
        ),
        Handler="index.handler",
        Role=GetAtt("LambdaExecutionRole", "Arn"),
        Runtime="nodejs",
        MemorySize=Ref(MemorySize),
        Timeout=Ref(Timeout)
    ))

    LambdaExecutionRole = t.add_resource(Role(
        "LambdaExecutionRole",
        Path="/",
        Policies=[Policy(
            PolicyName="root",
            PolicyDocument={
                "Version": "2012-10-17",
                "Statement": [{
                    "Action": ["logs:*"],
                    "Resource": "arn:aws:logs:*:*:*",
                    "Effect": "Allow"
                }]
            })],
        AssumeRolePolicyDocument={
            "Version": "2012-10-17",
            "Statement": [{
                "Action": ["sts:AssumeRole"],
                "Effect": "Allow",
                "Principal": {
                    "Service": ["lambda.amazonaws.com"]
                }
            }]
        },
    ))
    return t
