#!/usr/bin/python
import serial
import sys
connection = serial.Serial(
    port='/dev/ttyUSB0',
    baudrate=19200,
    parity=serial.PARITY_EVEN,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

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
    return message_received
'''
===============================================================================
 Byte |    Abbreviation     | Description
------|---------------------|----------------------
  0   |         STX         | Start bit
  1   |         LGE         | Length of payload
  2   |         ADR         | Address
 3-4  |         PKE         | Parameter number and type of access
  5   |         ---         | Reserved
  6   |         IND         | Parameter index
 7-10 |         PWE         | Parameter value
11-12 |    PZD1,STW,ZSW     | Status and control bits
13-14 |  PZD2,HSW,HIW,(MSW) | Stator frequency (= P3)
15-16 |  PZD3,HSW,HIW,(LSW) | Temperature (= P11)
17-18 |        PZD4         | Motor current (= P5)
19-20 |        ---          | Reserved
21-22 |        PZD6         | Intermediate circuit voltage (= P4)
  23  |        BCC          | Checksum
===============================================================================

Obs.1: before the start byte (STX) there should be a delay of at least 1.15 ms

'''

STX = "\x02"
ADR = "\x00"

#==============================================================================
def checksum(byte, index):
    if (index == 0):
        return ord(byte[0])
    else:
        return (checksum(byte, (index-1)) ^ ord(byte[index]))
#==============================================================================
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
    ##############
    return message
#==============================================================================
# read parameter 1: ID
def id():
    # PKW area
    AK = 0b0001
    PNU = 1
    PKE = chr((AK << 4) + (0 << 3) + ((PNU >> 8) & 0x300)) + chr(PNU & 0xFF)
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
    command = pack_message(PKW, PZD)
    connection.write(command)
    receive_message()

#starting the pump
def start_pump():
    # PKW area
    AK = 0b0000
    PNU = 0
    PKE = chr((AK << 4) + (0 << 3) + ((PNU >> 8) & 0x300)) + chr(PNU & 0xFF)
    IND = "\x00"
    PWE = "\x00\x00\x00\x00"
    # joining the fields
    PKW = PKE + "\x00" + IND + PWE
    #-----------------------------------------------------
    # PZD area
    PZD1 = "\x04\x01"
    PZD2 = "\x00\x00"
    PZD3 = "\x00\x00"
    PZD4 = "\x00\x00"
    PZD6 = "\x00\x00"
    # joining the fields
    PZD = PZD1 + PZD2 + PZD3 + PZD4 + "\x00\x00" + PZD6
    #-----------------------------------------------------
    command = pack_message(PKW, PZD)
    connection.write(command)
    receive_message()

#stopping the pump
def stop_pump():
    # PKW area
    AK = 0b0000
    PNU = 0
    PKE = chr((AK << 4) + (0 << 3) + ((PNU >> 8) & 0x300)) + chr(PNU & 0xFF)
    IND = "\x00"
    PWE = "\x00\x00\x00\x00"
    # joining the fields
    PKW = PKE + "\x00" + IND + PWE
    #-----------------------------------------------------
    # PZD area
    PZD1 = "\x40\x00"
    PZD2 = "\x00\x00"
    PZD3 = "\x00\x00"
    PZD4 = "\x00\x00"
    PZD6 = "\x00\x00"
    # joining the fields
    PZD = PZD1 + PZD2 + PZD3 + PZD4 + "\x00\x00" + PZD6
    #-----------------------------------------------------
    command = pack_message(PKW, PZD)
    connection.write(command)
    receive_message()

# setpoint active
def setpoint():
    # PKW area
    AK = 0b0000
    PNU = 0
    PKE = chr((AK << 4) + (0 << 3) + ((PNU >> 8) & 0x300)) + chr(PNU & 0xFF)
    IND = "\x00"
    PWE = "\x00\x00\x00\x00"
    # joining the fields
    PKW = PKE + "\x00" + IND + PWE
    #-----------------------------------------------------
    # PZD area
    PZD1 = "\x04\x41"
    PZD2 = "\x02\xBC"
    PZD3 = "\x00\x00"
    PZD4 = "\x00\x00"
    PZD6 = "\x00\x00"
    # joining the fields
    PZD = PZD1 + PZD2 + PZD3 + PZD4 + "\x00\x00" + PZD6
    #-----------------------------------------------------
    command = pack_message(PKW, PZD)
    connection.write(command)
    receive_message()

# read parameter 150 (0x96)
def read_parameter():
    # PKW area
    AK = 0b0001
    PNU = 150
    PKE = chr((AK << 4) + (0 << 3) + ((PNU >> 8) & 0x300)) + chr(PNU & 0xFF)
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
    command = pack_message(PKW, PZD)
    connection.write(command)
    receive_message()

# write in parameter 150 (0x96)
def write_parameter():
    # PKW area
    AK = 0b0010
    PNU = 150
    PKE = chr((AK << 4) + (0 << 3) + ((PNU >> 8) & 0x300)) + chr(PNU & 0xFF)
    IND = "\x00"
    PWE = "\x00\x00\x01\xF4"
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
    command = pack_message(PKW, PZD)
    connection.write(command)
    receive_message()

# write in parameter 150 (0x96)
def standby():
    # PKW area
    AK = 0b0000
    PNU = 0
    PKE = chr((AK << 4) + (0 << 3) + ((PNU >> 8) & 0x300)) + chr(PNU & 0xFF)
    IND = "\x00"
    PWE = "\x00\x00\x00\x00"
    # joining the fields
    PKW = PKE + "\x00" + IND + PWE
    #-----------------------------------------------------
    # PZD area
    PZD1 = "\x50\x01"
    PZD2 = "\x00\x00"
    PZD3 = "\x00\x00"
    PZD4 = "\x00\x00"
    PZD6 = "\x00\x00"
    # joining the fields
    PZD = PZD1 + PZD2 + PZD3 + PZD4 + "\x00\x00" + PZD6
    #-----------------------------------------------------
    command = pack_message(PKW, PZD)
    connection.write(command)
    receive_message()
