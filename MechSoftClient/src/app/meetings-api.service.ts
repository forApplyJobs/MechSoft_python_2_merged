import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { catchError, Observable, throwError } from 'rxjs';
@Injectable({
  providedIn: 'root'
})
export class MeetingsAPIService {

  private apiUrl = 'http://127.0.0.1:5000'; // API'nin URL'si

  constructor(private http: HttpClient) { }

  // Toplantı oluşturma
  private formatTime(time: string): string {
    const [hours, minutes] = time.split(':');
    return `${hours}:${minutes}:00`;
  }

  // Toplantı oluşturma
  addMeeting(meetingData: any): Observable<any> {
    const headers = new HttpHeaders({
      'Content-Type': 'application/json'
    });
  
    // Zaman verilerini formatla
    const formattedMeetingData = {
      ...meetingData,
      start_time: this.formatTime(meetingData.start_time),
      end_time: this.formatTime(meetingData.end_time),
      participants: meetingData.participants || [],  // Katılımcı ID'leri
      guests: meetingData.guests || [],  // Misafirler
      owner_id: meetingData.owner_id  // Toplantının sahibi
    };
  
    return this.http.post<any>(`${this.apiUrl}/AddMeeting`, formattedMeetingData, { headers });
  }

  // Toplantıyı güncelleme
  editMeeting(meetingId: number, meetingData: any): Observable<any> {
    // Zaman verilerini formatla
    const formattedMeetingData = {
      ...meetingData,
      start_time: this.formatTime(meetingData.start_time),
      end_time: this.formatTime(meetingData.end_time),
      participants: meetingData.participants  // Katılımcı ID'lerini sayıya çevir
    };

    return this.http.post<any>(`${this.apiUrl}/EditMeeting`, { meeting_id: meetingId, ...formattedMeetingData });
  }

  // Tüm toplantıları getirme
  getMeetings(): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/GetAllMeetings`);
  }
  deleteMeeting(meetingId: number): Observable<any> {
    // DELETE isteği gönder
    return this.http.delete<any>(`${this.apiUrl}/DeleteMeeting/${meetingId}`);
  }
  // Belirli bir kullanıcının toplantılarını getirme
  getUserMeetings(userId: number): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/user/${userId}/meetings`);
  }

  getMeetingById(meetingId: number): Observable<any> {
    const url = `${this.apiUrl}/GetMeeting/${meetingId}`;
    return this.http.get<any>(url).pipe(
      catchError(error => {
        console.error('Error fetching meeting data:', error);
        return throwError(() => new Error('Error fetching meeting data'));
      })
    );
  }
  
  
}
