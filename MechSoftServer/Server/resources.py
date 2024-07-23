from datetime import datetime
from sqlite3 import IntegrityError
from flask import abort, jsonify, request
from flask_restful import Resource
from Server import db
from Server.forms import EditMeetingForm, GuestForm, MeetingForm, UserForm
from Server.models import Guest, Meeting, User


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
# class AddMeeting(Resource):
#     def post(self):
#         print(request.get_json())
#         form = MeetingForm(data=request.get_json())
#         if form.validate():
#             try:
#                 data = request.get_json()
#                 topic = data.get('topic')
#                 date = datetime.strptime(data.get('date'), '%Y-%m-%d').date()
#                 start_time = datetime.strptime(data.get('start_time'), '%H:%M:%S').time()
#                 end_time = datetime.strptime(data.get('end_time'), '%H:%M:%S').time()
#                 participant_ids = data.get('participants')
#                 participants = User.query.filter(User.id.in_(participant_ids)).all()
#                 if(len(participant_ids)!=len(participants)):
#                     return "not valid users"

#                 meeting = Meeting(
#                     topic=topic,
#                     date=date,
#                     start_time=start_time,
#                     end_time=end_time,
#                     participants=participants
#                 )
#                 print(meeting)
#                 db.session.add(meeting)
#                 db.session.commit()
#                 return {"message": "Meeting created successfully", "meeting": str(meeting)}, 201
#             except IntegrityError:
#                 db.session.rollback()
#                 abort(300)
#             except ValueError:
#                 abort(400)
#         else:
#             print("not validated")
#             abort(400)


class AddMeeting(Resource):
    def post(self):
        form = MeetingForm(data=request.get_json())
        if form.validate():
            print(request.get_json())
            try:
                data = request.get_json()
                topic = data.get('topic')
                date = datetime.strptime(data.get('date'), '%Y-%m-%d').date()
                start_time = datetime.strptime(data.get('start_time'), '%H:%M:%S').time()
                end_time = datetime.strptime(data.get('end_time'), '%H:%M:%S').time()
                participant_ids = data.get('participants')
                guest_list = data.get('guests', [])
                owner_id = data.get('owner_id')

                participants = User.query.filter(User.id.in_(participant_ids)).all()
                guests = [Guest(name=g['name'], email=g['email']) for g in guest_list]
                owner = User.query.get(owner_id)
                
                if len(participant_ids) != len(participants) or not owner:
                    return {"message": "Invalid data"}, 400

                meeting = Meeting(
                    topic=topic,
                    date=date,
                    start_time=start_time,
                    end_time=end_time,
                    participants=participants,
                    guests=guests,
                    owner=owner
                )
                db.session.add(meeting)
                db.session.commit()
                return {"message": "Meeting created successfully", "meeting": str(meeting)}, 201
            except IntegrityError:
                db.session.rollback()
                abort(500)
            except ValueError:
                abort(400)
        else:
            abort(400)


class EditMeeting(Resource):
    def post(self):
        form = EditMeetingForm(data=request.get_json())
        print(request.get_json())
        print(form.errors)
        if form.validate():
            print("helloooo")
            try:
                # Formdan gelen veriyi al
                meeting_id = form.meeting_id.data
                topic = form.topic.data
                date = form.date.data
                start_time = form.start_time.data
                end_time = form.end_time.data
                participant_ids = form.participants.data
                guest_forms = form.guests.data
                
                # Toplantıyı ID'sine göre bul
                meeting = db.session.get(Meeting, meeting_id)
                if not meeting:
                    abort(404, description="Meeting not found")

                # Katılımcıları al
                participants = User.query.filter(User.id.in_(participant_ids)).all()
                if len(participant_ids) != len(participants):
                    return {"message": "Not valid users"}, 400
                
                # Misafirleri kontrol et
                if guest_forms is None or len(guest_forms) == 0:
                    # Misafirleri temizle
                    for guest in meeting.guests:
                        db.session.delete(guest)
                else:
                    # Yeni misafirleri oluştur veya güncelle
                    existing_guests = {guest.id for guest in meeting.guests}
                    new_guests = {guest_data.get('id') for guest_data in guest_forms if 'id' in guest_data}

                    guests_to_remove = existing_guests - new_guests
                    for guest_id in guests_to_remove:
                        guest_to_remove = Guest.query.get(guest_id)
                        if guest_to_remove:
                            db.session.delete(guest_to_remove)

                    for guest_data in guest_forms:
                        guest_id = guest_data.get('id')
                        guest = Guest.query.get(guest_id)
                        if guest:
                            guest.name = guest_data.get('name')
                            guest.email = guest_data.get('email')
                        else:
                            guest = Guest(name=guest_data.get('name'), email=guest_data.get('email'))
                            guest.meeting = meeting
                            db.session.add(guest)

                # Toplantı verilerini güncelle
                meeting.topic = topic
                meeting.date = date
                meeting.start_time = start_time
                meeting.end_time = end_time
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
                ],
                "guests": [
                    {
                        "name": guest.name,
                        "email": guest.email
                    }
                    for guest in meeting.guests
                ],
                "owner_id":meeting.owner_id
            }
            
            return jsonify(meeting_data)
        
        except Exception as e:
            return {"message": "An error occurred", "error": str(e)}, 500


class DeleteMeeting(Resource):
    def delete(self, meeting_id):
        try:
            # Toplantıyı ID'sine göre bul
            meeting = Meeting.query.get(meeting_id)
            if not meeting:
                return {"message": "Meeting not found"}, 404
            
            # Toplantının misafirlerini sil
            if meeting.guests:
                for guest in meeting.guests:
                    db.session.delete(guest)
            
            # Toplantıyı sil
            db.session.delete(meeting)
            db.session.commit()
            
            return {"message": "Meeting deleted successfully"}, 200
        
        except Exception as e:
            db.session.rollback()
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