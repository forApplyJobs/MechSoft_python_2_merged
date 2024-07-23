from dataclasses import fields
import os
from wsgiref.validate import validator
from flask import Flask, abort, jsonify, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from mysqlx import IntegrityError
from wtforms import FieldList, Form, StringField,validators,IntegerField,DateField,TimeField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm
from flask_restful import Resource, Api 
from sqlalchemy.sql import func

## db ve api kurma muhabbetleri


basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mssql+pyodbc://eurocommerce:eurocommerce@DESKTOP-MS8F2DP/MechSoft1?driver=ODBC+Driver+17+for+SQL+Server"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
# ...

api = Api(app) 

## form ve validation muhabbetleri
  
def is_email_valid(address):
    # Check if the e-mail address already exists in database.
    return True  # or False

def user_email(form, field):
    if not is_email_valid(field.data):
        raise validator.ValidationError("The e-mail address {} is already taken.".format(field.data))

class MeetingForm(FlaskForm):
    topic = StringField('Topic')
    date = DateField('Date', format='%Y-%m-%d')
    start_time = TimeField('Start Time', format='%H:%M:%S')
    end_time = TimeField('End Time', format='%H:%M:%S')
    participants = FieldList(IntegerField('Participant ID'))


# Flask-RESTful resource route muhabbeti
class AddMeeting(Resource):
    def post(self):
        form = MeetingForm(data=request.get_json())
        if form.validate():
            try:
                participants_ids = [int(id.strip()) for id in request.get_json().get('participants', '').split(',')]
                participants = User.query.filter(User.id.in_(participants_ids)).all()
                
                meeting=Meeting(**request.get_json())
                
                db.session.add(meeting)
                db.session.commit()
                
                return {"message": "Meeting created successfully", "meeting": str(meeting)}, 201
            except IntegrityError:
                db.session.rollback()
                abort(300)
            except ValueError:
                abort(400)
        else:
            print("not validated")
            abort(400)
class Hello(Resource): 
  
    # corresponds to the GET request. 
    # this function is called whenever there 
    # is a GET request for this resource 
    def get(self): 
  
        return jsonify({'message': 'hello world'}) 
  
    # Corresponds to POST request 
    def post(self): 
          
        data = request.get_json()     # status code 
        return jsonify({'data': data}), 201
  
class Square(Resource): 
  
    def get(self, num): 
  
        return jsonify({'square': num**2}) 







## routing muhabbetleri
api.add_resource(AddMeeting, '/AddMeeting')  

# adding the defined resources along with their corresponding urls 
api.add_resource(Hello, '/') 
api.add_resource(Square, '/square/<int:num>') 



















##model 

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return f'<User {self.firstname} {self.lastname}>'

# Meeting Model
meeting_participants = db.Table('meeting_participants',
    db.Column('meeting_id', db.Integer, db.ForeignKey('meeting.id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True)
)

class Meeting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    topic = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    participants = db.relationship('User', secondary=meeting_participants, backref=db.backref('meetings', lazy=True))

    def __repr__(self):
        return f'<Meeting {self.topic}>'
    


if __name__ == '__main__':
    # app.app_context().push()
    # db.create_all()
    # user=User(firstname="bilka",lastname="bilkasoy",email="bilka@bilka.com")
    # db.session.add(user)
    # db.session.commit()
    app.run(debug=True)