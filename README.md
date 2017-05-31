# E96-Localization-Spring-17

Collect data with collectData.py
collectData.py calls movingScript.sh to organize results into a single folder

Use combine.py to generate the csv file output from the results folder created
by collectData.py
Then, taking this csv file, manually add in the expected quadrant output (eg 
1,0,0,0 for quad 1; 0,1,0,0 for quad 2) for each input.

The configuration file simply contains 3 rows, with each row containing an int
MAC address on it.  In the first row should be the int MAC address of the AP
where the first RSSI column comes from, the second row should be the int MAC
address of the AP where the second RSSI column comes from, and so on.

###############################################################################
Edison Guide

Int Converted MAC Address: 159113607448223 
MAC Address: 90:B6:86:0D:06:9F
Name: Edison
Visual Description: No markings on chip
xxxxConvention: Place in back right corner of room (quadrant 0)
Convention: Place in front of room (quadrant 2 or 1)

278020541036329
FC:DB:B3:96:B7:29
Eddie
Clean "Xu" written on chip
Convention: Place in back left corner of room (quadrant 3)

159113606651491
90:B6:86:00:DE:63
Eduardo
Wiped off "Xu" written on chip
xxxConvention: Place in front of room (quadrant 2 or 1)
Convention: Place in back right corner of the room (quadrant 0)

IMPORTANT NOTE: This ordering, (159...223, 278...329, 159...491) is also the
                ordering of the RSSI values in the final outputted CSV file.
