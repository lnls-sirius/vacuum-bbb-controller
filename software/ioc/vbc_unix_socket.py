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
# creating PVs using PCASpy used to monitor the stage status in process scripts
#==============================================================================
# necessary modules
import threading
from pcaspy import Driver, SimpleServer
#-----------------------------------------------
PVs = {}
VBC = sys.argv[1]
#-----------------------------------------------
# status PVs for "turning the system ON" process
PVs["VBC" + VBC + ":ProcessOn:Status1"] = {"type" : "int"}
PVs["VBC" + VBC + ":ProcessOn:Status2"] = {"type" : "int"}
PVs["VBC" + VBC + ":ProcessOn:Status3"] = {"type" : "int"}
PVs["VBC" + VBC + ":ProcessOn:Status4"] = {"type" : "int"}
PVs["VBC" + VBC + ":ProcessOn:Status5"] = {"type" : "int"}
#-----------------------------------------------
# status PVs for "turning the system OFF" process (FV = full ventilation)
PVs["VBC" + VBC + ":ProcessOffFV:Status1"] = {"type" : "int"}
PVs["VBC" + VBC + ":ProcessOffFV:Status2"] = {"type" : "int"}
PVs["VBC" + VBC + ":ProcessOffFV:Status3"] = {"type" : "int"}
PVs["VBC" + VBC + ":ProcessOffFV:Status4"] = {"type" : "int"}
PVs["VBC" + VBC + ":ProcessOffFV:Status5"] = {"type" : "int"}
PVs["VBC" + VBC + ":ProcessOffFV:Status6"] = {"type" : "int"}
#-----------------------------------------------
# status PVs for "turning the system OFF" process (NV = no ventilation)
#PVs["VBC" + VBC + ":ProcessOffNV:Status1"] = {"type" : "int"}
#PVs["VBC" + VBC + ":ProcessOffNV:Status2"] = {"type" : "int"}
#PVs["VBC" + VBC + ":ProcessOffNV:Status3"] = {"type" : "int"}
#PVs["VBC" + VBC + ":ProcessOffNV:Status4"] = {"type" : "int"}
#PVs["VBC" + VBC + ":ProcessOffNV:Status5"] = {"type" : "int"}
#PVs["VBC" + VBC + ":ProcessOffNV:Status6"] = {"type" : "int"}
#-----------------------------------------------
# status PVs for "recovering from pressurized system" process (5*10^-2 ~ 1*10^-8)
PVs["VBC" + VBC + ":ProcessRecovery:Status1"] = {"type" : "int"}
PVs["VBC" + VBC + ":ProcessRecovery:Status2"] = {"type" : "int"}
PVs["VBC" + VBC + ":ProcessRecovery:Status3"] = {"type" : "int"}
PVs["VBC" + VBC + ":ProcessRecovery:Status4"] = {"type" : "int"}
PVs["VBC" + VBC + ":ProcessRecovery:Status5"] = {"type" : "int"}
#-----------------------------------------------
PVs["VBC" + VBC + ":ProcessOn:Bool"] = {"type" : "int"}
PVs["VBC" + VBC + ":ProcessOff:Bool"] = {"type" : "int"}
PVs["VBC" + VBC + ":ProcessRec:Bool"] = {"type" : "int"}
PVs["VBC" + VBC + ":Process:TriggerOn"] = {"type" : "int"}
PVs["VBC" + VBC + ":Process:TriggerPressurized"] = {"type" : "int"}
#-----------------------------------------------
# EPICS driver
class PSDriver(Driver):
    # class constructor
    def __init__(self):
        # call the superclass constructor
        Driver.__init__(self)

    # writing in PVs function
    def write(self, reason, value):
        self.setParam(reason, value)
        self.updatePVs()
        return (True)
#-----------------------------------------------
# start EPICS server
CAserver = SimpleServer()
CAserver.createPV("", PVs)
driver = PSDriver()
#-----------------------------------------------
# thread_1 is responsible for maintaining the process status PVss
def thread_1():
    while(True):
        CAserver.process(0.1)
#==============================================================================
# BBB functions support (for valves controls)
#==============================================================================
# defining pins used for valves controls
relay1 = "P9_12"
relay2 = "P9_24"
relay3 = "P8_16"
relay4 = "P8_18"
valve_open = "P9_16"
valve_closed = "P9_14"
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

    #print message_received
#==============================================================================
# TURBOVAC functions support
#==============================================================================
PNU = 134
IND = 2
PWE = 36
AK = 7
#-------------------
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

        #for i in range(len(msg)):
        #    sys.stdout.write("{:02x}".format(ord(msg[i])) + " ")
        #print "\n"

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
    # now we are able to set the new desired speed
    if ((speed > 6000) or (speed < 2100)):
        #print "error: minimum speed = 2100; maximum speed = 6000 rpm"
        pass
    else:
        # before setting a speed to the pump, we should change it to the standby speed
        acp_recv_msg("#000SBY\r")
        message = "#000RPM" + str(speed/10*10) + "\r"
        #print "Speed adjusted to " + str(speed/10*10) + " rpm (" + str(round((speed/10*10/60.0),2)) + " Hz)"
        #print message
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
    #msg = [STX, LGE, ADR, PKW, PZD, BCC]
    #print msg
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
#==============================================================================
# Initial configuration
#==============================================================================
# write value 600 in parameter 247 ==> set frequency at which the venting valve
# will open after a power failure
STX = 0x02
LGE = 0x16
ADR = 0x00
PNU = 247
AK = 0b0010
IND = 0
PWE = 600
PZD1_1 = PZD1_2 = PZD2 = 0
response = task_telegram(chr(STX), chr(LGE), chr(ADR), PNU, AK, IND, PWE, PZD1_1, PZD1_2, PZD2)
# unix socket is ready and the IOC can be started now
print "unix socket running!"
#==============================================================================
# Main loop that pools the entries from .proto EPICS files
#==============================================================================
# thread_2 is responsible for decoding/answering messages from/to IOC
def thread_2():
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
                    # switches relay
                    #--------------------------------------
                    elif (data[0] == "\x01"):
                        #---------------------------------------
                        # switch relay 1 (P8_18)
                        if (data[1] == "\x01"):
                            # switches OFF
                            if (data[2] == "0"):
                                GPIO.output(relay1, GPIO.LOW)
                            # switches ON
                            elif (data[2] == "1"):
                                GPIO.output(relay1, GPIO.HIGH)
                        #--------------------------------------
                        # switches relay 2 (P9_24)
                        elif (data[1] == "\x02"):
                            # switches OFF
                            if (data[2] == "0"):
                                GPIO.output(relay2, GPIO.LOW)
                            # switches ON
                            elif (data[2] == "1"):
                                GPIO.output(relay2, GPIO.HIGH)
                        #--------------------------------------
                        # switches relay 3 (P8_16)
                        elif (data[1] == "\x03"):
                            # switches OFF
                            if (data[2] == "0"):
                                GPIO.output(relay3, GPIO.LOW)
                            # switches ON
                            elif (data[2] == "1"):
                                GPIO.output(relay3, GPIO.HIGH)
                        #--------------------------------------
                        # switches relay 4 (P9_12)
                        elif (data[1] == "\x04"):
                            # switches OFF
                            if (data[2] == "0"):
                                GPIO.output(relay4, GPIO.LOW)
                            # switches ON
                            elif (data[2] == "1"):
                                GPIO.output(relay4, GPIO.HIGH)
                    #---------------------------------------
                    # reads relays status
                    #--------------------------------------
                    elif (data[0] == "\x02"):
                        # read relay 1 status
                        if (data[1] == "\x01"):
                            connection.sendall(str(GPIO.input(relay1)))
                        # read relay 2 status
                        elif (data[1] == "\x02"):
                            connection.sendall(str(GPIO.input(relay2)))
                        # read relay 3 status
                        elif (data[1] == "\x03"):
                            connection.sendall(str(GPIO.input(relay3)))
                        # read relay 4 status
                        elif (data[1] == "\x04"):
                            connection.sendall(str(GPIO.input(relay4)))
                    #---------------------------------------
                    # read open VAT valve status (P8_7)
                    elif (data[0] == "\x05"):
                        vopen = str(GPIO.input(valve_open))
                        connection.sendall(vopen)
                    #---------------------------------------
                    # read closed VAT valve status (P8_9)
                    elif (data[0] == "\x06"):
                        vclosed = str(GPIO.input(valve_closed))
                        connection.sendall(vclosed)
                    #---------------------------------------
                    elif (data[0] == "\x07"):
                        ADC_code = int(ADC.read_raw(analog_in))
                        voltage_ADC = ADC.read(analog_in) * 1.8
                        voltage_equipment = voltage_ADC * 6
                        #-----------------------------------------------------------
                        # reading vacuum pressure in Torr
                        pressure_torr = 10 ** ((2 * voltage_equipment) - 11)
                        # converting it into base and exponent
                        torr_base = pressure_torr
                        torr_exp = 0
                        if (torr_base >= 1):
                            while ((torr_base / 10) >= 1):
                                torr_exp += 1
                                torr_base /= 10
                        else:
                            while ((torr_base) * 10 < 10):
                                torr_exp -= 1
                                torr_base *= 10
                        #-----------------------------------------------------------
                        # reading vacuum pressure in mbar
                        mbar = 1.33 * 10 ** ((2 * voltage_equipment) - 11)
                        # converting it into base and exponent
                        mbar_base = mbar
                        mbar_exp = 0
                        if (mbar_base >= 1):
                            while ((mbar_base / 10) >= 1):
                                mbar_exp += 1
                                mbar_base /= 10
                        else:
                            while ((mbar_base) * 10 < 10):
                                mbar_exp -= 1
                                mbar_base *= 10
                        #-----------------------------------------------------------
                        # reading vacuum pressure in Pascal
                        pressure_pascal = 100 * mbar
                        # converting it into base and exponent
                        #pascal_base = mbar_base
                        #pascal_exp = mbar_exp + 2
                        #-----------------------------------------------------------
                        # reading differential pressure
                        #pressure_torr = 250 * (voltage_equipment - 4)
                        #pressure_mbar = 1.33 * 250 * (voltage_equipment - 4)
                        #pressure_pascal = 133 * 250 * (voltage_equipment - 4)
                        #-----------------------------------------------------------
                        connection.sendall(
                            str(ADC_code) + ";" +
                            str(voltage_ADC) + ";" +
                            str(voltage_equipment) + ";" +
                            str(pressure_torr) + ";" +
                            str(torr_base) + ";" +
                            str(torr_exp) + ";" +
                            str(mbar) + ";" +
                            str(mbar_base) + ";" +
                            str(mbar_exp) + ";" +
                            str(pressure_pascal)
                        )
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
                        # decoding PNU field
                        #---------------------------------------
                        # the OFFSET represents the number of characters sent before
                        # the PKW data:
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
                        # decoding and calculating the two bytes of PZD1
                        #---------------------------------------
                        OFFSET += digits + 1
                        for i in range(8):
                            PZD1_1 += (int(data[OFFSET + i]) << (7-i))
                            PZD1_2 += (int(data[OFFSET + 8 + i]) << (7-i))
                            # check if venting valve is set
                            if (data[OFFSET] == "1"):
                                PNU = 134
                                AK = 7
                                IND = 2
                                PWE = 18
                                PZD1_1 = 0x84
                                PZD1_2 = 0x00
                        #---------------------------------------
                        # Decoding PZD2 field
                        #---------------------------------------
                        # set the new OFFSET value for the PZD2 field
                        # the "+1" refers to the comma separator character
                        #   16 characters for status bits
                        OFFSET += 16
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
                                str(response[0]) + ";" +    # STX
                                str(response[1]) + ";" +    # LGE
                                str(response[2]) + ";" +    # ADR

                                str(response[3]) + ";" +    # PNU
                                str(response[4]) + ";" +    # AK
                                str(response[5]) + ";" +    # IND
                                str(response[6]) + ";" +    # PWE

                                str(response[7]) + ";" +    # PZD1_1
                                str(response[8]) + ";" +    # PZD1_2
                                str(response[9]) + ";" +    # PZD2
                                str(response[10]) + ";" +   # PZD3
                                str(response[11]) + ";" +   # PZD4
                                str(response[12])           # PZD6
                            )
                        else:
                            pass
                    #---------------------------------------
                    # open/close TURBOVAC venting valve (X1)
                    #---------------------------------------
                    elif ((data[0] == "\x11")):
                        # open X203 valve (TURBOVAC venting valve)
                        if (data[1] == "1"):
                            '''
                            this must be done because we need to change the value of parameter 134
                            from "36" to "18" in order to control the venting valve independently.
                            from the manual:
                                18: Fieldbus controlled (enabled via 24 V in X1 input)
                                36: Venting valves ("frequent dependent")
                            '''
                            STX = 0x02
                            LGE = 0x16
                            ADR = 0x00
                            PNU = 134
                            AK = 7
                            IND = 2
                            PWE = 18
                            PZD1_1 = 0x84
                            PZD1_2 = 0x00
                            PZD2 = 0
                            response = task_telegram(chr(STX), chr(LGE), chr(ADR), PNU, AK, IND, PWE, PZD1_1, PZD1_2, PZD2)
                        #---------------------------------------
                        # close X203 valve (TURBOVAC venting valve)
                        elif (data[1] == "0"):
                            '''
                            this must be done because we need to change the value of parameter 134
                            from "36" to "18" in order to control the venting valve independently.
                            from the manual:
                                18: Fieldbus controlled (enabled via 24 V in X1 input)
                                36: Venting valves ("frequent dependent")
                            '''
                            STX = 0x02
                            LGE = 0x16
                            ADR = 0x00
                            PNU = 134
                            AK = 7
                            IND = 2
                            PWE = 36
                            PZD1_1 = 0x04
                            PZD1_2 = 0x00
                            PZD2 = 0
                            response = task_telegram(chr(STX), chr(LGE), chr(ADR), PNU, AK, IND, PWE, PZD1_1, PZD1_2, PZD2)
                    #---------------------------------------
                    # commands from 0x12 to 0x14 reserved
                    # for future TURBOVAC implementations
                    #---------------------------------------
                    elif (data[0] == "\xde"):
                        pass
                    #---------------------------------------

                    else:
                        break

        finally:
            connection.close()
#==============================================================================
# starting both the threads
#==============================================================================
t1 = threading.Thread(target=thread_1, args=[])
t2 = threading.Thread(target=thread_2, args=[])
t1.start()
t2.start()
