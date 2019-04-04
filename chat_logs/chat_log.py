"""
A program that creates and connects to an SQlAlchemy database for SafeDrop chat logs
and can add new entries with this info:
buyer username, seller username, txid, all chat messages and sent dates

"""
#Author: Andrew Moreno
#Date: April 2nd 2019

#Imports
import sys
sys.path.append('../')

import psycopg2
from datetime import datetime
import json
from flask import Flask, render_template, redirect, url_for, request, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, update
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://uf7h8qb9gmo173:pbf3912778f0bbf470d5219c29f88204a8e5bf52b9bc284a105203c5bdd027d16@ec2-54-84-209-65.compute-1.amazonaws.com:5432/d7gkp4v5t20bml?sslmode=require'
app.config['SECRET_KEY'] = 'thisissecret'

db = SQLAlchemy(app)

class ChatData(db.Model):
    __tablename__="chatlog"
    id = db.Column(db.Integer, primary_key=True)
    TXID = db.Column(db.String(254))
    B_username = db.Column(db.String(64))
    S_username = db.Column(db.String(64))
    Sender_username = db.Column(db.String(64))
    msg = db.Column(db.String(254))
    msg_date = db.Column(db.String(64))
db.create_all()


def newMsg (txid, B_username, S_username, Sender_username, msg):
    msg_date = str(datetime.now())
    new_entry = ChatData(TXID = txid, B_username = B_username, S_username = S_username, \
        Sender_username = Sender_username, msg = msg, msg_date = msg_date)
    db.session.add(new_entry)
    db.session.commit()
    db.session.close()

def searchMsg (txid):
    row = ChatData.query.filter_by(TXID=txid)
    db.session.close()
    return row
