#!/usr/bin/python
from epics import caget, caput
import time
import sys
#------------------------------------------------------------------------------
'''
this is script is used to commute a valve value
'''
#------------------------------------------------------------------------------
# define the PREFIX that will be used (passed as a parameter)
VBC = sys.argv[1]
VALVE = sys.argv[2]
SW = VBC + ":BBB:Relay" + VALVE + "-SW"
UI = VBC + ":BBB:Relay" + VALVE + "-UI"
#------------------------------------------------------------------------------
time.sleep(1)
if (sys.argv[3] == "yes"):
    if (VALVE == "1"):
        caput(SW, not(caget(SW)))
    elif (VALVE == "2"):
        caput(SW, not(caget(SW)))
    elif (VALVE == "3"):
        caput(SW, not(caget(SW)))
    elif (VALVE == "4"):
        caput(SW, not(caget(SW)))
    elif (VALVE == "venting_valve"):
        caput(VBC + ":TURBOVAC:VentingValve-SW", not(caget(VBC + ":TURBOVAC:VentingValve-SW")))
elif (sys.argv[3] == "no"):
    if (VALVE == "venting_valve"):
        caput(VBC + ":TURBOVAC:VentingValve-UI", not(caget(VBC + ":TURBOVAC:VentingValve-UI")))
    #elif (VALVE == "1"):
    #    caput(UI + ".RVAL", caget(SW))
    #elif (VALVE == "2"):
    #    caput(UI + ".RVAL", caget(SW))
    #elif (VALVE == "3"):
    #    caput(UI + ".RVAL", caget(SW))
    #elif (VALVE == "4"):
    #    caput(UI + ".RVAL", caget(SW))
