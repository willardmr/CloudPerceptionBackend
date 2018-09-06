from troposphere.constants import NUMBER
from troposphere import FindInMap, GetAtt, Join, Output
from troposphere import Parameter, Ref, Template
from troposphere.awslambda import Function, Code, MEMORY_VALUES
from troposphere.cloudformation import CustomResource
from troposphere.ec2 import Instance
from troposphere.ec2 import SecurityGroup
from troposphere.iam import Role, Policy


def convertMarkersToTemplate(markers):
    print(markers)
    t = Template()
    return t
