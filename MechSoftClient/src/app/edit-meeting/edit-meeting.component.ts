import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { MeetingsAPIService } from '../meetings-api.service';
import { catchError, throwError } from 'rxjs';
import { UsersAPIService } from '../users-api.service';

import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-edit-meeting',
  standalone: true,
  imports: [CommonModule,ReactiveFormsModule],
  templateUrl: './edit-meeting.component.html',
  styleUrls: ['./edit-meeting.component.css']
})
export class EditMeetingComponent implements OnInit {
  meetingForm: FormGroup;
  meetingId: number;
  users: any[] = [];
  availableUsers: any[] = [];
  selectedUsers: any[] = [];

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private meetingService: MeetingsAPIService,
    private fb: FormBuilder,
    private usersService: UsersAPIService
  ) {
    this.meetingForm = this.fb.group({
      topic: ['', Validators.required],
      date: ['', Validators.required],
      start_time: ['', Validators.required],
      end_time: ['', Validators.required],
      participants: ['']
    });
  }

  ngOnInit(): void {
    this.meetingId = Number(this.route.snapshot.paramMap.get('id'));
    this.loadMeeting();
    this.loadUsers();
  }

  // Toplantı verilerini yükler
  loadMeeting(): void {
    this.meetingService.getMeetingById(this.meetingId).pipe(
      catchError(error => {
        console.error('Error loading meeting:', error);
        return throwError(() => new Error('Error loading meeting'));
      })
    ).subscribe(
      response => {
        if (response) {
          const meeting = response;
          this.selectedUsers = meeting.participants; // Mevcut katılımcıları seçili kullanıcılar olarak ayarla
          this.meetingForm.patchValue({
            topic: meeting.topic,
            date: meeting.date,
            start_time: meeting.start_time,
            end_time: meeting.end_time,
            participants: meeting.participants.map((p: any) => p.id) // Katılımcı ID'lerini seçili olarak ayarla
          });
        } else {
          console.error('Meeting data is missing');
        }
      },
      error => {
        console.error('Error loading meeting:', error);
      }
    );
  }

  // Kullanıcıları yükler
  loadUsers(): void {
    this.usersService.getUsers().subscribe(
      response => {
        if (response && response.users) {
          this.users = response.users;
          this.updateAvailableUsers();
        } else {
          console.error('User data is missing');
        }
      },
      error => {
        console.error('Error loading users:', error);
      }
    );
  }

  // Kullanıcıları günceller
  updateAvailableUsers(): void {
    this.availableUsers = this.users.filter(user => !this.selectedUsers.find(selected => selected.id === user.id));
  }

  // Kullanıcı ekler
  addUser(user: any): void {
    this.selectedUsers.push(user);
    this.updateAvailableUsers();
  }

  // Kullanıcı çıkarır
  removeUser(user: any): void {
    this.selectedUsers = this.selectedUsers.filter(u => u.id !== user.id);
    this.updateAvailableUsers();
  }

  // Toplantıyı günceller
  editMeeting(): void {
    if (this.meetingForm.valid) {
      const meetingData = this.meetingForm.value;
      // Katılımcı ID'lerini string olarak değil dizi olarak gönder
      meetingData.participants = this.selectedUsers.map((p: any) => p.id);

      this.meetingService.editMeeting(this.meetingId, meetingData).subscribe(
        response => {
          alert(response.message);
          this.router.navigate(['/meetings']);
        },
        error => {
          console.error('Error updating meeting', error);
          alert('Error updating meeting');
        }
      );
    } else {
      alert('Please fill in all required fields.');
    }
  }
}
