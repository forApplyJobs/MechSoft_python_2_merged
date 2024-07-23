import { Routes } from '@angular/router';
import { MeetingsComponent } from './meetings/meetings.component';
import { AddMeetingComponent } from './add-meeting/add-meeting.component';
import { EditMeetingComponent } from './edit-meeting/edit-meeting.component';

export const routes: Routes = [{ path: 'meetings', component: MeetingsComponent },{ path: 'add-meeting', component: AddMeetingComponent },{ path: 'edit-meeting/:id', component: EditMeetingComponent }];
