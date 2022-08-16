import boto3
import logging
import pkg.utils.client.client as client
import pkg.utils.common.common as common

# AWS_AZ class is checking the status of LoadBalancer and availablity zone
class AWS_AZ(object):
    def __init__(self, client=None):
        self.clients = client

    # CheckAWSStatus will verify and give the ec2 instance details 
    def CheckAWSStatus(self, experimentsDetails):
        
        self.clients = client.AWSClient().clientEC2
        if experimentsDetails.EC2InstanceId == "" or experimentsDetails.InstanceRegion == "" :
            return ValueError("Provided EC2InstanceId or InstanceRegion are empty")

        try:
            reservations = self.clients.describe_instances(Filters=[
            {
                "Name": "instance-state-name",
                "Values": ["running"],
            }
            ])
        except Exception as exp:
            return ValueError(exp)
        logging.info("[Info]: EC2instanceID and InstanceRegion of region has been checked")
        '''for reservation in reservations:
            for instance in reservation["Instances"]:
                instance_id = instance["InstanceId"]
                instance_type = instance["InstanceType"]
                public_ip = instance["PublicIpAddress"]
                private_ip = instance["PrivateIpAddress"]
                print(f"{instance_id}, {instance_type}, {public_ip}, {private_ip}")'''



       