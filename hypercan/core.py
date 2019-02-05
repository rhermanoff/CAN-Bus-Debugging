#!/usr/bin/python
 
import can
import time
import os
import struct
can.rc['interface'] = 'socketcan'
 
from can import Bus
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
		self.notifier = can.Notifier(bus, [on_message_received].extend(listeners))
		self.verbose = verbose
		
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
			bus.shutdown()
			notifier.stop()

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
		if message['arbitration_id'] == 0x18FF50E5:
			return ccs.handle(message)
		elif message['arbitration_id'] >= 0x620 and message['arbitration_id'] <= 0x628:
			return bms.handle(message)
		else:
			# Eventually I need to add an eexception class here....and add the motor controller
			raise Exception('Unknown arbitration ID '+str(message['arbitration_id']))
			
			
			
			
###OLD CODE 
###OLD CODE 
###OLD CODE 
###OLD CODE 
###OLD CODE 
###OLD CODE 
				
	def send_message(bus, Message):
		try:
			bus.send(Message);
		except:
			print("Some error was handled")


	def set_charger(bus, data):
		print("Enabling Charger")
		Message.extended_id = True
		Message.is_remote_frame = False
		Message.id_type = 1
		Message.is_error_frame = False
		Message.arbitration_id = 0x1806E5F4 # The arbitration ID of the charger
		Message.dlc = 5
		Message.data = bytearray([ vol_set_h, vol_set_l, cur_set_h, cur_set_l, enable ]) # 50.4V @ 10A
		send_message(bus, Message)

	def enable_charger(bus):
		print("Enabling Charger")
		set_charger(bus, [0x05, 0x04, 0x01, 0x00, 0x01])

	def disable_charger(bus):
		print("Disabling Charger")
		set_charger(bus, [0x05, 0x04, 0x01, 0x00, 0x00])