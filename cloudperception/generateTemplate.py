import json

import boto3

import cloudperception.sendEMail as sendEmail
from cloudperception.markerConverter import convertMarkersToTemplate


def handler(event, context):
    print(event)
    bodyJson = json.loads(event['body'])
    template = convertMarkersToTemplate(bodyJson)
    with open("/tmp/template.yaml", "w+") as templateFile:
        templateFile.write(template.to_yaml())
    sendEmail.sendEmail("/tmp/template.yaml")
    return {}
