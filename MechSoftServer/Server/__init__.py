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
## db ve api kurma muhabbetleri


basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mssql+pyodbc://eurocommerce:eurocommerce@DESKTOP-MS8F2DP/MechSoft1?driver=ODBC+Driver+17+for+SQL+Server"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
# ...

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
api = Api(app) 

## form ve validation muhabbetleri





## routing muhabbetleri





















    


if __name__ == '__main__':
    # app.app_context().push()
    # db.create_all()
    # user=User(firstname="bikka2",lastname="bilkasoy2",email="bilka2@bilka.com")
    # db.session.add(user)
    # db.session.commit()
    app.run(debug=True)