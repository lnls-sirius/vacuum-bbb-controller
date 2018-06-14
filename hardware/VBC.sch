EESchema Schematic File Version 2
LIBS:power
LIBS:device
LIBS:transistors
LIBS:conn
LIBS:linear
LIBS:regul
LIBS:74xx
LIBS:cmos4000
LIBS:adc-dac
LIBS:memory
LIBS:xilinx
LIBS:microcontrollers
LIBS:dsp
LIBS:microchip
LIBS:analog_switches
LIBS:motorola
LIBS:texas
LIBS:intel
LIBS:audio
LIBS:interface
LIBS:digital-audio
LIBS:philips
LIBS:display
LIBS:cypress
LIBS:siliconi
LIBS:opto
LIBS:atmel
LIBS:contrib
LIBS:valves
LIBS:Controle
EELAYER 25 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 1 1
Title ""
Date ""
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
$Comp
L BeagleBone Beagle1
U 1 1 5B192C7F
P 4875 2600
F 0 "Beagle1" H 4875 3850 50  0000 C CNN
F 1 "BeagleBone" H 5025 1350 50  0000 C CNN
F 2 "Controle:BEAGLEBONEBLACK" H 4875 1500 60  0001 C CNN
F 3 "" H 4875 1500 60  0000 C CNN
	1    4875 2600
	1    0    0    -1  
$EndComp
$Comp
L BeagleBone Beagle1
U 2 1 5B192CC4
P 6475 2600
F 0 "Beagle1" H 6475 3850 50  0000 C CNN
F 1 "BeagleBone" H 6625 1350 50  0000 C CNN
F 2 "Controle:BEAGLEBONEBLACK" H 6475 1500 60  0001 C CNN
F 3 "" H 6475 1500 60  0000 C CNN
	2    6475 2600
	1    0    0    -1  
$EndComp
$Comp
L TS5A21366 U1
U 1 1 5B1EC0A7
P 2825 5075
F 0 "U1" H 3300 5500 60  0000 C CNN
F 1 "TS5A21366" H 2525 5500 60  0000 C CNN
F 2 "Controle:VSSOP-8" H 2825 5075 60  0001 C CNN
F 3 "" H 2825 5075 60  0000 C CNN
	1    2825 5075
	1    0    0    -1  
$EndComp
$Comp
L TS5A21366 U2
U 1 1 5B1EC116
P 2875 6175
F 0 "U2" H 3350 6600 60  0000 C CNN
F 1 "TS5A21366" H 2575 6600 60  0000 C CNN
F 2 "Controle:VSSOP-8" H 2875 6175 60  0001 C CNN
F 3 "" H 2875 6175 60  0000 C CNN
	1    2875 6175
	1    0    0    -1  
$EndComp
$Comp
L RELAY_Metaltex K1
U 1 1 5B1EC145
P 2725 3200
F 0 "K1" H 2675 3600 50  0000 C CNN
F 1 "RELAY_Metaltex" H 2875 2700 50  0000 C CNN
F 2 "" H 2725 3200 50  0001 C CNN
F 3 "" H 2725 3200 50  0000 C CNN
	1    2725 3200
	1    0    0    -1  
$EndComp
$Comp
L CONN_01X01 P1
U 1 1 5B1FDE52
P 4625 6400
F 0 "P1" H 4625 6500 50  0000 C CNN
F 1 "CONN_01X01" V 4725 6400 50  0000 C CNN
F 2 "Controle:LNLS_LOGO" H 4625 6400 50  0001 C CNN
F 3 "" H 4625 6400 50  0000 C CNN
	1    4625 6400
	-1   0    0    1   
$EndComp
$EndSCHEMATC
