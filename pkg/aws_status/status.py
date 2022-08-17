from optparse import Values
import sys
import boto3
import logging
import pkg.utils.client.client as client
import pkg.utils.common.common as common
from botocore.exceptions import ClientError
import time
# import config

# AWS_AZ class is checking the status of Ec2 instances


class AWS_AZ():
    def __init__(self, client=None):
        self.clients = client

    # CheckAWSStatus will verify and give the ec2 instance details
    def CheckAWSStatus(self, experimentsDetails):

        self.clients = client.AWSClient().clientEC2
        if experimentsDetails.EC2InstanceId == "" or experimentsDetails.InstanceRegion == "":
            return ValueError("Provided EC2InstanceId or InstanceRegion are empty")
        
        try:
            
            reservations = self.clients.describe_instances(
                InstanceIds=[experimentsDetails.EC2InstanceId])
            #print(reservations)   
            for pythonins in reservations['Reservations']:
                for printout in pythonins['Instances']:
                    print(printout['InstanceId'])
                    #print(printout['InstanceType'])
                    print(printout['State']['Name'])
                    if  printout['State']['Name'] != "running":
                        logging.info("[Info]: The instance state is not running")
                        sys.exit("The instance state is not running")
                    else :
                        logging.info("[Info]: EC2instanceID and InstanceRegion of region has been checked")
        except ClientError as e:
                logging.error(e.args[0])
                print(e)
            