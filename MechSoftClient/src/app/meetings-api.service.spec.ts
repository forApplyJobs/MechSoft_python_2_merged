import { TestBed } from '@angular/core/testing';

import { MeetingsAPIService } from './meetings-api.service';

describe('MeetingsAPIService', () => {
  let service: MeetingsAPIService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(MeetingsAPIService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
