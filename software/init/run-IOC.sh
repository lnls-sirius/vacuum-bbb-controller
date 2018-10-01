#!/bin/bash

# start socket unix
sleep 5
cd /root/vacuum-bbb-controller/software/ioc
EPICS_CAS_SERVER_PORT=5068 python vbc_unix_socket.py 1 &
sleep 10

# start IOC
procServ --chdir /root/stream-ioc/iocBoot 20400 ./VBC.cmd &
sleep 10

# check if system is pressurized. If yes, run "process_recovery" script
PYEPICS_LIBCA=/opt/epics-R3.15.5/base/lib/linux-arm/libca.so python /root/vacuum-bbb-controller/software/pydm/pydm_1.2/scripts/initialization.py VBC1
