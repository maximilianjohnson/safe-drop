"""
A program that creates an SQLAlchemy database for new user profiles
and adds new entries with this info:
first name, last name, username, email, age, date joined, address, city,
province, country, postal code, distance, txa, user_rating, status
uses SQLAlchemy

"""

#Author: Andrew Moreno
#Date: April 2nd, 2019

#Imports
import psycopg2
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import json
from flask import Flask, render_template, redirect, url_for, request, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, update, or_
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgre123@\
localhost:5432/SafeDrop_Users'
app.config['SECRET_KEY'] = 'thisissecret'

db = SQLAlchemy(app)

#make new profile using the following information
#first name, last name, username, email, age, postal code,
#address, city, province, country

class UserData(db.Model):
    __tablename__="users"
    id = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    username = db.Column(db.String(64))
    password_hash = db.Column(db.String(254))
    email = db.Column(db.String(254))
    age = db.Column(db.Integer)
    date_joined = db.Column(db.String(64))
    address = db.Column(db.String(64))
    city = db.Column(db.String(64))
    province = db.Column(db.String(64))
    country = db.Column(db.String(64))
    postal_code = db.Column(db.String(64))
    txA = db.Column(db.Integer)
    user_rating = db.Column(db.Integer)
    status = db.Column(db.String(64))


def insert_newprofile_up_db(first_name, last_name, username, email, age, address, city, \
    province, country, postal_code):
    date = datetime.now()
    new_entry = UserData(first_name = first_name, last_name = last_name, \
        username = username, email = email, age = age, date_joined = date, \
        address = address, city = city, province = province, country = country, \
        postal_code = postal_code, txA = 0, user_rating = 5,\
        status = "Good Standing")
    db.session.add(new_entry)
    db.session.commit()
    db.session.close()

def search_value(column, username):
    row = UserData.query.filter_by(username = username).first()
    search = getattr(row, column)
    db.session.close()
    return search
