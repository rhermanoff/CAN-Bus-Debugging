#!/usr/bin/python

import math

"""
Utility function to convert a float to a
list of ccs values for voltage or amperage
@param val  Float to convert
@return list
@throws on a val with length greater than 4 after 
        truncating to one trailing decimal
"""
def float_to_ccs_value(val):
	# Truncate and move decimal place
	truncated = str(int(float("{0:.1f}".format(val))*10)).zfill(4)
	
	if len(truncated) != 4:
		raise Exception('Truncated CCS value expected to be 4')
	
	return [ int(truncated[0:2]), int(truncated[2:4]) ]

"""
Utility function to translate a boolean character
to a boolean
@param chr  Character to convert
@return bool  Boolean values
@throws on chr != ['0','1']
"""
def bool_str(chr):
	if chr not in ['0','1']:
		raise Exception('Expected \'0\' or \'1\'!')
		
	return bool(1 if chr == '1' else 0)

"""
Utility function to turn a hex string
to a signed integer, converts to a certain size var
by the size of the hex string
@param hex  Hex string to convert
@return int
"""
def hex_to_signed_int(hex):
    uintval = int(hex,16)
    bits = 4 * (len(hex) - 2)
    if uintval >= math.pow(2,bits-1):
        uintval = int(0 - (math.pow(2,bits) - uintval))
    return uintval
	
"""
Converts an array of hex values to a little endian integer
@param data  Array of hex values
@return  Integer representation of hex value
"""
def hex_to_little_endian_int(data):
	parsed_data = map(lambda x: format(x, 'x').zfill(2), data)
	parsed_data.reverse()
	return int('0x' + ''.join(parsed_data), 16)

"""
Converts an int to a little endian formatted
array of hex values
@param val  Integer to convert
@return list  List of hex values
"""
def int_to_little_endian_hex(val):
    int_hex = hex(val)[2::]
    hex_len = len(int_hex)
    filled_hex = int_hex.zfill(hex_len + 1 if hex_len % 2 == 1 else hex_len)
    split_hex = wrap(filled_hex, 2)
    split_hex.reverse()
    print(split_hex)
    x = map(lambda x: hex(int(x, 16)), split_hex)
    print(x)
	
"""
Splits string s into a list of w lengths
@param s
@param w
@return list
"""
def wrap(s, w):
    return [s[i:i + w] for i in range(0, len(s), w)]
	