"""
A program that creates an webpage for safedrop
working functions:
log in, log out (user: admin, pass: admin), signup, profile view, basic visuals
all uses postgresql, sqlalchemy, flask and flask_login

"""
#FOR PROTOTYPING ONLY, TO BE EXPANDED UPON FOR WEB INTEGRATION/POSTGRESQL
#Author: Maximilian Johnson
#Date: Feb 26th




import sys
sys.path.append('../')

from flask import Flask, render_template, redirect, url_for, request, url_for
from flask_login import LoginManager, UserMixin, login_user, login_required,\
logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from werkzeug.security import generate_password_hash, check_password_hash
from User_Profiles.User_Profiles_DB import search_value, insert_newprofile_up_db
from flask_socketio import SocketIO, join_room, leave_room, send
from Order_Info.OrderInfo_Backend import search_OrderValue, newOrder, confirmBuyer

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgre123@\
localhost:5432/SafeDrop_Logins'
app.config['SECRET_KEY'] = 'thisissecret'

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

#possibly unnecessary ??
db2 = create_engine('postgresql://postgres:postgre123@localhost:5432/ \
SafeDrop_Users')
DB2Session = sessionmaker(db2)
db2session = DB2Session()

#for the chat portion
socketio = SocketIO(app)



#keep indents and formating on this as is, necessary for user creation
#keeps UserLogins as contained function
class UserLogins(UserMixin, db.Model):
    __tablename__="Logins"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True)
    password_hash = db.Column(db.String(254))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return UserLogins.query.get(int(user_id))


@app.route('/')
def index():
        return render_template("index.html")


@app.route('/signup/', methods=['GET', 'POST'])
def signup():
    if request.method=='POST':
        username = request.form["username"]
        password = request.form["password"]
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        email = request.form["email"]
        age = request.form["age"]
        address = request.form["address"]
        city = request.form["city"]
        province = request.form["province"]
        country = request.form["country"]
        postal_code = request.form["postal_code"]
        newuser = UserLogins(username = username)
        newuser.set_password(password)
        db.session.add(newuser)
        insert_newprofile_up_db(first_name, last_name, username, email, age, \
        address, city, province, country, postal_code)
        db.session.commit()
    return render_template("signup.html")


@app.route('/login/', methods=['GET', 'POST'])
def login():
    message= None
    if current_user.is_authenticated:
        return redirect(url_for('profile'))
    if request.method == 'POST':
        userentry = request.form['username']
        passentry = request.form['password']
        user = UserLogins.query.filter_by(username=userentry).first()
        if user is None or not user.check_password(passentry):
            message='Invalid Credentials. Please try again.'
            return render_template("login.html", error = message)
        else:
            login_user(user)
            return redirect(url_for('profile'))
    return render_template("login.html", error = message)

@app.route('/profile/')
@login_required
def profile():
    FirstName = str(search_value('first_name', str(current_user.username)))
    LastName = str(search_value('last_name', current_user.username))
    Age = str(search_value('age', current_user.username))
    Email = str(search_value('email', current_user.username))
    date_joined = str(search_value('date_joined', current_user.username))
    Address = str(search_value('address', current_user.username))
    user_rating = str(search_value('user_rating', current_user.username))
    status = search_value('status', current_user.username)
    return render_template("profile.html", FirstName=FirstName, \
    LastName=LastName, Age=Age, Email=Email, date_joined=date_joined, \
    Address=Address, user_rating=user_rating, status=status)

@app.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/active_drops/',  methods=['GET', 'POST'])
@login_required
def active_drops():
    s_txid = search_OrderValue('TXID', S_username = current_user.username)
    s_txids = []
    s_len = len(s_txid)
    for item in s_txid:
        txid = str(item)
        txid = txid[2:-3]
        s_txids.append(txid)
    b_txid = search_OrderValue('TXID', B_username = current_user.username)
    b_txids = []
    b_len = len(b_txid)
    for item in b_txid:
        txid = str(item)
        txid = txid[2:-3]
        b_txids.append(txid)
    currentuser = current_user.username
    return render_template('active_drops.html', s_len=s_len, s_txids=s_txids, \
    b_len = b_len, b_txids = b_txids)

@app.route('/active_drops/<string:chat_id>/', methods=['GET', 'POST'])
@login_required
def transactionpage(chat_id):
    return render_template('message.html', currentuser = str(current_user.username), chatid = chat_id)

def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')

@socketio.on('my event')
def handle_my_custom_event(data, methods=['GET', 'POST']):
    print('received my event: ' + str(data))
    room = data['room']
    join_room(room)
    socketio.emit('my response',  data, callback=messageReceived, room=room)

@app.route('/new_drop/', methods=['GET', 'POST'])
@login_required
def new_drop():
    if request.method=='POST':
        I_name = request.form["Item_name"]
        I_cost = request.form["Item_cost"]
        I_desc = request.form["Item_desc"]
        Location = request.form["Location"]
        S_name = current_user.username
        B_name = None
        newOrder(S_name, B_name, I_name, I_desc, I_cost, Location)
    return render_template("new_drop.html")


@app.route('/browse/', methods=['GET', 'POST'])
def browse():
    if request.method=='POST':
        SellerName = str(search_OrderValue('S_username', recent = 0))
        ItemName = str(search_OrderValue('I_name', recent = 0))
        ItemDesc = str(search_OrderValue('description', recent = 0))
        ItemCost = str(search_OrderValue('Cost', recent = 0))
        Location = str(search_OrderValue('Location', recent = 0))
        date_post = str(search_OrderValue('date_initialized', recent = 0))
        txid = str(search_OrderValue('TXID', recent = 0))
        sub = request.form.get("submit")
        if sub == 'submit':
            request.form.get("message")
            confirmBuyer(current_user.username, txid)
        SellerName1 = str(search_OrderValue('S_username', recent = 1))
        ItemName1 = str(search_OrderValue('I_name', recent = 1))
        ItemDesc1 = str(search_OrderValue('description', recent = 1))
        ItemCost1 = str(search_OrderValue('Cost', recent = 1))
        Location1 = str(search_OrderValue('Location', recent = 1))
        date_post1 = str(search_OrderValue('date_initialized', recent = 1))
        txid1 = str(search_OrderValue('TXID', recent = 1))
        sub1 = request.form.get("submit1")
        if sub1 == 'submit1':
            request.form.get("message1")
            confirmBuyer(current_user.username, txid1)
        return render_template("browse.html", SellerName=SellerName, \
        ItemName=ItemName, ItemDesc=ItemDesc, ItemCost=ItemCost, Location=Location,\
        date_post=date_post, SellerName1=SellerName1, \
        ItemName1=ItemName1, ItemDesc1=ItemDesc1, ItemCost1=ItemCost1, Location1=Location1,\
        date_post1=date_post1)

    else:
        SellerName = str(search_OrderValue('S_username', recent = 0))
        ItemName = str(search_OrderValue('I_name', recent = 0))
        ItemDesc = str(search_OrderValue('description', recent = 0))
        ItemCost = str(search_OrderValue('Cost', recent = 0))
        Location = str(search_OrderValue('Location', recent = 0))
        date_post = str(search_OrderValue('date_initialized', recent = 0))
        txid = str(search_OrderValue('TXID', recent = 0))
        SellerName1 = str(search_OrderValue('S_username', recent = 1))
        ItemName1 = str(search_OrderValue('I_name', recent = 1))
        ItemDesc1 = str(search_OrderValue('description', recent = 1))
        ItemCost1 = str(search_OrderValue('Cost', recent = 1))
        Location1 = str(search_OrderValue('Location', recent = 1))
        date_post1 = str(search_OrderValue('date_initialized', recent = 1))
        txid1 = str(search_OrderValue('TXID', recent = 1))

        return render_template("browse.html", SellerName=SellerName, \
        ItemName=ItemName, ItemDesc=ItemDesc, ItemCost=ItemCost, Location=Location,\
        date_post=date_post, SellerName1=SellerName1, \
        ItemName1=ItemName1, ItemDesc1=ItemDesc1, ItemCost1=ItemCost1, Location1=Location1,\
        date_post1=date_post1)



if __name__ == '__main__':
    socketio.run(app, debug=True)

if __name__ == "__main__":
    app.run(debug=True)
