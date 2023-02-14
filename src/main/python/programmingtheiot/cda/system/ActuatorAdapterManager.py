#####
# 
# This class is part of the Programming the Internet of Things project.
# 
# It is provided as a simple shell to guide the student and assist with
# implementation for the Programming the Internet of Things exercises,
# and designed to be modified by the student as needed.
#

import logging

from importlib import import_module

import programmingtheiot.common.ConfigConst as ConfigConst
from programmingtheiot.common.ConfigUtil import ConfigUtil
from programmingtheiot.common.IDataMessageListener import IDataMessageListener

from programmingtheiot.data.ActuatorData import ActuatorData

from programmingtheiot.cda.sim.HvacActuatorSimTask import HvacActuatorSimTask
from programmingtheiot.cda.sim.HumidifierActuatorSimTask import HumidifierActuatorSimTask

class ActuatorAdapterManager(object):
	"""
	Shell representation of class for student implementation.
	
	"""
	def _initEnvironmentalActuationTasks(self):
		if not self.useEmulator:
			# load the environmental tasks for simulated actuation
			self.humidifierActuator = HumidifierActuatorSimTask()
			
			# create the HVAC actuator
			self.hvacActuator = HvacActuatorSimTask()
		else:
			hueModule = import_module('programmingtheiot.cda.emulated.HumidifierEmulatorTask', 'HumidiferEmulatorTask')
			hueClazz = getattr(hueModule, 'HumidifierEmulatorTask')
			self.humidifierActuator = hueClazz()
			
			# create the HVAC actuator emulator
			hveModule = import_module('programmingtheiot.cda.emulated.HvacEmulatorTask', 'HvacEmulatorTask')
			hveClazz = getattr(hveModule, 'HvacEmulatorTask')
			self.hvacActuator = hveClazz()
			
			# create the LED display actuator emulator
			leDisplayModule = import_module('programmingtheiot.cda.emulated.LedDisplayEmulatorTask', 'LedDisplayEmulatorTask')
			leClazz = getattr(leDisplayModule, 'LedDisplayEmulatorTask')
			self.ledDisplayActuator = leClazz()
	
	def __init__(self):
		pass

	def sendActuatorCommand(self, data: ActuatorData) -> bool:
		pass
	
	def setDataMessageListener(self, listener: IDataMessageListener) -> bool:
		pass
