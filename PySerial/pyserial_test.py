import serial #Imports PySerial for sending information to and from Arduino.
import time #Imports time.
import random # imports function to generate random number.
ser = serial.Serial("COM4",9600) #COM4 is the port for the Arduino. Change to appropriate port on your computer. Second number is baudrate. Match to rate in Arduino.
time.sleep(5) #Adds 5 second delay before Python starts searching for a signal from the Arduino.
cond = True
while cond == True:
    #code = random(100000,999999) (WIP - Need keypad to test entering the code)
    #print(code)
    print("Sending code to Arduino for verification...")
    ser.write(b'8') #Writes the number 8 in binary to the serial port for the Arduino to read.
    cond = input("Would you like to repeat?") #Conditional to continue the loop.
    if cond == 'y':
        cond = True
    else:
        cond = False
