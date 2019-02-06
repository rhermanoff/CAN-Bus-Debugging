#!/usr/bin/python

import hypercan
from pprint import pprint

def main():

	# Create a CCS object to eventually send messages to
	ccs = hypercan.device.ccs()
	
	# Start a can driver on the can1 interface with no verbosity and a specified listener
	can_driver = hypercan.driver('can1', False, [listener])
	
	# An example message: Begin charging at 10v, 10A
	# DO NOT UNCOMMENT THIS LINE UNLESS YOU SERIOUSLY
	# KNOW WHAT YOU'RE DOING, THE CHARGER CAN BE DEATHLY
	# IF USED IMPROPERLY OR WITHOUT PRIOR KNOWLEDGE OF 
	# BATTERY SYSTEMS
	#ccs.charge(can_driver, 10.0, 10.0)
	
	# Enter a blocking loop to listen for messages
	can_driver.listen()
	
	
# A hypecan listener to consume messages
def listener(hypercan_message):
	pprint(hypercan_message)

if __name__ == "__main__":
	main()