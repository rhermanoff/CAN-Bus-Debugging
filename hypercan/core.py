#!/usr/bin/python
 
import can
import click
import time
import os
import struct
from hypercan import bms, ccs, motorController

can.rc['interface'] = 'socketcan'
 
from can.interfaces.interface import Bus
from can import Message
 

# By default, the can library will look for a function
# parse_can which is called on the event of a can message
# Alernatively one can initiate a loop to look for received
# messages with no timeout, or iterate through the bytes
# directly.	It is suggested that you use a listener, though
# to tidy up code and have can messages be handled as an event.
class driver:

	"""
	Driver construcotr
	@param interface  Name of the CAN interface to listen on
	@param verbose  On true, print extra verbose debugging info
	@param listeners  Additional listeners for CAN notifier
	"""
	def __init__(self, interface, verbose = False, listeners = None):
		self.bus = Bus(interface, bustype = 'socketcan')
		self.verbose = verbose
		self.listeners = listeners
		self.bms = bms.bms()
		self.ccs = ccs.ccs()
		self.motorController = motorController.motorController()
		self.notifier = can.Notifier(self.bus, [self.on_message_received])
		
	"""
	Starts a loop to keep notifier alive.  Do not use 
	if you already have an event loop.
	@exception on any thrown event, shuts down bus and stops notifier
	"""
	def listen(self):
		try:
			while True:
				time.sleep(1)
		except KeyboardInterrupt:
			print("Exception Handled!")
			self.bus.shutdown()
			self.notifier.stop()
	
	
	"""
	TODO DOC
	"""
	def notify_listeners(self, hypercan_message):
		for listener in self.listeners:
			listener(hypercan_message, self)

	"""
	Function is called whenever the notifier receives a message.
	@param message  Python-CAN message object
	@return hypermessage  Hyperloop level message dictionary
	"""
	def on_message_received(self, message):
		
		# Verbose output
		if self.verbose:
			print("Message Receieved")
			canFrameVars = vars(message)
			for var in canFrameVars:
				print(var+": "+str(canFrameVars[var]))
		
		# Properly handle messages
		if message.arbitration_id == 0x18FF50E5:
			self.notify_listeners(self.ccs.handle_message(message))
		elif message.arbitration_id >= 0x620 and message.arbitration_id <= 0x628:
			self.notify_listeners(self.bms.handle_message(message))
		elif self.verbose:
			# Eventually I need to add an exception class here....and add the motor controller
			# It is also noteworthy that this block may be deleted completely, there are many
			# arbitration IDs that we can safely ignore transmitted over the bus
			#raise Exception('Unknown arbitration ID '+str(message.arbitration_id))
			click.echo(click.style('Unknown arbitration ID '+hex(message.arbitration_id), bg='red', fg='white'))
			

	"""
	Attempts to send message over CAN bus
	@param Message  CAN message object to TX
	@throws on CAN error
	"""
	def send_message(self, Message):
		try:
			self.bus.send(Message);
		except:
			print("Some error was handled")