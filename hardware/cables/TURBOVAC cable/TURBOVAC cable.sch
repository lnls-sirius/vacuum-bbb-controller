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
LIBS:TURBOVAC cable-cache
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
Text Notes 1650 1100 0    79   ~ 0
TURBOVAC cable for RS-485: without fail-safe and termination
$Comp
L RJ25 J1
U 1 1 5B2BA9D1
P 2450 1825
F 0 "J1" H 2700 2325 60  0000 C CNN
F 1 "RJ25" H 2300 2325 60  0000 C CNN
F 2 "" H 2450 1825 60  0000 C CNN
F 3 "" H 2450 1825 60  0000 C CNN
	1    2450 1825
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR?
U 1 1 5B2BA9D7
P 2750 2425
F 0 "#PWR?" H 2750 2175 50  0001 C CNN
F 1 "GND" H 2750 2275 50  0000 C CNN
F 2 "" H 2750 2425 50  0000 C CNN
F 3 "" H 2750 2425 50  0000 C CNN
	1    2750 2425
	-1   0    0    -1  
$EndComp
$Comp
L GND #PWR?
U 1 1 5B2BA9DD
P 2350 2425
F 0 "#PWR?" H 2350 2175 50  0001 C CNN
F 1 "GND" H 2350 2275 50  0000 C CNN
F 2 "" H 2350 2425 50  0000 C CNN
F 3 "" H 2350 2425 50  0000 C CNN
	1    2350 2425
	-1   0    0    -1  
$EndComp
NoConn ~ 4175 3400
$Comp
L DB9 J2
U 1 1 5B2BA9E4
P 4625 3000
F 0 "J2" H 4625 3550 50  0000 C CNN
F 1 "DB9" H 4625 2450 50  0000 C CNN
F 2 "" H 4625 3000 50  0000 C CNN
F 3 "" H 4625 3000 50  0000 C CNN
	1    4625 3000
	1    0    0    -1  
$EndComp
NoConn ~ 4175 3200
NoConn ~ 4175 3000
NoConn ~ 4175 2800
$Comp
L GND #PWR?
U 1 1 5B2BA9ED
P 4075 2525
F 0 "#PWR?" H 4075 2275 50  0001 C CNN
F 1 "GND" H 4075 2375 50  0000 C CNN
F 2 "" H 4075 2525 50  0000 C CNN
F 3 "" H 4075 2525 50  0000 C CNN
	1    4075 2525
	1    0    0    1   
$EndComp
Wire Wire Line
	4175 2600 4075 2600
Wire Wire Line
	4075 2600 4075 2525
Wire Wire Line
	2750 2275 2750 2425
Wire Wire Line
	2350 2275 2350 2425
NoConn ~ 2250 2275
Text Label 3300 2700 0    60   ~ 0
V+(A)
Text Label 3300 2900 0    60   ~ 0
V-(B)
Wire Bus Line
	1550 925  1550 3800
Wire Bus Line
	1550 3800 5625 3800
Wire Bus Line
	5625 3800 5625 925 
Wire Bus Line
	5625 925  1550 925 
Wire Wire Line
	2450 2275 2450 2350
Wire Wire Line
	2450 2350 2350 2350
Connection ~ 2350 2350
NoConn ~ 4175 3300
Wire Wire Line
	2550 2275 2550 2900
Wire Wire Line
	2550 2900 4175 2900
Wire Wire Line
	2650 2275 2650 2700
Wire Wire Line
	2650 2700 4175 2700
NoConn ~ 4175 3100
$EndSCHEMATC
