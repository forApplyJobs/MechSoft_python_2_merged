import { Component, OnInit } from '@angular/core';
import { MeetingsAPIService } from '../meetings-api.service';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { UsersAPIService } from '../users-api.service';


@Component({
  selector: 'app-add-meeting',
  standalone: true,
  imports: [CommonModule,FormsModule],
  templateUrl: './add-meeting.component.html',
  styleUrl: './add-meeting.component.css'
})
export class AddMeetingComponent  implements OnInit{
  meetingData = {
    topic: '',
    date: '',
    start_time: '',
    end_time: '',
    participants: [] as any[],
    guests: [] as any[],  // Misafirler
    owner_id: null as number | null // Toplantı sahibi
  };

  availableUsers: any[] = [];
  selectedUsers: any[] = [];
  availableGuests: any[] = [];

  newGuest = {
    name: '',
    email: ''
  };

  constructor(
    private meetingService: MeetingsAPIService,
    private router: Router,
    private usersService: UsersAPIService
  ) {}

  ngOnInit(): void {
    this.loadUsers();
  }

  // Kullanıcıları yükler
  loadUsers(): void {
    this.usersService.getUsers().subscribe(
      response => {
        if (response && response.users) {
          this.availableUsers = [...response.users];
        } else {
          console.error('User data is missing');
        }
      },
      error => {
        console.error('Error loading users:', error);
      }
    );
  }

  // Kullanıcı ekler
  addUser(user: any): void {
    this.selectedUsers.push(user);
    this.availableUsers = this.availableUsers.filter(u => u.id !== user.id);
  }

  // Kullanıcı çıkarır
  removeUser(user: any): void {
    this.selectedUsers = this.selectedUsers.filter(u => u.id !== user.id);
    this.availableUsers.push(user);
  }

  // Misafir ekler
  addGuest(guest: any): void {
    if (guest.name && guest.email) {
      this.meetingData.guests.push(guest);
      this.newGuest = { name: '', email: '' }; // Temizle
      // Kapat modal
      const modalElement = document.getElementById('guestModal');
      if (modalElement) {
        const modal = (window as any).bootstrap.Modal.getInstance(modalElement);
        if (modal) {
          modal.hide();
        }
      }
    }
  }

  // Misafir çıkarır
  removeGuest(guest: any): void {
    this.meetingData.guests = this.meetingData.guests.filter(g => g.email !== guest.email);
  }

  // Toplantıyı eklemek için kullanılan fonksiyon
  addMeeting(): void {
    const participantsArray = this.selectedUsers.map(user => user.id);

    // API'ye veri gönder
    this.meetingService.addMeeting({
      ...this.meetingData,
      start_time: this.meetingData.start_time, // Zaman formatını değiştirmiyoruz
      end_time: this.meetingData.end_time,
      participants: participantsArray // Katılımcı ID'leri
    }).subscribe(response => {
      alert(response.message);
      this.router.navigate(['/meetings']);
    });
  }
}
