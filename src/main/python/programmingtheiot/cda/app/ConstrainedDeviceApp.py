#####
# 
# This class is part of the Programming the Internet of Things
# project, and is available via the MIT License, which can be
# found in the LICENSE file at the top level of this repository.
# 
# You may find it more helpful to your design to adjust the
# functionality, constants and interfaces (if there are any)
# provided within in order to meet the needs of your specific
# Programming the Internet of Things project.
# 

import logging

from time import sleep

import programmingtheiot.common.ConfigConst as ConfigConst

from programmingtheiot.common.ConfigUtil import ConfigUtil
from programmingtheiot.cda.app.DeviceDataManager import DeviceDataManager

from programmingtheiot.cda.system.SystemPerformanceManager import SystemPerformanceManager

logging.basicConfig(format = '%(asctime)s:%(name)s:%(levelname)s:%(message)s', level = logging.DEBUG)

class ConstrainedDeviceApp():
	def __init__(self):
		logging.info("Initializing CDA...")
		
		self.dataMgr = DeviceDataManager()

	def startApp(self):
		logging.info("Starting CDA...")
		
		self.dataMgr.startManager()
		
		logging.info("CDA started.")

	def stopApp(self, code: int):
		logging.info("CDA stopping...")
		
		self.dataMgr.stopManager()
		
		logging.info("CDA stopped with exit code %s.", str(code))
		
def main():
	cda = ConstrainedDeviceApp()
	cda.startApp()
	
	runForever = ConfigUtil().getBoolean(ConfigConst.CONSTRAINED_DEVICE, ConfigConst.RUN_FOREVER_KEY)
	
	if runForever:
		while (True):
			sleep(5)
			
	else:
		# TODO: Make the '65' value configurable
		sleep(65)
		cda.stopApp(0)

if __name__ == '__main__':
	main()
	