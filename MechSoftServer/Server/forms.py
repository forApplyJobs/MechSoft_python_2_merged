from wtforms import DateField, FieldList, Form, FormField, IntegerField, StringField, TimeField
from wtforms.validators import DataRequired

class UserForm(Form):
    firstname = StringField('Firstname', validators=[DataRequired()])
    lastname = StringField('Lastname', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])

class GuestForm(Form):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])

class MeetingForm(Form):
    topic = StringField('Topic', validators=[DataRequired()])
    date = DateField('Date', format='%Y-%m-%d', validators=[DataRequired()])
    start_time = TimeField('Start Time', format='%H:%M:%S', validators=[DataRequired()])
    end_time = TimeField('End Time', format='%H:%M:%S', validators=[DataRequired()])
    participants = FieldList(IntegerField())
    guests = FieldList(FormField(GuestForm))
    owner_id = IntegerField('Owner ID', validators=[DataRequired()])

    

class EditMeetingForm(Form):
    meeting_id = IntegerField('Meeting ID', validators=[DataRequired()])
    topic = StringField('Topic', validators=[DataRequired()])
    date = DateField('Date', format='%Y-%m-%d', validators=[DataRequired()])
    start_time = TimeField('Start Time', format='%H:%M:%S', validators=[DataRequired()])
    end_time = TimeField('End Time', format='%H:%M:%S', validators=[DataRequired()])
    participants = FieldList(IntegerField())
    guests = FieldList(FormField(GuestForm), min_entries=0)
    owner_id = IntegerField('Owner ID', validators=[DataRequired()])