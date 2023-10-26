import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { EventService } from '../event.service';

@Component({
  selector: 'app-create-event',
  templateUrl: './create-event.component.html',
  styleUrls: ['./create-event.component.css']
})
export class CreateEventComponent {
  createEventForm: FormGroup;

  constructor(private fb: FormBuilder, private router: Router, private eventService: EventService) {
    this.createEventForm = this.fb.group({
      title: ['', Validators.required],
      description: ['', Validators.required],
      location: ['', Validators.required],
      isPublic: [false],
      price: [null],
      capacity: [null],
      registrationEndDate: [null],
      startDate: [null],
      endDate: [null],
      image: [null]
    });
  }

  publish() {
    const formData = this.createEventForm.value;
    console.log(formData);
    if (this.createEventForm.valid) {
      const newEvent = this.createEventForm.value as Event;
      const eventId = this.eventService.addEvent(newEvent);
      this.router.navigate(['/events/event'], {
        queryParams: { id: eventId }
      });
    }
  }

}
