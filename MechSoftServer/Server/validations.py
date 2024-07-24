
from datetime import datetime
from wsgiref.validate import validator

from wtforms import ValidationError

from Server.models import Meeting
from Server import db

def is_email_valid(address):
    # Check if the e-mail address already exists in database.
    return True  # or False

def user_email(form, field):
    if not is_email_valid(field.data):
        raise ValidationError("The e-mail address {} is already taken.".format(field.data))
    
def endtime_control(form, field):
    if form.start_time.data>field.data:
        raise ValidationError("Start time must be smaller than end time.".format(field.data))
    
    
def not_null_or_empty(form, field):
     if form.owner_id.data is None or []:
            raise ValidationError('Owner ID cannot be null.')


def owner_cannot_added(form,field):
     if form.owner_id.data in field.data:
            raise ValidationError('Owner cannot be added as participant.')


def validate_future_datetime(form, field):
    if not form.date.data or not field.data:
         raise ValidationError("This field is required.")
    date_obj = datetime.strptime(form.date.data, '%Y-%m-%d').date()
    start_time_obj = datetime.strptime(field.data, '%H:%M:%S').time()
    current_datetime = datetime.now()
    
    start_datetime = datetime.combine(date_obj, start_time_obj)
    
    if start_datetime <= current_datetime:
        raise ValidationError("Start time must be in the future.")




def owner_has_conflicting_meeting(form, field):
    # Tarih ve zaman verilerini almak için
    if not form.date.data or not field.data:
        raise ValidationError("This field is required.")
    date_obj = datetime.strptime(form.date.data, '%Y-%m-%d').date()
    start_time_obj = datetime.strptime(form.start_time.data, '%H:%M:%S').time()
    end_time_obj = datetime.strptime(form.end_time.data, '%H:%M:%S').time()

    start_datetime = datetime.combine(date_obj, start_time_obj)
    end_datetime = datetime.combine(date_obj, end_time_obj)

    query = db.session.query(Meeting).filter(
        Meeting.owner_id == field.data,
        Meeting.date == date_obj,
        (
            (Meeting.start_time <= start_time_obj) & (Meeting.end_time > start_time_obj) |
            (Meeting.start_time < end_time_obj) & (Meeting.end_time >= end_time_obj) |
            (Meeting.start_time >= start_time_obj) & (Meeting.end_time <= end_time_obj)
        )
    )
    if hasattr(form, 'meeting_id') and form.meeting_id.data:
        query = query.filter(Meeting.id != form.meeting_id.data)
    conflicting_meeting = query.first()

    if conflicting_meeting:
        raise ValidationError('Owner has another meeting during this time.')