#####
# 
# This class is part of the Programming the Internet of Things project.
# 
# It is provided as a simple shell to guide the student and assist with
# implementation for the Programming the Internet of Things exercises,
# and designed to be modified by the student as needed.
#

from json import JSONEncoder

import json
import logging

from decimal import Decimal
from json import JSONEncoder

from programmingtheiot.data.ActuatorData import ActuatorData
from programmingtheiot.data.SensorData import SensorData
from programmingtheiot.data.SystemPerformanceData import SystemPerformanceData

class DataUtil():
	def __init__(self, encodeToUtf8 = False):
		self.encodeToUtf8 = encodeToUtf8
		
		logging.info("Created DataUtil instance.")
	
	def actuatorDataToJson(self, actuatorData):
		if not actuatorData:
			logging.debug("ActuatorData is null. Returning empty string.")
			return ""
		
		jsonData = json.dumps(actuatorData, indent = 4, cls = JsonDataEncoder)
		return jsonData
	  
	def sensorDataToJson(self, sensorData):
		if not sensorData:
			logging.debug("SensorData is null. Returning empty string.")
			return "" 
		jsonData = json.dumps(sensorData, indent = 4, cls = JsonDataEncoder)
		return jsonData

	def systemPerformanceDataToJson(self, sysPerfData):
		if not sysPerfData:
			logging.debug("SystemPerformanceData is null. Returning empty string.")
			return "" 
		jsonData = json.dumps(sysPerfData, indent = 4, cls = JsonDataEncoder)
		return jsonData
	
	def jsonToActuatorData(self, jsonData):
		if not jsonData:
			logging.warning("JSON data is empty or null.")
			return None
		jsonData = jsonData.replace("\'", "\"").replace('False', 'false').replace('True', 'true')
		ad = ActuatorData()
		jsonStruct = json.loads(jsonData)
		self._updateIotData(jsonStruct, ad)
		return ad
	
	def jsonToSensorData(self, jsonData):
		if not jsonData:
			logging.warning("JSON data is empty or null.")
			return None
		jsonData = jsonData.replace("\'", "\"").replace('False', 'false').replace('True', 'true')
		ad = SensorData()
		jsonStruct = json.loads(jsonData)
		self._updateIotData(jsonStruct, ad)
		return ad
	
	def jsonToSystemPerformanceData(self, jsonData):
		if not jsonData:
			logging.warning("JSON data is empty or null.")
			return None
		jsonData = jsonData.replace("\'", "\"").replace('False', 'false').replace('True', 'true')
		ad = SystemPerformanceData()
		jsonStruct = json.loads(jsonData)
		self._updateIotData(jsonStruct, ad)
		return ad	
	
	def _formatDataAndLoadDictionary(self, jsonData: str, useDecForFloat: bool = False) -> dict:
		jsonData = jsonData.replace("\'", "\"").replace('False', 'false').replace('True', 'true')
		
		jsonStruct = None
		
		if useDecForFloat:
			jsonStruct = json.loads(jsonData, parse_float = Decimal)
		else:
			jsonStruct = json.loads(jsonData)
		
		return jsonStruct
		
	def _generateJsonData(self, obj, useDecForFloat: bool = False) -> str:
		jsonData = None
		
		if self.encodeToUtf8:
			jsonData = json.dumps(obj, cls = JsonDataEncoder).encode('utf8')
		else:
			jsonData = json.dumps(obj, cls = JsonDataEncoder, indent = 4)
		
		if jsonData:
			jsonData = jsonData.replace("\'", "\"").replace('False', 'false').replace('True', 'true')
		
		return jsonData
	
	def _updateIotData(self, jsonStruct, obj):
		varStruct = vars(obj)
		
		for key in jsonStruct:
			if key in varStruct:
				setattr(obj, key, jsonStruct[key])
			else:
				logging.warn("JSON data contains key not mappable to object: %s", key)
		
class JsonDataEncoder(JSONEncoder):
	"""
	Convenience class to facilitate JSON encoding of an object that
	can be converted to a dict.
	
	"""
	def default(self, o):
		return o.__dict__