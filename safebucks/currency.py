"""
A program that creates and connects to an SQL database for SafeBucks
and can add new entries with this info:
username, safebucks

"""
#Author: Andrew Moreno
#Date: April 2nd, 2019

#Imports
import sys
sys.path.append('../')

from Order_Info.OrderInfo_Backend import search_OrderValue
import psycopg2
import json
from flask import Flask, render_template, redirect, url_for, request, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, update, or_
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgre123@\
localhost:5432/SafeDrop_SafeBucks'
app.config['SECRET_KEY'] = 'thisissecret'

db = SQLAlchemy(app)

#connects to database
#Info stored: Transaction number in ascending order, random generated order ID,
#Buyer username, seller username, item name, date initialized, cost, location,
#order status, date in which data was last modified, date transaction resolves

class SafeBucksData(db.Model):
    __tablename__="safebucks"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64))
    bucks = db.Column(db.Float)


def addUserBucks(username):
    bucks = 100.00
    SafeBucksData(username = username, bucks = bucks)
    db.session.add(addUserBucks)
    db.session.commit()

def searchBucks(username):
    row = SafeBucksData.query.filter_by(username = username).first()
    search = row.bucks
    return search

def updateBucks(username, bucks):
    row = SafeBucksData(username = username).first()
    row.bucks = bucks
    db.session.commit()

def add100Bucks(username):
    row = SafeBucksData.query.filter_by(username = username).first()
    bucks_i = float(searchBucks(user))
    bucks = bucks_i + 100
    row.bucks = bucks
    db.session.commit()

def completeMoneyTransfer(txid):
    cost = search_OrderValue('cost', txid)
    b_user = search_OrderValue('B_username', txid)
    s_user = search_OrderValue('S_username', txid)
    b_bucks = searchBucks(b_user) - cost
    s_bucks = searchBucks(s_user) + cost
    updateBucks(b_user, b_bucks)
    updateBucks(s_user, s_bucks)
    return cost
