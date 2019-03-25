"""
A program that creates and connects to an SQL database for SafeBucks
and can add new entries with this info:
username, safebucks

"""
#Author: Maximilian Johnson
#Date: March 24th 2019

#Imports

import sys
sys.path.append('../')

from Order_Info.OrderInfo_Backend import search_OrderValue
import psycopg2

#connects to database
#Info stored: Transaction number in ascending order, random generated order ID,
#Buyer username, seller username, item name, date initialized, cost, location,
#order status, date in which data was last modified, date transaction resolves
def connect_safebucks():
    conn=psycopg2.connect("dbname='SafeDrop_SafeBucks' user='postgres' password='postgre123' host='localhost' port = '5433'")
    cur=conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS safebucks (username TEXT, \
                 bucks REAL)")
    conn.commit()
    conn.close()

#connects to database
#connect_safebucks()

#Function uses values to add new order to psycopg2 database
def addUserBucks(user):
    connect_safebucks()
    conn=psycopg2.connect("dbname='SafeDrop_SafeBucks' user='postgres' password='postgre123' host='localhost' port = '5433'")
    cur=conn.cursor()
    bucks = 100.00
    cur.execute("INSERT INTO safebucks VALUES(%s, %s)", (user, bucks))
    conn.commit()
    conn.close()

def searchBucks(user):
    connect_safebucks()
    conn=psycopg2.connect("dbname='SafeDrop_SafeBucks' user='postgres' password='postgre123' host='localhost' port = '5433'")
    cur=conn.cursor()
    cur.execute("SELECT bucks FROM safebucks WHERE username=%s", (user,))
    value = cur.fetchall()
    for item in value:
        return ("%s" % item)

def updateBucks(user, bucks):
    connect_safebucks()
    conn=psycopg2.connect("dbname='SafeDrop_SafeBucks' user='postgres' password='postgre123' host='localhost' port = '5433'")
    cur=conn.cursor()
    cur.execute("UPDATE safebucks SET bucks=%s WHERE username=%s", (bucks, user))
    conn.commit()
    conn.close()

def add100Bucks(user):
    connect_safebucks()
    conn=psycopg2.connect("dbname='SafeDrop_SafeBucks' user='postgres' password='postgre123' host='localhost' port = '5433'")
    cur=conn.cursor()
    bucks_i = float(searchBucks(user))
    bucks = bucks_i + 100

    cur.execute("UPDATE safebucks SET bucks=%s WHERE username=%s", (bucks, user))
    conn.commit()
    conn.close()

def completeMoneyTransfer(txid):
    cost = search_OrderValue('cost', txid)
    b_user = search_OrderValue('B_username', txid)
    s_user = search_OrderValue('S_username', txid)
    b_bucks = searchBucks(b_user) - cost
    s_bucks = searchBucks(s_user) + cost
    updateBucks(b_user, b_bucks)
    updateBucks(s_user, s_bucks)
    return cost
