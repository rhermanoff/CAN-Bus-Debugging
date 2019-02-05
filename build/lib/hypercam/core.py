#!/usr/bin/python
 
import can
import time
import os
can.rc['interface'] = 'socketcan_ctypes'
 
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
	"""
	def __init__(self, interface, verbose):
		self.bus = Bus(interface, bustype = 'socketcan')
		self.notifier = can.Notifier(bus, [on_message_received])
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
	This function handles any messages from the CCS
	@param message
	@return dictionary
	"""
	def handle_ccs_receive(self, message):
		# Decode voltage and current, {V/C} = {V/C}_high_bit * 10 + {V/C}_low_bit / 10.0
		voltage = message.data[0] * 10 + message.data[1] / 10.0
		current = message.data[2] * 10 + message.data[3] / 10.0
	
		# Status_bytes contains array of bit data for charger status, maybe a hack?
		status_bytes = int(bin(message.data[5])[2:])
		
		return {
			'success':True,
			'device':'ccs',
			'voltage':voltage,
			'current':current,
			'hardware_failure':True if status_bytes[0] == '1' else False,
			'temperature_of_charger':True if status_bytes[1] == '1' else False,
			'input_voltage':True if status_bytes[2] == '1' else False,
			'stating_state':True if status_bytes[3] == '1' else False,
			'communication_state':True if status_bytes[4] == '1' else False,
		}
	
	"""
	This function handles any messages from the BMS
	@param message
	@return dictionary
	"""
	def handle_bms_receive(self, message):
		# Bleh.  This is probably a traction message, which means we have
		# 9 possible arbitration IDs.  It also sends out other information
		# meant for things we don't currently use, so we will have to handle
		# or log that information.
		#
		# Python doesn't have switch statements and I'm not sure how this code
		# should be formatted in practice, so please read with a grain of salt
		# 
		# The BMS uses little endian multi-byte values
		
		
		""" TODIOFJJWEOR"""
		status_bytes = int(bin(message.data[5])[2:])
		
		arbitration_id = message['arbitration_id']
		
		if arbitration_id == 0x620:
			# Unneeded message, just says ELITHION
			return {'success':True,'device':'bms'}
		elif arbitration_id == 0x621:
			# Unneeded message, just gives us the software revision
			return {'success':True,'device':'bms'}
		elif arbitration_id == 0x622:
			# Now we're to the meat and potatoes!
			state_bytes = int(bin(message.data[0])[2:])
			flag_bytes = int(bin(message.data[3])[2:])
			level_bytes = int(bin(message.data[5])[2:])
			warnings_bytes = int(bin(message.data[6])[2:])
			
			return {
				'success':True,
				'device':'bms',
				'state':{
					
					'relay_fault':True if state_bytes[4] == '1' else False,
					'k3_on':True if state_bytes[3] == '1' else False,
					'k2_on':True if state_bytes[2] == '1' else False,
					'k1_on':True if state_bytes[1] == '1' else False,
					'fault_state':True if state_bytes[0] == '1' else False,
				},
				'timer':int(int(bin(message.data[1])[2:]) + int(bin(message.data[1])[3:])),
				'flags':{
					'fan':True if flag_bytes[7] == '1' else False,
					'llim':True if flag_bytes[6] == '1' else False,
					'hlim':True if flag_bytes[5] == '1' else False,
					'can_contactor_request':True if flag_bytes[4] == '1' else False,
					'hard_wire_contactor_request':True if flag_bytes[3] == '1' else False,
					'interlock':True if flag_bytes[2] == '1' else False,
					'load_power':True if flag_bytes[1] == '1' else False,
					'source_power':True if flag_bytes[1] == '1' else False,
				},
				'fault_code':message.data[4],
				'level_faults':{
					'over_voltage':True if level_fault_flags[7] == '1' else False,
					'under_voltage':True if level_fault_flags[6] == '1' else False,
					'over_temperature':True if level_fault_flags[5] == '1' else False,
					'discharge_overcurrent':True if level_fault_flags[4] == '1' else False,
					'charge_overcurrent':True if level_fault_flags[3] == '1' else False,
					'bank_communication_fault':True if level_fault_flags[2] == '1' else False,
					'interlock_tripped':True if level_fault_flags[1] == '1' else False,
					'driving_off_while_plugged_in':True if level_fault_flags[0] == '1' else False,
				},
				'warnings':{
					'isolation_fault':True if warnings_bytes[7] == '1' else False,
					'low_soc':True if warnings_bytes[6] == '1' else False,
					'hot_temperature':True if warnings_bytes[5] == '1' else False,
					'cold_temperature':True if warnings_bytes[4] == '1' else False,
					'discharge_overcurrent':True if warnings_bytes[3] == '1' else False,
					'charge_overcurrent':True if warnings_bytes[2] == '1' else False,
					'high_voltage':True if warnings_bytes[1] == '1' else False,
					'low_voltage':True if warnings_bytes[0] == '1' else False,
				}
			}
			
		elif arbitration_id == 0x623:
			return {'success':True,'device':'bms'}
		elif arbitration_id == 0x624:
			return {'success':True,'device':'bms'}
		elif arbitration_id == 0x625:
			return {'success':True,'device':'bms'}
		elif arbitration_id == 0x626:
			return {'success':True,'device':'bms'}
		elif arbitration_id == 0x627:
			return {'success':True,'device':'bms'}
		elif arbitration_id == 0x628:
			return {'success':True,'device':'bms'}
		
	
	
		
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
		
		# Handle messages from the charger
		if message['arbitration_id'] == 0x18FF50E5:
			return self.handle_ccs_receive(message)
		elif message['arbitration_id'] >= 0x620 and message['arbitration_id'] <= 0x628:
			return self.handle_bms_receive(message)
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