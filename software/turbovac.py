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
'''
===============================================================================
 Byte |    Abbreviation     | Description
------|---------------------|--------------------------------------------------
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
 23   |        BCC          | Checksum
===============================================================================

Obs.1: before the start byte (STX) there should be a delay of at least 1.15 ms

'''
#==============================================================================
STX = "\x02"
ADR = "\x00"
# mirror telegram
#ADR = "\x40"
#==============================================================================
def checksum(byte, index):
    if (index == 0):
        return ord(byte[0])
    else:
        return (checksum(byte, (index-1)) ^ ord(byte[index]))
#==============================================================================
def receive_message():
    msg = ""
    next_byte = connection.read(1)
    # after read the first byte, set the timeout to 100ms
    connection.timeout = 0.1
    # keep reading bytes until timeout exceed
    while (next_byte != ""):
	    msg += next_byte
	    next_byte = connection.read(1)

    print "==================="
    print " Response telegram "
#    print "==================="
    if (len(msg) == 24):
#        print "STX = 0x" + "{:02x}".format((ord(msg[0])))
#        print "LGE = 0x" + "{:02x}".format((ord(msg[1])))
#        print "ADR = 0x" + "{:02x}".format((ord(msg[2]))) + "\n"

        print "PKE = " + str((((ord(msg[3]) & 0b111) << 8)) + (ord(msg[4])))
        print "IND = " + str((ord(msg[6])))
        print "PWE = " + str((ord(msg[7]) << 24) + (ord(msg[8]) << 16) + (ord(msg[9]) << 8) + ord(msg[10])) + "\n"

        print "PZD1 = 0x" + "{:02x}".format((ord(msg[11]))) + "{:02x}".format((ord(msg[12])))
        print "PZD2 = " + str(((ord(msg[13])) << 8) + ord(msg[14])) + " Hz"
#        print "PZD3 = " + str(((ord(msg[15])) << 8) + ord(msg[16])) + " oC"
#        print "PZD4 = " + str((((ord(msg[17])) << 8) + ord(msg[18])) / 10.0) + " A"
#        print "PZD6 = " + str((((ord(msg[21])) << 8) + ord(msg[22])) / 10.0) + " V\n"

    #    print "PKE = 0x" + "{:02x}".format((ord(msg[3]))) + "{:02x}".format((ord(msg[4])))
    #    print "IND = 0x" + "{:02x}".format((ord(msg[6])))
    #    print "PZD2 = 0x" + "{:02x}".format((ord(msg[13]))) + "{:02x}".format((ord(msg[14])))
    #    print "PZD3 = 0x" + "{:02x}".format((ord(msg[15]))) + "{:02x}".format((ord(msg[16])))
    #    print "PZD4 = 0x" + "{:02x}".format((ord(msg[17]))) + "{:02x}".format((ord(msg[18])))
    #    print "PZD6 = 0x" + "{:02x}".format((ord(msg[21]))) + "{:02x}".format((ord(msg[22]))) + "\n"

#        print "BCC = 0x" + "{:02x}".format((ord(msg[23])))
#        print "==================="

        for i in range(len(msg)):
            sys.stdout.write("{:02x}".format(ord(msg[i])) + " ")
        print "\n"

    else:
        print "Message received corrupted!"

    return msg
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

    for i in range(len(msg)):
        for j in range(len(msg[i])):
            sys.stdout.write("{:02x}".format(ord(msg[i][j])) + " ")
    sys.stdout.write("\n")
#    print "==================="
#    print "   Task telegram   "
#    print "==================="
#    print "STX = 0x" + "{:02x}".format(ord(STX))
#    print "LGE = 0x" + "{:02x}".format(ord(LGE))
#    print "ADR = 0x" + "{:02x}".format(ord(ADR)) + "\n"

#    print "PKE = " + str((((ord(PKW[0]) & 0b111) << 8)) + (ord(PKW[1])))
#    print "IND = " + str(ord(PKW[3]))
#    print "PWE = " + str((ord(PKW[4]) << 24) + (ord(PKW[5]) << 16) + (ord(PKW[6]) << 8) + ord(PKW[7])) + "\n"

#    print "PZD1 = 0x" + "{:02x}".format((ord(PZD[0]))) + "{:02x}".format((ord(PZD[1])))
#    print "PZD2 = " + str(((ord(PZD[2])) << 8) + ord(PZD[3])) + " Hz"
#    print "PZD3 = " + str(((ord(PZD[4])) << 8) + ord(PZD[5])) + " oC"
#    print "PZD4 = " + str((((ord(PZD[6])) << 8) + ord(PZD[7])) / 10.0) + " A"
#    print "PZD6 = " + str((((ord(PZD[10])) << 8) + ord(PZD[11])) / 10.0) + " V\n"

#    print "PKE = 0x" + "{:02x}".format(ord(PKW[0])) + "{:02x}".format(ord(PKW[1]))
#    print "IND = 0x" + "{:02x}".format(ord(PKW[3]))

#    print "PZD1 = 0x" + "{:02x}".format(ord(PZD[0])) + "{:02x}".format(ord(PZD[1]))
#    print "PZD2 = 0x" + "{:02x}".format(ord(PZD[2])) + "{:02x}".format(ord(PZD[3]))
#    print "PZD3 = 0x" + "{:02x}".format(ord(PZD[4])) + "{:02x}".format(ord(PZD[5]))
#    print "PZD4 = 0x" + "{:02x}".format(ord(PZD[6])) + "{:02x}".format(ord(PZD[7]))
#    print "PZD6 = 0x" + "{:02x}".format(ord(PZD[10])) + "{:02x}".format(ord(PZD[11])) + "\n"

#    print "BCC = 0x" + "{:02x}".format(ord(BCC))
    ##############
    return message
#==============================================================================
# read parameter 1: ID
def id():
    read_parameter(1)
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
def r():
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
    PZD1 = "\x04\x80"
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
    PZD1 = "\x04\x00"
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
def read_parameter(parameter, index = 0):
    # PKW area
    AK = 0b0001
    PNU = parameter
    PKE = chr((AK << 4) + (0 << 3) + (PNU >> 8)) + chr(PNU & 0xFF)
    IND = chr(index)
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
def write_parameter(parameter, value, index = 0):
    # PKW area
    AK = 0b0010
    PNU = parameter
    PKE = chr((AK << 4) + (0 << 3) + (PNU >> 8)) + chr(PNU & 0xFF)
    IND = chr(index)
    PWE = (chr((value & 0xF000) >> 24) + chr((value & 0x0F00) >> 16) + chr((value & 0x00F0) >> 8) + chr(value & 0x000F))
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
def PZD(byte1, byte2):
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
    PZD1 = chr(byte1) + chr(byte2)
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
def test(parameter, index = 0):
    read_parameter(parameter, index)
    start_pump()
    while(1):
        read_parameter(parameter, index)

    # parameters
    # 171: 5 --> temperature
    # 174: 5 -->
    # 179: 3 --> temperature 3 exceeded

    # 28 (upper limit)
    #   0: 1199
    #   1: 5
    #   2: 5
    # 647 (lower limit)
    #   0: 5
    #   1: 5
    #   2: 5

    # 678
    # 679

    # 134
    #   0: 28
    #   1: 5
    #   2: 5
