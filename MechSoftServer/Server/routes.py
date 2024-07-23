from Server.resources import AddMeeting, DeleteMeeting, EditMeeting, GetAllMeetings, GetMeetingById, GetUserMeetings, GetUsers, Users
from Server import api

api.add_resource(AddMeeting, '/AddMeeting')  
api.add_resource(EditMeeting, '/EditMeeting')  
api.add_resource(Users, '/deneme')  
api.add_resource(GetAllMeetings,'/GetAllMeetings')
api.add_resource(GetUserMeetings, '/user/<int:user_id>/meetings')
api.add_resource(GetMeetingById, '/GetMeeting/<int:meeting_id>')
api.add_resource(DeleteMeeting, '/DeleteMeeting/<int:meeting_id>')
api.add_resource(GetUsers, '/GetUsers')  

