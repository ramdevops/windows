import boto3
import os
import winrm
import sys
REGION='us-west-2'
STACK_NAME='radar-vyshnavi-bandaru'
#PASSWORD=sys.argv[3]
os.system("echo [windows] > /root/Datadog-Windows/hosts")
CFT = boto3.client('cloudformation', region_name=REGION)
ASG = boto3.client('autoscaling', region_name=REGION)
EC2 = boto3.client('ec2', region_name=REGION)
CFT_RESOURCES = CFT.describe_stack_resources(StackName=STACK_NAME)
for RESOURCE in range(len(CFT_RESOURCES['StackResources'])):
    if CFT_RESOURCES['StackResources'][RESOURCE]['ResourceType'] == 'AWS::AutoScaling::AutoScalingGroup':
        ASG_ID = CFT_RESOURCES['StackResources'][RESOURCE]['PhysicalResourceId']
	ASG_RESOURCES = ASG.describe_auto_scaling_groups(AutoScalingGroupNames=[ASG_ID])
	for INSTANCES in range(len(ASG_RESOURCES['AutoScalingGroups'][0]['Instances'])):
	    INSTANCE_ID = ASG_RESOURCES['AutoScalingGroups'][0]['Instances'][INSTANCES]['InstanceId']
	    EC2_META = EC2.describe_instances(InstanceIds=[INSTANCE_ID])
	    INSTANCE_IP = str(EC2_META['Reservations'][0]['Instances'][0]['NetworkInterfaces'][0]['PrivateIpAddress'])
            LINE = int(INSTANCES) + 1
            print LINE
#            os.system("sed -i \'" + str(LINE) + " " + str(INSTANCE_IP) +"\' hosts")
            os.system("echo " + INSTANCE_IP + " >> /root/Datadog-Windows/hosts")
