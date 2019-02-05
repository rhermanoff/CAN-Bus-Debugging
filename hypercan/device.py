#!/usr/bin/python

class device:
	_name = None
	
	def handle(self, message):
		raise NotImplementedError("{} has not implemented handle".format(self.__class__.__name__))
	