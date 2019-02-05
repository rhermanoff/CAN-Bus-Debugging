#!/usr/bin/python
class bms():
	"""
	This function handles any messages from the BMS
	@param message
	@return dictionary
	"""
	def handle(self, message):
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
		elif arbitration_id == 0x625: # TODO
			return {
				'success':True,
				'device':'bms',
				'type':None,
				'data':{
				}
			}
		elif arbitration_id == 0x626: # TODO
			return {
				'success':True,
				'device':'bms',
				'type':None,
				'data':{}
			}
		elif arbitration_id == 0x627: # TODO
			return {
				'success':True,
				'device':'bms',
				'type':None,
				'data':{}
			}
		elif arbitration_id == 0x628: # TODO
			return {
				'success':True,
				'device':'bms',
				'type':None,
				'data':{}
			}
		
	
	
		