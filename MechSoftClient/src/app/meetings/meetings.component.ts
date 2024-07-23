import { Component } from '@angular/core';
import { MeetingsAPIService } from '../meetings-api.service';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';

@Component({
  selector: 'app-meetings',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './meetings.component.html',
  styleUrl: './meetings.component.css'
})
export class MeetingsComponent {
  meetings: any[] = [];

  constructor(private meetingService: MeetingsAPIService,
    private router: Router,
  ) { }

  ngOnInit(): void {
    this.meetingService.getMeetings().subscribe(data => {
      this.meetings = data.meetings;
    });
  }
  editMeeting(meetingId: number): void {
    this.router.navigate(['/edit-meeting', meetingId]);
  }
}
