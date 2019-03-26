import sys
sys.path.append('../')

import serial #Imports PySerial for sending information to and from Arduino.
import time #Imports time.
import random # imports function to generate random number.
import struct
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, update
from sqlalchemy.orm import sessionmaker
import psycopg2
import datetime
from random import randint
from flask import Flask

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://nldxvejqlwiaav:adc8a0817b8f7be358af1e9e8e8833f08ba79e15ef380f8e5bf453b9a7ce2288@ec2-184-72-238-22.compute-1.amazonaws.com:5432/d8q8hsqf239vo8?sslmode=require'
app.config['SECRET_KEY'] = 'thisissecret'

db = SQLAlchemy(app)

def codeGen():
    user = Data.query.filter_by(TXID = 'demo').first()

    code = randint(100000, 999999)
    user.access_code = code
    expiry = (datetime.datetime.now()) + datetime.timedelta(minutes = 1)
    user.expiry_time = expiry
    db.session.commit()
    return code

def codeGet():
    user = Data.query.filter_by(TXID = 'demo').first()

    code = user.access_code

    return code

#code = codeGet()
#print(code)

def attemptCode(code, txid):
    user = Data.query.filter_by(TXID = txid).first()
    date = datetime.datetime.now()
    user.code_attempt = code
    user.attempt_time = date
    db.session.commit()

def codeResult(txid):
    user = Data.query.filter_by(TXID = txid).first()
    time = datetime.datetime.now()
    expiry = user.expiry_time
    datetime_expiry = datetime.datetime.strptime(expiry, "%Y-%m-%d %H:%M:%S.%f")
    input_code = user.code_attempt
    if datetime_expiry < time:
        return "Error. The timer has expired, please request another code."
    else:
        box_code = user.access_code
        if input_code == box_code:
            return "Success! You may now access your SafeDrop."
        else:
            return "Error, you have entered an incorrect code."

def writeToScaleDoor(txid, door_status = None, scale_status = None):
    user = Data.query.filter_by(TXID = txid).first()

    if door_status != None:
        user.door_status = door_status
    if scale_status != None:
        user.scale_status = scale_status
    db.session.commit()

def search_ChatValue(column, txid):
    user = Data.query.filter_by(TXID = txid).first()
    data = user.column
    return data


def txnStage(stage, buyOrSell): #0 for seller, 1 for buyer
    if (stage == "Seller Access"):
        buyOrSell = '0'
    else:
        buyOrSell = '1'
    return buyOrSell

ser = serial.Serial("COM4",9600) #COM4 is the port for the Arduino. Change to appropriate port on your computer. Second number is baudrate. Match to rate in Arduino.
time.sleep(2) #Adds 5 second delay before Python starts searching for a signal from the Arduino.
writeToScaleDoor('demo', scale_status ='0')
writeToScaleDoor('demo', door_status ='0')
buyOrSell = '0'
codeStr = ''
cond = True
codeGen() #Generate a new door code


while cond == True:
    print('here')
    weightList = []
    sellWeight = ''
    itemStatus = 0
    byteLen = 0
    var = ''
    #doorStatus = search_ChatValue("door_status","demo")
    buyWeight = search_ChatValue("scale_status","demo") #string
    stage = search_ChatValue("stage", "demo")
    txStage = txnStage(stage, buyOrSell) #0/1 string
    print(txStage)
    if txStage == '0':
        genCode = search_ChatValue("access_code","demo") #Find the value in the database table
        if (ser.inWaiting() != 0):
            for i in len(6):
                codeDigit = ser.readline()
                codeDigit = var.decode("utf-8")
                fullCode[i] = codeDigit
            codeStr = ''.join(fullCode)
            print(codeStr)
        attemptCode(codeStr, "demo") #check the entered code against the database code
        doorVer = codeResult("demo") #Check if the code was correct
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
            writeToScaleDoor('demo', scale_status = sellWeight)
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
