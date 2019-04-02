"""
A program that creates and connects to an SQL database for new SafeDrop images
and can add new entries with this info:
url_id connected to orderinfo, image url, username, date, txid

"""
#Author: Maximilian Johnson
#Date: March 23rd

#Imports
import psycopg2
from datetime import datetime

#connects to database
#Info stored: Transaction number in ascending order, random generated order ID,
#Buyer username, seller username, item name, date initialized, cost, location,
#order status, date in which data was last modified, date transaction resolves
def connect_images_db():
    conn=psycopg2.connect("dbname='SafeDrop_OrderImages' user='postgres' password='postgre123' host='localhost' port = '5433'")
    cur=conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS images (url_id TEXT, TXID TEXT, \
                 username TEXT, url TEXT, date TEXT)")
    conn.commit()
    conn.close()

#Function uses values to add new order to psycopg2 database
def newImage (url_id, TXID, user, url):
    connect_images_db()
    conn=psycopg2.connect("dbname='SafeDrop_OrderImages' user='postgres' password='postgre123' host='localhost' port = '5433'")
    cur=conn.cursor()
    date = str(datetime.now())
    cur.execute("INSERT INTO images VALUES(%s, %s, %s, %s, %s)", (url_id, \
                TXID, user, url, date))
    conn.commit()
    conn.close()

#Searchable perameters
#Order number, TXID, Seller username, buyer username, item name,
#cost, location, date initialized
def search_allImages(url_id=(None), UN=(None)):
    conn=psycopg2.connect("dbname='SafeDrop_OrderImages' user='postgres' password='postgre123' host='localhost' port = '5433'")
    cur=conn.cursor()
    cur.execute("SELECT * FROM images WHERE url_id=%s OR\
                username=%s",\
                (url_id, UN))
    rows = cur.fetchall()
    conn.close()
    return rows
