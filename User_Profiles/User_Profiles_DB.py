"""
A program that creates an SQL database for new user profiles
and adds new entries with this info:
first name, last name, username, email, age, date joined, address, city,
province, country, postal code, distance, txa, user_rating, status

"""
#FOR PROTOTYPING ONLY, TO BE EXPANDED UPON FOR WEB INTEGRATION/POSTGRESQL
#Author: Maximilian Johnson
#Date: Feb 6th


#imports
import sqlite3
from datetime import datetime
import user_distance

#function creates user profile database
def create_up_db():
    conn=sqlite3.connect("User_ProfileDataBase.db")
    cur=conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, \
                first_name TEXT, last_name TEXT, user_name TEXT, email TEXT, \
                age INTEGER, date_joined DATE, address TEXT, city TEXT, \
                province TEXT, country TEXT, postal_code TEXT, distance FLOAT, \
                txA INTEGER, user_rating INTEGER, status TEXT)")
    conn.commit()
    conn.close()

#make new profile using the following information
#first name, last name, username, email, age, postal code,
#address, city, province, country
def insert_newprofile_up_db(fn, ln, un, em, age, ad, city, prov, ctry, pc):
    date = datetime.now()
    conn=sqlite3.connect("User_ProfileDataBase.db")
    cur=conn.cursor()
    cur.execute("INSERT INTO users VALUES(NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, \
    ?, ?, ?, ?)", (fn, ln, un, em, age, date, ad, city, prov, ctry, pc, \
    user_distance.get_distance(ad,city), 0, 5, "Good Standing"))
    conn.commit()
    conn.close()

#command line view function for sqlite3 database
def view():
    conn=sqlite3.connect("User_ProfileDataBase.db")
    cur=conn.cursor()
    cur.execute("SELECT * FROM users")
    rows = cur.fetchall()
    conn.close()
    return rows

def search(fn="", ln="", un="", em="", age="", dj="", ad="", city="", prov="", \
           ctry="", pc="", dist="", txa="", ur="", status=""):
    conn=sqlite3.connect("User_ProfileDataBase.db")
    cur=conn.cursor()
    cur.execute("SELECT * FROM users WHERE first_name=? OR last_name=? OR \
                user_name=? OR email=? OR age=? OR date_joined=? OR address=? \
                OR city=? OR province=? OR country=? OR postal_code=? OR \
                distance=? OR txA=? OR user_rating=? OR status=?", \
                (fn, ln, un, em, age, dj, ad, city, prov, ctry, pc, dist, \
                txa, ur, status))
    rows = cur.fetchall()
    conn.close()
    return rows

def delete(id):
    conn=sqlite3.connect("User_ProfileDataBase.db")
    cur=conn.cursor()
    cur.execute("DELETE FROM users WHERE id=?", (id,))
    conn.commit()
    conn.close()

def update(fn, ln, un, em, age, dj, ad, city, prov, ctry, pc, txa, ur, \
            status):
    conn=sqlite3.connect("User_ProfileDataBase.db")
    cur_conn.cursor()
    cur.execute("UPDATE users SET first_name=? OR last_name=? OR \
                user_name=? OR email=? OR age=? OR date_joined=? OR address=? \
                OR city=? OR province=? OR country=? OR postal_code=? OR \
                distance=? OR txA=? OR user_rating=? OR status=?", \
                (fn, ln, un, em, age, dj, ad, city, prov, ctry, pc, \
                txa, ur, status))
    conn.close()





'''
#prototype using cmd line inputs
fn = input("Enter your first name: ")
ln = input("Enter your last name: ")
un = input("Enter your username: ")
em = input("Enter your email: ")
age = input("Enter your age: ")
ad = input("Enter your address: ")
city = input("Enter your current city: ")
prov = input("Enter your current province: ")
ctry = input("Enter your current country: ")
pc = input("Enter your postal code: ")

create_up_db()
insert_newprofile_up_db(fn, ln, un, em, age, ad, city, prov, ctry, pc)
print(view())
'''
create_up_db()
