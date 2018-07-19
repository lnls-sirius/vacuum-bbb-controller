#!/usr/bin/python
from epics import caget, caput
#------------------------------------------------------------------------------
'''
this script do all the procedures turn off the system with full ventilation
it is divided in 6 stages, described as follow:
    -stage 1: close pre-vacuum valve (keep gate valve open)
    -stage 2: turn ACP15 and TURBOVAC pumps off
    -stage 3: wait TURBOVAC slowdown to 600 Hz
    -stage 4: open X203 (TURBOVAC venting valve)
    -stage 5: wait pressure decrease to 760 Torr
    -stage 6: close X203 and gate valves
'''
#------------------------------------------------------------------------------
# valve names definition
PRE-VACUUM_VALVE = "VBC:BBB:Relay2"
GATE_VALVE = "VBC:BBB:Relay4"
#==============================================================================
# Stage 1:
#==============================================================================
# close pre-vacuum valve (and keeps gate valve open)
caput("VBC:ProcessOff:Status1", 1)
caput(PRE-VACUUM_VALVE, 0)
#==============================================================================
# Stage 2:
#==============================================================================
# turn TURBOVAC and ACP15 pumps OFF
caput("VBC:ProcessOff:Status2", 1)
caput("VBC:TURBOVAC:OnOff", 0)
caput("VBC:ACP:OnOff", 0)
#==============================================================================
# Stage 3:
#==============================================================================
# wait until TURBOVAC frequency decrease to 600 Hz
caput("VBC:ProcessOff:Status3", 1)
while (caget("VBC:TURBOVAC:PZD2-RB") > 600):
    pass
#==============================================================================
# Stage 4:
#==============================================================================
# open X203 valve (TURBOVAC venting valve)
caput("VBC:ProcessOff:Status4", 1)
caput("VBC:TURBOVAC:PZD1-SP.FFVL", 1)
#==============================================================================
# Stage 5:
#==============================================================================
# wait until pressure gets 760 Torr
caput("VBC:ProcessOff:Status5", 1)
while (caget("VBC:BBB:Torr") < 760):
    pass
#==============================================================================
# Stage 6:
#==============================================================================
# close all the valves (gate valve is already closed)
caput("VBC:ProcessOff:Status6", 1)
caput("VBC:TURBOVAC:PZD1-SP.FFVL", 0)       # close X203
caput(PRE-VACUUM_VALVE, 0)
#==============================================================================
