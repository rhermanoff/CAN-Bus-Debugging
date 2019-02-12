#!/usr/bin/python

import can
import click
from can import Message
from device import device
from util import *
from apscheduler.schedulers.background import BackgroundScheduler

"""
This function handles any messages from the motor controller
@param message
@return dictionary
"""
class motorController(device):
	"""
	Initializes all motor controller attributes
	"""
	def __init__(self, can_arbitration_tx, can_arbitration_rx):
		# Daemonic scheduler for motor controller
		self.scheduler = BackgroundScheduler(daemon=True)
	
		# Configured CAN arbitration IDs for TX/RX
		self.can_arbitration_rx = can_arbitration_rx;
		self.can_arbitration_tx = can_arbitration_tx;
		
		# Motor Controller constants
		self.max_speed_def = 32767 # 100%
	
	"""
	"Private" helper functions
	"""
	
	"""
	
	"""
	def _tx(self, driver, parsedBytes):
		message = Message(
			extended_id = False,
			is_remote_frame = False,
			is_error_frame = False,
			arbitration_id = self.can_arbitration_tx
			dlc = len(parsedBytes),
			data = parsedBytes,
		)
		
		driver.send_message(message)
		
	def _request_parameter_interval(self, driver, regId, interval):
		if(interval < 0 || interval > 255)
			raise Exception("Interval must be between 0 and 255")
			
		self.tx(driver, [0x3D, regId, hex(interval)])
		
	def _request_parameter_once(self, driver, regId):
		self._request_parameter_interval(driver, regId, 0)
		
	def _request_parameter_stop(self, driver, regId):
		self._request_parameter_interval(driver, regId, 255)
		
	"""
	"Public" member functions
	"""
		
	def request_btb(self, driver):
		self._request_parameter_once(driver, 0xE2)
		
	def request_speed(self, driver):
		self._request_parameter_once(driver, 0x30)
		
	def disable(self, driver):
		self._tx(driver, [0x51, 0x04, 0x00])
		
	def transmission_request_enable(self, driver):
		self._tx(driver, [0x3D, 0xE8, 0X00])
		
	def enable(self, driver):
		self._tx(driver, [0x51, 0x00, 0x00])
		
	def set_acc_ramp(self, driver, timing):
		self.tx(driver, [0x35] + int_to_little_endian_hex(timing))
		
	def set_dec_ramp(self, driver, timing):
		self.tx(driver, [0xED] + int_to_little_endian_hex(timing))
		
	def set_speed(self, driver, percentage):
		# Convert speed percentage to speed integer
		ratio = 100.0/self.max_speed_def
		speed_int = int(percentage/ratio)
		self.tx(driver, [0x31] + int_to_little_endian_hex(speed_int))
		
		
		
	
		
	
	"""
	Handles message for motor controller
	@param message  CAN message to parse
	@return hypercan_message
	"""
	def handle_message(self, message):
		# Check for valid length message
		if(message.dlc != 3 && message.dlc != 5)
			raise Exception("Expected a DLC of 3 or 5 for Bamocar messages")
			
		# Fetch and decode regId
		regId = message.data[0]
		
		# Parse rest of data in little endian
		data = hex_to_little_endian_int(message.data[1::])
		
		"""
		TODO
		There are quite a large amount of registers that could possibly
		be updated.  I don't want to add these ALL as member variables,
		as the list would be 254 registers long.  I am waiting to finish
		implementing this until I figure out a better way to structure
		this code.  For now it will just print debug messages.
		"""
		click.echo(click.style('RX Motor Controller Message', bg='red', fg='white'))
		print(regId)
		print(hex(regId))
		print(data)
		print(message.data)
		
		# Update object
		# self.update_device(hypercan_message)
		
		# return hypercan_message
		return {}

	