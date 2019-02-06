#!/usr/bin/python

import can
from can import Message
from pprint import pprint
from hypercan.util import *

"""
This function handles any messages from the CCS
@param message
@return dictionary
"""
class ccs():
	def handle_message(message):
		# Decode voltage and current, {V/C} = {V/C}_high_bit * 10 + {V/C}_low_bit / 10.0
		voltage = message.data[0] * 10 + message.data[1] / 10.0
		current = message.data[2] * 10 + message.data[3] / 10.0

		# Status_bytes contains array of bit data for charger status, maybe a hack?
		status_bytes = format(message.data[4], 'b')
		pprint(status_bytes)
		
		return {
			'success':True,
			'device':'ccs',
			'type':None,
			'data':{
				'voltage':voltage,
				'current':current,
				'hardware_failure':bool_str(status_bytes[0]),
				'temperature_of_charger':bool_str(status_bytes[1]),
				'input_voltage':bool_str(status_bytes[2]),
				'stating_state':bool_str(status_bytes[3]),
				'communication_state':bool_str(status_bytes[4]),
			}
		}
		
	"""
	Commands CCS to begin charging at a specified voltage and current
	PLEASE READ:
	THE CHARGER HAS THE ABILITY TO OUTPUT EXTREMELY HIGH VOLTAGES AND
	HIGH CURRENTS.  IF YOU MISUSE THE CHARGER AND COMMAND IT WRONG YOU
	COULD SERIOUSLY INJURE OR KILL YOURSELF.  THE BATTERY IS ALSO EXTREMELY
	SENSITIVE TO CHARGING AND CARE SHOULD BE TAKEN TO ENSURE THAT THE BMS
	CAN SHUT OFF THE CHARGER WHEN HLIM IS REACHED.  FAILURE TO DO SO WILL
	RESULT IN THE BATTERY BEING OVERCHARGED AND EXPLODING.
	
	@param driver  CAN driver to send message to
	@param voltage  Voltage to a precision of 0.1v	
	@param current  Current to a precision of 0.1A
	"""
	def charge(self, driver, voltage, current):
		# Check for bad values
		if current < 0:
			raise Exception('Commanded current is negative')
		elif current > 12:
			raise Exception('Commanded current is greater than max rating')
		if voltage < 0:
			raise Exception('Commanded voltage is negative')
		elif voltage > 650:
			raise Exception('Commanded voltage is greater than max rating')
	
		# Convert to a ccs friendly value
		ccs_voltage = float_to_ccs_value(voltage)
		ccs_current = float_to_ccs_value(current)
		
		# Construct and send message
		Message.extended_id = True
		Message.is_remote_frame = False
		Message.id_type = 1
		Message.is_error_frame = False
		Message.arbitration_id = 0x1806E5F4
		Message.dlc = 5
		Message.data = bytearray(ccs_voltage + ccs_current + [0])
		driver.send_message(Message)
		
	"""
	Commands CCS to begin stop charging and reset voltage/current
	"""
	def halt_charge():
		# Construct and send message
		Message.extended_id = True
		Message.is_remote_frame = False
		Message.id_type = 1
		Message.is_error_frame = False
		Message.arbitration_id = 0x1806E5F4
		Message.dlc = 5
		Message.data = bytearray([0x00, 0x00, 0x00, 0x00, 0x01])
		send_message(bus, Message)
	
"""
This function handles any messages from the BMS
@param message
@return dictionary
"""
class bms:
	def handle_message(message):
		# Bleh.  This is probably a traction message, which means we have
		# 9 possible arbitration IDs.  It also sends out other information
		# meant for things we don't currently use, so we will have to handle
		# or log that information.
		#
		# Python doesn't have switch statements and I'm not sure how this code
		# should be formatted in practice, so please read with a grain of salt
		# 
		# The BMS uses little endian multi-byte values
		
		arbitration_id = message['arbitration_id']
		
		if arbitration_id == 0x620:
			# Unneeded message, just says ELITHION
			return {
				'success':True,
				'device':'bms',
				'type':None,
				'data':{}
			}
		elif arbitration_id == 0x621:
			# Unneeded message, just gives us the software revision
			return {
				'success':True,
				'device':'bms',
				'type':None,
				'data':{}
			}
		elif arbitration_id == 0x622:
			# Now we're to the meat and potatoes!
			state_bytes = format(message.data[0],'b')
			flag_bytes = format(message.data[3],'b')
			level_bytes = format(message.data[5],'b')
			warnings_bytes = format(message.data[6],'b')
			
			return {
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
					'timer':int(hex(message.data[1]<<16) | message.data[2], 16), # Little trick to combine these two properly
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
			return {
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
			return {
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
			
			return {
				'success':True,
				'device':'bms',
				'type':'0+5',
				'data':{
					'energy_in':int(energy_in_bits, 16),
					'energy_out':int(energy_out_bits, 16),
				}
			}
		elif arbitration_id == 0x626: 
			return {
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
			return {
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
			return {
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