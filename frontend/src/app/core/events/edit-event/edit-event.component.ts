import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { EventService } from '../event.service';

@Component({
  selector: 'app-edit-event',
  templateUrl: './edit-event.component.html',
  styleUrls: ['./edit-event.component.css']
})
export class EditEventComponent implements OnInit {
  createEventForm!: FormGroup;
  tags: string[] = [];
  selectedTags: string[] = [];
  newTag: string = '';
  eventId!: number;
  event: any;

  constructor(private fb: FormBuilder, private route: ActivatedRoute, private router: Router, private eventService: EventService) {

  }

  ngOnInit(): void {
    this.tags = this.eventService.getTags();
    this.route.queryParamMap.subscribe(params => {
      const eventId = params.get('id');
      if (eventId) {
        this.eventId = parseInt(eventId, 10)
        this.event = this.eventService.getEventById(this.eventId);
      }
    });
    this.createEventForm = this.fb.group({
      title: [this.event.title, Validators.required],
      description: [this.event.description, Validators.required],
      location: [this.event.location, Validators.required],
      isPublic: [this.event.isPublic],
      price: [this.event.price],
      capacity: [this.event.capacity],
      registrationEndDate: [this.event.registrationEndDate],
      startDate: [this.event.startDate],
      endDate: [this.event.endDate],
      image: [this.event.image]
    });
    this.selectedTags = this.event.tags;
  }

  publish() {
    const formData = this.createEventForm.value;
    if (this.createEventForm.valid) {
      let newEvent = this.createEventForm.value as Event;
      this.eventService.editEvent(this.eventId, newEvent);
      this.router.navigate(['/event'], {
        queryParams: { id: this.eventId }
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
