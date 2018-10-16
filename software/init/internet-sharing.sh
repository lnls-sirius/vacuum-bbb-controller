#!/bin/bash

echo "nameserver 10.0.0.71" >> /etc/resolv.conf
echo "nameserver 10.0.0.72" >> /etc/resolv.conf
echo "search abtlus.org.br" >> /etc/resolv.conf

route add default gw 10.128.40.100
route add default gw 10.128.40.101
route add default gw 10.128.40.102
route add default gw 10.128.40.103
route add default gw 10.128.40.104
route add default gw 10.128.40.105
route add default gw 10.128.40.106
route add default gw 10.128.40.107
route add default gw 10.128.40.108
route add default gw 10.128.40.109
route add default gw 10.128.40.110

