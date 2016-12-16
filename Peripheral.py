#This code was tested on Python 2.7.12 on a Windows 7 machine
#pyserial must be installed for script to work

#Tested with version 3.0.0 
#To get a copy of the API document visit http://www.ty-top.com/ and contact your 
#local sales office.

#NOTE: This sample code assumes that the device is in its default factory
#setting and has never been paired before.

import serial
import sys
import time

def readResponse(ser):
    var=2
    while var != 0:
        line = ser.readline()
        if len(line) > 0:
            var = var -1 
        if var == 0:
            return line

def main():
    print "Set serial port to N,8,1  @ 9600..."     
    ser = serial.Serial(sys.argv[1], 9600, timeout=2)

    print "Reset module to put it in a known state..."
    ser.write("BRS\r\n")
    print readResponse(ser) #Should return version number 3.0.0 for Peripheral  
    
    #Module by default is configured as a Peripheral out of the factory and it
    #will automatically go into advertising mode after reset.
    print "Stop advertising so we can configure device..."
    ser.write("BCD0\r\n")
    print readResponse(ser) #Should get ACK back
    
    print "Enable LE Security Mode 1 Level 2..."
    ser.write("BST5080001\r\n")
    print readResponse(ser) #Should get ACK back
    
    print "Disable Auto Advertising..."
    ser.write("BST5070001\r\n")
    print readResponse(ser) #Should get ACK back    
    
    print "Set Device Name to TYBLEDemo..."
    ser.write("BST3TYBLEDemo\r\n")
    print readResponse(ser) #Should get ACK back

    print "Reset to update Device Name, Security and Auto Advertising settings..."
    ser.write("BRS\r\n")
    print readResponse(ser) #Should return version number 3.0.0 for Peripheral
     
    print "Advertising, connectable and discoverable"
    ser.write("BCD3\r\n")
    print readResponse(ser) #Should get ACK back

    #Wait for connection. Should get CON[BD_ADDR]
    #where BD_ADDR is the address of Central device
    while True:
        line=ser.readline()
        if len(line) > 0 and line != "\r\n":
            print line
            if line[0:3] == "CON":
                print "Connected!\n" 
            if line[0:3] == "PAS":
                print "Paired!\n" 
                break

    ser.write("Hi Central!\n") #send message to Central Device
    time.sleep(2)
    print ser.readline() #read message from Central Device     
if __name__ == "__main__": main()