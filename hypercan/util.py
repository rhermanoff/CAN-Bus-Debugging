#!/usr/bin/python

def hex_to_signed_int(hex):
	try:
		int(hex, 16)
	except ValueError:
		print "hex_to_signed_int accepts hex strings - Ex: \"0x7fff\""
		raise Exception('')
	
	return -(hex & 0x8000) | (hex & 0x7fff)