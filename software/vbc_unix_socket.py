#!/usr/bin/python
# -*- coding: utf-8 -*-
import socket
import sys
import os
import serial
import Adafruit_BBIO.GPIO as GPIO
#------------------------------------------------------------------------------
PORT = "/dev/ttyUSB0"
#------------------------------------------------------------------------------
'''
=================
ACP 15
=================
acp_recv_msg
=================
TURBOVAC
=================
checksum
turbovac_recv_msg
pack_message
read_parameter
=================
Subroutines called from the main loop
=================
-----------------
tb
-----------------
ta

'''


#==============================================================================
# BBB functions support (for valves controls)
#==============================================================================
# defining pins used for valves controls
relay1 = "P9_23"
relay2 = "P9_21"
relay3 = "P9_24"
relay4 = "P9_12"
valve_open = "P8_7"
valve_closed = "P8_9"
#------------------------------------------------------------------------------
# defining pins direction
GPIO.setup(relay1, GPIO.OUT)
GPIO.setup(relay2, GPIO.OUT)
GPIO.setup(relay3, GPIO.OUT)
GPIO.setup(relay4, GPIO.OUT)
GPIO.setup(valve_open, GPIO.IN)
GPIO.setup(valve_closed, GPIO.IN)
#------------------------------------------------------------------------------
# setting output pins as low
GPIO.output(relay1, GPIO.LOW)
GPIO.output(relay2, GPIO.LOW)
GPIO.output(relay3, GPIO.LOW)
GPIO.output(relay4, GPIO.LOW)

#---------------------------------------
#
#---------------------------------------
'''
input parameters:
    - xxx:
    - yyy:
output parameters:
    - zzz:
----------------------------
description:
    blablabla
'''

#---------------------------------------
#
#---------------------------------------
'''
input parameters:
    - xxx:
    - yyy:
output parameters:
    - zzz:
----------------------------
description:
    blablabla
'''
#==============================================================================
# ACP15 functions support
#==============================================================================
#---------------------------------------
# sending a command to the pump
#---------------------------------------
'''
input parameters:
    - command: command to be sent to the pump
output parameters:
    - message_received: the answer back from the pump
----------------------------
description:
    this function is responsible for opening the serial connection with the
    USB/RS-485 converter through the FTDI chip, and also to send the desired
    command to the pump and receiving the answer back.
'''
def acp_recv_msg(command):
    con1 = serial.Serial(PORT, 9600, timeout=1)
    print "con1 = 9600"
    con1.write(command)

    message_received = ""
    next_byte = con1.read(1)
    # after read the first byte, set the timeout to 100ms
    con1.timeout = 0.1
    # keep reading bytes until timeout exceed
    while (next_byte != ""):
	    message_received += next_byte
	    next_byte = con1.read(1)

    print message_received
#==============================================================================
# TURBOVAC functions support
#==============================================================================
STX = "\x02"
ADR = "\x00"
# mirror telegram
#ADR = "\x40"
#---------------------------------------
# calculating the telegram checksum (BCC)
#---------------------------------------
'''
input parameters:
    - byte: array of bytes used in recursive call of this function. At the first
        call, this array represents all 23 bytes excluding the BCC field.
    - index: number of elements in "byte" array. It is used while calling
        recursively this function. At the first call, this number is 22.
output parameters:
    - BCC: checksum of the task telegram. It is calculated as an xor'ed of all
        characters in the task telegram.
----------------------------
description:
    this function takes as input the task telegram (24 bytes), send it to the
    TURBOVAC pump and returns the response telegram as an output parameter.
'''
def checksum(byte, index):
    if (index == 0):
        return ord(byte[0])
    else:
        return (checksum(byte, (index-1)) ^ ord(byte[index]))
#---------------------------------------
# sending and receiving telegrams
#---------------------------------------
'''
input parameters:
    - task telegram: the whole telegram that will be sent to the pump (24 bytes)
output parameters:
    - msg: response telegram
----------------------------
description:
    this function is responsible for opening the connection with the FTDI
    through a serial port represented in "/dev/ttyUSB0". Besides of that, this
    function also takes as input the task telegram (24 bytes), send it to the
    TURBOVAC pump and returns the response telegram as an output parameter.
'''
def turbovac_recv_msg(task_telegram):
    con2 = serial.Serial(
        port=PORT,
        baudrate=19200,
        parity=serial.PARITY_EVEN,
    #    stopbits=serial.STOPBITS_ONE,
    #    bytesize=serial.EIGHTBITS,
        timeout=1
    )
    #-----------------------------------------------------
    print "con2 = 19200"
    con2.write(task_telegram)
    #-----------------------------------------------------
    msg = ""
    next_byte = con2.read(1)
    # after read the first byte, set the timeout to 100ms
    con2.timeout = 0.1
    # keep reading bytes until timeout exceed
    while (next_byte != ""):
	    msg += next_byte
	    next_byte = con2.read(1)
    #-----------------------------------------------------
    print "==================="
    print " Response telegram "
    print "==================="
    if (len(msg) == 24):
        print "STX = 0x" + "{:02x}".format((ord(msg[0])))
        print "LGE = 0x" + "{:02x}".format((ord(msg[1])))
        print "ADR = 0x" + "{:02x}".format((ord(msg[2]))) + "\n"

        print "PKE = " + str((((ord(msg[3]) & 0b111) << 8)) + (ord(msg[4])))
        print "IND = " + str((ord(msg[6])))
        print "PWE = " + str((ord(msg[7]) << 24) + (ord(msg[8]) << 16) + (ord(msg[9]) << 8) + ord(msg[10])) + "\n"

        print "PZD1 = 0x" + "{:02x}".format((ord(msg[11]))) + "{:02x}".format((ord(msg[12])))
        print "PZD2 = " + str(((ord(msg[13])) << 8) + ord(msg[14])) + " Hz"
        print "PZD3 = " + str(((ord(msg[15])) << 8) + ord(msg[16])) + " oC"
        print "PZD4 = " + str((((ord(msg[17])) << 8) + ord(msg[18])) / 10.0) + " A"
        print "PZD6 = " + str((((ord(msg[21])) << 8) + ord(msg[22])) / 10.0) + " V\n"

    #    print "PKE = 0x" + "{:02x}".format((ord(msg[3]))) + "{:02x}".format((ord(msg[4])))
    #    print "IND = 0x" + "{:02x}".format((ord(msg[6])))
    #    print "PZD2 = 0x" + "{:02x}".format((ord(msg[13]))) + "{:02x}".format((ord(msg[14])))
    #    print "PZD3 = 0x" + "{:02x}".format((ord(msg[15]))) + "{:02x}".format((ord(msg[16])))
    #    print "PZD4 = 0x" + "{:02x}".format((ord(msg[17]))) + "{:02x}".format((ord(msg[18])))
    #    print "PZD6 = 0x" + "{:02x}".format((ord(msg[21]))) + "{:02x}".format((ord(msg[22]))) + "\n"

        print "BCC = 0x" + "{:02x}".format((ord(msg[23])))
        print "==================="

        for i in range(len(msg)):
            sys.stdout.write("{:02x}".format(ord(msg[i])) + " ")
        print "\n"

    else:
        print "Message received corrupted!"

    return msg
#---------------------------------------
# packing the task telegram
#---------------------------------------
'''
input parameters:
    - PWK: parameter ID value area
        length: 8 bytes
        PKW = PKE + reserved + IND + PWE
            PKE: 2 bytes
            reserved: 1 byte ("\x00")
            IND: 1 byte
            PWE: 4 bytes
    - PZD: process data area
        length: 12 bytes
        PZD = PZD1 + PZD2 + PZD3 + PZD4 + reserved + PZD6
            PZD1: 2 bytes
            PZD2: 2 bytes
            PZD3: 2 bytes
            PZD4: 2 bytes
            reserved: 2 bytes ("\x00\x00")
            PZD6: 2 bytes
output parameters:
    - message: task telegram
----------------------------
description:
    this function takes as input the fields PKW and PZD and merge them with the
    other fields (STX, LGE, ADR and BCC) to form the whole task telegram.
'''
def pack_message(PKW, PZD):
    byte = []
    LGE = chr(len(PKW + PZD) + 2)
    message = STX + LGE + ADR + PKW + PZD

    for i in range(len(message)):
        if (len(message[i]) > 1):
            for j in range(len(message[i])):
                byte += message[i][j]
        else:
            byte += message[i]

    BCC = chr(checksum(byte, (len(byte)-1)))
    byte.append(BCC)
    message = STX + LGE + ADR + PKW + PZD + BCC
    ##############
    msg = [STX, LGE, ADR, PKW, PZD, BCC]
    print msg

    print "==================="
    print "   Task telegram   "
    print "==================="
    print "STX = 0x" + "{:02x}".format(ord(STX))
    print "LGE = 0x" + "{:02x}".format(ord(LGE))
    print "ADR = 0x" + "{:02x}".format(ord(ADR)) + "\n"

    print "PKE = " + str((((ord(PKW[0]) & 0b111) << 8)) + (ord(PKW[1])))
    print "IND = " + str(ord(PKW[3]))
    print "PWE = " + str((ord(PKW[4]) << 24) + (ord(PKW[5]) << 16) + (ord(PKW[6]) << 8) + ord(PKW[7])) + "\n"

    print "PZD1 = 0x" + "{:02x}".format((ord(PZD[0]))) + "{:02x}".format((ord(PZD[1])))
    print "PZD2 = " + str(((ord(PZD[2])) << 8) + ord(PZD[3])) + " Hz"
    print "PZD3 = " + str(((ord(PZD[4])) << 8) + ord(PZD[5])) + " oC"
    print "PZD4 = " + str((((ord(PZD[6])) << 8) + ord(PZD[7])) / 10.0) + " A"
    print "PZD6 = " + str((((ord(PZD[10])) << 8) + ord(PZD[11])) / 10.0) + " V\n"

#    print "PKE = 0x" + "{:02x}".format(ord(PKW[0])) + "{:02x}".format(ord(PKW[1]))
#    print "IND = 0x" + "{:02x}".format(ord(PKW[3]))

#    print "PZD1 = 0x" + "{:02x}".format(ord(PZD[0])) + "{:02x}".format(ord(PZD[1]))
#    print "PZD2 = 0x" + "{:02x}".format(ord(PZD[2])) + "{:02x}".format(ord(PZD[3]))
#    print "PZD3 = 0x" + "{:02x}".format(ord(PZD[4])) + "{:02x}".format(ord(PZD[5]))
#    print "PZD4 = 0x" + "{:02x}".format(ord(PZD[6])) + "{:02x}".format(ord(PZD[7]))
#    print "PZD6 = 0x" + "{:02x}".format(ord(PZD[10])) + "{:02x}".format(ord(PZD[11])) + "\n"

    print "BCC = 0x" + "{:02x}".format(ord(BCC))

    ##############
    return message
#---------------------------------------
# reading a parameter
#---------------------------------------
'''
input parameters:
    - parameter: parameter number
output parameters:
    - response telegram
----------------------------
description:
    this function reads a parameter value and return the response telegram.
'''
def read_parameter(parameter):
    # PKW area
    AK = 0b0001
    PNU = parameter
    PKE = chr((AK << 4) + (0 << 3) + (PNU >> 8)) + chr(PNU & 0xFF)
    IND = "\x00"
    PWE = "\x00\x00\x00\x00"
    # joining the fields
    PKW = PKE + "\x00" + IND + PWE
    #-----------------------------------------------------
    # PZD area
    PZD1 = "\x00\x00"
    PZD2 = "\x00\x00"
    PZD3 = "\x00\x00"
    PZD4 = "\x00\x00"
    PZD6 = "\x00\x00"
    # joining the fields
    PZD = PZD1 + PZD2 + PZD3 + PZD4 + "\x00\x00" + PZD6
    #-----------------------------------------------------
    task_telegram = pack_message(PKW, PZD)
    recv_msg(task_telegram)
#==============================================================================
# Subroutines called from the main loop
#==============================================================================
def ta():
    print "test A"
    read_parameter(1)
def tb():
    print "test B"
    acp_recv_msg("#000IDN\r")
def tc():
    pass
def td():
    pass
def te():
    pass
def tf():
    pass
#==============================================================================
def ACP_OnOff(current_state):
    if (current_state == 0):
        print "Turning ACP15 pump OFF"
        acp_recv_msg("#000ACPOFF\r")
    if (current_state == 1):
        print "Turning ACP15 pump ON"
        acp_recv_msg("#000ACPON\r")
def ACP_SetSpeed(speed):
    # before setting a speed to the pump, we should change it to the standby speed
    acp_recv_msg("#000SBY\r")
    # now we are able to set the new desired speed
    if ((speed > 6000) or (speed < 2100)):
        print "error: minimum speed = 2100; maximum speed = 6000 rpm"
    else:
        message = "#000RPM" + str(speed/10*10) + "\r"
        print "Speed adjusted to " + str(speed/10*10) + " rpm (" + str(round((speed/10*10/60.0),2)) + " Hz)"
        print message
        acp_recv_msg(message)
        #000,ok

#==============================================================================
# Creating the UNIX SOCKET for EPICS support
#==============================================================================
server_address = "/tmp/socket_vbc"
try:
    # delete the file path
    os.unlink(server_address)
except OSError:
    if os.path.exists(server_address):
        raise

sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
sock.bind(server_address)
sock.listen(1)
print "unix socket running!"
#==============================================================================
# Main loop that pools the entries from .proto EPICS files
#==============================================================================
while(True):
    connection, client_address = sock.accept()
    try:
        while(True):
            data = connection.recv(512)
            if(data):
                #==============================================================
                # set GPIO pin direction
                if (data[0] == "\x00"):
                    # reserved
                    ta()
                elif (data[0] == "\x01"):
                    # switch relay 1
                    if (int(data[1]) == 0):
                        print "Switching Relay 1 OFF"
                        GPIO.output(relay1, GPIO.LOW)
                    if (int(data[1]) == 1):
                        print "Switching Relay 1 ON"
                        GPIO.output(relay1, GPIO.HIGH)
                elif (data[0] == "\x02"):
                    # switch relay 2
                    if (int(data[1]) == 0):
                        print "Switching Relay 2 OFF"
                        GPIO.output(relay2, GPIO.LOW)
                    if (int(data[1]) == 1):
                        print "Switching Relay 2 ON"
                        GPIO.output(relay2, GPIO.HIGH)

                elif (data[0] == "\x03"):
                    # switch relay 3
                    if (int(data[1]) == 0):
                        print "Switching Relay 3 OFF"
                        GPIO.output(relay3, GPIO.LOW)
                    if (int(data[1]) == 1):
                        print "Switching Relay 3 ON"
                        GPIO.output(relay3, GPIO.HIGH)

                elif (data[0] == "\x04"):
                    # switch relay 4
                    if (int(data[1]) == 0):
                        print "Switching Relay 4 OFF"
                        GPIO.output(relay4, GPIO.LOW)
                    if (int(data[1]) == 1):
                        print "Switching Relay 4 ON"
                        GPIO.output(relay4, GPIO.HIGH)

                elif (data[0] == "\x05"):
                    # read open VAT valve status
                    tf()
                elif (data[0] == "\x06"):
                    # read closed VAT valve status
                    tf()
                # commands from 0x07 to 0x0A reserved for future BBB implementations
                elif (data[0] == "\x0B"):
                    # turns ACP15 pump On/Off
                    ACP_OnOff(int(data[1]))
                elif ((data[0] == "\x0C")):
                    # the first character is a form feed ('\f' or 0x0C in ASCII)
                    # the last character is a carriage return ('\r' or 0x0D in ASCII)
                    speed = 0
                    for i in range(len(data)-2):
                        digit = int(data[i+1])
                        exponent = 10**(len(data)-i-3)
                        speed += digit * exponent
                    ACP_SetSpeed(speed)

                else:
                    break
    finally:
        connection.close()
