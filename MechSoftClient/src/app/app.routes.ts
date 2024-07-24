import { Routes } from '@angular/router';
import { MeetingsComponent } from './meetings/meetings.component';
import { AddMeetingComponent } from './add-meeting/add-meeting.component';
import { EditMeetingComponent } from './edit-meeting/edit-meeting.component';
import { MeetingDetailsComponent } from './meeting-details/meeting-details.component';

export const routes: Routes = [{ path: '', component: MeetingsComponent },{ path: 'meetings/:meetingId', component: MeetingDetailsComponent },{ path: 'add-meeting', component: AddMeetingComponent },{ path: 'edit-meeting/:id', component: EditMeetingComponent }];
