#!/bin/bash

# start socket unix
python /root/vacuum-bbb-controller/software/ioc/vbc_unix_socket.py 1 &
sleep 5

# start IOC
procServ --chdir /root/stream-ioc/iocBoot 20400 ./VBC.cmd
