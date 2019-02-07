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
import sqlite3
import uuid
from datetime import datetime

#connects to database
#Info stored: Transaction number in ascending order, random generated order ID,
#Buyer username, seller username, item name, date initialized, cost, location,
#order status, date in which data was last modified, date transaction resolves
def connect_OrderInfo_db():
    conn=sqlite3.connect("OrderInfo_Database.db")
    cur=conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS orderInfo (Order_num INTEGER\
                 PRIMARY KEY, ID TEXT, B_username TEXT, S_username TEXT, I_name\
                 TEXT, date_initialized TEXT, Cost REAL, Location TEXT,\
                 status TEXT, data_modified TEXT, date_resolved TEXT)")
    conn.commit()
    conn.close()

#connects to database
#connect_OrderInfo_db()

#Function uses values to add new order to SQLite3 database
def newOrder (S_username, B_username, I_name, Cost, Location):
    conn=sqlite3.connect("OrderInfo_Database.db")
    cur=conn.cursor()
    cur.execute("SELECT COUNT(Order_num) FROM orderInfo")
    ID = str(uuid.uuid4())
    date_init = str(datetime.now())
    date_resolved = (None)
    date_modified = str(datetime.now())
    status = "Initialized_sellerDrop_FALSE_buyerPickup_FALSE"
    #while check_dup_id(ID) == 1: #commented out due to redundancy
    #    ID = uuid.uuid4()
    cur.execute("INSERT INTO orderInfo VALUES(NULL, ?, ?, ?, ?, ?, ?, \
                ?, ?, ?, ?)", (ID, B_username, S_username, I_name, date_init,\
                Cost,Location, status, date_modified, date_resolved))
    conn.commit()
    conn.close()


#view Function
def view():
    conn=sqlite3.connect("OrderInfo_Database.db")
    cur=conn.cursor()
    cur.execute("SELECT * FROM orderInfo")
    rows = cur.fetchall()
    conn.close()
    return rows

#Searchable perameters
#Order number, TXID, Seller username, buyer username, item name,
#cost, location, date initialized
def search(ON=(None), TXID=(None), SUN=(None), BUN=(None), IN=(None),\
           Cost=(None), Loc=(None), DI=(None)):
    conn=sqlite3.connect("OrderInfo_Database.db")
    cur=conn.cursor()
    cur.execute("SELECT * FROM orderInfo WHERE Order_num=? OR ID=? OR\
                S_username=? OR B_username=? OR I_name=? OR Cost=? OR\
                Location=? OR date_initialized=?",\
                (ON, TXID, SUN, BUN, IN, Cost, Loc, DI))
    rows = cur.fetchall()
    conn.close()
    return rows

#delete function for selected record
def delete(id):
    conn=sqlite3.connect("OrderInfo_Database.db")
    cur=conn.cursor()
    cur.execute("DELETE FROM orderInfo WHERE Order_num=?", (id,))
    conn.commit()
    conn.close()


def update(SUN, BUN, IN, Cost, Loc, ID):
    conn=sqlite3.connect("OrderInfo_Database.db")
    cur=conn.cursor()
    cur.execute("UPDATE orderInfo SET S_username=?, B_username=?, I_name=?,\
                Cost=?, Location=?  WHERE ID=?",\
               (SUN, BUN, IN, Cost, Loc, ID))
    conn.commit()
    conn.close()


#newOrder("nchu6", "maximilianjohnson", "coffee", 1.00, "UBC ESC")
#print("New order logged. Thank you.")
#print(search())
