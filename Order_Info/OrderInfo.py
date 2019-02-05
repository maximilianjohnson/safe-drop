#Imports
import uuid
from datetime import datetime
import sqlite3
#Create database
def create_OrderInfo_db():
    conn=sqlite3.connect("OrderInfo_Database.db") #UP.db = user_profile.db
    cur=conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS orderInfo (Order_num INTEGER, ID TEXT, B_username TEXT, S_username TEXT, I_name TEXT, date_initialized TEXT, Cost REAL, Location TEXT, status TEXT, data_modified TEXT, date_resolved TEXT)")
    conn.commit()
    conn.close()

#Create database
#create_OrderInfo_db()

#view Function
def view():
    conn=sqlite3.connect("OrderInfo_Database.db") #UP.db = user_profile.db
    cur=conn.cursor()
    cur.execute("SELECT * FROM orderInfo")
    rows = cur.fetchall()
    conn.close()
    return rows
#Function uses values to add new order to database
def newOrder (S_username, B_username, I_name, Cost, Location):
    conn=sqlite3.connect("OrderInfo_Database.db") #UP.db = user_profile.db
    cur=conn.cursor()
    cur.execute("SELECT COUNT(Order_num) FROM orderInfo")
    Order_num = cur.fetchone()[0]
    print(type(Order_num))
    ID = str(uuid.uuid4())
    date_init = str(datetime.now())
    date_resolved = (None)
    date_modified = str(datetime.now())
    status = "Initialized_sellerDrop_FALSE_buyerPickup_FALSE"
    #while check_dup_id(ID) == 1: #commented out due to redundancy
    #    ID = uuid.uuid4()
    cur.execute("INSERT INTO orderInfo VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (Order_num, ID, B_username, S_username, I_name, date_init, Cost, Location, status, date_modified, date_resolved))
    conn.commit()
    conn.close()

#prototype using cmd line inputs
#n1 = input("Enter Seller's Name: ")
#n2 = input("Enter Buyer's Name: ")
#i1 = input("Enter Item Name: ")
#c1 = input("Enter Cost: ")
#l1 = input("Enter Location: ")

#newOrder(n1, n2, i1, c1, l1)
#print("New order logged. Thank you.")
#print(view())
