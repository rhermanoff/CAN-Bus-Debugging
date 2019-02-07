#!/usr/bin/python

import hypercan
import click

from hypercan import core, device, ccs, bms
from pprint import pprint

def main():
	# Create a CCS and BMS object to eventually send messages to
	ccs = hypercan.ccs.ccs()
	bms = hypercan.bms.bms()
	
	
	# Start a can driver on the can1 interface with no verbosity and a specified listener
	can_driver = hypercan.core.driver('can1', False, [listener])
	
	
	# An example message: Begin charging at 10v, 10A
	# DO NOT UNCOMMENT THIS LINE UNLESS YOU SERIOUSLY
	# KNOW WHAT YOU'RE DOING, THE CHARGER CAN BE DEATHLY
	# IF USED IMPROPERLY OR WITHOUT PRIOR KNOWLEDGE OF 
	# BATTERY SYSTEMS
	#ccs.set_charge(can_driver, 10.0, 10.0, False)
	
	# Another example message: Switch on the contactors
	# DO NOT UNCOMMENT THIS LINE UNLESS YOU SERIOUSLY 
	# KNOW WHAT YOU'RE DOING, ENABLING THE CONTACTORS
	# ALLOWS HIGH VOLTAGE TO FLOW THROUGH THE POD SYSTEMS
	#bms.switch_contactors(can_driver, True)
	 
	
	# Enter a blocking loop to listen for messages
	can_driver.listen()
	
	
# A hypercan listener to consume messages
# Only used if you need to directly interface
# with CAN messages, otherwise use device attributes
def listener(hypercan_message, can_driver):
	pprint(hypercan_message)

if __name__ == "__main__":
	main()