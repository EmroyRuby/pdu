import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';

@Component({
  selector: 'app-create-event',
  templateUrl: './create-event.component.html',
  styleUrls: ['./create-event.component.css']
})
export class CreateEventComponent {
  createEventForm: FormGroup;

  constructor(private fb: FormBuilder, private router: Router) {
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

  review() {
    const formData = this.createEventForm.value;
    console.log(formData);
    if (this.createEventForm.valid) {
      const eventId = 1; // TO DO
      this.router.navigate(['/events/event'], {
        queryParams: { id: eventId }
      });
    }
  }

}
