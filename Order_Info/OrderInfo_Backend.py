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
import psycopg2
import uuid
from datetime import datetime

#connects to database
#Info stored: Transaction number in ascending order, random generated order ID,
#Buyer username, seller username, item name, date initialized, cost, location,
#order status, date in which data was last modified, date transaction resolves
def connect_OrderInfo_db():
    conn=psycopg2.connect("dbname='SafeDrop_Orders' user='postgres' password='postgre123' host='localhost' port = '5433'")
    cur=conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS orderInfo (id SERIAL, TXID TEXT, \
                 B_username TEXT, S_username TEXT, I_name TEXT, description\
                 TEXT, date_initialized TEXT, Cost REAL, Location TEXT,\
                 status TEXT, data_modified TEXT, date_resolved TEXT)")
    conn.commit()
    conn.close()

#connects to database
#connect_OrderInfo_db()

#Function uses values to add new order to psycopg2 database
def newOrder (S_username, B_username, I_name, desc, Cost, Location):
    connect_OrderInfo_db()
    conn=psycopg2.connect("dbname='SafeDrop_Orders' user='postgres' password='postgre123' host='localhost' port = '5433'")
    cur=conn.cursor()
    TXID = str(uuid.uuid4())
    date_init = str(datetime.now())
    date_resolved = (None)
    date_modified = str(datetime.now())
    status = "Initialized_sellerDrop_FALSE_buyerPickup_FALSE"
    #while check_dup_id(ID) == 1: #commented out due to redundancy
    #    ID = uuid.uuid4()
    cur.execute("INSERT INTO orderInfo VALUES(default, %s, %s, %s, %s, %s, %s, %s, \
                %s, %s, %s, %s)", (TXID, B_username, S_username, I_name, desc, \
                date_init, Cost,Location, status, date_modified, date_resolved))
    conn.commit()
    conn.close()


#view Function
def view():
    conn=psycopg2.connect("dbname='SafeDrop_Orders' user='postgres' password='postgre123' host='localhost' port = '5433'")
    cur=conn.cursor()
    cur.execute("SELECT * FROM orderInfo")
    rows = cur.fetchall()
    conn.close()
    return rows

#Searchable perameters
#Order number, TXID, Seller username, buyer username, item name,
#cost, location, date initialized
def search(id=(None), TXID=(None), SUN=(None), BUN=(None), IN=(None),\
           Cost=(None), Loc=(None), DI=(None)):
    conn=psycopg2.connect("dbname='SafeDrop_Orders' user='postgres' password='postgre123' host='localhost' port = '5433'")
    cur=conn.cursor()
    cur.execute("SELECT * FROM orderInfo WHERE id=%s OR TXID=%s OR\
                S_username=%s OR B_username=%s OR I_name=%s OR Cost=%s OR\
                Location=%s OR date_initialized=%s",\
                (ON, TXID, SUN, BUN, IN, Cost, Loc, DI))
    rows = cur.fetchall()
    conn.close()
    return rows

#function to search specific value in an order
def search_OrderValue(column, txid=None, recent=None):
    conn=psycopg2.connect("dbname='SafeDrop_Orders' user='postgres' password='postgre123' host='localhost' port = '5433'")
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

#delete function for selected record
def delete(id):
    conn=psycopg2.connect("dbname='SafeDrop_Orders' user='postgres' password='postgre123' host='localhost' port = '5433'")
    cur=conn.cursor()
    cur.execute("DELETE FROM orderInfo WHERE id=%s", (id,))
    conn.commit()
    conn.close()

def confirmBuyer(BUN, ID):
    conn=psycopg2.connect("dbname='SafeDrop_Orders' user='postgres' password='postgre123' host='localhost' port = '5433'")
    cur=conn.cursor()
    cur.execute("UPDATE orderInfo SET B_username=%s WHERE TXID=%s",
               (BUN, ID))
    conn.commit()
    conn.close()

def update(SUN, BUN, IN, desc, Cost, Loc, ID):
    conn=psycopg2.connect("dbname='SafeDrop_Orders' user='postgres' password='postgre123' host='localhost' port = '5433'")
    cur=conn.cursor()
    cur.execute("UPDATE orderInfo SET S_username=%s, B_username=%s, I_name=%s,\
                description=%s, Cost=%s, Location=%s  WHERE ID=%s",\
               (SUN, BUN, IN, desc, Cost, Loc, ID))
    conn.commit()
    conn.close()

#connect_OrderInfo_db()
#newOrder("nchu6", "maximilianjohnson", "coffee", "cuppa joe", 1.00, "UBC ESC")
#print("New order logged. Thank you.")
#print(search())
