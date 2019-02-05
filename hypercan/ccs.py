#!/usr/bin/python

class ccs():
	"""
	This function handles any messages from the CCS
	@param message
	@return dictionary
	"""
	def handle(self, message):
		# Decode voltage and current, {V/C} = {V/C}_high_bit * 10 + {V/C}_low_bit / 10.0
		voltage = message.data[0] * 10 + message.data[1] / 10.0
		current = message.data[2] * 10 + message.data[3] / 10.0
	
		# Status_bytes contains array of bit data for charger status, maybe a hack?
		status_bytes = format(message.data[5], 'b')
		
		return {
			'success':True,
			'device':'ccs',
			'type':None,
			'data':{
				'voltage':voltage,
				'current':current,
				'hardware_failure':bool(status_bytes[0]),
				'temperature_of_charger':bool(status_bytes[1]),
				'input_voltage':bool(status_bytes[2]),
				'stating_state':bool(status_bytes[3]),
				'communication_state':bool(status_bytes[4]),
			}
		}