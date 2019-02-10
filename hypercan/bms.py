#!/usr/bin/python

import can
from can import Message
from device import device
from util import *
from apscheduler.schedulers.background import BackgroundScheduler

"""
This function handles any messages from the BMS
@param message
@return dictionary
"""
class bms(device):

	"""
	Initializes all BMS attributes
	"""
	def __init__(self):
		# Daemonic scheduler for contactor requests
		self.scheduler = BackgroundScheduler(daemon=True)
		
		# BMS attributes
		self.relay_fault = None
		self.k3_on = None
		self.k2_on = None
		self.k1_on = None
		self.fault_state = None
		self.fan = None
		self.llim = None
		self.hlim = None
		self.can_contactor_request = None
		self.hard_wire_contactor_request = None
		self.interlock = None
		self.load_power = None
		self.source_power = None
		self.over_voltage = None
		self.under_voltage = None
		self.over_temperature = None
		self.discharge_overcurrent = None
		self.bank_communication_fault = None
		self.interlock_tripped = None
		self.driving_off_while_plugged_in = None
		self.isolation_fault = None
		self.low_soc = None
		self.hot_temperature = None
		self.cold_temperature = None
		self.high_voltage = None
		self.low_voltage = None
		self.pack_voltage = None
		self.min_voltage = None
		self.min_voltage_pack = None
		self.max_voltage = None
		self.max_voltage_pack = None
		self.current = None
		self.charge_limit = None
		self.discharge_limit = None
		self.energy_in = None
		self.energy_out = None
		self.soc = None
		self.dod = None
		self.capacity = None
		self.soh = None
		self.temperature = None
		self.min_temperature = None
		self.min_temperature_pack = None
		self.max_temperature = None
		self.max_temperature_pack = None
		self.pack_resistance = None
		self.min_resistance = None
		self.min_resistance_pack = None
		self.max_resistance = None
		self.max_resistance_pack = None

	"""
	Handles message for BMS
	@param message  CAN message to parse
	@return hypercan_message
	"""
	def handle_message(self, message):
		# Bleh.  This is probably a traction message, which means we have
		# 9 possible arbitration IDs...  It also sends out other information
		# meant for things we don't currently use, so we will have to handle
		# or log that information.
		#
		# Python doesn't have switch statements and I'm not sure how this code
		# should be formatted in practice, so please read with a grain of salt
		# 
		# The BMS uses little endian multi-byte values
		
		arbitration_id = message.arbitration_id
		
		if arbitration_id == 0x620:
			# Unneeded message, just says ELITHION
			hypercan_message = {
				'success':True,
				'device':'bms',
				'type':None,
				'data':{}
			}
		elif arbitration_id == 0x621:
			# Unneeded message, just gives us the software revision
			hypercan_message = {
				'success':True,
				'device':'bms',
				'type':None,
				'data':{}
			}
		elif arbitration_id == 0x622:
			# Now we're to the meat and potatoes!
			state_bytes = format(message.data[0],'b').zfill(8)
			flag_bytes = format(message.data[3],'b').zfill(8)
			level_bytes = format(message.data[5],'b').zfill(8)
			warnings_bytes = format(message.data[6],'b').zfill(8)
			
			hypercan_message = {
				'success':True,
				'device':'bms',
				'type':'0+2',
				'data':{
					'state':{
						'relay_fault':bool(state_bytes[4]),
						'k3_on':bool(state_bytes[3]),
						'k2_on':bool(state_bytes[2]),
						'k1_on':bool(state_bytes[1]),
						'fault_state':bool(state_bytes[0]),
					},
					'timer':int(message.data[1]<<16 | message.data[2], 16), # Little trick to combine these two properly
					'flags':{
						'fan':bool(flag_bytes[7]),
						'llim':bool(flag_bytes[6]),
						'hlim':bool(flag_bytes[5]),
						'can_contactor_request':bool(flag_bytes[4]),
						'hard_wire_contactor_request':bool(flag_bytes[3]),
						'interlock':bool(flag_bytes[2]),
						'load_power':bool(flag_bytes[1]),
						'source_power':bool(flag_bytes[1]),
					},
					'fault_code':message.data[4],
					'level_faults':{
						'over_voltage':bool(level_fault_flags[7]),
						'under_voltage':bool(level_fault_flags[6]),
						'over_temperature':bool(level_fault_flags[5]),
						'discharge_overcurrent':bool(level_fault_flags[4]),
						'charge_overcurrent':bool(level_fault_flags[3]),
						'bank_communication_fault':bool(level_fault_flags[2]),
						'interlock_tripped':bool(level_fault_flags[1]),
						'driving_off_while_plugged_in':bool(level_fault_flags[0]),
					},
					'warnings':{
						'isolation_fault':bool(warnings_bytes[7]),
						'low_soc':bool(warnings_bytes[6]),
						'hot_temperature':bool(warnings_bytes[5]),
						'cold_temperature':bool(warnings_bytes[4]),
						'discharge_overcurrent':bool(warnings_bytes[3]),
						'charge_overcurrent':bool(warnings_bytes[2]),
						'high_voltage':bool(warnings_bytes[1]),
						'low_voltage':bool(warnings_bytes[0]),
					}
				}
			}
			
		elif arbitration_id == 0x623:
			hypercan_message = {
				'success':True,
				'device':'bms',
				'type':'0+3',
				'data':{
					'pack_voltage':int(int(bin(message.data[0])[2:]) + int(bin(message.data[1])[2:])),
					'min_voltage':int(message.data[2]) * 10,
					'min_voltage_pack':int(message.data[3]),
					'max_voltage':int(message.data[4]) * 10,
					'max_voltage_pack':int(message.data[5]),
				}
			}
		elif arbitration_id == 0x624:
			hypercan_message = {
				'success':True,
				'device':'bms',
				'type':'0+4',
				'data':{
					'current':hex_to_signed_int((message.data[0]>>16)|message.data[1], 16),
					'charge_limit':int((message.data[2]>>16)|message.data[3], 16),
					'dischage_limit':int((message.data[4]>>16)|message.data[5],16),
				}
			}
		elif arbitration_id == 0x625: 
			energy_in_bits = '' 
			energy_out_bits = ''
			for i in range(4):
				energy_in_bits += format(message.data[i],'b')
				enerty_out_bits += format(message.data[i + 4],'b')
			
			hypercan_message = {
				'success':True,
				'device':'bms',
				'type':'0+5',
				'data':{
					'energy_in':int(energy_in_bits, 16),
					'energy_out':int(energy_out_bits, 16),
				}
			}
		elif arbitration_id == 0x626: 
			hypercan_message = {
				'success':True,
				'device':'bms',
				'type':'0_6',
				'data':{
					'soc':int(message.data[0]),
					'dod':int(hex(message.data[1]<<16) | message.data[2], 16),
					'capacity':int(hex(message.data[3]<<16) | message.data[4], 16),
					'soh':int(message.data[6]),
				}
			}
		elif arbitration_id == 0x627: 
			hypercan_message = {
				'success':True,
				'device':'bms',
				'type':'0+7',
				'data':{
					'temperature':hex_to_signed_int(hex(message.data[0])),
					'min_temperature':hex_to_signed_int(hex(message.data[2])),
					'min_temperature_pack':int(message.data[3]),
					'max_temperature':hex_to_signed_int(hex(message.data[4])),
					'max_temperature_pack':int(message.data[5]),
				}
			}
		elif arbitration_id == 0x628: 
			hypercan_message = {
				'success':True,
				'device':'bms',
				'type':'0+8',
				'data':{
					'pack_resistance':int(format(message.data[0],'b')+format(message.data[1],'b')) / 10,
					'min_resistance':int(message.data[2])/10.0,
					'min_resistance_pack':int(message.data[3]),
					'max_resistance':int(message.data[4])/10.0,
					'max_resistance_pack':int(message.data[5]),
				}
			}
			
		# Update object
		self.update_device(hypercan_message)
		
		return hypercan_message
		
	"""
	Internal function to send contactor request over bus
	@param driver  CAN driver to send message to
	@param enable Enable contactors
	"""
	def _send_contactor_request(self, driver, enable):
		# Construct and send message
		message = Message(
			extended_id = False,
			is_remote_frame = False,
			is_error_frame = False,
			arbitration_id = 0x632,
			dlc = 8,
			data = [0x01 if enable else 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
		)
		
		driver.send_message(message)
		
	"""
	Starts a scheduler to send a contactor request every 300ms
	@param driver  CAN driver to send message to
	@param enable  Enable contactors
	"""
	def switch_contactors(self, driver, enable):
		# Register job with scheduler and begin
		self.scheduler.add_job(self._send_contactor_request,'interval',args=[driver, enable], seconds=0.3)
		self.scheduler.start()