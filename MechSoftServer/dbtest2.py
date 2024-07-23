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

class Users(Resource):
    def post(self):
        form = UserForm(data=request.get_json())

        print("hello")
        if form.validate():
            # Create the new user with form.populate_obj()
            pass
        else:
            abort(400)
        return "user representation", 201

# Flask-RESTful resource route muhabbeti
class AddMeeting(Resource):
    def post(self):
        print(request.get_json())
        form = MeetingForm(data=request.get_json())
        if form.validate():
            try:
                data = request.get_json()
                topic = data.get('topic')
                date = datetime.strptime(data.get('date'), '%Y-%m-%d').date()
                start_time = datetime.strptime(data.get('start_time'), '%H:%M:%S').time()
                end_time = datetime.strptime(data.get('end_time'), '%H:%M:%S').time()
                participant_ids = data.get('participants')
                participants = User.query.filter(User.id.in_(participant_ids)).all()
                if(len(participant_ids)!=len(participants)):
                    return "not valid users"

                meeting = Meeting(
                    topic=topic,
                    date=date,
                    start_time=start_time,
                    end_time=end_time,
                    participants=participants
                )
                print(meeting)
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


class EditMeeting(Resource):
    def post(self):
        form = EditMeetingForm(data=request.get_json())
        
        if form.validate():
            try:
                # Formdan gelen veriyi al
                meeting_id = form.meeting_id.data
                topic = form.topic.data
                date = form.date.data
                start_time = form.start_time.data
                end_time = form.end_time.data
                participant_ids = form.participants.data
                
                # Toplantıyı ID'sine göre bul
                meeting = db.session.get(Meeting, meeting_id)
                if not meeting:
                    abort(404, description="Meeting not found")

                # Katılımcıları al
                participants = User.query.filter(User.id.in_(participant_ids)).all()
                print(len(participant_ids))
                print(participant_ids)
                if len(participant_ids) != len(participants):
                    return {"message": "Not valid users"}, 400
                
                # Toplantı verilerini güncelle
                if topic:
                    meeting.topic = topic
                if date:
                    meeting.date = date
                if start_time:
                    meeting.start_time = start_time
                if end_time:
                    meeting.end_time = end_time
                if participant_ids:
                    meeting.participants = participants

                # Değişiklikleri veritabanına kaydet
                db.session.commit()
                return {"message": "Meeting updated successfully", "meeting": str(meeting)}, 200
            
            except IntegrityError:
                db.session.rollback()
                abort(400, description="Error updating meeting")
            except ValueError:
                abort(400, description="Invalid date or time format")
        else:
            return {"message": "Invalid form data", "errors": form.errors}, 400


class GetAllMeetings(Resource):
    def get(self):
        try:
            # Tüm toplantıları al
            meetings = Meeting.query.all()
            
            # Toplantıları JSON formatına dönüştür
            meetings_list = []
            for meeting in meetings:
                meeting_data = {
                    "id": meeting.id,
                    "topic": meeting.topic,
                    "date": meeting.date.strftime('%Y-%m-%d'),
                    "start_time": meeting.start_time.strftime('%H:%M:%S'),
                    "end_time": meeting.end_time.strftime('%H:%M:%S'),
                    "participants": [
                        {
                            "id": participant.id,
                            "name": participant.firstname+" "+participant.lastname,  # Kullanıcının adı
                            "email": participant.email  # Kullanıcının e-posta adresi
                        }
                        for participant in meeting.participants
                    ]
                }
                meetings_list.append(meeting_data)
            
            return jsonify({"meetings": meetings_list})
        except Exception as e:
            return {"message": "An error occurred", "error": str(e)}, 500

class GetUserMeetings(Resource):
    def get(self, user_id):
        try:
            # Kullanıcıyı ID'ye göre bul
            user = User.query.get(user_id)
            if not user:
                abort(404, description="User not found")
            
            # Kullanıcının katıldığı toplantıları al
            meetings = user.meetings
            
            # Toplantıları JSON formatına dönüştür
            meetings_list = []
            for meeting in meetings:
                meeting_data = {
                    "id": meeting.id,
                    "topic": meeting.topic,
                    "date": meeting.date.strftime('%Y-%m-%d'),
                    "start_time": meeting.start_time.strftime('%H:%M:%S'),
                    "end_time": meeting.end_time.strftime('%H:%M:%S'),
                    "participants": [
                        {
                            "id": participant.id,
                            "name": participant.firstname+" "+participant.lastname,  # Kullanıcının adı
                            "email": participant.email  # Kullanıcının e-posta adresi
                        }
                        for participant in meeting.participants
                    ]
                }
                meetings_list.append(meeting_data)
            
            return jsonify({"meetings": meetings_list})
        except Exception as e:
            return {"message": "An error occurred", "error": str(e)}, 500

class GetMeetingById(Resource):
    def get(self, meeting_id):
        try:
            # Toplantıyı ID'sine göre bul
            meeting = Meeting.query.get(meeting_id)
            if not meeting:
                return {"message": "Meeting not found"}, 404
            
            # Toplantı verilerini JSON formatına dönüştür
            meeting_data = {
                "id": meeting.id,
                "topic": meeting.topic,
                "date": meeting.date.strftime('%Y-%m-%d'),
                "start_time": meeting.start_time.strftime('%H:%M:%S'),
                "end_time": meeting.end_time.strftime('%H:%M:%S'),
                "participants": [
                    {
                        "id": participant.id,
                        "name": participant.firstname + " " + participant.lastname,  # Kullanıcının adı
                        "email": participant.email  # Kullanıcının e-posta adresi
                    }
                    for participant in meeting.participants
                ]
            }
            
            return jsonify(meeting_data)
        
        except Exception as e:
            return {"message": "An error occurred", "error": str(e)}, 500



## users


class GetUsers(Resource):
    def get(self):
        try:
            # Tüm kullanıcıları al
            users = User.query.all()
            
            # Kullanıcıları JSON formatına dönüştür
            users_list = [
                {
                    "id": user.id,
                    "name": f"{user.firstname} {user.lastname}",
                    "email": user.email
                }
                for user in users
            ]
            
            return jsonify({"users": users_list})
        except Exception as e:
            return {"message": "An error occurred", "error": str(e)}, 500
## routing muhabbetleri


api.add_resource(AddMeeting, '/AddMeeting')  
api.add_resource(EditMeeting, '/EditMeeting')  
api.add_resource(Users, '/deneme')  
api.add_resource(GetAllMeetings,'/GetAllMeetings')
api.add_resource(GetUserMeetings, '/user/<int:user_id>/meetings')
api.add_resource(GetMeetingById, '/GetMeeting/<int:meeting_id>')

api.add_resource(GetUsers, '/GetUsers')  

















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
    # user=User(firstname="bikka2",lastname="bilkasoy2",email="bilka2@bilka.com")
    # db.session.add(user)
    # db.session.commit()
    app.run(debug=True)