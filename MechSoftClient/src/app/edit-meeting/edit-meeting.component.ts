import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { FormArray, FormBuilder, FormGroup, FormsModule, ReactiveFormsModule, Validators } from '@angular/forms';
import { MeetingsAPIService } from '../meetings-api.service';
import { catchError, throwError } from 'rxjs';
import { UsersAPIService } from '../users-api.service';

import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-edit-meeting',
  standalone: true,
  imports: [CommonModule,ReactiveFormsModule,FormsModule],
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
      participants: this.fb.array([]),
      guests: this.fb.array([]),
      owner_id: ['']
    });
  }

  ngOnInit(): void {
    this.meetingId = Number(this.route.snapshot.paramMap.get('id'));
    this.loadMeeting();
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
            owner_id: meeting.owner_id // owner_id'yi form alanına ekleyin
          });

          // Katılımcıları form alanına ekle
          const participantsArray = this.meetingForm.get('participants') as FormArray;
          participantsArray.clear(); // Önceki katılımcıları temizle
          meeting.participants.forEach((participant: { id: number }) => {
            participantsArray.push(this.fb.control(participant.id));
          });

          // Misafirleri form alanına ekle
          const guestsArray = this.meetingForm.get('guests') as FormArray;
          guestsArray.clear(); // Önceki misafirleri temizle
          meeting.guests.forEach((guest: { name: string; email: string }) => {
            guestsArray.push(this.fb.group({
              name: [guest.name, Validators.required],
              email: [guest.email, [Validators.required, Validators.email]]
            }));
          });

          this.loadUsers();
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

  // Misafir ekler
  addGuest(): void {
    const guestsArray = this.meetingForm.get('guests') as FormArray;
    guestsArray.push(this.fb.group({
      name: ['', Validators.required],
      email: ['', [Validators.required, Validators.email]]
    }));
  }

  // Misafiri çıkarır
  removeGuest(index: number): void {
    const guestsArray = this.meetingForm.get('guests') as FormArray;
    guestsArray.removeAt(index);
  }

  // Toplantıyı günceller
  editMeeting(): void {
    if (this.meetingForm.valid) {
      // Katılımcı ID'lerini güncel `selectedUsers` ile güncelle
      const participantsArray = this.meetingForm.get('participants') as FormArray;
      participantsArray.clear(); // Önceki katılımcıları temizle
      this.selectedUsers.forEach(user => {
        participantsArray.push(this.fb.control(user.id));
      });
  
      // Form verilerini al
      const meetingData = this.meetingForm.value;
      meetingData.participants = participantsArray.value; // Güncellenmiş katılımcıları al
      meetingData.guests = this.meetingForm.get('guests')?.value;
  
      console.log(meetingData);
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
      console.log(this.meetingForm.controls);
      alert('Please fill in all required fields.');
    }
  }
  
}
