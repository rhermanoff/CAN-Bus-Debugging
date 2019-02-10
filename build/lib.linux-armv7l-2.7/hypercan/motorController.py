#!/usr/bin/python

import can
from can import Message
from device import device
from util import *

"""
This function handles any messages from the motor controller
@param message
@return dictionary
"""
class motorController(device):
	"""
	Initializes all motor controller attributes
	"""
	def __init__(self):
		raise Exception("NOT YET IMPLEMENTED")
	
	"""
	Handles message for motor controller
	@param message  CAN message to parse
	@return hypercan_message
	"""
	def handle_message(self, message):
		raise Exception("NOT YET IMPLEMENTED")
		
		# Update object
		self.update_device(hypercan_message)
		
		return hypercan_message

	