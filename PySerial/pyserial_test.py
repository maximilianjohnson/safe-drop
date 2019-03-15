import serial #Imports PySerial for sending information to and from Arduino.
import time #Imports time.
import random # imports function to generate random number.
import struct
ser = serial.Serial("COM4",9600) #COM4 is the port for the Arduino. Change to appropriate port on your computer. Second number is baudrate. Match to rate in Arduino.
time.sleep(2) #Adds 5 second delay before Python starts searching for a signal from the Arduino.
cond = True
codeLoop = False
while cond == True:
    #code = random(100000,999999) #(WIP - Need keypad to test entering the code)
    #print(code)
    tester = 900
    testerBin = (struct.pack('>H', tester))
    print("Sending code to Arduino for verification...")
    print (testerBin)
    ser.write(testerBin) #Writes the number 8 in binary to the serial port for the Arduino to read
    cond = False
