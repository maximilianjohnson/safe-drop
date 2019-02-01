import sqlite3
from datetime import datetime

#function creates user profile database
def create_up_db():
    conn=sqlite3.connect("UP.db") #UP.db = user_profile.db
    cur=conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS users (first_name TEXT, last_name TEXT, user_name TEXT, email TEXT, age INTEGER, date_joined DATE, city TEXT, province TEXT, country TEXT, txA INTEGER, user_rating INTEGER, status TEXT)")
    conn.commit()
    conn.close()

#make new profile #first name, last name, username, email, age, city, province, country
def insert_newprofile_up_db(fn, ln, un, em, age, city, prov, ctry):
    date = datetime.now()
    conn=sqlite3.connect("UP.db") #UP.db = user_profile.db
    cur=conn.cursor()
    cur.execute("INSERT INTO users VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (fn, ln, un, em, age, date, city, prov, ctry, 0, 5, "Good Standing"))
    conn.commit()
    conn.close()

def view():
    date = datetime.now()
    conn=sqlite3.connect("UP.db") #UP.db = user_profile.db
    cur=conn.cursor()
    cur.execute("SELECT * FROM users")
    rows = cur.fetchall()
    conn.close()
    return rows

#prototype using cmd line inputs
fn = input("Enter your first name: ")
ln = input("Enter your last name: ")
un = input("Enter your username: ")
em = input("Enter your email: ")
age = input("Enter your age: ")
city = input("Enter your current city: ")
prov = input("Enter your current province: ")
ctry = input("Enter your current country: ")

insert_newprofile_up_db(fn, ln, un, em, age, city, prov, ctry)
print(view())
