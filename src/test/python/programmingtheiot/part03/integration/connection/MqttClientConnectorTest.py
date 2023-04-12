#####
# 
# This class is part of the Programming the Internet of Things
# project, and is available via the MIT License, which can be
# found in the LICENSE file at the top level of this repository.
# 
# Copyright (c) 2020 by Andrew D. King
# 

import logging
import unittest

from time import sleep, time

import programmingtheiot.common.ConfigConst as ConfigConst

from programmingtheiot.cda.connection.MqttClientConnector import MqttClientConnector
from programmingtheiot.common.ConfigUtil import ConfigUtil
from programmingtheiot.common.ResourceNameEnum import ResourceNameEnum
from programmingtheiot.common.DefaultDataMessageListener import DefaultDataMessageListener
from programmingtheiot.data.ActuatorData import ActuatorData
from programmingtheiot.data.SensorData import SensorData
from programmingtheiot.data.DataUtil import DataUtil

class MqttClientConnectorTest(unittest.TestCase):
	"""
	This test case class contains very basic unit tests for
	MqttClientConnector. It should not be considered complete,
	but serve as a starting point for the student implementing
	additional functionality within their Programming the IoT
	environment.
	"""
	NS_IN_MILLIS = 1000000

	# NOTE: We'll use only 10,000 requests for MQTT
	MAX_TEST_RUNS = 10000
	
	@classmethod
	def setUpClass(self):
		logging.basicConfig(format = '%(asctime)s:%(module)s:%(levelname)s:%(message)s', level = logging.DEBUG)
		logging.info("Testing MqttClientConnector class...")
		
		self.cfg = ConfigUtil()
		self.mcc = MqttClientConnector()
		
	def setUp(self):
		self.mqttClient = MqttClientConnector(clientID = 'CDAMqttClientPerformanceTest001')
		pass

	def tearDown(self):
		pass

	@unittest.skip("Ignore for now.")
	def testConnectAndDisconnect(self):
		startTime = time.time_ns()
		
		self.assertTrue(self.mqttClient.connectClient())
		self.assertTrue(self.mqttClient.disconnectClient())
		
		endTime = time.time_ns()
		elapsedMillis = (endTime - startTime) / self.NS_IN_MILLIS
		
		logging.info("Connect and Disconnect: " + str(elapsedMillis) + " ms")
		
	#@unittest.skip("Ignore for now.")
	def testPublishQoS0(self):
		self._execTestPublish(self.MAX_TEST_RUNS, 0)

	#@unittest.skip("Ignore for now.")
	def testPublishQoS1(self):
		self._execTestPublish(self.MAX_TEST_RUNS, 1)

	#@unittest.skip("Ignore for now.")
	def testPublishQoS2(self):
		self._execTestPublish(self.MAX_TEST_RUNS, 2)

	def _execTestPublish(self, maxTestRuns: int, qos: int):
		self.assertTrue(self.mqttClient.connectClient())
		
		sensorData = SensorData()
		payload = DataUtil().sensorDataToJson(sensorData)
		
		startTime = time.time_ns()
		
		for seqNo in range(0, maxTestRuns):
			self.mqttClient.publishMessage(resource = ResourceNameEnum.CDA_SENSOR_MSG_RESOURCE, msg = payload, qos = qos)
			
		endTime = time.time_ns()
		elapsedMillis = (endTime - startTime) / self.NS_IN_MILLIS
		
		self.assertTrue(self.mqttClient.disconnectClient())
		
		logging.info("Publish message - QoS " + str(qos) + " [" + str(maxTestRuns) + "]: " + str(elapsedMillis) + " ms")

	@unittest.skip("Ignore for now.")
	def testConnectAndCDAManagementStatusPubSub(self):
		qos = 1
		delay = self.cfg.getInteger(ConfigConst.MQTT_GATEWAY_SERVICE, ConfigConst.KEEP_ALIVE_KEY, ConfigConst.DEFAULT_KEEP_ALIVE)
		
		self.mcc.connectClient()
		self.mcc.subscribeToTopic(resource = ResourceNameEnum.CDA_MGMT_STATUS_MSG_RESOURCE, qos = qos)
		sleep(5)
		
		self.mcc.publishMessage(resource = ResourceNameEnum.CDA_MGMT_STATUS_MSG_RESOURCE, msg = "TEST: This is the CDA message payload.", qos = qos)
		sleep(5)
		
		self.mcc.unsubscribeFromTopic(resource = ResourceNameEnum.CDA_MGMT_STATUS_MSG_RESOURCE)
		sleep(5)
		
  # sleep(delay)
		
		self.mcc.disconnectClient()

	unittest.skip("Ignore for now.")
	def testNewActuatorCmdPubSub(self):
		qos = 1
	
		# NOTE: delay can be anything you'd like - the sleep() calls are simply to slow things down a bit for observation
		delay = self.cfg.getInteger(ConfigConst.MQTT_GATEWAY_SERVICE, ConfigConst.KEEP_ALIVE_KEY, ConfigConst.DEFAULT_KEEP_ALIVE)
		
		actuatorData = ActuatorData()
		payload = DataUtil().actuatorDataToJson(actuatorData)
		
		self.mcc.setDataMessageListener(DefaultDataMessageListener())
		self.mcc.connectClient()
		
		sleep(5)
		
		self.mcc.publishMessage(resource = ResourceNameEnum.CDA_ACTUATOR_CMD_RESOURCE, msg = payload, qos = qos)
		
		sleep(delay)
		
		self.mcc.disconnectClient()
		
	@unittest.skip("Ignore for now.")
	def testActuatorCmdPubSub(self):
		qos = 1

		# NOTE: delay can be anything you'd like - the sleep() calls are simply to slow things down a bit for observation
		delay = self.cfg.getInteger(ConfigConst.MQTT_GATEWAY_SERVICE, ConfigConst.KEEP_ALIVE_KEY,
									ConfigConst.DEFAULT_KEEP_ALIVE)

		actuatorData = ActuatorData()
		payload = DataUtil().actuatorDataToJson(actuatorData)

		# NOTE: the `DefaultDataMessageListener()` is just a placeholder for
		# handling callbacks from the MQTT client - it is optional
		self.mcc.setDataMessageListener(DefaultDataMessageListener())
		self.mcc.connectClient()

		sleep(5)

		self.mcc.publishMessage(resource=ResourceNameEnum.CDA_ACTUATOR_CMD_RESOURCE, msg=payload, qos=qos)

		sleep(delay)

		self.mcc.disconnectClient()

	@unittest.skip("Ignore for now.")
	def testSensorMsgPub(self):
		qos = 0
		delay = self.cfg.getInteger(ConfigConst.MQTT_GATEWAY_SERVICE, ConfigConst.KEEP_ALIVE_KEY, ConfigConst.DEFAULT_KEEP_ALIVE)
		
		sensorData = SensorData()
		sensorData.setValue(22.0)
		
		self.mcc.setDataMessageListener(DefaultDataMessageListener())
		
		payload = DataUtil().sensorDataToJson(sensorData)
		
		self.mcc.connectClient()
		
		sleep(5)
				
		self.mcc.publishMessage(resource = ResourceNameEnum.CDA_SENSOR_MSG_RESOURCE, msg = payload, qos = qos)
		
		sleep(delay + 5)
		
		self.mcc.disconnectClient()

	@unittest.skip("Ignore for now.")
	def testCDAManagementStatusSubscribe(self):
		qos = 1
		delay = self.cfg.getInteger(ConfigConst.MQTT_GATEWAY_SERVICE, ConfigConst.KEEP_ALIVE_KEY, ConfigConst.DEFAULT_KEEP_ALIVE)
		
		self.mcc.connectClient()
		self.mcc.subscribeToTopic(resource = ResourceNameEnum.CDA_MGMT_STATUS_CMD_RESOURCE, qos = qos)
		
		sleep(delay)
		
		self.mcc.disconnectClient()

	@unittest.skip("Ignore for now.")
	def testCDAActuatorCmdSubscribe(self):
		qos = 1
		delay = self.cfg.getInteger(ConfigConst.MQTT_GATEWAY_SERVICE, ConfigConst.KEEP_ALIVE_KEY, ConfigConst.DEFAULT_KEEP_ALIVE)
		
		self.mcc.connectClient()
		self.mcc.subscribeToTopic(resource = ResourceNameEnum.CDA_ACTUATOR_CMD_RESOURCE, qos = qos)
		
		sleep(300)
		
		self.mcc.disconnectClient()

	@unittest.skip("Ignore for now.")
	def testCDAManagementStatusPublish(self):
		"""
		Uncomment this test when integration between the GDA and CDA using MQTT.
		
		"""
		qos = 1
		delay = self.cfg.getInteger(ConfigConst.MQTT_GATEWAY_SERVICE, ConfigConst.KEEP_ALIVE_KEY, ConfigConst.DEFAULT_KEEP_ALIVE)
		
		self.mcc.connectClient()
		self.mcc.publishMessage(resource = ResourceNameEnum.CDA_MGMT_STATUS_MSG_RESOURCE, msg = "TEST: This is the CDA message payload.", qos = qos)
		
		sleep(delay)
		
		self.mcc.disconnectClient()

if __name__ == "__main__":
	unittest.main()

	