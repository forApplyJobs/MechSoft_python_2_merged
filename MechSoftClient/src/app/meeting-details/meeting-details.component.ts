import { Component } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { MeetingsAPIService } from '../meetings-api.service';
import { CommonModule } from '@angular/common';
import { UsersAPIService } from '../users-api.service';

@Component({
  selector: 'app-meeting-details',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './meeting-details.component.html',
  styleUrl: './meeting-details.component.css'
})
export class MeetingDetailsComponent {
  meeting: any;
  meetingId: number;
  owner: any;

  constructor(
    private route: ActivatedRoute,
    private meetingService: MeetingsAPIService,
    private usersService:UsersAPIService
  ) {}

  ngOnInit(): void {
    const id = this.route.snapshot.paramMap.get('meetingId');
    if (id !== null) {
      this.meetingId = +id;
      this.getMeetingDetails();
    } else {
      console.error('Meeting ID is null');
    }
  }

  getMeetingDetails(): void {
    this.meetingService.getMeetingById(this.meetingId).subscribe(
      data => {
        this.meeting = data;
        this.getOwnerDetails(this.meeting.owner_id);
      },
      error => {
        console.error('Error fetching meeting details:', error);
      }
    );
  }

  getOwnerDetails(ownerId: number): void {
    this.usersService.getUsers().subscribe(
      data => {
        this.owner = data.find((user: { id: number; }) => user.id === ownerId);
      },
      error => {
        console.error('Error fetching owner details:', error);
      }
    );
  }
}
