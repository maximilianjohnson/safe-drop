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

@app.route('/message/',  methods=['GET', 'POST'])
@login_required
def message_redirect():
    if request.method == 'POST':
        userentry = request.form['username']
        currentuser = current_user.username
        if len(userentry) > len(currentuser):
            chatid = currentuser + "_" + userentry
        else:
            chatid = userentry + "_" + currentuser
        return redirect(url_for('message', chat_id=chatid))
    return render_template('message_redirect.html')

@app.route('/message/<string:chat_id>_chat/', methods=['GET', 'POST'])
@login_required
def message(chat_id):
    return render_template('message.html', currentuser = str(current_user.username), chatid = chat_id)

def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')

@socketio.on('my event')
def handle_my_custom_event(data, methods=['GET', 'POST']):
    print('received my event: ' + str(data))
    room = data['room']
    join_room(room)
    socketio.emit('my response',  data, callback=messageReceived, room=room)


if __name__ == '__main__':
    socketio.run(app, debug=True)

if __name__ == "__main__":
    app.run(debug=True)
