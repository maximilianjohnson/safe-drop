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
cond = True

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
    txStage = txnStage(stage, buyOrSell) #0/1 string'
    print(txStage)
    if txStage == '0':
        if ser.inWaiting() != 0:
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
            print("No data is currently being sent.")

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
            print("No data is currently being sent.")
