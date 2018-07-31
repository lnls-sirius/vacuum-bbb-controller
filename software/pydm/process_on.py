#!/usr/bin/python
from epics import caget, caput
import sys
#------------------------------------------------------------------------------
'''
this script do all the procedures to decrease the pressure of the system
it is divided in 5 stages, described as follow:
    -stage 1: open gate and pre-vacuum valves
    -stage 2: wait until gate valve actually closes
    -stage 3: turn ACP15 on
    -stage 4: wait pressure decrease to less than 0.05 Torr
    -stage 5: turn TURBOVAC on
'''
#------------------------------------------------------------------------------
# define the PREFIX that will be used (passed as a parameter)
VBC = sys.argv[1]
#------------------------------------------------------------------------------
# valve names definition
PRE_VACUUM_VALVE = VBC + ":BBB:Relay2"
GATE_VALVE = VBC + ":BBB:Relay4"
#------------------------------------------------------------------------------
# clear all status PVs
caput(VBC + ":ProcessOn:Status1", 1)
caput(VBC + ":ProcessOn:Status1", 2)
caput(VBC + ":ProcessOn:Status1", 3)
caput(VBC + ":ProcessOn:Status1", 4)
caput(VBC + ":ProcessOn:Status1", 5)
#==============================================================================
# Stage 1:
#==============================================================================
# open gate valve (VAT) and the pre-vacuum valve
caput(VBC + ":ProcessOn:Status1", 1)
caput(GATE_VALVE, 1)
caput(PRE_VACUUM_VALVE, 1)
#==============================================================================
# Stage 2:
#==============================================================================
# read gate valve (VAT) status to check if it is really closed
caput(VBC + ":ProcessOn:Status2", 1)
loop = True
while (loop):
    Lo = caget(VBC + ":BBB:ValveOpen")
    Lg = caget(VBC + ":BBB:ValveClosed")
    if (Lo & (not Lg)):
        loop = False
#==============================================================================
# Stage 3:
#==============================================================================
# turn ACP15 pump ON
caput(VBC + ":ProcessOn:Status3", 1)
caput(VBC + ":ACP:OnOff", 1)
#==============================================================================
# Stage 4:
#==============================================================================
# read the pressure and proceed when its value is under 5*(10^-2) Torr
caput(VBC + ":ProcessOn:Status4", 1)
while (caget(VBC + ":BBB:Torr") > (caget(VBC + ":SYSTEM:OnPressureBase") * 10 ** caget(VBC + ":SYSTEM:OnPressureExp")):
    pass
#==============================================================================
# Stage 5:
#==============================================================================
# turn TURBOVAC pump ON
caput(VBC + ":ProcessOn:Status5", 1)
caput(VBC + ":TURBOVAC:PZD1-SP.ZRVL", 1)
caput(VBC + ":TURBOVAC:PZD1-SP.TEVL", 1)
#==============================================================================
