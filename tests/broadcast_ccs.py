#!/usr/bin/python

# Imports
import can
import random
import time
import argparse
import logging
import sys
import click

can.rc['interface'] = 'socketcan'

from can.interfaces.interface import Bus
from can import Message
from hypercan.util import float_to_ccs_value
from apscheduler.schedulers.background import BackgroundScheduler

# Helper function to parse arguments
def str2bool(v):
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

# Sends random CCS message
def _send_ccs_rand(bus):
	test_voltage = random.uniform(0, 650)
	test_current = random.uniform(0, 10)
	
	click.echo(
		click.style(
			"Broadcasting CCS frame: "+str(test_voltage)+"V "+str(test_current)+"A",
			bg='green',
			fg='black'
		)
	)

	message = Message(
		extended_id = True,
		is_remote_frame = False,
		is_error_frame = False,
		arbitration_id = 0x18FF50E5,
		dlc = 8,
		data = bytearray(float_to_ccs_value(test_voltage) + float_to_ccs_value(test_current) + [0x18, 0, 0, 0]),
	)
	
	bus.send(message)

# Parse CMD arguments
parser = argparse.ArgumentParser(description='Simulates CAN bus messages from CCS')
parser.add_argument("--verbose", type=str2bool, nargs='?',
                        const=True, default=False,
                        help="Prints verbose logger messages")
args = parser.parse_args()

# Add verbose logger
if args.verbose:
	logging.basicConfig()
	logging.getLogger('apscheduler').setLevel(logging.DEBUG)

# Init CAN
bus = Bus('can1', bustype = 'socketcan')

# Pose as CCS and send out some messages
scheduler = BackgroundScheduler()
scheduler.add_job(_send_ccs_rand, 'interval', args=[bus], seconds=1)
scheduler.start()

# Enter blocking loop to keep daemon alive
while True:
	try:
		time.sleep(1)
	except:
		# Gracefully shutdown scheduler
		click.echo(click.style('Exception Handled! Killing thread', bg='red', fg='white'))
		scheduler.shutdown()
		sys.exit()