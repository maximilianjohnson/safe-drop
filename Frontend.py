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

import json
from datetime import datetime
from flask import Flask, render_template, redirect, url_for, request, url_for
from flask_login import LoginManager, UserMixin, login_user, login_required,\
logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, exc
from sqlalchemy.orm import sessionmaker
from werkzeug.security import generate_password_hash, check_password_hash
from User_Profiles.User_Profiles_DB import search_value, insert_newprofile_up_db
from flask_socketio import SocketIO, join_room, leave_room, send
from Order_Info.OrderInfo_Backend import search_OrderValue, newOrder, confirmBuyer, statusUpdate, repostOffer, browseRecent, search_allOrders, deleteOrder
from chat_logs.chat_log import newMsg, searchMsg
from safebox_connection.code_connect import requestCode, newBoxAssignment, dropStatus, search_ChatValue, attemptCode, codeResult
from images.order_images import newImage, search_allImages
from safebucks.currency import searchBucks, add100Bucks, addUserBucks
from difflib import SequenceMatcher

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://yktqvccycywrgp:92ced6796cbd9fc37a5eb27614fec29edcb0b404b1611794a4c2ea219870d8cd@ec2-23-21-106-241.compute-1.amazonaws.com:5432/d3iko5eei5ss3a?sslmode=require'
app.config['SECRET_KEY'] = 'thisissecret'

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

#possibly unnecessary ??
engine = create_engine('postgres://yktqvccycywrgp:92ced6796cbd9fc37a5eb27614fec29edcb0b404b1611794a4c2ea219870d8cd@ec2-23-21-106-241.compute-1.amazonaws.com:5432/d3iko5eei5ss3a?sslmode=require', pool_size = 20, max_overflow=0)
engine_session = sessionmaker(engine)
db2session = engine_session()
connection = db2session.connection()

#for the chat portion
socketio = SocketIO(app)


@app.teardown_appcontext
def shutdown_session(exception=None):
    db.session.remove()


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

class DataOrders(db.Model):
    __tablename__="orderInfo"
    id = db.Column(db.Integer, primary_key=True)
    TXID = db.Column(db.String(254))
    B_username = db.Column(db.String(64))
    S_username = db.Column(db.String(64))
    I_name = db.Column(db.String(128))
    description = db.Column(db.String(1500))
    date_initialized = db.Column(db.String(128))
    Cost = db.Column(db.Float)
    Location = db.Column(db.String(64))
    status = db.Column(db.String(128))
    img_url = db.Column(db.String(24))
    date_resolved = db.Column(db.String(128))

class SafeBucksData(db.Model):
    __tablename__="safebucks"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64))
    bucks = db.Column(db.Float)

class ImagesData(db.Model):
    __tablename__="images"
    id = db.Column(db.Integer, primary_key=True)
    url_id = db.Column(db.String(254))
    TXID = db.Column(db.String(254))
    username = db.Column(db.String(64))
    url = db.Column(db.String(254))
    date = db.Column(db.String(64))

class ConnectData(db.Model):
    __tablename__="codelog"
    id = db.Column(db.Integer, primary_key = True)
    TXID = db.Column(db.String(254))
    B_username = db.Column(db.String(64))
    S_username = db.Column(db.String(64))
    stage = db.Column(db.String(128))
    box_id = db.Column(db.String(128))
    access_code = db.Column(db.String(64))
    expiry_time = db.Column(db.String(128))
    code_attempt = db.Column(db.String(64))
    attempt_time = db.Column(db.String(128))
    seller_close_date = db.Column(db.String(128))
    buyer_close_date = db.Column(db.String(128))
    door_status = db.Column(db.String(64))
    scale_status = db.Column(db.String(64))
    scale_delta = db.Column(db.String(64))
    in_box_image_url = db.Column(db.String(254))

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


#changes displayed initialized date based on how long ago they were posted
def date_time (date):
    date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S.%f')
    date_now = datetime.now()
    delta = date_now - date
    if delta.days > 0:
        display = date.strftime("%B %d, %Y")
    elif delta.days == 0 and delta.seconds >= 3600:
        display = (str(int(delta.seconds / 3600)) + " hours ago")
    else:
        display = (str(int(delta.seconds / 60)) + " minutes ago")
    return display


@login_manager.user_loader
def load_user(user_id):
    return UserLogins.query.get(int(user_id))


@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/signup/', methods=['GET', 'POST'])
def signup():
    if request.method=='POST':
        username = request.form["username"]
        password = request.form["password"]
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        email = None
        age = None
        address = None
        city = "Vancouver"
        province = "BC"
        country = "Canada"
        postal_code = None

        if request.form["signup_button"] == "signup":
            newuser = UserLogins(username = username)
            newuser.set_password(password)
            try:
                db.session.add(newuser)
                db.session.commit()
            except exc.IntegrityError:
                return render_template('login.html', error = "Username taken!")

            insert_newprofile_up_db(first_name, last_name, username, email, age, \
            address, city, province, country, postal_code)

            addUserBucks(username)

            user = UserLogins.query.filter_by(username=username).first()
            if user is None or not user.check_password(password):
                message='Invalid Credentials. Please try again.'
                return render_template("login.html", error = message)
            else:
                login_user(user)
                return redirect(url_for('browse', page_id = 1))

            return redirect(url_for('profile'))


@app.route('/login/', methods=['GET', 'POST'])
def login(message=None):
    if current_user.is_authenticated:
        return redirect(url_for('browse', page_id = 1))
    if request.method == 'POST':
        userentry = request.form['userentry']
        passentry = request.form['passentry']

        if request.form["login_value"] == "login":
            user = UserLogins.query.filter_by(username=userentry).first()
            if user is None or not user.check_password(passentry):
                message='Invalid Credentials. Please try again.'
                return render_template("login.html", error = message)
            else:
                login_user(user)
                return redirect(url_for('browse', page_id = 1))
    error = message
    return render_template("login.html", error = error)

@app.route('/profile/')
@login_required
def profile():
    FirstName = str(search_value('first_name', str(current_user.username)))
    LastName = str(search_value('last_name', current_user.username))
    Age = str(search_value('age', current_user.username))
    Email = str(search_value('email', current_user.username))
    date_joined_ugly = datetime.strptime(search_value('date_joined', current_user.username), '%Y-%m-%d %H:%M:%S.%f')
    date_joined = date_joined_ugly.strftime("%B %d, %Y")
    Address = str(search_value('address', current_user.username))
    user_rating = str(search_value('user_rating', current_user.username))
    id = str(search_value('id', current_user.username))
    status = search_value('status', current_user.username)
    bucks = searchBucks(current_user.username)
    return render_template("profile.html", FirstName=FirstName, id=id, \
        LastName=LastName, Age=Age, Email=Email, date_joined=date_joined, \
        Address=Address, user_rating=user_rating, status=status, bucks=bucks)

@app.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/active_drops/',  methods=['GET', 'POST'])
@login_required
def active_drops():
    FirstName = str(search_value('first_name', str(current_user.username)))
    LastName = str(search_value('last_name', current_user.username))

    s_txid = search_OrderValue('TXID', S_username = current_user.username)
    s_txids = []
    s_names = []
    s_other_user = []
    s_price = []
    s_location = []
    s_date = []
    s_return = []

    a_txids = []
    a_names = []
    a_price = []
    a_location = []
    a_date = []

    for item in s_txid:
        txid = str(item)
        if (search_OrderValue('status', txid = txid) != "TRANSACTION COMPLETE"):
            if (search_OrderValue('B_username', txid=txid)) != 'None':
                s_txids.append(txid)
                s_names.append(search_OrderValue('I_name', txid=txid))
                s_other_user.append(search_OrderValue('B_username', txid=txid))
                s_price.append(search_OrderValue('Cost', txid=txid))
                s_location.append(search_OrderValue('Location', txid=txid))
                s_date.append(date_time(search_OrderValue('date_initialized', txid=txid)))
                if (search_OrderValue('status', txid = txid) == "ITEM RETURNED"):
                    s_return.append('waiting')
                else:
                    s_return.append('else')
            else:
                txid = str(item)
                a_txids.append(txid)
                a_names.append(search_OrderValue('I_name', txid=txid))
                a_price.append(search_OrderValue('Cost', txid=txid))
                a_location.append(search_OrderValue('Location', txid=txid))
                a_date.append(date_time(search_OrderValue('date_initialized', txid=txid)))

    b_txid = search_OrderValue('TXID', B_username = current_user.username)
    b_txids = []
    b_names = []
    b_other_user = []
    b_price = []
    b_location = []
    b_date = []
    for item in b_txid:
        txid = str(item)
        if (search_OrderValue('status', txid = txid) != "TRANSACTION COMPLETE"):
            b_txids.append(txid)
            b_names.append(search_OrderValue('I_name', txid=txid))
            b_other_user.append(search_OrderValue('S_username', txid=txid))
            b_price.append(search_OrderValue('Cost', txid=txid))
            b_location.append(search_OrderValue('Location', txid=txid))
            b_date.append(date_time(search_OrderValue('date_initialized', txid=txid)))
    currentuser = current_user.username
    return render_template('active_drops.html', FirstName=FirstName, \
        LastName = LastName, s_txids=s_txids, b_txids = b_txids,\
        s_names=s_names, b_names=b_names, s_other_user = s_other_user, \
        s_price = s_price, s_location = s_location, s_date = s_date,\
        b_other_user = b_other_user, b_price = b_price, b_location = b_location\
        , b_date = b_date, a_price = a_price, a_location = a_location\
        , a_date = a_date, a_txids=a_txids, a_names=a_names, s_return=s_return)

@app.route('/active_drops_<string:chat_id>_delete/')
@login_required
def deleteTX(chat_id):
    deleteOrder(chat_id)
    return redirect(url_for('active_drops'))


@app.route('/active_drops_<string:chat_id>_decline/')
@login_required
def declineTX(chat_id):
    repostOffer(chat_id)
    return redirect(url_for('active_drops'))

@app.route('/active_drops_<string:chat_id>_confirm/')
@login_required
def confirmTX(chat_id):
    #dropStatus updates as per current values
    tx_status = dropStatus(chat_id, current_user.username, status = True)
    order_status = search_OrderValue('status', txid = chat_id)

    if order_status != "Buyer_Seller_TX_Confirm":
        statusUpdate(tx_status, chat_id)
        return redirect(url_for('transactionpage', chat_id = chat_id))

    if order_status == "Buyer_Seller_TX_Confirm":
        newBoxAssignment(chat_id, "SafeDrop UBC Box 1")
        return redirect(url_for('boxUse', chat_id = chat_id))




@app.route('/active_drops_<string:chat_id>/', methods=['GET', 'POST'])
@login_required
def transactionpage(chat_id):
    FirstName = str(search_value('first_name', str(current_user.username)))
    LastName = str(search_value('last_name', current_user.username))

    request_code = url_for('confirmTX', chat_id = chat_id)
    code_msg = dropStatus(chat_id, current_user.username, msg = True)
    if search_OrderValue('status', txid = chat_id) == "Buyer_Seller_TX_Confirm":
        code_msg = 'Request Box Access Code'
    item_name = search_OrderValue('I_name', txid = chat_id)
    location = search_OrderValue('Location', txid = chat_id)
    item_desc = search_OrderValue('description', txid = chat_id)
    item_cost = search_OrderValue('Cost', txid = chat_id)
    buy_user = search_OrderValue('B_username', txid = chat_id)
    sell_user = search_OrderValue('S_username', txid = chat_id)
    date_init = date_time(search_OrderValue('date_initialized', txid = chat_id))
    oldMsg = searchMsg(chat_id)
    oldMsgTime = []
    oldMsgMsg = []
    oldMsgSender = []
    for item in oldMsg:
        try:
            oldMsgSender.append(item.Sender_username)
            oldMsgMsg.append(item.msg)
            oldMsgTime.append(date_time(item.msg_date))
        except TypeError:
            oldMsgTime.append('<i>time not available</i>')


    return render_template('message.html', currentuser = \
    str(current_user.username), FirstName=FirstName, LastName=LastName, \
    chatid = chat_id, item_name=item_name, location = location, \
    item_desc=item_desc, item_cost=item_cost, buy_user=buy_user, \
    sell_user=sell_user, date_init=date_init, oldMsgMsg = oldMsgMsg, oldMsgSender=oldMsgSender,\
    request_code = request_code, code_msg = code_msg, oldMsgTime=oldMsgTime)

def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')

@socketio.on('my event')
def handle_my_custom_event(data, methods=['GET', 'POST']):
    print('received my event: ' + str(data))
    room = data['room']
    join_room(room)

    try:
        msg = data['message']
        Send_name = data['user_name']
        txid = data['room']
        B_name = search_OrderValue('B_username', txid = txid)
        S_name = search_OrderValue('S_username', txid = txid)
        newMsg(txid, B_name, S_name, Send_name, msg)
    except KeyError:
        pass

    socketio.emit('my response',  data, callback=messageReceived, room=room)


@app.route('/<string:chat_id>_box_use/', methods=['GET', 'POST'])
@login_required
def boxUse(chat_id):
    if request.method=='POST':
        item = search_OrderValue('I_name', txid = chat_id)

        sub = request.form.get("submit")
        if sub == 'submit':
            confirm_msg = dropStatus(chat_id, current_user.username, msg = True)
            codeView = requestCode(chat_id, current_user.username)
            return render_template("boxUse.html", code = codeView, item = item,\
            confirm_msg = confirm_msg)


    else:
        b_user = search_OrderValue('B_username', txid = chat_id)
        s_user = search_OrderValue('S_username', txid = chat_id)
        confirm_msg = dropStatus(chat_id, current_user.username, msg = True)
        stage = search_ChatValue('stage', chat_id)
        if stage == "Buyer Access" and current_user.username == b_user:
            code_msg = "Request Box Access Code"
        elif stage == "Seller Access" and current_user.username == s_user:
            code_msg = "Request Box Access Code"
        elif stage == "Buyer Access" and current_user.username == s_user:
            code_msg = "Item successfully dropped!"
        elif stage == "Seller Access" and current_user.username == b_user:
            code_msg = "Awaiting seller drop..."
        else:
            code_msg = 'Confirm transaction before requesting an access code.'
        item = search_OrderValue('I_name', txid = chat_id)
        return render_template("boxUse.html",code = code_msg, item = item,\
        confirm_msg = confirm_msg, stage=stage)


@socketio.on('confirm_drop')
def handle_confirm_drop(data, methods=['GET', 'POST']):
    print('got the sauce: ' + str(data))
    url = data['image_list']
    print
    user = str(current_user.username)
    I_name = str(data["I_name"])
    I_cost = str(data["I_cost"])
    I_desc = str(data["I_desc"])
    location = str(data["place"])
    S_name = str(current_user.username)
    B_name = 'None'
    txid = newOrder(S_name, B_name, I_name, I_desc, I_cost, location)
    url_id = search_OrderValue('img_url', txid=txid)
    for item in url:
        url = str(item)
        newImage(url_id, txid, user, url)


@app.route('/new_drop/', methods=['GET', 'POST'])
@login_required
def new_drop():
    FirstName = str(search_value('first_name', str(current_user.username)))
    LastName = str(search_value('last_name', current_user.username))
    if request.method=='POST':
        return redirect(url_for('active_drops'))
    return render_template("new_drop.html", FirstName = FirstName,\
    LastName = LastName)

@app.route('/safebucks_add_100/')
@login_required
def add100():
    user = current_user.username
    try:
        if searchBucks(user) == None:
            addUserBucks(user)
        else:
            add100Bucks(user)
        return redirect(url_for('profile'))
    except AttributeError:
        addUserBucks(user)
        return redirect(url_for('profile'))

@app.route('/buy_<string:txid>', methods=['GET', 'POST'])
@login_required
def buypage(txid):
    FirstName = str(search_value('first_name', str(current_user.username)))
    LastName = str(search_value('last_name', current_user.username))

    if request.method=='POST':
        SellerName = str(search_OrderValue('S_username', txid=txid))
        sub = request.form.get("submit")
        if sub == 'submit':
            msg = request.form.get("message")
            newMsg(txid, current_user.username, SellerName, current_user.username, msg)
            confirmBuyer(current_user.username, txid)
            return(redirect(url_for('active_drops')))
    else:
        url = []
        img = search_allImages(search_OrderValue('img_url', txid=txid))
        for item in img:
            try:
                img_url = item.url
                img_url = str(img_url)
                url.append(img_url)
            except IndexError:
                img_url = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAOEAAADhCAMAAAAJbSJIAAAAMFBMVEXp7vG6vsHs8fS3u77Cxsnn7O/d4uXFyczN0dTKztHS19rk6ezi5+rX3N+9wcS1ubzIzxKwAAACWElEQVR4nO3b4XKiMBRAYUkUhQT6/m+7CK2GABJjdrl3e75/djo0p2FIGOF0AgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAczpRxdMa2rrkW0LQnmY2mtrYqwtpWYqLpvsr0jY0SEy+FJvA7sT66Z8E0JQOr6ixuEs00sKaAaRKPDloYT1LblVgrvBV5ml4KDuu/Lyz5zyroFxYOe6/M/ZeOQtNdrbV9e8loVFHo+mn9t8PV9cNDiTEbln/ubzL2XxoKw83J19tDlV9obrMtav/uJCoonO/B3x6r/MI6KrxtTaK57B1KkmBYXXQf1WwUDrcjq4nyC+u0QtMMv7eWKL/QR2fp+noxBq4myi9MutJ8B64lKihMWC0egSuJ8gsTVvwgcJmooXBv1zYLXCRqKNzZeUeBcaKKwvvdU7V197QIjBJ1FL64A14JnCdqKdyyGjhLVF64ERgm6i7cDAwSVRe+CHwmKiv0PvjwMvCRqKvQWeseH3YCfxJVFbr7D38SdwOrym0f6nCrw3LBuFMCpy2eokIXTk1CoLpC9xy5SwrUVujCsbuUQGWFbj72hD5lhW6vRnthVqCmwrxARYWZgXoKcwPVFGYHqimMv7egkEIhKKSQwuOFhedsXXQoScJhffgagoJCOYcqicJ3yCychtWWeM57fFrF+v0/+W+Zfrzc519Gn8bFRt6z+tEDGB+7invfYv4AxseCbzvk8AUnMefR4r/PuLMtpPcSAwfGt7cC2lpo312JxULyK6QAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA8Gv8AbboIxLMxQycAAAAAElFTkSuQmCC"
                url.append(img_url)
        item_name = search_OrderValue('I_name', txid = txid)
        location = search_OrderValue('Location', txid = txid)
        item_desc = search_OrderValue('description', txid = txid)
        item_cost = search_OrderValue('Cost', txid = txid)
        SellerName = search_OrderValue('S_username', txid=txid)
        date_init = date_time(search_OrderValue('date_initialized', txid = txid))
        return render_template("buyPage(new).html", FirstName = FirstName, \
            LastName = LastName, i_name = item_name,\
            location = location, i_desc = item_desc, i_cost = item_cost,\
            SellerName = SellerName, date_init = date_init, \
            currentuser = current_user.username, txid = txid, url=url)

#not connected to date_time function
@app.route('/history/',  methods=['GET', 'POST'])
@login_required
def history():
    FirstName = str(search_value('first_name', str(current_user.username)))
    LastName = str(search_value('last_name', current_user.username))

    h_txid = search_allOrders(SUN = current_user.username, BUN = current_user.username)
    h_txids = []
    b_names = []
    s_names = []
    h_item = []
    h_price = []
    h_location = []
    h_date_open = []
    h_date_close = []
    h_status = []
    h_txstatus = []
    h_url = []
    for item in h_txid:
        txid = str(item)
        h_txids.append(item.TXID)
        b_names.append(item.B_username)
        s_names.append(item.S_username)
        h_item.append(item.I_name)
        h_price.append(item.Cost)
        h_location.append(item.Location)
        h_date_open.append(item.date_initialized)
        h_date_close.append(item.date_resolved)
        h_txstatus.append(item.status)
        h_status.append(search_OrderValue('status',item.TXID))
        h_url.append(item.img_url)
    currentuser = current_user.username
    return render_template('history.html', FirstName=FirstName, currentuser=currentuser, \
        LastName = LastName, h_txids=h_txids, b_names=b_names, s_names=s_names,\
        h_item=h_item, h_price=h_price, h_location=h_location, h_url=h_url,\
        h_date_open=h_date_open, h_date_close=h_date_close,\
        h_status=h_status, h_txstatus = h_txstatus)


@app.route('/browse_<int:page_id>/', methods=['GET', 'POST'])
def browse(page_id):
    FirstName = str(search_value('first_name', str(current_user.username)))
    LastName = str(search_value('last_name', current_user.username))

    if request.method == "POST":
        searchValue = request.form.get("Search")

        SellerName = []
        ItemName = []
        ItemDesc = []
        ItemCost = []
        Location = []
        date_post = []
        txid = []
        url = []

        load_start = (page_id - 1)*10
        load_pages = []
        load_txids = browseRecent()

        load_pages = load_txids[load_start:(load_start+10)]

        for item in load_pages:
            if item.S_username != None:
                if SequenceMatcher(None, item.I_name, searchValue).ratio() > 0.6:
                    SellerName.append(item.S_username)
                    ItemName.append(item.I_name)
                    ItemDesc.append(item.description)
                    ItemCost.append(item.Cost)
                    Location.append(item.Location)
                    date_post.append(date_time(item.date_initialized))
                    txid.append(item.TXID)
                    img = search_allImages(url_id=item.img_url)
                    for item in img:
                        try:
                            img_url = img.url
                            img_url = str(img)
                        except IndexError:
                            img_url = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAOEAAADhCAMAAAAJbSJIAAAAMFBMVEXp7vG6vsHs8fS3u77Cxsnn7O/d4uXFyczN0dTKztHS19rk6ezi5+rX3N+9wcS1ubzIzxKwAAACWElEQVR4nO3b4XKiMBRAYUkUhQT6/m+7CK2GABJjdrl3e75/djo0p2FIGOF0AgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAczpRxdMa2rrkW0LQnmY2mtrYqwtpWYqLpvsr0jY0SEy+FJvA7sT66Z8E0JQOr6ixuEs00sKaAaRKPDloYT1LblVgrvBV5ml4KDuu/Lyz5zyroFxYOe6/M/ZeOQtNdrbV9e8loVFHo+mn9t8PV9cNDiTEbln/ubzL2XxoKw83J19tDlV9obrMtav/uJCoonO/B3x6r/  MI6KrxtTaK57B1KkmBYXXQf1WwUDrcjq4nyC+u0QtMMv7eWKL/QR2fp+noxBq4myi9MutJ8B64lKihMWC0egSuJ8gsTVvwgcJmooXBv1zYLXCRqKNzZeUeBcaKKwvvdU7V197QIjBJ1FL64A14JnCdqKdyyGjhLVF64ERgm6i7cDAwSVRe+CHwmKiv0PvjwMvCRqKvQWeseH3YCfxJVFbr7D38SdwOrym0f6nCrw3LBuFMCpy2eokIXTk1CoLpC9xy5SwrUVujCsbuUQGWFbj72hD5lhW6vRnthVqCmwrxARYWZgXoKcwPVFGYHqimMv7egkEIhKKSQwuOFhedsXXQoScJhffgagoJCOYcqicJ3yCychtWWeM57fFrF+v0/+W+Zfrzc519Gn8bFRt6z+tEDGB+7invfYv4AxseCbzvk8AUnMefR4r/PuLMtpPcSAwfGt7cC2lpo312JxULyK6QAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA8Gv8AbboIxLMxQycAAAAAElFTkSuQmCC"
                        url.append(img_url)
            else:
                pass
        if len(ItemName) == 0:
            searches = "empty"
        else:
            searches = "values"
        return render_template("browse.html", FirstName = FirstName, \
        LastName = LastName, SellerName=SellerName, \
        ItemName=ItemName, ItemDesc=ItemDesc, ItemCost=ItemCost, \
        Location=Location, date_post=date_post, txid=txid, url=url, searches=searches)



    SellerName = []
    ItemName = []
    ItemDesc = []
    ItemCost = []
    Location = []
    date_post = []
    txid = []
    url = []

    load_start = (page_id - 1)*10
    load_pages = []
    load_txids = browseRecent()

    load_pages = load_txids[load_start:(load_start+10)]

    for item in load_pages:
        if item.S_username != None:
            SellerName.append(item.S_username)
            ItemName.append(item.I_name)
            ItemDesc.append(item.description)
            ItemCost.append(item.Cost)
            Location.append(item.Location)
            date_post.append(date_time(item.date_initialized))
            txid.append(item.TXID)
            img = search_allImages(url_id=item.img_url)
            if len(img) != 0:
                for item in img:
                    try:
                        img_url = item.url
                        img_url = str(img_url)
                    except IndexError:
                        img_url = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAOEAAADhCAMAAAAJbSJIAAAAMFBMVEXp7vG6vsHs8fS3u77Cxsnn7O/d4uXFyczN0dTKztHS19rk6ezi5+rX3N+9wcS1ubzIzxKwAAACWElEQVR4nO3b4XKiMBRAYUkUhQT6/m+7CK2GABJjdrl3e75/djo0p2FIGOF0AgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAczpRxdMa2rrkW0LQnmY2mtrYqwtpWYqLpvsr0jY0SEy+FJvA7sT66Z8E0JQOr6ixuEs00sKaAaRKPDloYT1LblVgrvBV5ml4KDuu/Lyz5zyroFxYOe6/M/ZeOQtNdrbV9e8loVFHo+mn9t8PV9cNDiTEbln/ubzL2XxoKw83J19tDlV9obrMtav/uJCoonO/B3x6r/MI6KrxtTaK57B1KkmBYXXQf1WwUDrcjq4nyC+u0QtMMv7eWKL/QR2fp+noxBq4myi9MutJ8B64lKihMWC0egSuJ8gsTVvwgcJmooXBv1zYLXCRqKNzZeUeBcaKKwvvdU7V197QIjBJ1FL64A14JnCdqKdyyGjhLVF64ERgm6i7cDAwSVRe+CHwmKiv0PvjwMvCRqKvQWeseH3YCfxJVFbr7D38SdwOrym0f6nCrw3LBuFMCpy2eokIXTk1CoLpC9xy5SwrUVujCsbuUQGWFbj72hD5lhW6vRnthVqCmwrxARYWZgXoKcwPVFGYHqimMv7egkEIhKKSQwuOFhedsXXQoScJhffgagoJCOYcqicJ3yCychtWWeM57fFrF+v0/+W+Zfrzc519Gn8bFRt6z+tEDGB+7invfYv4AxseCbzvk8AUnMefR4r/PuLMtpPcSAwfGt7cC2lpo312JxULyK6QAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA8Gv8AbboIxLMxQycAAAAAElFTkSuQmCC"
                    except TypeError:
                        img_url = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAOEAAADhCAMAAAAJbSJIAAAAMFBMVEXp7vG6vsHs8fS3u77Cxsnn7O/d4uXFyczN0dTKztHS19rk6ezi5+rX3N+9wcS1ubzIzxKwAAACWElEQVR4nO3b4XKiMBRAYUkUhQT6/m+7CK2GABJjdrl3e75/djo0p2FIGOF0AgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAczpRxdMa2rrkW0LQnmY2mtrYqwtpWYqLpvsr0jY0SEy+FJvA7sT66Z8E0JQOr6ixuEs00sKaAaRKPDloYT1LblVgrvBV5ml4KDuu/Lyz5zyroFxYOe6/M/ZeOQtNdrbV9e8loVFHo+mn9t8PV9cNDiTEbln/ubzL2XxoKw83J19tDlV9obrMtav/uJCoonO/B3x6r/MI6KrxtTaK57B1KkmBYXXQf1WwUDrcjq4nyC+u0QtMMv7eWKL/QR2fp+noxBq4myi9MutJ8B64lKihMWC0egSuJ8gsTVvwgcJmooXBv1zYLXCRqKNzZeUeBcaKKwvvdU7V197QIjBJ1FL64A14JnCdqKdyyGjhLVF64ERgm6i7cDAwSVRe+CHwmKiv0PvjwMvCRqKvQWeseH3YCfxJVFbr7D38SdwOrym0f6nCrw3LBuFMCpy2eokIXTk1CoLpC9xy5SwrUVujCsbuUQGWFbj72hD5lhW6vRnthVqCmwrxARYWZgXoKcwPVFGYHqimMv7egkEIhKKSQwuOFhedsXXQoScJhffgagoJCOYcqicJ3yCychtWWeM57fFrF+v0/+W+Zfrzc519Gn8bFRt6z+tEDGB+7invfYv4AxseCbzvk8AUnMefR4r/PuLMtpPcSAwfGt7cC2lpo312JxULyK6QAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA8Gv8AbboIxLMxQycAAAAAElFTkSuQmCC"
                    url.append(img_url)
            else:
                img_url = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAOEAAADhCAMAAAAJbSJIAAAAMFBMVEXp7vG6vsHs8fS3u77Cxsnn7O/d4uXFyczN0dTKztHS19rk6ezi5+rX3N+9wcS1ubzIzxKwAAACWElEQVR4nO3b4XKiMBRAYUkUhQT6/m+7CK2GABJjdrl3e75/djo0p2FIGOF0AgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAczpRxdMa2rrkW0LQnmY2mtrYqwtpWYqLpvsr0jY0SEy+FJvA7sT66Z8E0JQOr6ixuEs00sKaAaRKPDloYT1LblVgrvBV5ml4KDuu/Lyz5zyroFxYOe6/M/ZeOQtNdrbV9e8loVFHo+mn9t8PV9cNDiTEbln/ubzL2XxoKw83J19tDlV9obrMtav/uJCoonO/B3x6r/MI6KrxtTaK57B1KkmBYXXQf1WwUDrcjq4nyC+u0QtMMv7eWKL/QR2fp+noxBq4myi9MutJ8B64lKihMWC0egSuJ8gsTVvwgcJmooXBv1zYLXCRqKNzZeUeBcaKKwvvdU7V197QIjBJ1FL64A14JnCdqKdyyGjhLVF64ERgm6i7cDAwSVRe+CHwmKiv0PvjwMvCRqKvQWeseH3YCfxJVFbr7D38SdwOrym0f6nCrw3LBuFMCpy2eokIXTk1CoLpC9xy5SwrUVujCsbuUQGWFbj72hD5lhW6vRnthVqCmwrxARYWZgXoKcwPVFGYHqimMv7egkEIhKKSQwuOFhedsXXQoScJhffgagoJCOYcqicJ3yCychtWWeM57fFrF+v0/+W+Zfrzc519Gn8bFRt6z+tEDGB+7invfYv4AxseCbzvk8AUnMefR4r/PuLMtpPcSAwfGt7cC2lpo312JxULyK6QAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA8Gv8AbboIxLMxQycAAAAAElFTkSuQmCC"
                url.append(img_url)


        else:
            pass
    return render_template("browse.html", FirstName = FirstName, \
    LastName = LastName, SellerName=SellerName, \
    ItemName=ItemName, ItemDesc=ItemDesc, ItemCost=ItemCost, \
    Location=Location, date_post=date_post, txid=txid, url=url)


if __name__ == '__main__':
    socketio.run(app, debug=False)

if __name__ == "__main__":
    app.run(debug=False)
