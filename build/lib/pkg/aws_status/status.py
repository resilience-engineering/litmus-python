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
            



    '''# stopEC2 instance
    def EC2Stop(self, experimentsDetails):
     
        self.clients = client.AWSClient().clientEC2   
        if experimentsDetails.EC2InstanceId == "" or experimentsDetails.InstanceRegion == "":
            return ValueError("Provided EC2InstanceId or InstanceRegion are empty")

        try:
            self.clients.stop_instances(experimentsDetails.EC2InstanceId)
            print(f'Stopping EC2 instance: {experimentsDetails.EC2InstanceId}')
            self.instance.wait_until_stopped()
            print(
                f'EC2 instance "{experimentsDetails.EC2InstanceId}" has been stopped')

        except ClientError as e:
            logging.error(e.args[0])
            print(e)

    def EC2Start(self, experimentsDetails):

        self.clients = client.AWSClient().clientEC2
        if experimentsDetails.EC2InstanceId == "" or experimentsDetails.InstanceRegion == "":
            return ValueError("Provided EC2InstanceId or InstanceRegion are empty")

        try:

            response = "Successfully started instances: " + \
                str(experimentsDetails.EC2InstanceId)
            self.clients.start_instances(experimentsDetails.EC2InstanceId)
            print(f'Starting EC2 instance: {experimentsDetails.EC2InstanceId}')
            self.clients.wait_until_stopped()
            print(
                f'EC2 instance "{experimentsDetails.EC2InstanceId}" has been started')

        except ClientError as e:
            logging.error(e.args[0])
            print(e)

    def WaitForEC2Down(self, experimentsDetails):

        self.clients = client.AWSClient().clientEC2
        if experimentsDetails.EC2InstanceId == "" or experimentsDetails.InstanceRegion == "":
            return ValueError("Provided EC2InstanceId or InstanceRegion are empty")
        try:

            reservations = self.clients.GetEC2InstanceStatus(
                experimentsDetails.EC2InstanceId, experimentsDetails.InstanceRegion)
            if reservations != "stopped":
                logging.info("[Info]: The instance state is not yet stopped")
            elif reservations != "terminated" :
                logging.info("[Info]: The instance state is not yet stopped")
        except ClientError as e:
            logging.error(e.args[0])
            print(e)
            
    def WaitForEC2Ups(self, experimentsDetails):

        self.clients = client.AWSClient().clientEC2
        if experimentsDetails.EC2InstanceId == "" or experimentsDetails.InstanceRegion == "":
            return ValueError("Provided EC2InstanceId or InstanceRegion are empty")
        try:

            reservations = self.clients.GetEC2InstanceStatus(
                experimentsDetails.EC2InstanceId, experimentsDetails.InstanceRegion)
            if reservations != "Running":
                logging.info("[Info]: The instance state is not yet started")
        except ClientError as e:
            logging.error(e.args[0])
            print(e)        '''