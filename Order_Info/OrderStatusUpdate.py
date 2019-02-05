import sqlite3
from datetime import datetime
from tkinter import *
#view function for testing
def view():
    conn=sqlite3.connect("OrderInfo_Database.db") #UP.db = user_profile.db
    cur=conn.cursor()
    cur.execute("SELECT * FROM orderInfo")
    rows = cur.fetchall()
    conn.close()
    return rows

#Function to change status of order.
def status_change(status_code):
    status_codes = ["Initialized_sellerDrop_FALSE_buyerPickup_FALSE", "Initialized_sellerDrop_TRUE_buyerPickup_FALSE", "Initialized_sellerDrop_ERROR_buyerPickup_FALSE", "Initialized_sellerDrop_TRUE_buyerPickup_TRUE", "Initialized_sellerDrop_TRUE_buyerPickup_ERROR", "Completed_sellerDrop_TRUE_buyerPickup_TRUE_return_FALSE", "Completed_sellerDrop_TRUE_buyerPickup_TRUE_return_TRUE_transactionReversed", "Completed_sellerDrop_TRUE_buyerPickup_TRUE_returnInconsitancy_MANUAL_REVIEW_REQUIRED", "TRANSACTION_ERROR_MANUAL_REVIEW_REQUIRED", "SYSTEM_ERROR"]
    #status_codes with list numbers = [(0)"Initialized_sellerDrop_FALSE_buyerPickup_FALSE", (1)"Initialized_sellerDrop_TRUE_buyerPickup_FALSE", (2)"Initialized_sellerDrop_ERROR_buyerPickup_FALSE", (3)"Initialized_sellerDrop_TRUE_buyerPickup_TRUE", (4)"Initialized_sellerDrop_TRUE_buyerPickup_ERROR", (5)"Completed_sellerDrop_TRUE_buyerPickup_TRUE_return_FALSE", (6)"Completed_sellerDrop_TRUE_buyerPickup_TRUE_return_TRUE_transactionReversed", (7)"Completed_sellerDrop_TRUE_buyerPickup_TRUE_returnInconsitancy_MANUAL_REVIEW_REQUIRED", (8)"TRANSACTION_ERROR_MANUAL_REVIEW_REQUIRED", (9)"SYSTEM_ERROR"]
    try:
        return status_codes[status_code]
    except IndexError:
        return "STATUS_CODE_INVALID"

def Database_Status_Update(status_code, ID):
    date_modified = str(datetime.now())
    conn=sqlite3.connect("OrderInfo_Database.db") #UP.db = user_profile.db
    cur=conn.cursor()
    cur.execute("UPDATE orderInfo SET status=?, data_modified=? WHERE ID =?", (status_change(status_code), date_modified, ID))
    conn.commit()
    conn.close()
