"""
A program that creates and connects to an SQL database for SafeDrop keypad codes
and can add new entries with this info:
buyer username, txid, seller username, who should be accessing the box,
which box, access codes, expiry times, attempt time, attempt status

"""
#Author: Andrew Moreno
#Date: April 3rd, 2019

#Imports
import sys
sys.path.append('../')

from Order_Info.OrderInfo_Backend import search_OrderValue, statusUpdate
from safebucks.currency import completeMoneyTransfer
import psycopg2
import datetime
from random import randint
import json
from flask import Flask, render_template, redirect, url_for, request, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, update, or_
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgre123@\
localhost:5432/SafeDrop_KeypadCode'
app.config['SECRET_KEY'] = 'thisissecret'

db = SQLAlchemy(app)

#connects to database
#Info stored: Transaction number in ascending order, random generated order ID,
#Buyer username, seller username, item name, date initialized, cost, location,
#order status, date in which data was last modified, date transaction resolves

class ConnectData(db.Model):
    __tablename__="codelog"
    id = db.Column(db.Integer, primary_key = True)
    TXID = db.Column(db.String(254))
    B_username = db.Column(db.String(64))
    S_username = db.Column(db.String(64))
    stage = db.Column(db.String(128))
    box_id = db.Column(db.String(128))
    access_code = db.Column(db.String(64))
    expiry_time = db.Column(db.String(128))
    code_attempt = db.Column(db.String(64))
    attempt_time = db.Column(db.String(128))
    seller_close_date = db.Column(db.String(128))
    buyer_close_date = db.Column(db.String(128))
    door_status = db.Column(db.String(64))
    scale_status = db.Column(db.String(64))
    scale_delta = db.Column(db.String(64))
    in_box_image_url = db.Column(db.String(254))


def newBoxAssignment(txid, box_id):
    B_username = search_OrderValue('B_username', txid = txid)
    S_username = search_OrderValue('S_username', txid = txid)
    stage = 'Seller Access'
    date = None
    code = None
    status = None
    new_entry = ConnectData(TXID = txid, B_username = B_username, \
        S_username = S_username, stage = stage, box_id = box_id, \
        access_code = code, expiry_time = date, code_attempt = code, attempt_time = date, seller_close_date = date, \
        buyer_close_date = date, door_status = status, scale_status = status, scale_delta = status)
    db.session.add(new_entry)
    db.session.commit()
    db.session.close()

def codeGen(TXID):
    code = randint(100000, 999999)
    expiry = datetime.datetime.now() + datetime.timedelta(minutes = 1)
    row = ConnectData.query.filter_by(TXID = TXID).first()
    row.access_code = code
    row.expiry_time = expiry
    db.session.commit()
    db.session.close()
    return code

def search_ChatValue(column, txid):
    row = ConnectData.query.filter_by(TXID = txid).first()
    search = getattr(row, column)
    db.session.close()
    return search

def attemptCode(code, txid):
    date = datetime.datetime.now()
    row = ConnectData.query.filter_by(TXID = txid).first()
    row.attempt_time = date
    row.code_attempt = code
    db.session.commit()
    db.session.close()

def writeToScaleDoor(txid, door_status = None, scale_status = None, stage = None):
    if door_status != None:
        row = ConnectData.query.filter_by(TXID = txid).first()
        row.door_status = door_status
    if scale_status != None:
        row = ConnectData.query.filter_by(TXID = txid).first()
        row.scale_status = scale_status
    if stage != None:
        row = ConnectData.query.filter_by(TXID = txid).first()
        row.stage = stage
    db.session.commit()
    db.session.close()

#result = def boxResult()
def accessSet(result, txid):
    stage = search_ChatValue('stage', txid)
    if stage == 'Seller Access':
        if result == 'Success':
            date = datetime.datetime.now()
            row = ConnectData.query.filter_by(TXID = txid)
            row.access_code = None
            row.expiry_time = None
            row.seller_close_date = date
            row.stage = 'Buyer Access'

        else:
            row = ConnectData.query.filter_by(TXID = txid)
            row.access_code = None
            row.expiry_time = None
            row.seller_close_date = None
            row.stage = 'Seller Access'

    elif stage == 'Buyer Access':
        if result == 'Success':
            date == datetime.datetime.now()
            row = ConnectData.query.filter_by(TXID = txid)
            row.access_code = None
            row.expiry_time = None
            row.buyer_close_date = date
            row.stage = 'Complete'

        elif result == 'Return':
            row = ConnectData.query.filter_by(TXID = txid)
            row.access_code = None
            row.expiry_time = None
            row.buyer_close_date = date
            row.stage = 'Return'

        elif result == 'False Return':
            row = ConnectData.query.filter_by(TXID = txid)
            row.access_code = None
            row.expiry_time = None
            row.buyer_close_date = date
            row.stage = 'False Return'

        else:
            row = ConnectData.query.filter_by(TXID = txid)
            row.access_code = None
            row.expiry_time = None
            row.buyer_close_date = None
            row.stage = 'Buyer Access'

    db.session.commit()
    db.session.close()

#can be adjusted to send unlock signal
def codeResult(txid):
    time = datetime.datetime.now()
    expiry = search_ChatValue('expiry_time', txid)
    datetime_expiry = datetime.datetime.strptime(expiry, "%Y-%m-%d %H:%M:%S.%f")
    input_code = search_ChatValue('code_attempt', txid)
    if datetime_expiry < time:
        db.session.close()
        return "Error. The timer has expired, please request another code."
    else:
        box_code = search_ChatValue('access_code', txid)
        if input_code == box_code:
            db.session.close()
            return "Success! You may now access your SafeDrop."
        else:
            db.session.close()
            return "Error, you have entered an incorrect code."

#code_result = def codeResult()
#door_status = def doorStatus() linked to aurduino code, must be completed with box team
#scale_reads = def scaleReads() linked to aurduino code, must be completed with box team
#return = webpage button
def boxResult(txid, return_status = None):
    scale_reads = search_ChatValue('scale_status', txid)
    door_status = search_ChatValue('door_status', txid)
    if stage == 'Buyer Access' and return_status != None:
        if scale_reads == 'Match' and door_status == 'Closed':
            returnProtocol(txid, returnStatus = True)
            return 'Returned'
        else:
            returnProtocol(txid, returnStatus = False)
            return 'False Return'
    elif stage == 'Buyer Access' and return_status == None:
        if scale_reads == 'Empty' and door_status == 'Closed':
            return 'Full Success'
        elif scale_reads != 'Empty' and door_status == 'Closed':
            return 'Error. An item was left in the box'
        elif scale_reads == 'Empty' and door_status != 'Closed':
            return 'Error. The door was not properly closed'
        else:
            return 'Error'
    elif stage == 'Seller Access':
        if scale_reads == 'New Item' and door_status == 'Closed':
            return 'Half Success'
        elif scale_reads == 'Empty' and door_status == 'Closed':
            return 'Error. No item was placed'
        elif door_status != 'Closed':
            return 'Error. The door was not properly closed'
        else:
            return 'Error'

def endofTXProtocol(txid, returnStatus):
    txResult = boxResult(txid, returnStatus)
    writeToScaleDoor(txid, stage = txResult)
    if txResult == 'Full Success':
        completeMoneyTransfer(txid)
        statusUpdate("TRANSACTION COMPLETE", txid)
    elif txResult == 'Returned':
        statusUpdate("ITEM RETURNED", txid)
    elif txResult == 'False Return':
        completeMoneyTransfer(txid)
        statusUpdate("FALSE RETURN")

def dropStatus(txid, user, msg = None, status = None):
    drop_status = search_OrderValue('status', txid = txid)
    b_user = search_OrderValue('B_username', txid = txid)
    s_user = search_OrderValue('S_username', txid = txid)
    if drop_status == "Buyer_Seller_TX_Confirm":
        confirm_msg = "Sale Confirmed!"
        tx_status = "Buyer_Seller_TX_Confirm"

    elif drop_status == "ITEM RETURNED":
        confirm_msg = "The item has been successfully returned by the buyer."
        tx_status = "ITEM RETURNED"

    elif drop_status == "FALSE RETURN":
        confirm_msg = "The buyer attempted a false return, transaction completed."
        tx_status = "ITEM FALSE RETURNED"

    elif drop_status == "TRANSACTION COMPLETE":
        confirm_msg = "Transaction complete!"
        tx_status = "TRANSACTION COMPLETE"

    else:
        if user == b_user:

            if drop_status == "Buyer_TX_Confirm":
                confirm_msg = 'Awaiting seller confirmation.'
                tx_status = "Buyer_TX_Confirm"

            elif drop_status == "Seller_TX_Confirm":
                confirm_msg = 'Confirm Buy.'
                tx_status = "Buyer_Seller_TX_Confirm"


            elif drop_status == 'None':
                confirm_msg = 'Confirm Buy.'
                tx_status = 'Buyer_TX_Confirm'


        elif user == s_user:

            if drop_status == "Seller_TX_Confirm":
                confirm_msg = 'Awaiting buyer confirmation.'
                tx_status = 'Seller_TX_Confirm'

            elif drop_status == "Buyer_TX_Confirm":
                confirm_msg = 'Confirm Sale.'
                tx_status = "Buyer_Seller_TX_Confirm"

            elif drop_status == 'None':
                confirm_msg = 'Confirm Sale.'
                tx_status = 'Seller_TX_Confirm'

    if msg == True:
        return confirm_msg
    elif status == True:
        return tx_status

def requestCode(txid, user):
    stage = str(search_ChatValue('stage', txid))
    b_user = search_ChatValue('B_username', txid)
    s_user = search_ChatValue('S_username', txid)
    if stage == 'Buyer Access' and b_user == user:
        code = codeGen(txid)
        return code
    elif stage == 'Seller Access' and s_user == user:
        code = codeGen(txid)
        return code
    elif stage == 'None':
        return 'The transaction must be confirmed first.'
    else:
        return 'You cannot request a code for this transaction. ' \
        + stage + ' only.'
