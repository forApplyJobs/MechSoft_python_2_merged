from wtforms import DateField, FieldList, Form, FormField, IntegerField, StringField, TimeField, ValidationError
from wtforms.validators import DataRequired

from Server.validations import endtime_control, not_null_or_empty, owner_cannot_added, owner_has_conflicting_meeting, validate_future_datetime

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
    start_time = TimeField('Start Time', format='%H:%M:%S', validators=[DataRequired(),validate_future_datetime])
    end_time = TimeField('End Time', format='%H:%M:%S', validators=[DataRequired(),endtime_control])
    participants = FieldList(IntegerField())
    guests = FieldList(FormField(GuestForm))
    owner_id = IntegerField('Owner ID', validators=[DataRequired(),owner_has_conflicting_meeting])

    # def validate(self):
    #     if not Form.validate(self):
    #         return False
    #     if owner_has_conflicting_meeting(self.owner_id.data, self.date.data, self.start_time.data, self.end_time.data):
    #         self.owner_id.errors.append('Owner has another meeting during this time.')
    #         return False

    #     return True

    

class EditMeetingForm(Form):
    meeting_id = IntegerField('Meeting ID', validators=[DataRequired()])
    topic = StringField('Topic', validators=[DataRequired()])
    date = DateField('Date', format='%Y-%m-%d', validators=[DataRequired()])
    start_time = TimeField('Start Time', format='%H:%M:%S', validators=[DataRequired()])
    end_time = TimeField('End Time', format='%H:%M:%S', validators=[DataRequired()])
    participants = FieldList(IntegerField(),validators=[owner_cannot_added])
    guests = FieldList(FormField(GuestForm), min_entries=0)
    owner_id = IntegerField('Owner ID', validators=[DataRequired(),not_null_or_empty,owner_has_conflicting_meeting])
    # def validate(self): 
    #     if not Form.validate(self):
    #         return False

    #     if owner_has_conflicting_meeting(self.owner_id.data, self.date.data, self.start_time.data, self.end_time.data):
    #         self.owner_id.errors.append('Owner has another meeting during this time.')
    #         return False

    #     return True