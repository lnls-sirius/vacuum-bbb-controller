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
LIBS:VBC-cache
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
P 9155 5030
F 0 "Beagle1" H 9155 6280 50  0000 C CNN
F 1 "BeagleBone" H 9305 3780 50  0000 C CNN
F 2 "Controle:BEAGLEBONEBLACK" H 9155 3930 60  0001 C CNN
F 3 "" H 9155 3930 60  0000 C CNN
	1    9155 5030
	1    0    0    -1  
$EndComp
$Comp
L BeagleBone Beagle1
U 2 1 5B192CC4
P 10755 5030
F 0 "Beagle1" H 10755 6280 50  0000 C CNN
F 1 "BeagleBone" H 10905 3780 50  0000 C CNN
F 2 "Controle:BEAGLEBONEBLACK" H 10755 3930 60  0001 C CNN
F 3 "" H 10755 3930 60  0000 C CNN
	2    10755 5030
	1    0    0    -1  
$EndComp
$Comp
L TS5A21366 U1
U 1 1 5B1EC0A7
P 10055 1380
F 0 "U1" H 10530 1805 60  0000 C CNN
F 1 "TS5A21366" H 9755 1805 60  0000 C CNN
F 2 "Controle:VSSOP-8" H 10055 1380 60  0001 C CNN
F 3 "" H 10055 1380 60  0000 C CNN
	1    10055 1380
	1    0    0    -1  
$EndComp
$Comp
L TS5A21366 U2
U 1 1 5B1EC116
P 10105 2480
F 0 "U2" H 10580 2905 60  0000 C CNN
F 1 "TS5A21366" H 9805 2905 60  0000 C CNN
F 2 "Controle:VSSOP-8" H 10105 2480 60  0001 C CNN
F 3 "" H 10105 2480 60  0000 C CNN
	1    10105 2480
	1    0    0    -1  
$EndComp
$Comp
L CONN_01X01 P1
U 1 1 5B1FDE52
P 10295 3300
F 0 "P1" H 10295 3400 50  0000 C CNN
F 1 "CONN_01X01" V 10395 3300 50  0000 C CNN
F 2 "Controle:LNLS_LOGO" H 10295 3300 50  0001 C CNN
F 3 "" H 10295 3300 50  0000 C CNN
	1    10295 3300
	-1   0    0    1   
$EndComp
$Comp
L BC817 Q3
U 1 1 5B2153FC
P 2070 3455
F 0 "Q3" H 2270 3530 50  0000 L CNN
F 1 "BC817" H 2270 3455 50  0000 L CNN
F 2 "TO_SOT_Packages_SMD:SOT-23" H 2270 3380 50  0001 L CIN
F 3 "" H 2070 3455 50  0001 L CNN
	1    2070 3455
	1    0    0    -1  
$EndComp
$Comp
L RELAY_Metaltex K1
U 1 1 5B1EC145
P 2570 2620
F 0 "K1" H 2520 3020 50  0000 C CNN
F 1 "RELAY_Metaltex" H 2720 2120 50  0000 C CNN
F 2 "Relays_THT:Relay_DPDT_Omron_G5V-2" H 2570 2620 50  0001 C CNN
F 3 "" H 2570 2620 50  0000 C CNN
	1    2570 2620
	1    0    0    -1  
$EndComp
$Comp
L VCC #PWR3
U 1 1 5B2150B6
P 1860 2870
F 0 "#PWR3" H 1860 2720 50  0001 C CNN
F 1 "VCC" H 1860 3020 50  0000 C CNN
F 2 "" H 1860 2870 50  0001 C CNN
F 3 "" H 1860 2870 50  0001 C CNN
	1    1860 2870
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR10
U 1 1 5B2152BC
P 2170 3765
F 0 "#PWR10" H 2170 3515 50  0001 C CNN
F 1 "GND" H 2170 3615 50  0000 C CNN
F 2 "" H 2170 3765 50  0001 C CNN
F 3 "" H 2170 3765 50  0001 C CNN
	1    2170 3765
	1    0    0    -1  
$EndComp
$Comp
L R R3
U 1 1 5B215472
P 1635 3455
F 0 "R3" V 1715 3455 50  0000 C CNN
F 1 "R" V 1635 3455 50  0000 C CNN
F 2 "Resistors_SMD:R_0805_HandSoldering" V 1565 3455 50  0001 C CNN
F 3 "" H 1635 3455 50  0001 C CNN
	1    1635 3455
	0    -1   -1   0   
$EndComp
Text Label 1485 3455 2    60   ~ 0
BBB_p?
$Comp
L BC817 Q1
U 1 1 5B215ED8
P 1915 1745
F 0 "Q1" H 2115 1820 50  0000 L CNN
F 1 "BC817" H 2115 1745 50  0000 L CNN
F 2 "TO_SOT_Packages_SMD:SOT-23" H 2115 1670 50  0001 L CIN
F 3 "" H 1915 1745 50  0001 L CNN
	1    1915 1745
	1    0    0    -1  
$EndComp
$Comp
L RELAY_Metaltex K2
U 1 1 5B215EDE
P 2415 910
F 0 "K2" H 2365 1310 50  0000 C CNN
F 1 "RELAY_Metaltex" H 2565 410 50  0000 C CNN
F 2 "Relays_THT:Relay_DPDT_Omron_G5V-2" H 2415 910 50  0001 C CNN
F 3 "" H 2415 910 50  0000 C CNN
	1    2415 910 
	1    0    0    -1  
$EndComp
$Comp
L VCC #PWR1
U 1 1 5B215EE4
P 1705 1160
F 0 "#PWR1" H 1705 1010 50  0001 C CNN
F 1 "VCC" H 1705 1310 50  0000 C CNN
F 2 "" H 1705 1160 50  0001 C CNN
F 3 "" H 1705 1160 50  0001 C CNN
	1    1705 1160
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR6
U 1 1 5B215EEA
P 2015 2055
F 0 "#PWR6" H 2015 1805 50  0001 C CNN
F 1 "GND" H 2015 1905 50  0000 C CNN
F 2 "" H 2015 2055 50  0001 C CNN
F 3 "" H 2015 2055 50  0001 C CNN
	1    2015 2055
	1    0    0    -1  
$EndComp
$Comp
L R R1
U 1 1 5B215EF0
P 1480 1745
F 0 "R1" V 1560 1745 50  0000 C CNN
F 1 "R" V 1480 1745 50  0000 C CNN
F 2 "Resistors_SMD:R_0805_HandSoldering" V 1410 1745 50  0001 C CNN
F 3 "" H 1480 1745 50  0001 C CNN
	1    1480 1745
	0    -1   -1   0   
$EndComp
Text Label 1330 1745 2    60   ~ 0
BBB_p?
$Comp
L BC817 Q4
U 1 1 5B2165FE
P 2105 6885
F 0 "Q4" H 2305 6960 50  0000 L CNN
F 1 "BC817" H 2305 6885 50  0000 L CNN
F 2 "TO_SOT_Packages_SMD:SOT-23" H 2305 6810 50  0001 L CIN
F 3 "" H 2105 6885 50  0001 L CNN
	1    2105 6885
	1    0    0    -1  
$EndComp
$Comp
L RELAY_Metaltex K4
U 1 1 5B216604
P 2605 6050
F 0 "K4" H 2555 6450 50  0000 C CNN
F 1 "RELAY_Metaltex" H 2755 5550 50  0000 C CNN
F 2 "Relays_THT:Relay_DPDT_Omron_G5V-2" H 2605 6050 50  0001 C CNN
F 3 "" H 2605 6050 50  0000 C CNN
	1    2605 6050
	1    0    0    -1  
$EndComp
$Comp
L VCC #PWR4
U 1 1 5B21660A
P 1895 6300
F 0 "#PWR4" H 1895 6150 50  0001 C CNN
F 1 "VCC" H 1895 6450 50  0000 C CNN
F 2 "" H 1895 6300 50  0001 C CNN
F 3 "" H 1895 6300 50  0001 C CNN
	1    1895 6300
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR12
U 1 1 5B216610
P 2205 7195
F 0 "#PWR12" H 2205 6945 50  0001 C CNN
F 1 "GND" H 2205 7045 50  0000 C CNN
F 2 "" H 2205 7195 50  0001 C CNN
F 3 "" H 2205 7195 50  0001 C CNN
	1    2205 7195
	1    0    0    -1  
$EndComp
$Comp
L R R4
U 1 1 5B216616
P 1670 6885
F 0 "R4" V 1750 6885 50  0000 C CNN
F 1 "R" V 1670 6885 50  0000 C CNN
F 2 "Resistors_SMD:R_0805_HandSoldering" V 1600 6885 50  0001 C CNN
F 3 "" H 1670 6885 50  0001 C CNN
	1    1670 6885
	0    -1   -1   0   
$EndComp
Text Label 1520 6885 2    60   ~ 0
BBB_p?
$Comp
L BC817 Q2
U 1 1 5B216621
P 1950 5175
F 0 "Q2" H 2150 5250 50  0000 L CNN
F 1 "BC817" H 2150 5175 50  0000 L CNN
F 2 "TO_SOT_Packages_SMD:SOT-23" H 2150 5100 50  0001 L CIN
F 3 "" H 1950 5175 50  0001 L CNN
	1    1950 5175
	1    0    0    -1  
$EndComp
$Comp
L RELAY_Metaltex K3
U 1 1 5B216627
P 2450 4340
F 0 "K3" H 2400 4740 50  0000 C CNN
F 1 "RELAY_Metaltex" H 2600 3840 50  0000 C CNN
F 2 "Relays_THT:Relay_DPDT_Omron_G5V-2" H 2450 4340 50  0001 C CNN
F 3 "" H 2450 4340 50  0000 C CNN
	1    2450 4340
	1    0    0    -1  
$EndComp
$Comp
L VCC #PWR2
U 1 1 5B21662D
P 1740 4590
F 0 "#PWR2" H 1740 4440 50  0001 C CNN
F 1 "VCC" H 1740 4740 50  0000 C CNN
F 2 "" H 1740 4590 50  0001 C CNN
F 3 "" H 1740 4590 50  0001 C CNN
	1    1740 4590
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR8
U 1 1 5B216633
P 2050 5485
F 0 "#PWR8" H 2050 5235 50  0001 C CNN
F 1 "GND" H 2050 5335 50  0000 C CNN
F 2 "" H 2050 5485 50  0001 C CNN
F 3 "" H 2050 5485 50  0001 C CNN
	1    2050 5485
	1    0    0    -1  
$EndComp
$Comp
L R R2
U 1 1 5B216639
P 1515 5175
F 0 "R2" V 1595 5175 50  0000 C CNN
F 1 "R" V 1515 5175 50  0000 C CNN
F 2 "Resistors_SMD:R_0805_HandSoldering" V 1445 5175 50  0001 C CNN
F 3 "" H 1515 5175 50  0001 C CNN
	1    1515 5175
	0    -1   -1   0   
$EndComp
Text Label 1365 5175 2    60   ~ 0
BBB_p?
$Comp
L R R5
U 1 1 5B216A34
P 4340 1305
F 0 "R5" V 4420 1305 50  0000 C CNN
F 1 "R" V 4340 1305 50  0000 C CNN
F 2 "Resistors_SMD:R_0805_HandSoldering" V 4270 1305 50  0001 C CNN
F 3 "" H 4340 1305 50  0001 C CNN
	1    4340 1305
	1    0    0    -1  
$EndComp
$Comp
L R R6
U 1 1 5B216CF3
P 4340 1760
F 0 "R6" V 4420 1760 50  0000 C CNN
F 1 "R" V 4340 1760 50  0000 C CNN
F 2 "Resistors_SMD:R_0805_HandSoldering" V 4270 1760 50  0001 C CNN
F 3 "" H 4340 1760 50  0001 C CNN
	1    4340 1760
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR13
U 1 1 5B216E09
P 4340 1995
F 0 "#PWR13" H 4340 1745 50  0001 C CNN
F 1 "GND" H 4340 1845 50  0000 C CNN
F 2 "" H 4340 1995 50  0001 C CNN
F 3 "" H 4340 1995 50  0001 C CNN
	1    4340 1995
	1    0    0    -1  
$EndComp
Text Label 4625 1530 0    60   ~ 0
AIn_BBB
$Comp
L Conn_SMA_90graus C1
U 1 1 5B2176A6
P 4340 955
F 0 "C1" H 4435 835 60  0000 C CNN
F 1 "Conn_SMA_90graus" H 4340 1085 60  0000 C CNN
F 2 "Connectors:SMA_THT_Jack_Straight" H 4340 955 60  0001 C CNN
F 3 "" H 4340 955 60  0000 C CNN
	1    4340 955 
	0    -1   -1   0   
$EndComp
$Comp
L Jack-DC J1
U 1 1 5B217841
P 6160 870
F 0 "J1" H 6160 1080 50  0000 C CNN
F 1 "Jack-DC" H 6160 695 50  0000 C CNN
F 2 "Connectors:BARREL_JACK" H 6210 830 50  0001 C CNN
F 3 "" H 6210 830 50  0001 C CNN
	1    6160 870 
	1    0    0    -1  
$EndComp
$Comp
L 6P6C J3
U 1 1 5B21792E
P 6215 1770
F 0 "J3" H 6465 2270 60  0000 C CNN
F 1 "6P6C" H 6065 2270 60  0000 C CNN
F 2 "Connectors:RJ12_E" H 6215 1770 60  0001 C CNN
F 3 "" H 6215 1770 60  0000 C CNN
	1    6215 1770
	1    0    0    -1  
$EndComp
$Comp
L USB_OTG J2
U 1 1 5B217A65
P 6210 2655
F 0 "J2" H 6010 3105 50  0000 L CNN
F 1 "USB_OTG" H 6010 3005 50  0000 L CNN
F 2 "Connectors:USB_Micro-B" H 6360 2605 50  0001 C CNN
F 3 "" H 6360 2605 50  0001 C CNN
	1    6210 2655
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR14
U 1 1 5B217CD2
P 4610 955
F 0 "#PWR14" H 4610 705 50  0001 C CNN
F 1 "GND" H 4610 805 50  0000 C CNN
F 2 "" H 4610 955 50  0001 C CNN
F 3 "" H 4610 955 50  0001 C CNN
	1    4610 955 
	0    -1   -1   0   
$EndComp
$Comp
L +24V #PWR7
U 1 1 5B228269
P 2050 4390
F 0 "#PWR7" H 2050 4240 50  0001 C CNN
F 1 "+24V" H 2050 4530 50  0000 C CNN
F 2 "" H 2050 4390 50  0001 C CNN
F 3 "" H 2050 4390 50  0001 C CNN
	1    2050 4390
	1    0    0    -1  
$EndComp
$Comp
L +24V #PWR9
U 1 1 5B2283A6
P 2170 2670
F 0 "#PWR9" H 2170 2520 50  0001 C CNN
F 1 "+24V" H 2170 2810 50  0000 C CNN
F 2 "" H 2170 2670 50  0001 C CNN
F 3 "" H 2170 2670 50  0001 C CNN
	1    2170 2670
	1    0    0    -1  
$EndComp
$Comp
L +24V #PWR5
U 1 1 5B2285BB
P 2015 960
F 0 "#PWR5" H 2015 810 50  0001 C CNN
F 1 "+24V" H 2015 1100 50  0000 C CNN
F 2 "" H 2015 960 50  0001 C CNN
F 3 "" H 2015 960 50  0001 C CNN
	1    2015 960 
	1    0    0    -1  
$EndComp
$Comp
L +24V #PWR11
U 1 1 5B2287EB
P 2205 6100
F 0 "#PWR11" H 2205 5950 50  0001 C CNN
F 1 "+24V" H 2205 6240 50  0000 C CNN
F 2 "" H 2205 6100 50  0001 C CNN
F 3 "" H 2205 6100 50  0001 C CNN
	1    2205 6100
	1    0    0    -1  
$EndComp
$Comp
L Conn_01x02 J4
U 1 1 5B227EDA
P 7220 790
F 0 "J4" H 7220 890 50  0000 C CNN
F 1 "Conn_01x02" H 7220 590 50  0000 C CNN
F 2 "Connectors_Terminal_Blocks:TerminalBlock_Altech_AK300-2_P5.00mm" H 7220 790 50  0001 C CNN
F 3 "" H 7220 790 50  0001 C CNN
	1    7220 790 
	1    0    0    -1  
$EndComp
$Comp
L VCC #PWR15
U 1 1 5B229BB9
P 6460 770
F 0 "#PWR15" H 6460 620 50  0001 C CNN
F 1 "VCC" H 6460 920 50  0000 C CNN
F 2 "" H 6460 770 50  0001 C CNN
F 3 "" H 6460 770 50  0001 C CNN
	1    6460 770 
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR16
U 1 1 5B229C45
P 6460 970
F 0 "#PWR16" H 6460 720 50  0001 C CNN
F 1 "GND" H 6460 820 50  0000 C CNN
F 2 "" H 6460 970 50  0001 C CNN
F 3 "" H 6460 970 50  0001 C CNN
	1    6460 970 
	1    0    0    -1  
$EndComp
$Comp
L +24V #PWR17
U 1 1 5B229D79
P 7020 790
F 0 "#PWR17" H 7020 640 50  0001 C CNN
F 1 "+24V" H 7020 930 50  0000 C CNN
F 2 "" H 7020 790 50  0001 C CNN
F 3 "" H 7020 790 50  0001 C CNN
	1    7020 790 
	1    0    0    -1  
$EndComp
$Comp
L RJ11 J7
U 1 1 5B22CA71
P 3810 2620
F 0 "J7" H 3960 2970 60  0000 C CNN
F 1 "RJ11" H 3660 2970 60  0000 C CNN
F 2 "Controle:RJ11" H 3810 2620 60  0001 C CNN
F 3 "" H 3810 2620 60  0000 C CNN
	1    3810 2620
	0    1    1    0   
$EndComp
$Comp
L RJ11 J6
U 1 1 5B22CBB4
P 3695 4340
F 0 "J6" H 3845 4690 60  0000 C CNN
F 1 "RJ11" H 3545 4690 60  0000 C CNN
F 2 "Controle:RJ11" H 3695 4340 60  0001 C CNN
F 3 "" H 3695 4340 60  0000 C CNN
	1    3695 4340
	0    1    1    0   
$EndComp
$Comp
L RJ11 J8
U 1 1 5B22CDAB
P 3860 6050
F 0 "J8" H 4010 6400 60  0000 C CNN
F 1 "RJ11" H 3710 6400 60  0000 C CNN
F 2 "Controle:RJ11" H 3860 6050 60  0001 C CNN
F 3 "" H 3860 6050 60  0000 C CNN
	1    3860 6050
	0    1    1    0   
$EndComp
Wire Wire Line
	2170 3255 2170 2970
Wire Wire Line
	2170 3765 2170 3655
Wire Wire Line
	1860 2870 2170 2870
Wire Wire Line
	1785 3455 1870 3455
Wire Wire Line
	2015 1545 2015 1260
Wire Wire Line
	2015 2055 2015 1945
Wire Wire Line
	1705 1160 2015 1160
Wire Wire Line
	1630 1745 1715 1745
Wire Wire Line
	2205 6685 2205 6400
Wire Wire Line
	2205 7195 2205 7085
Wire Wire Line
	1895 6300 2205 6300
Wire Wire Line
	1820 6885 1905 6885
Wire Wire Line
	2050 4975 2050 4690
Wire Wire Line
	2050 5485 2050 5375
Wire Wire Line
	1740 4590 2050 4590
Wire Wire Line
	1665 5175 1750 5175
Wire Wire Line
	4340 1455 4340 1610
Wire Wire Line
	4340 1910 4340 1995
Wire Wire Line
	4340 1530 4625 1530
Connection ~ 4340 1530
Wire Wire Line
	2970 2570 3210 2570
Wire Wire Line
	2970 2770 3105 2770
Wire Wire Line
	3105 2770 3105 2470
Wire Wire Line
	3105 2470 3210 2470
$Comp
L RJ11 J5
U 1 1 5B22C67E
P 3580 910
F 0 "J5" H 3730 1260 60  0000 C CNN
F 1 "RJ11" H 3430 1260 60  0000 C CNN
F 2 "Controle:RJ11" H 3580 910 60  0001 C CNN
F 3 "" H 3580 910 60  0000 C CNN
	1    3580 910 
	0    1    1    0   
$EndComp
Wire Wire Line
	2815 860  2980 860 
Wire Wire Line
	2980 760  2895 760 
Wire Wire Line
	2895 760  2895 1060
Wire Wire Line
	2895 1060 2815 1060
Wire Wire Line
	2850 4290 3095 4290
Wire Wire Line
	3095 4190 2935 4190
Wire Wire Line
	2935 4190 2935 4490
Wire Wire Line
	2935 4490 2850 4490
Wire Wire Line
	3005 6000 3260 6000
Wire Wire Line
	3005 6200 3110 6200
Wire Wire Line
	3110 6200 3110 5900
Wire Wire Line
	3110 5900 3260 5900
$Comp
L USB_A J9
U 1 1 5B22F8E0
P 7150 2635
F 0 "J9" H 6950 3085 50  0000 L CNN
F 1 "USB_A" H 6950 2985 50  0000 L CNN
F 2 "Connectors:USB_A" H 7300 2585 50  0001 C CNN
F 3 "" H 7300 2585 50  0001 C CNN
	1    7150 2635
	1    0    0    -1  
$EndComp
Wire Wire Line
	6510 2455 6825 2455
Wire Wire Line
	6825 2455 6825 2120
Wire Wire Line
	6825 2120 7450 2120
Wire Wire Line
	7450 2120 7450 2435
Wire Wire Line
	6510 2655 6835 2655
Wire Wire Line
	6835 2655 6835 3195
Wire Wire Line
	6835 3195 7560 3195
Wire Wire Line
	7560 3195 7560 2635
Wire Wire Line
	7560 2635 7450 2635
Wire Wire Line
	7450 2735 7450 3155
Wire Wire Line
	7450 3155 6790 3155
Wire Wire Line
	6790 3155 6790 2755
Wire Wire Line
	6790 2755 6510 2755
Wire Wire Line
	7150 3035 7050 3035
$Comp
L GND #PWR?
U 1 1 5B23090D
P 7150 3035
F 0 "#PWR?" H 7150 2785 50  0001 C CNN
F 1 "GND" H 7150 2885 50  0000 C CNN
F 2 "" H 7150 3035 50  0001 C CNN
F 3 "" H 7150 3035 50  0001 C CNN
	1    7150 3035
	0    -1   -1   0   
$EndComp
$Comp
L GND #PWR?
U 1 1 5B230A7D
P 6210 3055
F 0 "#PWR?" H 6210 2805 50  0001 C CNN
F 1 "GND" H 6210 2905 50  0000 C CNN
F 2 "" H 6210 3055 50  0001 C CNN
F 3 "" H 6210 3055 50  0001 C CNN
	1    6210 3055
	1    0    0    -1  
$EndComp
Wire Wire Line
	6110 3055 6210 3055
$EndSCHEMATC
