from dataclasses import fields
from datetime import datetime
import os
from wsgiref.validate import validator
from flask import Flask, abort, jsonify, render_template, request, url_for, redirect
from flask_cors import CORS
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
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
api = Api(app) 

## form ve validation muhabbetleri
  
def is_email_valid(address):
    # Check if the e-mail address already exists in database.
    return True  # or False

def user_email(form, field):
    if not is_email_valid(field.data):
        raise validator.ValidationError("The e-mail address {} is already taken.".format(field.data))

class MeetingForm(Form):
    topic = StringField('Topic')
    date = DateField('Date', format='%Y-%m-%d')
    start_time = TimeField('Start Time', format='%H:%M:%S')
    end_time = TimeField('End Time', format='%H:%M:%S')
    participants = FieldList(IntegerField('Participant ID'))

class EditMeetingForm(Form):
    class Meta:
        csrf = False
    meeting_id = IntegerField('Meeting ID')
    topic = StringField('Topic')
    date = DateField('Date', format='%Y-%m-%d')
    start_time = TimeField('Start Time', format='%H:%M:%S')
    end_time = TimeField('End Time', format='%H:%M:%S')
    participants = FieldList(IntegerField('Participant ID'))


class UserForm(Form):
    topic = StringField("Topic")
    date = DateField('Date', format='%Y-%m-%d')
    start_time = TimeField('Start Time', format='%H:%M:%S')
    end_time = TimeField('End Time', format='%H:%M:%S')
    participants = FieldList(IntegerField('Participant ID'))


## routing muhabbetleri





















    


if __name__ == '__main__':
    # app.app_context().push()
    # db.create_all()
    # user=User(firstname="bikka2",lastname="bilkasoy2",email="bilka2@bilka.com")
    # db.session.add(user)
    # db.session.commit()
    app.run(debug=True)