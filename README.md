# CAN-Bus-Debugging
CAN Bus Debugging for Michigan Hyperloop


This is a piece of software that lets the power subteam of Michigan Hyperloop test, debug, and otherwise develop our various electrical pod systems.  It contains common functions for interfacing with the Battery Management System (BMS), Charge Control System (CCS), and motor controllers.  I will document this code as well as I can but please understand that is a set of personal tools and not neccessarily a representation of what is acceptable.  I'm still a Python (and CAN) beginner.

Please refer to my document on CAN theory if you are still a beginner. It can be found in `Mhype/2019/subteams/controls/MC/HVBMS/CAN/CAN Bus Tranceiver/CAN_Tranceiver/Documentation/`.

## Installation

Hypercam was developed in a Python 2.7 environment.  To install please run `python setup.py install`. 

## Usage

Usage is still to be documented.  Eventually I would like to add a menu system as a demo and some tools for logging things like the traction pack messages, or number of can messages transmitted and receieved by certain devices over time, or message distribution by arbitration ID.  I would also like to include a number of command line tools for easily extracting information from the various pod subsystems. 


For now it will simply be a collection of sample code to eventually be worked into a module of abstracted commands to interface with each system.  

## License

I don't currently have a license as I'm not entirely educated on which is most appropriate for this use.  If anyone knows please feel free to reach out to rherma@umich.edu