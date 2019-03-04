import psycopg2
from datetime import datetime

#view function for testing
def view():
    conn=psycopg2.connect("dbname='SafeDrop_Orders' user='postgres' password='postgre123' host='localhost' port = '5432'") #UP.db = user_profile.db
    cur=conn.cursor()
    cur.execute("SELECT * FROM orderInfo")
    rows = cur.fetchall()
    conn.close()
    return rows

#Function to change status of order.
def status_change(status_code):
    status_codes = ["Initialized_sellerDrop_FALSE_buyerPickup_FALSE", \
    "Initialized_sellerDrop_TRUE_buyerPickup_FALSE",\
    "Initialized_sellerDrop_ERROR_buyerPickup_FALSE",\
    "Initialized_sellerDrop_TRUE_buyerPickup_TRUE",\
    "Initialized_sellerDrop_TRUE_buyerPickup_ERROR",\
    "Completed_sellerDrop_TRUE_buyerPickup_TRUE_return_FALSE",\
    "Completed_sellerDrop_TRUE_buyerPickup_TRUE_return_TRUE_TX_Reversed",\
    "Completed_sellerDrop_TRUE_buyerPickup_TRUE_returnError_MRR",\
    "TRANSACTION_ERROR_MRR", "SYSTEM_ERROR"] #MRR = Manial Review Required

    #status_codes with list numbers =
    #[(0)"Initialized_sellerDrop_FALSE_buyerPickup_FALSE",
    #(1)"Initialized_sellerDrop_TRUE_buyerPickup_FALSE",
    #(2)"Initialized_sellerDrop_ERROR_buyerPickup_FALSE",
    #(3)"Initialized_sellerDrop_TRUE_buyerPickup_TRUE",
    #(4)"Initialized_sellerDrop_TRUE_buyerPickup_ERROR",
    #(5)"Completed_sellerDrop_TRUE_buyerPickup_TRUE_return_FALSE",
    #(6)"Completed_sellerDrop_TRUE_buyerPickup_TRUE_return_TRUE_TXReversed",
    #(7)"Completed_sellerDrop_TRUE_buyerPickup_TRUE_returnInconsitancy_MRR",
    #(8)"TRANSACTION_ERROR_MANUAL_REVIEW_REQUIRED", (9)"SYSTEM_ERROR"]

    try:
        return status_codes[status_code]
    except IndexError:
        return "STATUS_CODE_INVALID"

def Database_Status_Update(status_code, ID):
    date_modified = str(datetime.now())
    conn=psycopg2.connect("dbname='SafeDrop_Orders' user='postgres' password='postgre123' host='localhost' port = '5432'") #UP.db = user_profile.db
    cur=conn.cursor()
    cur.execute("UPDATE orderInfo SET status=%s, data_modified=%s WHERE TXID =%s", (status_change(status_code), date_modified, ID))
    conn.commit()
    conn.close()
