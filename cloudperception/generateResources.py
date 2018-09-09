from troposphere import *
from troposphere.dynamodb import *
from troposphere.applicationautoscaling import *
from troposphere.iam import *
import awacs.aws as awacs


def generateDynamoDbTable(template, name="test"):
    table = template.add_resource(Table(
	    name,
	    AttributeDefinitions=[
	        AttributeDefinition(
		    AttributeName="testHashKey",
		    AttributeType="S"
	        ),
	    ],
	    KeySchema=[
	        KeySchema(
		        AttributeName="testHashKey",
		        KeyType="HASH"
	        )
	    ],
	    ProvisionedThroughput=ProvisionedThroughput(
	        ReadCapacityUnits=1,
	        WriteCapacityUnits=1
	    )
    ))

    cfnrole = template.add_resource(Role(
        name + "ScalingRole",
        AssumeRolePolicyDocument=awacs.Policy(
            Statement=[
                awacs.Statement(
                    Effect=awacs.Allow,
                    Action=[awacs.Action("sts", "AssumeRole")],
                    Principal=awacs.Principal("Service", ["application-autoscaling.amazonaws.com"])
                )
            ]
        ),
        Policies=[
            Policy(
                PolicyName="giveaccesstoqueueonly",
                PolicyDocument=awacs.Policy(
                    Statement=[
                        awacs.Statement(
                            Effect=awacs.Allow,
                            Action=[
                                awacs.Action("dynamodb", "*"),
                                awacs.Action("couldwatch", "*")
                            ],
                            Resource=[GetAtt(name, "Arn")],
                        ),
                    ],
                )
            ),
         ]
    ))

    scalable_target = template.add_resource(ScalableTarget(
	    name + 'ScalableTarget',
	    MaxCapacity=5,
	    MinCapacity=1,
	    ResourceId=Join("/",["table", Ref(table)]),
	    RoleARN=GetAtt(name+"ScalingRole", "Arn"),
	    ScalableDimension='dynamodb:table:WriteCapacityUnits',
	    ServiceNamespace='dynamodb',
    ))

    scaling_policy = template.add_resource(ScalingPolicy(
	    name + 'ScalingPolicy',
        PolicyName=name,
	    PolicyType='TargetTrackingScaling',
	    ScalingTargetId=Ref(scalable_target),
        TargetTrackingScalingPolicyConfiguration=TargetTrackingScalingPolicyConfiguration(
            TargetValue=20.0,
            PredefinedMetricSpecification=PredefinedMetricSpecification(
                PredefinedMetricType="DynamoDBWriteCapacityUtilization"
            )
        )
    ))

