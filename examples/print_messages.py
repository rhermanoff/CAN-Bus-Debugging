#!/usr/bin/python
from hypercan import driver

def main():
	can_driver = driver('can1')
	can_driver.listen()

if __name__ == "__main__":
	main()