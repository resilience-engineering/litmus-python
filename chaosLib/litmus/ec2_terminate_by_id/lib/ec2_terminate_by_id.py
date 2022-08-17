
from distutils.log import error
import string
from time import time
import pkg.types.types  as types
import pkg.events.events as events
import logging, threading, signal, sys
import pkg.utils.common.common as common
import pkg.utils.common.pods as pods
import pkg.utils.exec.exec as litmusexec
import pkg.aws_status.status as awslib
import pkg.aws_status.operations as awslib1
import logging
from datetime import datetime
import pkg.maths.maths as maths
import os


# signal object
class Signals(object):
	def __init__(self, timeSignal=None, sigSignal=None):
		self.timeSignal = timeSignal
		self.sigSignal = sigSignal

#PrepareEC2TerminateByID contains the prepration and injection steps for the experiment
def PrepareChaos(experimentsDetails, clients , resultDetails , eventsDetails , chaosDetails):
	if experimentsDetails.RampTime != 0:
		logging.error(" Waiting for the %s ramp time before injecting chaos", experimentsDetails.RampTime)
		common.WaitForDuration(experimentsDetails.RampTime)
	
	#get the instance id or list of instance ids
	EC2InstanceIdList = experimentsDetails.EC2InstanceId
	print(EC2InstanceIdList)
	print(experimentsDetails)
	if len(EC2InstanceIdList) == 0:
		return error.Errorf("no instance id found to terminate")
	

 	# mode for chaos injection
	if experimentsDetails.Sequence.lower() == "serial":
		err = injectChaosInSerialMode(experimentsDetails , EC2InstanceIdList, chaosDetails , eventsDetails , resultDetails, clients, awslib, awslib1)
		if err != None:
			return err
	elif experimentsDetails.Sequence.lower() == "parallel":
		err = injectChaosInParallelMode(experimentsDetails , EC2InstanceIdList, chaosDetails , eventsDetails , resultDetails, clients, awslib, awslib1)
		if err != None:
			return err
	else:
		return ValueError(": sequence is not supported".format(experimentsDetails.Sequence))

	# Waiting for the ramp time after chaos injection
	if experimentsDetails.RampTime != 0 :
		logging.error(" Waiting for the %s ramp time after injecting chaos",experimentsDetails.RampTime)
		common.WaitForDuration(experimentsDetails.RampTime)

	return None

#injectChaosInSerialMode will inject the ec2 instance termination in serial mode that is one after other
def injectChaosInSerialMode(experimentsDetails , EC2InstanceIdList, chaosDetails , eventsDetails , resultDetails, clients, awslib, awslib1): 
	
	#ChaosStartTimeStamp contains the start timestamp, when the chaos injection begin
	ChaosStartTimeStamp = datetime.now()
	duration = (datetime.now() - ChaosStartTimeStamp).seconds
	
	while duration < experimentsDetails.ChaosDuration:
     
		
		
		logging.error("Target EC2InstanceId list, %s", EC2InstanceIdList)

		if experimentsDetails.EngineName != "" :
			msg = "Injecting " + experimentsDetails.ExperimentName + " chaos on available zone"
			types.SetEngineEventAttributes(eventsDetails, types.ChaosInject, msg, "Normal", chaosDetails)
			events.GenerateEvents(eventsDetails, chaosDetails, "ChaosEngine", clients)
		
		#PowerOff the instance
		for i in range(EC2InstanceIdList):

			logging.error(" Stopping the desired EC2 instance")
			err = awslib1.EC2Stop(experimentsDetails)
			if err != None:
				return err
			
			if chaosDetails.Randomness:
				err = common.RandomInterval(experimentsDetails.ChaosInterval)
				if err != None:
					return err
			else:
				#Waiting for the chaos interval after chaos injection
				if experimentsDetails.ChaosInterval != "":
					logging.info("[Wait]: Wait for the chaos interval %s",(experimentsDetails.ChaosInterval))
					waitTime = maths.atoi(experimentsDetails.ChaosInterval)
					common.WaitForDuration(waitTime)

			#Starting the EC2 instance
			if experimentsDetails.ManagedNodegroup != "enable" :
				logging.info("[Status]: Starting back the EC2 instance")
				err = awslib1.EC2Start(id, experimentsDetails.InstanceRegion)
				if err != None:
					return err
				
				##Wait for ec2 instance to get in running state
				logging.info("[Status]: Checking AWS EC2 instance status")		
				err = awslib1.WaitForEC2Up(experimentsDetails.Timeout, experimentsDetails.Delay, experimentsDetails.ManagedNodegroup, experimentsDetails.InstanceRegion)
				if err != None:
					return err
				
		duration = (datetime.now() - ChaosStartTimeStamp).seconds

	logging.info("[Completion]: %s chaos is done",(experimentsDetails.ExperimentName))

	return None

# injectChaosInParallelMode will inject the ec2 instance termination in parallel mode that is all at once
def injectChaosInParallelMode(experimentsDetails , EC2InstanceIdList, chaosDetails , eventsDetails , resultDetails, clients, awslib, awslib1):
	

	#ChaosStartTimeStamp contains the start timestamp, when the chaos injection begin
	ChaosStartTimeStamp = datetime.now()
	duration = (datetime.now() - ChaosStartTimeStamp).seconds
	
	while duration < experimentsDetails.ChaosDuration:
		
  		
		if experimentsDetails.EngineName != "" :
			msg = "Injecting " + experimentsDetails.ExperimentName + experimentsDetails.InstanceRegion
			types.SetEngineEventAttributes(eventsDetails, types.ChaosInject, msg, "Normal", chaosDetails)
			events.GenerateEvents(eventsDetails, chaosDetails, "ChaosEngine",clients)
		
		# PowerOff the instance
	    #Stopping the EC2 instance
		logging.error(" Stopping the desired EC2 instance ")
		err = awslib1.EC2Stop(experimentsDetails)
		if err != None:
			return err	
		

		#Stopping the EC2 instance
		logging.error(" Wait for EC2 instance  to get in stopped state")
		err = awslib1.WaitForEC2Down(experimentsDetails)
		if err != None:
			return err	
		
		
		'''if chaosDetails.Randomness:
			err = common.RandomInterval(experimentsDetails.ChaosInterval)
			if err != None:
				return err
		else:'''
			#Waiting for the chaos interval after chaos injection
		if experimentsDetails.ChaosInterval != "" :
			logging.info("[Wait]: Wait for the chaos interval")
			waitTime = maths.atoi(experimentsDetails.ChaosInterval)
			common.WaitForDuration(waitTime)

		#Starting the EC2 instance
		if experimentsDetails.ManagedNodegroup != "enable":
			
			logging.info("[Status]:Starting back the EC2 instance")
			err = awslib1.EC2Start(experimentsDetails)
			if err != None:
				return err

			logging.info("[Status]:Wait for EC2 instance '%d' to get in running state")
			err = awslib1.WaitForEC2Up(experimentsDetails)
			if err != None:
					return err
		
			
		duration = (datetime.now() - ChaosStartTimeStamp).seconds


		#Verify the status of available zone after the chaos injection
		logging.info("[Status]: Checking AWS EC2 instance status")		
		err = awslib1.CheckAWSStatus(experimentsDetails)
		if err != None:
			return err

		duration = (datetime.now() - ChaosStartTimeStamp).seconds

	logging.info("[Completion]: %s chaos is done",(experimentsDetails.ExperimentName))

	return None








	