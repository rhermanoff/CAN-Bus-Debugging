#!/usr/bin/python

import hypercan
import click

from hypercan import core, device, ccs, bms
from pprint import pprint

def main():
	click.echo(click.style('Initializing Hypercan', bg='green', fg='black'))

	
	
	# Start a can driver on the can1 interface with no verbosity and a specified listener
	can_driver = hypercan.core.driver('can1', False, [listener])
	
	# Create a CCS and BMS object to eventually send messages to
	ccs = can_driver.ccs
	bms = can_driver.bms
	
	# Enter a blocking loop to listen for messages
	click.echo(click.style('Begin Listening', bg='green', fg='black'))
	can_driver.listen()
	
	# An example message: Begin charging at 10v, 10A
	# DO NOT UNCOMMENT THIS LINE UNLESS YOU SERIOUSLY
	# KNOW WHAT YOU'RE DOING, THE CHARGER CAN BE DEATHLY
	# IF USED IMPROPERLY OR WITHOUT PRIOR KNOWLEDGE OF 
	# BATTERY SYSTEMS
	# --
	# THIS CODE WILL NOT EXECUTE UNLESS YOU ADD 
	# YOUR OWN EVENT LOOP AND REMOVE THE LISTENER
	# OR HANDLE THE CHARGE ELSEWHERE
	
	# Another example message: Switch on the contactors
	# DO NOT UNCOMMENT THIS LINE UNLESS YOU SERIOUSLY 
	# KNOW WHAT YOU'RE DOING, ENABLING THE CONTACTORS
	# ALLOWS HIGH VOLTAGE TO FLOW THROUGH THE POD SYSTEMS
	# --
	# THIS CODE WILL NOT EXECUTE UNLESS YOU ADD 
	# YOUR OWN EVENT LOOP AND REMOVE THE LISTENER
	# OR HANDLE THE CONTACTORS ELSEWHERE
	#bms.switch_contactors(can_driver, True)
	 
	
	
	
# A hypercan listener to consume messages
# Only used if you need to directly interface
# with CAN messages, otherwise use device attributes
def listener(hypercan_message, can_driver):

	# Simply dump the message
	click.echo(click.style('Message Received:', bg='blue', fg='white'))
	pprint(hypercan_message)
	
	# We can also print device attributes
	# print can_driver.ccs.voltage
	# print can_driver.bms.pack_voltage

if __name__ == "__main__":
	main()