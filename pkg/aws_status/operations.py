import sys
import boto3
import logging
import pkg.utils.client.client as client
import pkg.utils.common.common as common
from botocore.exceptions import ClientError
import time
    # stopEC2 instance
def EC2Stop(experimentsDetails):
     
    ec2svc = client.AWSClient().clientEC2   
    if experimentsDetails.EC2InstanceId == "" or experimentsDetails.InstanceRegion == "":
        return ValueError("Provided EC2InstanceId or InstanceRegion are empty")

    try:
        #print([experimentsDetails.EC2InstanceId])
        ec2svc.stop_instances(InstanceIds=[experimentsDetails.EC2InstanceId])
        print(f'Stopping EC2 instance: {experimentsDetails.EC2InstanceId}')
        print(f'EC2 instance "{experimentsDetails.EC2InstanceId}" has been stopped')

    except ClientError as e:
        logging.error(e.args[0])
        print(e)

def EC2Start(experimentsDetails):

    ec2svc = client.AWSClient().clientEC2
    if experimentsDetails.EC2InstanceId == "" or experimentsDetails.InstanceRegion == "":
        return ValueError("Provided EC2InstanceId or InstanceRegion are empty")

    try:

        response = "Successfully started instances: " + \
        str(experimentsDetails.EC2InstanceId)
        ec2svc.start_instances(InstanceIds=[experimentsDetails.EC2InstanceId])
        print(f'Starting EC2 instance: {experimentsDetails.EC2InstanceId}')
        print(f'EC2 instance "{experimentsDetails.EC2InstanceId}" has been started')

    except ClientError as e:
        logging.error(e.args[0])
        print(e)

def WaitForEC2Down(experimentsDetails):

    ec2svc = client.AWSClient().clientEC2
    if experimentsDetails.EC2InstanceId == "" or experimentsDetails.InstanceRegion == "":
        return ValueError("Provided EC2InstanceId or InstanceRegion are empty")

    try:
        time.sleep(60) 
        instanceState = ec2svc.describe_instances(InstanceIds=
        [experimentsDetails.EC2InstanceId])
        for pythonins in instanceState['Reservations']:
                for printout in pythonins['Instances']:
                    #print(printout['InstanceId'])
                    #print(printout['InstanceType'])
                    #print(printout['State']['Name'])
                    if printout['State']['Name'] != "stopped":
                        logging.info("[Info]: The instance state is not yet stopped")
                        sys.exit("The instance state is not stopped")
    except ClientError as e:
        logging.error(e.args[0])
        print(e)
        
def WaitForEC2Up(experimentsDetails):
     
    ec2svc = client.AWSClient().clientEC2
    if experimentsDetails.EC2InstanceId == "" or experimentsDetails.InstanceRegion == "":
        return ValueError("Provided EC2InstanceId or InstanceRegion are empty")
    try:
        time.sleep(60)
        instanceState = ec2svc.describe_instances(InstanceIds=
        [experimentsDetails.EC2InstanceId])
        for pythonins in instanceState['Reservations']:
                for printout in pythonins['Instances']:
                    #print(printout['InstanceId'])
                    #print(printout['InstanceType'])
                    #print(printout['State']['Name'])
                    if printout['State']['Name'] != "running":
                        logging.info("[Info]: The instance state is not yet started")
                        sys.exit("The instance state is not running")
    except ClientError as e:
            logging.error(e.args[0])
            print(e)  


def CheckAWSStatus(experimentsDetails):

        ec2svc = client.AWSClient().clientEC2
        if experimentsDetails.EC2InstanceId == "" or experimentsDetails.InstanceRegion == "":
            return ValueError("Provided EC2InstanceId or InstanceRegion are empty")
        
        try:
            
            reservations = ec2svc.describe_instances(
                InstanceIds=[experimentsDetails.EC2InstanceId])
            #print(reservations)   
            for pythonins in reservations['Reservations']:
                for printout in pythonins['Instances']:
                    #print(printout['InstanceId'])
                    #print(printout['InstanceType'])
                    #print(printout['State']['Name'])
                    if  printout['State']['Name'] != "running":
                        logging.info("[Info]: The instance state is not running")
                        sys.exit("The instance state is not running")
                    else :
                        logging.info("[Info]: EC2instanceID and InstanceRegion of region has been checked")
        except ClientError as e:
                logging.error(e.args[0])
                print(e) 
