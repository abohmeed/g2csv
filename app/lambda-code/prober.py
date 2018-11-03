import logging
import json
import boto3
import paramiko

logging.basicConfig()
logger = logging.getLogger()
logger.setLevel('INFO')

def get_instance_name(tags):
    for t in tags:
        if t['Key'] == 'name':
            return t['Value']


def get_instance_details(instance_id):
    client = boto3.client('ec2')
    response = client.describe_instances(InstanceIds=[instance_id])
    return {"endpoint":response['Reservations'][0]['Instances'][0]['PublicDnsName'],"name":get_instance_name(response['Reservations'][0]['Instances'][0]['Tags'])}

def get_inside_info(endpoint):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(endpoint,key_filename='key.pem',username='ubuntu')
    shell = client.invoke_shell()
    _, stdout, stderr = client.exec_command("ps aux | sort -nrk 3,3 | head -n 5")
    output = stdout.readlines()
    shell.close()
    client.close()
    return output

def handler(event, context):
    # logger.info(event)
    instance_id = None
    message = json.loads(event['Records'][0]['Sns']['Message'])
    for d in message['Trigger']['Dimensions']:
        if d['name'] == "InstanceId":
            instance_id = d['value']
    instance_info = get_instance_details(instance_id)
    output = get_inside_info(instance_info['endpoint'])
    alarm_message = message['NewStateReason']
    alarm_time = message['StateChangeTime']
    notification = "The instance {} produced the following alarm: {}.\n Date: {}.\n The top five running processes are:\n {}".format(instance_info['name'],alarm_message,alarm_time,'\n'.join(output))
    json_notification = json.dumps({"default":notification})
    client = boto3.client('sns')
    client.publish(
        TopicArn="arn:aws:sns:us-west-2:790250078024:website_admin",
        Message=json_notification,
        MessageStructure='json'
    )