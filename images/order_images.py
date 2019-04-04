"""
A program that creates and connects to an SQLAlchemy database for new SafeDrop images
and can add new entries with this info:
url_id connected to orderinfo, image url, username, date, txid

"""
#Author: Andrew Moreno
#Date: April 2nd, 2019

#Imports
import sys
sys.path.append('../')

import psycopg2
from datetime import datetime
import json
from flask import Flask, render_template, redirect, url_for, request, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, update, or_, exc
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://yktqvccycywrgp:92ced6796cbd9fc37a5eb27614fec29edcb0b404b1611794a4c2ea219870d8cd@ec2-23-21-106-241.compute-1.amazonaws.com:5432/d3iko5eei5ss3a?sslmode=require'
app.config['SECRET_KEY'] = 'thisissecret'

db = SQLAlchemy(app)

#connects to database
#Info stored: Transaction number in ascending order, random generated order ID,
#Buyer username, seller username, item name, date initialized, cost, location,
#order status, date in which data was last modified, date transaction resolves

class ImagesData(db.Model):
    __tablename__="images"
    id = db.Column(db.Integer, primary_key=True)
    url_id = db.Column(db.String(254))
    TXID = db.Column(db.String(254), unique=True)
    username = db.Column(db.String(64))
    url = db.Column(db.Text())
    date = db.Column(db.String(64))
db.create_all()


def newImage (url_id, TXID, user, url):
    date = str(datetime.now())
    new_entry = ImagesData(url_id = url_id, TXID = TXID, username = user, url = url, date = date)
    db.session.add(new_entry)
    db.session.commit()
    db.session.close()

#Searchable perameters
#Order number, TXID, Seller username, buyer username, item name,
#cost, location, date initialized
def search_allImages(url_id=(None), username=(None)):
    try:
        row = ImagesData.query.filter(or_(ImagesData.url_id == url_id, ImagesData.username == username)).all()
        db.session.close()
        return row
    except exc.ProgrammingError:
        pass
