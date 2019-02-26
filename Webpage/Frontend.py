from flask import Flask, render_template, redirect, url_for, request
from flask_login import LoginManager, UserMixin, login_user, login_required,\
logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash



app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////logins.db'
app.config['SECRET_KEY'] = 'thisissecret'

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True)
    password_hash = db.Column(db.String(254))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def index():
        return render_template("index.html")

@app.route('/signup/')
def signup():
    return render_template("signup.html")


@app.route('/login/', methods=['GET', 'POST'])
def login():
    message= None
    if current_user.is_authenticated:
        return redirect(url_for('profile'))
    if request.method == 'POST':
        userentry = request.form['username']
        passentry = request.form['password']
        user = User.query.filter_by(username=userentry).first()
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
    return render_template("profile.html")

@app.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)
