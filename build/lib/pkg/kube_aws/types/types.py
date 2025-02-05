# ExperimentDetails is for collecting all the experiment-related details
class ExperimentDetails(object):
	def __init__(self, ExperimentName=None, EngineName=None, ChaosDuration=None, ChaosInterval=None, RampTime=None, Force=None, ChaosLib=None, 
		ChaosServiceAccount=None, AppNS=None, AppLabel=None, ChaosInjectCmd=None, AppKind=None, EC2InstanceId=None, ChaosNamespace=None, ChaosPodName=None, Timeout=None, 
		Delay=None, TargetPods=None, PodsAffectedPerc=None, ChaosKillCmd=None, Sequence=None, LIBImagePullPolicy=None, TargetContainer=None, UID=None, ActiveNodes=None, ManagedNodegroup=None, InstanceRegion=None):
		self.ExperimentName      = ExperimentName 
		self.EngineName          = EngineName
		self.ChaosDuration       = ChaosDuration
		self.ChaosInterval       = ChaosInterval
		self.RampTime            = RampTime
		self.ChaosLib            = ChaosLib
		self.AppNS               = AppNS
		self.AppLabel            = AppLabel
		self.AppKind             = AppKind
		self.EC2InstanceId       = EC2InstanceId
		self.ChaosUID            = UID
		self.ChaosNamespace      = ChaosNamespace
		self.ChaosPodName        = ChaosPodName
		self.Timeout             = Timeout
		self.Delay               = Delay
		self.TargetPods          = TargetPods
		self.PodsAffectedPerc    = PodsAffectedPerc
		self.LIBImagePullPolicy  = LIBImagePullPolicy
		self.ChaosInjectCmd	     = ChaosInjectCmd
		self.ChaosKillCmd        = ChaosKillCmd
		self.TargetContainer	 = TargetContainer
		self.EC2InstanceId       = EC2InstanceId
		self.InstanceRegion      = InstanceRegion
		self.ManagedNodegroup    = ManagedNodegroup
		self.Sequence            = Sequence
		self.ActiveNodes         = ActiveNodes