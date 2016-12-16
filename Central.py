#This code was tested on Python 2.7.12 on a Windows 7 machine
#pyserial must be installed for script to work

#Tested with version 3.0.0 
#To get a copy of the API document visit http://www.ty-top.com/ and contact your 
#local sales office.

#NOTE: This sample code assumes that the device is in its default factory
#setting and has never been paired before.

import serial
import sys
from Peripheral import readResponse

def main():    
    #Set serial port to N,8,1  @ 9600     
    ser = serial.Serial(sys.argv[1], 9600, timeout=2)

    print "Reset module to put it in a known state..."
    ser.write("BRS\r\n")
    print readResponse(ser) #Should return version number 3.0.0 for Peripheral

    #Module by default is configured as a Peripheral out of the factory, and it
    #will automatically go into advertising mode after reset.
    print "Stop Advertising so we can configure device..."
    ser.write("BCD0\r\n")
    print readResponse(ser) #Should get ACK back

    print "Switch to Central role..."
    ser.write("BRL1\r\n")
    print readResponse(ser) #Should get ACK back
 
    print "Reset to update role setting..."
    ser.write("BRS\r\n")
    print readResponse(ser) #Should return version number 3.0.0C for Central

    #When configured as Central, module will automatically go into Scan after Reset
    print "Stop Scanning so we can continue configuring device... "
    ser.write("BSC0\r\n")
    print readResponse(ser) #Should get ACK back
    
    print "Disable Auto Scan..."
    ser.write("BST5070001\r\n") 
    print readResponse(ser) #Should get ACK back
    
    print "Set Target Name to TYBLEDemo..."
    ser.write("BST3TYBLEDemo\r\n")
    print readResponse(ser) #Should get ACK back

    print "Reset to update Auto Scan setting and Target Name "
    ser.write("BRS\r\n")
    print readResponse(ser) #Should return version number 3.0.0C for Central

    print "Scan and connect to target TYBLEDemo..."
    ser.write("BSC1\r\n")
    print readResponse(ser) #Should get ACK back

    #Wait for connection. Should get CON[BD_ADDR]
    #where BD_ADDR is the address of Peripheral device
    while True:
        line=ser.readline()
        if len(line) > 0 and line != "\r\n":
            print line
            if line[0:3] == "CON":
                print "Connected and Paired!\n"    
                break
            
    #Receive/Send message...
    while True:
        line=ser.readline() #read message from Peripheral
        if len(line) > 0:
            print line
            ser.write("Hello Peripheral!\n")#send message back to Peripheral
            break
if __name__ == "__main__": main()