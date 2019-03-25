import sys
sys.path.append('../')

import serial #Imports PySerial for sending information to and from Arduino.
import time #Imports time.
import random # imports function to generate random number.
import struct
from safebox_connection.code_connect import search_ChatValue, writeToScaleDoor, newBoxAssignment,codeGen, attemptCode, codeResult

def txnStage(stage, buyOrSell): #0 for seller, 1 for buyer
    if (stage == "Seller Access"):
        buyOrSell = '0'
    else:
        buyOrSell = '1'
    return buyOrSell

ser = serial.Serial("COM4",9600) #COM4 is the port for the Arduino. Change to appropriate port on your computer. Second number is baudrate. Match to rate in Arduino.
time.sleep(2) #Adds 5 second delay before Python starts searching for a signal from the Arduino.
writeToScaleDoor('example', scale_status ='0')
writeToScaleDoor('example', door_status ='0')
buyOrSell = '0'
codeStr = ''
cond = True
codeGen("example") #Generate a new door code


while cond == True:
    print('here')
    weightList = []
    sellWeight = ''
    itemStatus = 0
    byteLen = 0
    var = ''
    #doorStatus = search_ChatValue("door_status","example")
    buyWeight = search_ChatValue("scale_status","example") #string
    stage = search_ChatValue("stage", "example")
    txStage = txnStage(stage, buyOrSell) #0/1 string
    print(txStage)
    if txStage == '0':
        genCode = search_ChatValue("access_code","example") #Find the value in the database table
        if (ser.inWaiting() != 0):
            for i in len(6):
                codeDigit = ser.readline()
                codeDigit = var.decode("utf-8")
                fullCode[i] = codeDigit
            codeStr = ''.join(fullCode)
            print(codeStr)
        attemptCode(codeStr, "example") #check the entered code against the database code
        doorVer = codeResult("example") #Check if the code was correct
        if (doorVer == "Success! You may now access your SafeDrop."):
            lockVer = 1
            ser.write(lockVer)
        '''if (ser.inWaiting() != 0 and lock = 1): # 1 = open for lock
            time.sleep(.5)
            len = ser.readline()[0:1]
            len = len.decode("utf-8")
            print(len)
            var = ser.readline()
            var = var.decode("utf-8")
            print(var)
            #weightList.append(var)
            #sellWeight = ''.join(weightList)
            #print(sellWeight)
            writeToScaleDoor('example', scale_status = sellWeight)
        else:
            time.sleep(.5)

    else:
        time.sleep(60)
        if (ser.inWaiting() != 0):
            while ser.inWaiting():
                var = ser.readline()[0:1]
                var = var.decode("utf-8")
                weightList.append(var)
            sellWeight = ''.join(code)
            buyWeight = int(buyWeight)
            sellWeight = int(sellWeight)
            if abs(buyWeight - sellWeight) < 30:
                itemStatus = 0
                print("Enjoy your purchase!")
            elif (sellWeight < 30):
                itemStatus = 1
                print("Thank you for returning the item!")
            else:
                print("You have attempted to steal from SafeDrop. ")
                print("Your life is now forfeit.")
        else:
            print("No data is currently being sent.")'''
