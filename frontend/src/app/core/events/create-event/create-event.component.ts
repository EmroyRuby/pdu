import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { EventService } from '../event.service';

@Component({
  selector: 'app-create-event',
  templateUrl: './create-event.component.html',
  styleUrls: ['./create-event.component.css']
})
export class CreateEventComponent implements OnInit {
  createEventForm: FormGroup;
  tags: string[] = [];
  selectedTags: string[] = [];
  newTag: string = '';

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

  ngOnInit(): void {
    this.tags = this.eventService.getTags();
  }

  publish() {
    const formData = this.createEventForm.value;
    if (this.createEventForm.valid) {
      // TO DO dodac tagi !!!
      const newEvent = this.createEventForm.value as Event;
      const eventId = this.eventService.addEvent(newEvent);
      this.router.navigate(['/event'], {
        queryParams: { id: eventId }
      });
    }
  }

  addTag(tag: string) {
    if (!this.isTagSelected(tag)) {
      this.selectedTags.push(tag);
    }
  }
  
  removeSelectedTag(tagToRemove: string) {
    if (this.selectedTags !== null) {
      const index = this.selectedTags.indexOf(tagToRemove);
      if (index !== -1) {
        this.selectedTags.splice(index, 1);
      }
    }
  }

  isTagSelected(tag: string): boolean {
    return this.selectedTags !== null && this.selectedTags.includes(tag);
  }

}
