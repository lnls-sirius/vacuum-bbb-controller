#!/usr/bin/python
# -*- coding: utf-8 -*-
import socket
import sys
import os
import serial
import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.ADC as ADC
#------------------------------------------------------------------------------
PORT = "/dev/ttyUSB0"
#------------------------------------------------------------------------------
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
#==============================================================================
# BBB ADC support (for analog reading)
#==============================================================================
# defining pin used in analog reading (pressure)
analog_in = "P9_36" # AIN5
ADC.setup()
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
    #print "con1 = 9600"
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
    #print "con2 = 19200"
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
    #print "==================="
    #print " Response telegram "
    #print "==================="
    if (len(msg) == 24):

        for i in range(len(msg)):
            sys.stdout.write("{:02x}".format(ord(msg[i])) + " ")
        print "\n"

        #return msg
        STX = ord(msg[0])
        LGE = ord(msg[1])
        ADR = ord(msg[2])
        #---------------------------------------------------
        PKE = ((ord(msg[3]) & 0b111) << 8) + (ord(msg[4]))
        AK = (ord(msg[3]) >> 4)
        PNU = (PKE & 0x07FF)
        # res = ord(msg[5])
        IND = ord(msg[6])
        PWE = (ord(msg[7]) << 24) + (ord(msg[8]) << 16) + (ord(msg[9]) << 8) + ord(msg[10])
        #---------------------------------------------------
        PZD1_1 = ord(msg[11])
        PZD1_2 = ord(msg[12])
        PZD2 = (ord(msg[13]) << 8) + ord(msg[14])
        PZD3 = ((ord(msg[15])) << 8) + ord(msg[16])
        PZD4 = (((ord(msg[17])) << 8) + ord(msg[18])) / 10.0
        # res = (ord(msg[19]) << 8) + ord(msg[20])
        PZD6 = (((ord(msg[21])) << 8) + ord(msg[22])) / 10.0

        return [STX, LGE, ADR, PNU, AK, IND, PWE, PZD1_1, PZD1_2, PZD2, PZD3, PZD4, PZD6]

    else:
        #print "Message received corrupted!"
        return 0
#==============================================================================
# Subroutines called from the main loop
#==============================================================================
#---------------------------------------
# turns ACP15 on/off
#---------------------------------------
def ACP_OnOff(current_state):
    if (current_state == 0):
        #print "Turning ACP15 pump OFF"
        acp_recv_msg("#000ACPOFF\r")
    if (current_state == 1):
        #print "Turning ACP15 pump ON"
        acp_recv_msg("#000ACPON\r")
#---------------------------------------
# set ACP15 speed
#---------------------------------------
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
#---------------------------------------
# send a task telegram to TURBOVAC
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
def task_telegram(STX, LGE, ADR, PNU, AK, IND, PWE, PZD1_1, PZD1_2, PZD2):
    # PKW area
    PKE = chr((AK << 4) + (0 << 3) + ((PNU >> 8) & 0x700)) + chr(PNU & 0xFF)
    IND = chr(IND)
    PWE = chr((PWE & 0xFF000000) >> 24) + chr((PWE & 0x00FF0000) >> 16) + chr((PWE & 0x0000FF00) >> 8) + chr(PWE & 0x000000FF)
    # joining the fields
    PKW = PKE + "\x00" + IND + PWE
    #-----------------------------------------------------
    # PZD area
    PZD1 = chr(PZD1_1) + chr(PZD1_2)
    PZD2_1 = chr((PZD2 & 0xFF00) >> 8)
    PZD2_2 = chr(PZD2 & 0x00FF)
    PZD2 = PZD2_1 + PZD2_2
    PZD3 = "\x00\x00"
    PZD4 = "\x00\x00"
    PZD6 = "\x00\x00"
    # joining the fields
    PZD = PZD1 + PZD2 + PZD3 + PZD4 + "\x00\x00" + PZD6
    #-----------------------------------------------------
    byte = []
    #LGE = chr(len(PKW + PZD) + 2)
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
    ##############

    response = turbovac_recv_msg(message)
    return response
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
                # reserved
                if (data[0] == "\x00"):
                    pass
                #---------------------------------------
                # switch relay 1 (P9_23)
                elif (data[0] == "\x01"):
                    if (int(data[1]) == 0):
                        #print "Switching Relay 1 OFF"
                        GPIO.output(relay1, GPIO.LOW)
                    if (int(data[1]) == 1):
                        #print "Switching Relay 1 ON"
                        GPIO.output(relay1, GPIO.HIGH)
                #---------------------------------------
                # switch relay 2 (P9_21)
                elif (data[0] == "\x02"):
                    if (int(data[1]) == 0):
                        #print "Switching Relay 2 OFF"
                        GPIO.output(relay2, GPIO.LOW)
                    if (int(data[1]) == 1):
                        #print "Switching Relay 2 ON"
                        GPIO.output(relay2, GPIO.HIGH)
                #---------------------------------------
                # switch relay 3 (P9_24)
                elif (data[0] == "\x03"):
                    if (int(data[1]) == 0):
                        #print "Switching Relay 3 OFF"
                        GPIO.output(relay3, GPIO.LOW)
                    if (int(data[1]) == 1):
                        #print "Switching Relay 3 ON"
                        GPIO.output(relay3, GPIO.HIGH)
                #---------------------------------------
                # switch relay 4 (P9_12)
                elif (data[0] == "\x04"):
                    if (int(data[1]) == 0):
                        #print "Switching Relay 4 OFF"
                        GPIO.output(relay4, GPIO.LOW)
                    if (int(data[1]) == 1):
                        #print "Switching Relay 4 ON"
                        GPIO.output(relay4, GPIO.HIGH)
                #---------------------------------------
                # read open VAT valve status (P8_7)
                elif (data[0] == "\x05"):
                    connection.sendall(str(GPIO.input(valve_open)))
                #---------------------------------------
                # read closed VAT valve status (P8_9)
                elif (data[0] == "\x06"):
                    connection.sendall(str(GPIO.input(valve_closed)))
                #---------------------------------------
                # read analog in corresponding to the pressure (P9_36)
                elif (data[0] == "\x07"):
                    voltage = ADC.read(analog_in)
                    #
                    # convert voltage to pressure
                    #
                    pressure = voltage * 1.0
                    connection.sendall("voltage = "+ str(voltage) + ", pressure = " + str(pressure))
                #---------------------------------------
                # commands from 0x08 to 0x0A reserved
                # for future BBB implementations
                #---------------------------------------
                # turns ACP15 pump On/Off
                elif (data[0] == "\x0B"):
                    ACP_OnOff(int(data[1]))
                #---------------------------------------
                # set ACP15 pump speed in rpm
                elif ((data[0] == "\x0C")):
                    # the first character is a form feed ('\f' or 0x0C in ASCII)
                    # the last character is a carriage return ('\r' or 0x0D in ASCII)
                    speed = 0
                    for i in range(len(data)-2):
                        digit = int(data[i+1])
                        exponent = 10**(len(data)-i-3)
                        speed += digit * exponent
                    ACP_SetSpeed(speed)
                #---------------------------------------
                # set ACP15 pump speed in Hz
                elif ((data[0] == "\x0D")):
                    # the first character is a form feed ('\f' or 0x0C in ASCII)
                    # the last character is a carriage return ('\r' or 0x0D in ASCII)
                    speed = 0
                    for i in range(len(data)-2):
                        digit = int(data[i+1])
                        exponent = 10**(len(data)-i-3)
                        speed += digit * exponent
                    speed *= 60
                    ACP_SetSpeed(speed)
                #---------------------------------------
                # commands from 0x0E to 0x0F reserved
                # for future ACP15 implementations
                #---------------------------------------
                # send a task telegram to TURBOVAC
                elif ((data[0] == "\x10")):
                    #---------------------------------------
                    # fields initialized
                    #---------------------------------------
                    STX = 0
                    LGE = 0
                    ADR = 0
                    #----------
                    IND = 0
                    PNU = 0
                    PWE = 0
                    #----------
                    PZD1_1 = 0
                    PZD1_2 = 0
                    PZD2 = 0
                    #---------------------------------------
                    # decoding the header (STX)
                    #---------------------------------------
                    # OFFSET is one because of the first character used in the protocol: 0x10
                    OFFSET = 1
                    i = OFFSET
                    digits = 0
                    # count number of digits of the field
                    while (data[i] != ","):
                        digits += 1
                        i += 1
                    # now that we now the number of digits, we can decode the field
                    for j in range(digits):
                        STX += (int(data[OFFSET + j]) * (10 ** (digits - j - 1)))
                    #---------------------------------------
                    # decoding the header (LGE)
                    #---------------------------------------
                    # set the new OFFSET value for the LGE field
                    # the "+1" refers to the comma separator character
                    OFFSET += digits + 1
                    i = OFFSET
                    digits = 0
                    # count number of digits of the field
                    while (data[i] != ","):
                        digits += 1
                        i += 1
                    # now that we now the number of digits, we can decode the field
                    for j in range(digits):
                        LGE += (int(data[OFFSET + j]) * (10 ** (digits - j - 1)))
                    #---------------------------------------
                    # decoding the header (ADR)
                    #---------------------------------------
                    # set the new OFFSET value for the ADR field
                    # the "+1" refers to the comma separator character
                    OFFSET += digits + 1
                    i = OFFSET
                    digits = 0
                    # count number of digits of the field
                    while (data[i] != ","):
                        digits += 1
                        i += 1
                    # now that we now the number of digits, we can decode the field
                    for j in range(digits):
                        ADR += (int(data[OFFSET + j]) * (10 ** (digits - j - 1)))
                    #---------------------------------------
                    # decoding and calculating the two bytes of PZD1
                    #---------------------------------------
                    OFFSET += digits + 1
                    for i in range(8):
                        PZD1_1 += (int(data[OFFSET + i]) << (7-i))
                        PZD1_2 += (int(data[OFFSET + 8 + i]) << (7-i))
                    #---------------------------------------
                    # decoding PNU field
                    #---------------------------------------
                    # the OFFSET represents the number of characters sent before
                    # the PKW data:
                    #    1 character for the protocol: 0x10
                    #   16 characters for status bits
                    OFFSET += 16
                    i = OFFSET
                    digits = 0
                    # count number of digits of the field
                    while (data[i] != ","):
                        digits += 1
                        i += 1
                    # now that we now the number of digits, we can decode the field
                    for j in range(digits):
                        PNU += (int(data[OFFSET + j]) * (10 ** (digits - j - 1)))
                    #---------------------------------------
                    # decoding AK field
                    #---------------------------------------
                    # set the new OFFSET value for the AK field
                    # the "+1" refers to the comma separator character
                    OFFSET += digits + 1
                    AK = int(data[OFFSET])
                    #---------------------------------------
                    # decoding IND field
                    #---------------------------------------
                    # set the new OFFSET value for the IND field
                    # the "+2" refers to the comma separator character and next character
                    OFFSET += 2
                    i = OFFSET
                    digits = 0
                    # count number of digits of the field
                    while (data[i] != ","):
                        digits += 1
                        i += 1
                    # now that we now the number of digits, we can decode the field
                    for j in range(digits):
                        IND += (int(data[OFFSET + j]) * (10 ** (digits - j - 1)))
                    #---------------------------------------
                    # decoding PWE field
                    #---------------------------------------
                    # set the new OFFSET value for the PWE field
                    # the "+1" refers to the comma separator character
                    OFFSET += digits + 1
                    i = OFFSET
                    digits = 0
                    # count number of digits of the field
                    while (data[i] != ","):
                        digits += 1
                        i += 1
                    # now that we now the number of digits, we can decode the field
                    for j in range(digits):
                        PWE += (int(data[OFFSET + j]) * (10 ** (digits - j - 1)))
                    #---------------------------------------
                    # Decoding PZD2 field
                    #---------------------------------------
                    # set the new OFFSET value for the PZD2 field
                    # the "+1" refers to the comma separator character
                    OFFSET += digits + 1
                    digits = (len(data) - OFFSET)
                    for j in range(digits):
                        PZD2 += (int(data[OFFSET + j]) * (10 ** (digits - j - 1)))
                    #---------------------------------------
                    response = task_telegram(chr(STX), chr(LGE), chr(ADR), PNU, AK, IND, PWE, PZD1_1, PZD1_2, PZD2)
                    if (response == 0):
                        # message corrupted!
                        pass
                    elif (len(response) == 13):
                        connection.sendall(
                            #-------------------------------
                              "STX=" + str(response[0]) +
                            ", LGE=" + str(response[1]) +
                            ", ADR=" + str(response[2]) +
                            #-------------------------------
                            ", PNU=" + str(response[3]) +
                            ", AK=" + str(response[4]) +
                            ", IND=" + str(response[5]) +
                            ", PWE=" + str(response[6]) +
                            #-------------------------------
                            ", PZD1_1=" + str(response[7]) +
                            ", PZD1_2=" + str(response[8]) +
                            ", PZD2=" + str(response[9]) +
                            ", PZD3=" + str(response[10]) +
                            ", PZD4=" + str(response[11]) +
                            ", PZD6=" + str(response[12])
                            #-------------------------------
                        )
                    else:
                        pass
                #---------------------------------------
                # commands from 0x11 to 0x14 reserved
                # for future TURBOVAC implementations
                #---------------------------------------
                else:
                    break
    finally:
        connection.close()
