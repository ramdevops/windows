import boto3
from datetime import datetime, timedelta
INSTANCE_ID = 'INSTANCEID'
REGION='us-west-2'
TODAY=datetime.utcnow().strftime("%Y%m%d")
NAME = 'NAA-windows-DEV-IMAGE-'
AMI_NAME = NAME + str(TODAY)
DESCRIPTION='Created as a Part of Daily Backup - ' + str(TODAY)
RETENTION_DAY_COUNT = '3'
DELETE_DATE = (datetime.today() - timedelta(int(RETENTION_DAY_COUNT))).strftime("%Y%m%d")
EC2=boto3.client('ec2',region_name=REGION)
IMAGE = EC2.create_image(InstanceId=INSTANCE_ID, NoReboot=True, DryRun=False, Name=AMI_NAME,Description=DESCRIPTION)
WAITER = EC2.get_waiter('image_available')
WAITER.wait(ImageIds=[IMAGE['ImageId']])
IMAGE_ATTRIBUTES=EC2.describe_images(Filters=[{'Name':'name','Values': [NAME + str(DELETE_DATE)]}])
if len(IMAGE_ATTRIBUTES['Images']) != 0:
        IMAGE_ID_TO_DELETE = IMAGE_ATTRIBUTES['Images'][0]['ImageId']
        DEREGISTER_IMAGE=EC2.deregister_image(ImageId=IMAGE_ID_TO_DELETE)
        for VOLUME in range(len(IMAGE_ATTRIBUTES['Images'][0]['BlockDeviceMappings'])):
                SNAPSHOT_ID=IMAGE_ATTRIBUTES['Images'][0]['BlockDeviceMappings'][VOLUME]['Ebs']['SnapshotId']
                DELETE_SNAPSHOT = EC2.delete_snapshot(SnapshotId=SNAPSHOT_ID)
else:
        print "No AMI To Delete"
