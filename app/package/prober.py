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
    # print get_instance_details(instance_id)
    instance_info = get_instance_details(instance_id)
    output = get_inside_info(instance_info['endpoint'])
    print "The top five running processes on {} are:".format(instance_info['name'])
    print '\n'.join(output)


event = {u'Records': [{u'EventVersion': u'1.0', u'EventSubscriptionArn': u'arn:aws:sns:us-west-2:790250078024:website_admin:a632a18e-82df-4df7-92ce-0e9365784efc', u'EventSource': u'aws:sns', u'Sns': {u'SignatureVersion': u'1', u'Timestamp': u'2018-11-02T14:49:02.640Z', u'Signature': u'KiMXBBURo+GpN6tGfycrCuGee5UF4jFHNds6chmpD24xOCPHBATCM5UsB95BArhSDv/MpKb1vxg7Axrbfb1bxh8j4JJze+EyiFxPF+cDXezBKJX6ykE6w8emtIS9GXvmfNDV8BCqos6eTqJW2eMPRXKECnDTtsVCGSbIOqMP/w7948TKc212J+UISOx9jwhKcNTVPuYXo9ShXXvfNUZ8pHkXdQGBfi0rRicxOMGdUIgb3/Na7DHaiDDXCPMx29Zw1np/sNVvRfDif+ywQr4+5YycD1s4H35SvjhIC/Ic0uuXWJvVcf5TNiJ5yGLTY0oYimW31jRawauLo/17PBycJw==', u'SigningCertUrl': u'https://sns.us-west-2.amazonaws.com/SimpleNotificationService-ac565b8b1a6c5d002d285f9598aa1d9b.pem', u'MessageId': u'9e1809d8-2e94-5cc2-b0b6-5d8e488a734e',
                                                                                                                                                                                                        u'Message': u'{"AlarmName":"CPU utlliization of the instance","AlarmDescription":null,"AWSAccountId":"790250078024","NewStateValue":"ALARM","NewStateReason":"Threshold Crossed: 1 out of the last 1 datapoints [99.7027322404378 (02/11/18 14:39:00)] was greater than or equal to the threshold (80.0) (minimum 1 datapoint for OK -> ALARM transition).","StateChangeTime":"2018-11-02T14:49:02.612+0000","Region":"US West (Oregon)","OldStateValue":"OK","Trigger":{"MetricName":"CPUUtilization","Namespace":"AWS/EC2","StatisticType":"Statistic","Statistic":"AVERAGE","Unit":null,"Dimensions":[{"value":"i-00f773169699b23e3","name":"InstanceId"}],"Period":300,"EvaluationPeriods":1,"ComparisonOperator":"GreaterThanOrEqualToThreshold","Threshold":80.0,"TreatMissingData":"","EvaluateLowSampleCountPercentile":""}}', u'MessageAttributes': {}, u'Type': u'Notification', u'UnsubscribeUrl': u'https://sns.us-west-2.amazonaws.com/?Action=Unsubscribe&SubscriptionArn=arn:aws:sns:us-west-2:790250078024:website_admin:a632a18e-82df-4df7-92ce-0e9365784efc', u'TopicArn': u'arn:aws:sns:us-west-2:790250078024:website_admin', u'Subject': u'ALARM: "CPU utlliization of the instance" in US West (Oregon)'}}]}
handler(event,'')