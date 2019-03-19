"""
A program that creates an SQL database for new user profiles
and adds new entries with this info:
first name, last name, username, email, age, date joined, address, city,
province, country, postal code, distance, txa, user_rating, status
uses postgresql, currently localhost:5432

"""
#FOR PROTOTYPING ONLY, TO BE EXPANDED UPON FOR WEB INTEGRATION
#Author: Maximilian Johnson
#Date: Feb 26th


#imports
import psycopg2
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
#from User_Profiles
#import user_distance

#function creates user profile database
def create_up_db():
    conn=psycopg2.connect("dbname='SafeDrop_Users' user='postgres' password='postgre123' host='localhost' port = '5432'")
    cur=conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS users (id SERIAL, \
                first_name TEXT, last_name TEXT, user_name TEXT, \
                password_hash TEXT, email TEXT, \
                age INTEGER, date_joined DATE, address TEXT, city TEXT, \
                province TEXT, country TEXT, postal_code TEXT,\
                txA INTEGER, user_rating INTEGER, status TEXT)")
    conn.commit()
    conn.close()

#create_up_db()
#make new profile using the following information
#first name, last name, username, email, age, postal code,
#address, city, province, country
def insert_newprofile_up_db(fn, ln, un, em, age, ad, city, prov, ctry, pc):
    create_up_db()
    date = datetime.now()
    conn=psycopg2.connect("dbname='SafeDrop_Users' user='postgres' password='postgre123' host='localhost' port = '5432'")
    cur=conn.cursor()
    cur.execute("INSERT INTO users VALUES(default, %s, %s, %s, %s, %s, %s, %s, %s,\
    %s, %s, %s, %s, %s, %s, %s)", (fn, ln, un, 'password_hash', em, age, date, ad, city,\
    prov, ctry, pc, 0, 5, "Good Standing"))
    conn.commit()
    conn.close()

#command line view function for psycopg2 database
def view():
    create_up_db()
    conn=psycopg2.connect("dbname='SafeDrop_Users' user='postgres' password='postgre123' host='localhost' port = '5432'")
    cur=conn.cursor()
    cur.execute("SELECT * FROM users")
    rows = cur.fetchall()
    conn.close()
    return rows

def search(fn="", ln="", un="", em="", age="", dj="", ad="", city="", prov="", \
           ctry="", pc="", dist="", txa="", ur="", status=""):
    create_up_db()
    conn=psycopg2.connect("dbname='SafeDrop_Users' user='postgres' password='postgre123' host='localhost' port = '5432'")
    cur=conn.cursor()
    cur.execute("SELECT * FROM users WHERE first_name=%s OR last_name=%s OR \
                user_name=%s OR email=%s OR age=%s OR date_joined=%s OR address=%s \
                OR city=%s OR province=%s OR country=%s OR postal_code=%s OR \
                distance=%s OR txA=%s OR user_rating=%s OR status=%s", \
                (fn, ln, un, em, age, dj, ad, city, prov, ctry, pc, dist, \
                txa, ur, status))
    rows = cur.fetchall()
    conn.close()
    return rows

def search_value(column, user):
    create_up_db()
    conn=psycopg2.connect("dbname='SafeDrop_Users' user='postgres' password='postgre123' host='localhost' port = '5432'")
    cur=conn.cursor()
    SQL = "SELECT " + column + " FROM users WHERE user_name=(%s)"
    data = (user,)
    cur.execute(SQL, data)
    value = cur.fetchall()
    for item in value:
        return ("%s" % item)

#search_value('status', 'maximilianjohnson')

def delete(id):
    conn=psycopg2.connect("dbname='SafeDrop_Users' user='postgres' password='postgre123' host='localhost' port = '5432'")
    cur=conn.cursor()
    cur.execute("DELETE FROM users WHERE id=%s", (id,))
    conn.commit()
    conn.close()

def update(fn, ln, un, ph, em, age, dj, ad, city, prov, ctry, pc, txa, ur, status):
    create_up_db()
    if ph != "":
        ph = generate_password_hash(ph)
    conn=psycopg2.connect("dbname='SafeDrop_Users' user='postgres' password='postgre123' host='localhost' port = '5432'")
    cur_conn.cursor()
    cur.execute("UPDATE users SET first_name=%s OR last_name=%s OR \
                user_name=%s OR password_hash=%s OR email=%s OR \
                age=%s OR date_joined=%s OR address=%s \
                OR city=%s OR province=%s OR country=%s OR postal_code=%s OR \
                distance=%s OR txA=%s OR user_rating=%s OR status=%s", \
                (fn, ln, un, ph, em, age, dj, ad, city, prov, ctry, pc, \
                txa, ur, status))
    conn.close()





'''
#prototype using cmd line inputs
fn = input("Enter your first name: ")
ln = input("Enter your last name: ")
un = input("Enter your username: ")
ph = input("Enter your password: ")
em = input("Enter your email: ")
age = input("Enter your age: ")
ad = input("Enter your address: ")
city = input("Enter your current city: ")
prov = input("Enter your current province: ")
ctry = input("Enter your current country: ")
pc = input("Enter your postal code: ")

create_up_db()
insert_newprofile_up_db(fn, ln, un, ph, em, age, ad, city, prov, ctry, pc)
print(view())
'''
