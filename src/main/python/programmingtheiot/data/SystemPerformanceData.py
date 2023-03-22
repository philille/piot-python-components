#####
# 
# This class is part of the Programming the Internet of Things project.
# 
# It is provided as a simple shell to guide the student and assist with
# implementation for the Programming the Internet of Things exercises,
# and designed to be modified by the student as needed.
#

import programmingtheiot.common.ConfigConst as ConfigConst

from programmingtheiot.data.BaseIotData import BaseIotData

class SystemPerformanceData(BaseIotData):
	"""
	Shell representation of class for student implementation.
	
	"""
	DEFAULT_VAL = 0.0
	
	def __init__(self, d = None):
		super(SystemPerformanceData, self).__init__(name = ConfigConst.SYSTEM_PERF_MSG, typeID = ConfigConst.SYSTEM_PERF_TYPE, d = d)
		self.cpuUtil = ConfigConst.DEFAULT_VAL
		self.memUtil = ConfigConst.DEFAULT_VAL
	
	def getCpuUtilization(self):
		"""
		Get the CpuUtilization of the instance
		
		"""
		return self.cpuUtil
	
	def getDiskUtilization(self):
		"""
		Get the DiskUtilization of the instance 
		
		"""
		return self.diskUtil 
	def getMemoryUtilization(self):
		"""
		Get the MemoryUtilization of the instance

		"""
		return self.memUtil
	
	def setCpuUtilization(self, cpuUtil):
		"""
		Set the CpuUtilization of the instance
		"""
		self.cpuUtil = cpuUtil
	
	def setDiskUtilization(self, diskUtil):
		"""
		Set the DiskUtilization of the instance
		"""
		self.diskUtil = diskUtil
	
	def setMemoryUtilization(self, memUtil):
		"""
		Set the MemoryUtilization of the instance
		"""
		self.memUtil = memUtil
	
	def _handleUpdateData(self, data):
		if data and isinstance(data, SystemPerformanceData):
			self.cpuUtil = data.getCpuUtilization()
			self.memUtil = data.getMemoryUtilization()