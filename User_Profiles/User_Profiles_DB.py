import sqlite3
from datetime import datetime
import user_distance

#function creates user profile database
def create_up_db():
    conn=sqlite3.connect("UP.db") #UP.db = user_profile.db
    cur=conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS users (first_name TEXT, last_name TEXT, user_name TEXT, email TEXT, age INTEGER, date_joined DATE, address TEXT, city TEXT, province TEXT, country TEXT, postal_code TEXT, distance  FLOAT, txA INTEGER, user_rating INTEGER, status TEXT)")
    conn.commit()
    conn.close()

#make new profile #first name, last name, username, email, age, postal code, address, city, province, country
def insert_newprofile_up_db(fn, ln, un, em, age, ad, city, prov, ctry, pc):
    date = datetime.now()
    conn=sqlite3.connect("UP.db") #UP.db = user_profile.db
    cur=conn.cursor()
    cur.execute("INSERT INTO users VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (fn, ln, un, em, age, date, ad, city, prov, ctry, pc, user_distance.get_distance(ad,city), 0, 5, "Good Standing"))
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
ad = input("Enter your address: ")
city = input("Enter your current city: ")
prov = input("Enter your current province: ")
ctry = input("Enter your current country: ")
pc = input("Enter your postal code: ")

create_up_db()
insert_newprofile_up_db(fn, ln, un, em, age, ad, city, prov, ctry, pc)
print(view())
