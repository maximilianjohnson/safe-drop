"""
A program that creates and connects to an SQL database for SafeDrop chat logs
and can add new entries with this info:
buyer username, seller username, txid, all chat messages and sent dates

"""
#Author: Maximilian Johnson
#Date: March 14th 2019

#Imports
import psycopg2
from datetime import datetime

#connects to database
#Info stored: Transaction number in ascending order, random generated order ID,
#Buyer username, seller username, item name, date initialized, cost, location,
#order status, date in which data was last modified, date transaction resolves
def connect_chatlog():
    conn=psycopg2.connect("dbname='SafeDrop_ChatLog' user='postgres' password='postgre123' host='localhost' port = '5433'")
    cur=conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS chatlog (id SERIAL, TXID TEXT, \
                 B_username TEXT, S_username TEXT, Sender_username TEXT,\
                 msg TEXT, msg_date TEXT)")
    conn.commit()
    conn.close()

#connects to database
#connect_chatlog()

#Function uses values to add new order to psycopg2 database
def newMsg(txid, B_username, S_username, Send_username, msg):
    connect_chatlog()
    conn=psycopg2.connect("dbname='SafeDrop_ChatLog' user='postgres' password='postgre123' host='localhost' port = '5433'")
    cur=conn.cursor()
    msg_date = str(datetime.now())
    cur.execute("INSERT INTO chatlog VALUES(default, %s, %s, %s, %s, %s, %s)", \
    (txid, B_username, S_username, Send_username, msg, msg_date))
    conn.commit()
    conn.close()

def searchMsg(TXID):
    connect_chatlog()
    conn=psycopg2.connect("dbname='SafeDrop_ChatLog' user='postgres' password='postgre123' host='localhost' port = '5433'")
    cur=conn.cursor()
    cur.execute("SELECT * FROM chatlog WHERE TXID=%s", (TXID,))
    rows = cur.fetchall()
    conn.close()
    return rows
