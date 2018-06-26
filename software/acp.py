#!/usr/bin/python
import serial
import sys
connection = serial.Serial("/dev/ttyUSB0", 9600, timeout=1)

def receive_message():
    message_received = ""
    next_byte = connection.read(1)
    # after read the first byte, set the timeout to 100ms
    connection.timeout = 0.1
    # keep reading bytes until timeout exceed
    while (next_byte != ""):
	    message_received += next_byte
	    next_byte = connection.read(1)

    print message_received

def adr():
    connection.write("#???ADR\r")
    receive_message()  

def set_adr(previous, new):
    message = "#" + previous + "ADR" + new + "\r"
    connection.write(message)
    receive_message()

def idn():
    connection.write("#000IDN\r")
    receive_message()  

def on():
    connection.write("#000ACPON\r")
    receive_message()  
    
def off():
    connection.write("#000ACPOFF\r")
    receive_message()  

def standby_speed():
    connection.write("#000SBY\r")
    receive_message()      

def nominal_speed():
    connection.write("#000NSP\r")
    receive_message()      

def set_speed(speed):
    if ((speed > 6000) or (speed < 2100)):
        print "error: minimum speed = 2100; maximum speed = 6000 rpm"
    else:
        message = "#000RPM" + str(speed/10*10) + "\r"
        print "Speed adjusted to " + str(speed/10*10) + " rpm (" + str(round((speed/10*10/60.0),2)) + " Hz)"
        connection.write(message)
        receive_message()  

