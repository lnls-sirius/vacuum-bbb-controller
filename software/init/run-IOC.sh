#!/bin/bash

# start socket unix
sleep 5
cd /root/vacuum-bbb-controller/software/ioc
EPICS_CAS_SERVER_PORT=5068 ./vbc_unix_socket.py 1 &
sleep 5

# start IOC
procServ --chdir /root/stream-ioc/iocBoot 20400 ./VBC.cmd
