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

  constructor(private meetingService: MeetingsAPIService, private router: Router) { }

  ngOnInit(): void {
    this.loadMeetings();
  }

  // Toplantıları yükleyen fonksiyon
  loadMeetings(): void {
    this.meetingService.getMeetings().subscribe(data => {
      this.meetings = data.meetings;
    });
  }

  // Toplantıyı düzenleme fonksiyonu
  editMeeting(meetingId: number): void {
    this.router.navigate(['/edit-meeting', meetingId]);
  }

  detailsButton(meetingId:number):void{
    this.router.navigate(['/meetings', meetingId]);
  }
  // Toplantıyı silme fonksiyonu
  deleteMeeting(meetingId: number): void {
    if (confirm('Are you sure you want to delete this meeting?')) {
      this.meetingService.deleteMeeting(meetingId).subscribe(
        response => {
          alert('Meeting deleted successfully');
          this.loadMeetings(); // Toplantılar listesine güncel verileri yükle
        },
        error => {
          console.error('Error deleting meeting', error);
          alert('Error deleting meeting');
        }
      );
    }
  }
}
