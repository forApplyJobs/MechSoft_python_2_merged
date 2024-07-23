import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TopperComponent } from './topper.component';

describe('TopperComponent', () => {
  let component: TopperComponent;
  let fixture: ComponentFixture<TopperComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [TopperComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(TopperComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
