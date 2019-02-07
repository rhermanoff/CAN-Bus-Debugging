#!/usr/bin/python

from pprint import pprint
from hypercan.util import *

class device():
	"""
	Updates a device's attributes using a hypercan message
	@param hypercan_message
	@throws on non existant object attribute
	"""
	def update_device(self, hypercan_message):
		# Iterate data replacing valid keys
		for key in hypercan_message['data']:
			if not hasattr(self,key):
				raise Exception("Key " + key + " does not exist for object " + self.__name__)
				
			setattr(self, key, hypercan_message['data'][key])