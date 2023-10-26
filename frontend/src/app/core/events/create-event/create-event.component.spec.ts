import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CreateEventComponent } from './create-event.component';

describe('CreateEventComponent', () => {
  let component: CreateEventComponent;
  let fixture: ComponentFixture<CreateEventComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [CreateEventComponent]
    });
    fixture = TestBed.createComponent(CreateEventComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
