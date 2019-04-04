"""
A program that creates and connects to an SQL database for new SafeDrop orders
and can add new entries with this info:
Transaction number in ascending order, random generated order ID,
Buyer username, seller username, item name, date initialized, cost, location,
order status, date in which data was last modified, date transaction resolves

"""
#FOR PROTOTYPING ONLY, TO BE EXPANDED UPON FOR WEB INTEGRATION/POSTGRESQL
#Author: Maximilian Johnson
#Date: Feb 6th

#Imports
import json
from flask import Flask, render_template, redirect, url_for, request, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, update, or_
from sqlalchemy.sql.expression import func
from sqlalchemy.orm import sessionmaker
import psycopg2
import uuid
from datetime import datetime

#connects to database
#Info stored: Transaction number in ascending order, random generated order ID,
#Buyer username, seller username, item name, date initialized, cost, location,
#order status, date in which data was last modified, date transaction resolves

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgre123@\
localhost:5432/SafeDrop_Orders'
app.config['SECRET_KEY'] = 'thisissecret'

db = SQLAlchemy(app)

"""
def connect_OrderInfo_db():
    conn=psycopg2.connect("dbname='SafeDrop_Orders' user='postgres' password='postgre123' host='localhost' port = '5432'")
    cur=conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS orderInfo (id SERIAL, TXID TEXT, \
                 B_username TEXT, S_username TEXT, I_name TEXT, description\
                 TEXT, date_initialized TEXT, Cost REAL, Location TEXT,\
                 status TEXT, img_url SERIAL, data_modified TEXT, date_resolved TEXT)")
    conn.commit()
    conn.close()
"""

class DataOrders(db.Model):
    __tablename__="orderInfo"
    id = db.Column(db.Integer, primary_key=True)
    TXID = db.Column(db.String(254))
    B_username = db.Column(db.String(64))
    S_username = db.Column(db.String(64))
    I_name = db.Column(db.String(128))
    description = db.Column(db.String(1500))
    date_initialized = db.Column(db.String(128))
    Cost = db.Column(db.Float)
    Location = db.Column(db.String(64))
    status = db.Column(db.String(128))
    img_url = db.Column(db.String(24))
    date_resolved = db.Column(db.String(128))

#connects to database
#connect_OrderInfo_db()
def newOrder(S_username, B_username, I_name, desc, Cost, Location, img_url=None):
    TXID = str(uuid.uuid4())
    date_init = str(datetime.now())
    date_resolved = 'None'
    status = 'None'
    if img_url != None:
        newOrderEntry = DataOrders(TXID=TXID, B_username=B_username,\
        S_username=S_username, I_name=I_name, description=desc, date_initialized=date_init,\
        Cost=Cost, Location=Location, status=status, date_resolved=date_resolved, img_url=img_url)
        db.session.add(newOrderEntry)
        db.session.commit()
        db.session.close()

    else:
        newOrderEntry = DataOrders(TXID=TXID, B_username=B_username,\
        S_username=S_username, I_name=I_name, description=desc, date_initialized=date_init,\
        Cost=Cost, Location=Location, status=status, date_resolved=date_resolved, img_url="None")
        db.session.add(newOrderEntry)
        db.session.commit()
        row = DataOrders.query.filter_by(TXID=TXID).first()
        serial=row.id
        row.img_url=str(serial)
        db.session.commit()
        db.session.close()
    return TXID
'''
#Function uses values to add new order to psycopg2 database
def newOrder (S_username, B_username, I_name, desc, Cost, Location, img_url=None):
    connect_OrderInfo_db()
    conn=psycopg2.connect("dbname='SafeDrop_Orders' user='postgres' password='postgre123' host='localhost' port = '5432'")
    cur=conn.cursor()
    TXID = str(uuid.uuid4())
    date_init = str(datetime.now())
    date_resolved = 'None'
    date_modified = str(datetime.now())
    status = 'None'
    #while check_dup_id(ID) == 1: #commented out due to redundancy
    #    ID = uuid.uuid4()
    if img_url == None:
        cur.execute("INSERT INTO orderInfo VALUES(default, %s, %s, %s, %s, %s, %s, %s, \
                    %s, %s, default, %s, %s)", (TXID, B_username, S_username, I_name, desc, \
                    date_init, Cost, Location, status, date_modified, date_resolved))
    else:
        cur.execute("INSERT INTO orderInfo VALUES(default, %s, %s, %s, %s, %s, %s, %s, \
                    %s, %s, %s, %s, %s)", (TXID, B_username, S_username, I_name, desc, \
                    date_init, Cost, Location, status, img_url, date_modified, date_resolved))
    conn.commit()
    conn.close()
    return TXID
'''

'''
#view Function
def view():
    conn=psycopg2.connect("dbname='SafeDrop_Orders' user='postgres' password='postgre123' host='localhost' port = '5432'")
    cur=conn.cursor()
    cur.execute("SELECT * FROM orderInfo")
    rows = cur.fetchall()
    conn.close()
    return rows
'''

#Searchable perameters
#Order number, TXID, Seller username, buyer username, item name,
#cost, location, date initialized
def search_allOrders(id=(None), TXID=(None), SUN=(None), BUN=(None), IN=(None),\
           Cost=(None), Loc=(None), DI=(None)):
    rows = DataOrders.query.filter(or_(DataOrders.id==id, DataOrders.TXID==TXID, DataOrders.S_username==SUN,\
    DataOrders.B_username==BUN, DataOrders.I_name==IN, DataOrders.Cost==Cost, DataOrders.Location==Loc, DataOrders.date_initialized==DI))
    db.session.close()
    return rows

'''
def search_allOrders(id=(None), TXID=(None), SUN=(None), BUN=(None), IN=(None),\
           Cost=(None), Loc=(None), DI=(None)):
    conn=psycopg2.connect("dbname='SafeDrop_Orders' user='postgres' password='postgre123' host='localhost' port = '5432'")
    cur=conn.cursor()
    cur.execute("SELECT * FROM orderInfo WHERE id=%s OR TXID=%s OR\
                S_username=%s OR B_username=%s OR I_name=%s OR Cost=%s OR\
                Location=%s OR date_initialized=%s",\
                (id, TXID, SUN, BUN, IN, Cost, Loc, DI))
    rows = cur.fetchall()
    conn.close()
    return rows
'''
def search_OrderValue(column, txid=None, recent=None, S_username=None, B_username=None):
    if recent != None:
        maxrow = DataOrders.query.filter_by(func.max(id))
        row = str(maxrow[0])
        row = row[1:2]
        row = int(row)
        row = row - recent
        rowdata = DataOrders.query.filter_by(id=row)
        value = getattr(rowdata, column)
        db.session.close()
        return value
    if txid != None:
        rowdata = DataOrders.query.filter_by(TXID=txid).first()
        value = getattr(rowdata, column)
        db.session.close()
        return value
    if S_username != None:
        rowdata = DataOrders.query.filter_by(S_username=S_username).all()
        valuearray = []
        for item in rowdata:
            value = item.TXID
            valuearray.append(value)
        db.session.close()
        return valuearray
    if B_username != None:
        rowdata = DataOrders.query.filter_by(B_username=B_username).all()
        valuearray = []
        for item in rowdata:
            value = item.TXID
            valuearray.append(value)
        db.session.close()
        return valuearray


'''
#function to search specific value in an order
def search_OrderValue(column, txid=None, recent=None, S_username=None, B_username=None):
    connect_OrderInfo_db()
    conn=psycopg2.connect("dbname='SafeDrop_Orders' user='postgres' password='postgre123' host='localhost' port = '5432'")
    cur=conn.cursor()
    if recent != None:
        cur.execute('SELECT MAX(id) FROM orderInfo')
        count = cur.fetchall()
        row = str(count[0])
        row = row[1:2]
        row = int(row)
        row = row - recent
        SQL = "SELECT " + column + " FROM orderInfo WHERE id=(%s)"
        data = (row,)
        cur.execute(SQL, data)
        value = cur.fetchall()
        for item in value:
            return ("%s" % item)
    if txid != None:
        SQL = "SELECT " + column + " FROM orderInfo WHERE TXID=(%s)"
        data = (txid,)
        cur.execute(SQL, data)
        value = cur.fetchall()
        for item in value:
            return ("%s" % item)
    if S_username != None:
        SQL = "SELECT " + column + " FROM orderInfo WHERE S_username=(%s)"
        data = (S_username,)
        cur.execute(SQL, data)
        value = cur.fetchall()
        return value
    if B_username != None:
        SQL = "SELECT " + column + " FROM orderInfo WHERE B_username=(%s)"
        data = (B_username,)
        cur.execute(SQL, data)
        value = cur.fetchall()
        return value
'''

def deleteOrder(txid):
    DataOrders.query.filter_by(TXID=txid).delete()
    db.session.commit()
    db.session.close()

'''
#delete function for selected record
def deleteOrder(txid):
    conn=psycopg2.connect("dbname='SafeDrop_Orders' user='postgres' password='postgre123' host='localhost' port = '5432'")
    cur=conn.cursor()
    cur.execute("DELETE FROM orderInfo WHERE txid=%s", (txid,))
    conn.commit()
    conn.close()
'''
def confirmBuyer(BUN, ID):
    rowdata = DataOrders.query.filter_by(TXID=ID).first()
    rowdata.B_username = BUN
    db.session.commit()
    db.session.close()

'''
def confirmBuyer(BUN, ID):
    connect_OrderInfo_db()
    conn=psycopg2.connect("dbname='SafeDrop_Orders' user='postgres' password='postgre123' host='localhost' port = '5432'")
    cur=conn.cursor()
    cur.execute("UPDATE orderInfo SET B_username=%s WHERE TXID=%s",
               (BUN, ID))
    conn.commit()
    conn.close()
'''
'''
def update(SUN, BUN, IN, desc, Cost, Loc, TXID):
    conn=psycopg2.connect("dbname='SafeDrop_Orders' user='postgres' password='postgre123' host='localhost' port = '5432'")
    cur=conn.cursor()
    cur.execute("UPDATE orderInfo SET S_username=%s, B_username=%s, I_name=%s,\
                description=%s, Cost=%s, Location=%s  WHERE TXID=%s",\
               (SUN, BUN, IN, desc, Cost, Loc, TXID))
    conn.commit()
    conn.close()
'''
def statusUpdate(status, TXID):
    rowdata = DataOrders.query.filter_by(TXID=TXID).first()
    rowdata.status = status
    db.session.commit()
    db.session.close()

'''
def statusUpdate(status, TXID):
    connect_OrderInfo_db()
    conn=psycopg2.connect("dbname='SafeDrop_Orders' user='postgres' password='postgre123' host='localhost' port = '5432'")
    cur=conn.cursor()
    cur.execute("UPDATE orderInfo SET status=%s WHERE TXID=%s",\
               (status, TXID))
    conn.commit()
    conn.close()
'''

def repostOffer(txid):
    S_username = search_OrderValue('S_username', txid=txid)
    B_username = 'None'
    I_name = search_OrderValue('I_name', txid=txid)
    desc = search_OrderValue('description', txid=txid)
    Cost = search_OrderValue('Cost', txid=txid)
    Location = search_OrderValue('Location', txid=txid)
    img_url = search_OrderValue('img_url', txid=txid)
    newOrder (S_username, B_username, I_name, desc, Cost, Location, img_url=img_url)
    deleteOrder(txid)

def browseRecent():
    value = DataOrders.query.filter_by(B_username='None').all()
    value = reversed(value)
    value = tuple(value)
    db.session.close()
    return value

'''
def browseRecent():
    connect_OrderInfo_db()
    conn=psycopg2.connect("dbname='SafeDrop_Orders' user='postgres' password='postgre123' host='localhost' port = '5432'")
    cur=conn.cursor()
    cur.execute("SELECT * FROM orderInfo WHERE B_username='None'")
    value = cur.fetchall()
    value = reversed(value)
    value = tuple(value)
    return value
'''

#connect_OrderInfo_db()
#newOrder("nchu6", "maximilianjohnson", "coffee", "cuppa joe", 1.00, "UBC ESC")
#newOrder("ajm", "lmaooo", "coffee", "also cuppa joe", 2.00, "UBC ESC")
#print("New order logged. Thank you.")
#print(search())
