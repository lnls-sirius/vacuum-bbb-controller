#!/usr/bin/python
from epics import caget, caput
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
# valve names definition
PRE-VACUUM_VALVE = "VBC:BBB:Relay2"
GATE_VALVE = "VBC:BBB:Relay4"
#==============================================================================
# Stage 1:
#==============================================================================
# open gate valve (VAT) and the pre-vacuum valve
caput(GATE_VALVE, 1)
caput(PRE-VACUUM_VALVE, 1)
#==============================================================================
# Stage 2:
#==============================================================================
# read gate valve (VAT) status to check if it is really closed
loop = True
while (loop):
    Lo = caget("VBC:BBB:ValveOpen")
    Lg = caget("VBC:BBB:ValveClosed")
    if (Lo & (not Lg)):
        loop = False
#==============================================================================
# Stage 3:
#==============================================================================
# turn ACP15 pump ON
caput("VBC:ACP15:OnOff", 1)
#==============================================================================
# Stage 4:
#==============================================================================
# read the pressure and proceed when its value is under 5*(10^-2) Torr
while (caget("VBC:BBB:Torr") > 0.05):
    pass
#==============================================================================
# Stage 5:
#==============================================================================
# turn TURBOVAC pump ON
caput("VBC:TURBOVAC:PZD1-SP.ZRVL", 1)
caput("VBC:TURBOVAC:PZD1-SP.TEVL", 1)
#==============================================================================
