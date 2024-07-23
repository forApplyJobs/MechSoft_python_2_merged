import { Component } from '@angular/core';
import { MeetingsAPIService } from '../meetings-api.service';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';


@Component({
  selector: 'app-add-meeting',
  standalone: true,
  imports: [CommonModule,FormsModule],
  templateUrl: './add-meeting.component.html',
  styleUrl: './add-meeting.component.css'
})
export class AddMeetingComponent {
  meetingData = {
    topic: '',
    date: '',
    start_time: '',
    end_time: '',
    participants: []
  };



  participantsString: string = '';  // Bu, formda kullanılan stringi temsil eder

  constructor(private meetingService: MeetingsAPIService, private router: Router) {}

  // Zaman verisini 'HH:mm:ss' formatına dönüştüren bir fonksiyon
  private formatTime(time: string): string {
    const [hours, minutes] = time.split(':');
    return `${hours}:${minutes}:00`;
  }

  // Toplantıyı eklemek için kullanılan fonksiyon
  addMeeting(): void {
    // Katılımcı ID'lerini diziye dönüştür
    const participantsArray = this.participantsString
      .split(',')
      .map(id => id.trim())
      .filter(id => id.length > 0)
      .map(id => parseInt(id, 10));

    // Zaman verilerini formatla
    const formattedMeetingData = {
      ...this.meetingData,
      start_time: this.formatTime(this.meetingData.start_time),
      end_time: this.formatTime(this.meetingData.end_time),
      participants: participantsArray // Katılımcıları dizi olarak gönder
    };

    // API'ye veri gönder
    this.meetingService.addMeeting(formattedMeetingData).subscribe(response => {
      alert(response.message);
      this.router.navigate(['/meetings']);
    });
  }
}
