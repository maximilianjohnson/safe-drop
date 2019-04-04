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
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://cbcsdsjpafwndn:485e906069a706743a7a7fe993889fe15c3145b66927d0c13ef6d08f327d1114@ec2-50-17-227-28.compute-1.amazonaws.com:5432/d3n6f8iutcli6p?sslmode=require'
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
