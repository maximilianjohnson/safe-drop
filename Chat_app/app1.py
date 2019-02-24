import pusher
from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///messages.db'

pusher_client = pusher.Pusher(
  app_id='720958',
  key='2bf1c4d449c7cdf89c2a',
  secret='0b30474d49bf7e6ebb23',
  cluster='us2',
  ssl=True
)

db = SQLAlchemy(app)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    message = db.Column(db.String(500))

db.create_all()

@app.route('/')
def index():

    messages = Message.query.all()

    return render_template('index.html', messages=messages)


@app.route('/message', methods=['POST'])
def message():

    try:

        username = request.form.get('username')
        message = request.form.get('message')

        new_message = Message(username=username, message=message)
        db.session.add(new_message)
        db.session.commit()

        pusher_client.trigger('chat-channel', 'new-message', {'username' : username, 'message': message})

        return jsonify({'result' : 'success'})

    except:

        return jsonify({'result' : 'failure'})


if __name__ == '__main__':
    app.run(debug=True)
