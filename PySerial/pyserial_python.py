import serial #Imports PySerial for sending information to and from Arduino.
import time #Imports time.
import random # imports function to generate random number.
import struct
ser = serial.Serial("COM4",9600) #COM4 is the port for the Arduino. Change to appropriate port on your computer. Second number is baudrate. Match to rate in Arduino.

time.sleep(2) #Adds 5 second delay before Python starts searching for a signal from the Arduino.
var = ''
codeStr = ''
codeLen = 0
checkVal = 0
cond = True
code = []
codeByte = []
returned = []

def code_gen(codeByte, codeNum):
    num = 0
    i = 0
    numStr = ''
    numToBytes = 0
    while (i < 6):
        num = random.randint(0,9)
        numStr = str(num)
        codeNum.append(numStr)
        numToBytes = bytes(numStr, encoding='utf-8')
        codeByte.append(numToBytes)
        i += 1
    return


while cond == True:
    ser.flushInput()
    code_gen(codeByte, code)
    codeLen = len(code)
    codeStr = ''.join(code)
    print('Your code for this instance is: ' + codeStr)
    print("Sending code to Arduino for verification...")
    for i in range(codeLen):
        ser.write(codeByte[i])
    time.sleep(10)
    while ser.inWaiting():
        var = ser.readline()[0:1]
        var = var.decode('utf-8')
        returned.append(var)
    try:
        checkVal = int(returned[0])
    except:
        print("You did not enter the correct number of values in the keypad.")
    if checkVal == len(code):
        print ("This code is correct! The door will now be unlocked.")
        print ("The scale is now active.")
    else:
        print ("This code is not correct.")
    scaleVals = []
    while ser.inWaiting():
        var = ser.readline()[0:1]
        var = var.decode('utf-8')
        scaleVals.append(var)
    cond = False
