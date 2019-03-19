"""
A program that creates and connects to an SQL database for SafeDrop keypad codes
and can add new entries with this info:
buyer username, txid, seller username, who should be accessing the box,
which box, access codes, expiry times, attempt time, attempt status

"""
#Author: Maximilian Johnson
#Date: March 14th 2019

#Imports

import sys
sys.path.append('../')

from Order_Info.codelog_Backend import search_OrderValue
import psycopg2
from datetime import datetime
from random import randint

#connects to database
#Info stored: Transaction number in ascending order, random generated order ID,
#Buyer username, seller username, item name, date initialized, cost, location,
#order status, date in which data was last modified, date transaction resolves
def connect_codelog():
    conn=psycopg2.connect("dbname='SafeDrop_KeypadCode' user='postgres' password='postgre123' host='localhost' port = '5433'")
    cur=conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS codelog (id SERIAL, TXID TEXT, \
                 B_username TEXT, S_username TEXT, stage TEXT,\
                 box_id TEXT, access_code TEXT, expiry_time TEXT, attempt_time\
                 TEXT, seller_close_date TEXT, buyer_close_date TEXT)")
    conn.commit()
    conn.close()

#connects to database
#connect_chatlog()

#Function uses values to add new order to psycopg2 database
def newBoxAssignment(txid, box_id):
    connect_chatlog()
    conn=psycopg2.connect("dbname='SafeDrop_KeypadCode' user='postgres' password='postgre123' host='localhost' port = '5433'")
    cur=conn.cursor()
    B_username = search_OrderValue('B_username', txid = txid)
    S_username = search_OrderValue('S_username', txid = txid)
    stage = 'Seller Access'
    dates = None
    code = None
    cur.execute("INSERT INTO codelog VALUES(default, %s, %s, %s, %s, %s, %s,\
    %s, %s, %s, %s)", \
    (txid, B_username, S_username, stage, box_id, code, date, date, date, date))
    conn.commit()
    conn.close()

def codeGen(TXID):
    conn=psycopg2.connect("dbname='SafeDrop_KeypadCode' user='postgres' password='postgre123' host='localhost' port = '5433'")
    cur=conn.cursor()
    code = randint(100000, 999999)
    expiry = str((datetime.datetime.now()) + datetime.timedelta(minutes = 1))
    cur.execute("UPDATE codelog SET access_code=%s, expiry_time=%s \
                WHERE TXID=%s", (code, expiry, TXID))
    conn.commit()
    conn.close()
    return code

def search_ChatValue(column, txid):
    conn=psycopg2.connect("dbname='SafeDrop_KeypadCode' user='postgres' password='postgre123' host='localhost' port = '5433'")
    cur=conn.cursor()
    SQL = "SELECT " + column + " FROM users WHERE TXID=(%s)"
    data = (txid,)
    cur.execute(SQL, data)
    value = cur.fetchall()
    for item in value:
        return ("%s" % item)

#result = def boxResult()
def accessSet(result, txid):
    conn=psycopg2.connect("dbname='SafeDrop_KeypadCode' user='postgres' password='postgre123' host='localhost' port = '5433'")
    cur=conn.cursor()
    stage = search_ChatValue('stage', txid)
    if stage == 'Seller Access':
        if result == 'Success':
            date = datetime.datetime.now()
            cur.execute("UPDATE codelog SET access_code=%s, expiry_time=%s, \
                        seller_close_date=%s, stage=%s WHERE TXID=%s",\
                       (None, None, date, 'Buyer Access', txid))
        else:
            cur.execute("UPDATE codelog SET access_code=%s, expiry_time=%s, \
                        seller_close_date=%s, stage=%s WHERE TXID=%s",\
                       (None, None, None, 'Seller Access', txid))

    elif stage == 'Buyer Access':
        if result == 'Success':
            date = datetime.datetime.now()
            cur.execute("UPDATE codelog SET access_code=%s, expiry_time=%s, \
                        buyer_close_date=%s, stage=%s WHERE TXID=%s",\
                       (None, None, date, 'Complete', txid))

        elif result == 'Return':
            cur.execute("UPDATE codelog SET access_code=%s, expiry_time=%s, \
                        buyer_close_date=%s, stage=%s WHERE TXID=%s",\
                       (None, None, date, 'Return', txid))

        elif result == 'False Return':
            cur.execute("UPDATE codelog SET access_code=%s, expiry_time=%s, \
                        buyer_close_date=%s, stage=%s WHERE TXID=%s",\
                       (None, None, date, 'False Return', txid))
        else:
            cur.execute("UPDATE codelog SET access_code=%s, expiry_time=%s, \
                        buyer_close_date=%s, stage=%s WHERE TXID=%s",\
                       (None, None, None, 'Buyer Access', txid))

#can be adjusted to send unlock signal
def codeResult(txid, input_code):
    conn=psycopg2.connect("dbname='SafeDrop_KeypadCode' user='postgres' password='postgre123' host='localhost' port = '5433'")
    cur=conn.cursor()
    time = datetime.datetime.now()
    expiry = search_ChatValue('expiry_time', txid)
    if expiry < time:
        return "Error. The timer has expired, please request another code."
    else:
        box_code = search_ChatValue('access_code', txid)
        if input_code == box_code:
            return "Success! You may now access your SafeDrop."
        else:
            "Error, you have entered an incorrect code."


#code_result = def codeResult()
#door_status = def doorStatus() linked to aurduino code, must be completed with box team
#scale_reads = def scaleReads() linked to aurduino code, must be completed with box team
#return = webpage button
def boxResult(txid, code_result, return = None, door_status, scale_reads):
    conn=psycopg2.connect("dbname='SafeDrop_KeypadCode' user='postgres' password='postgre123' host='localhost' port = '5433'")
    cur=conn.cursor()
    if stage == 'Buyer Access' and return != None:
        if scale_reads == 'Match' and door_status == 'Closed':
            returnProtocol(txid, returnStatus = True)
            return 'Return'
        else:
            returnProtocol(txid, returnStatus = False)
            return 'False Return'
    elif stage == 'Buyer Access' and return == None:
        if scale_reads == 'Empty' and door_status == 'Closed':
            return 'Success'
        elif scale_reads != 'Empty' and door_status == 'Closed':
            return 'Error. An item was left in the box'
        elif scale_reads == 'Empty' and door_status != 'Closed':
            return 'Error. The door was not properly closed'
        else:
            return 'Error'
    elif stage == 'Seller Access':
        if scale_reads == 'New Item' and door_status == 'Closed':
            return 'Success'
        elif scale_reads == 'Empty' and door_status == 'Closed':
            return 'Error. No item was placed'
        elif door_status != 'Closed':
            return 'Error. The door was not properly closed'
        else:
            return 'Error'

def requestCode(txid, user):
    stage = search_ChatValue('stage', txid)
    b_user = search_ChatValue('B_username', txid)
    s_user = search_ChatValue('S_username', txid)

    if stage == 'Buyer Access' and b_user == user:
        code = codeGen(txid)
        return code
    if stage == 'Seller Access' and s_user == user:
        code = codeGen(txid)
        return code
    else:
        return 'You cannot request a code for this transaction. ' \
        + stage + 'only.'

def returnProtocol(txid, returnStatus):
    sad
