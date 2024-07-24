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
from flask_migrate import Migrate
import os
from dotenv import load_dotenv

load_dotenv()
DBNAME=os.getenv('DBNAME')
USERNAME=os.getenv('DBUSERNAME')
PASSWORD=os.getenv('DBPASSWORD')
HOSTNAME=os.getenv('DBHOSTNAME')
basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = f"mssql+pyodbc://{USERNAME}:{PASSWORD}@{HOSTNAME}/{DBNAME}?driver=ODBC+Driver+17+for+SQL+Server"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
api = Api(app) 

