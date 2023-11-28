import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { EventService } from '../event.service';
import { Event } from '../../models';

@Component({
  selector: 'app-create-event',
  templateUrl: './create-event.component.html',
  styleUrls: ['./create-event.component.css']
})
export class CreateEventComponent implements OnInit {
  createEventForm: FormGroup;
  categories: string[] = [];
  selectedCategories: string[] = [];
  newCategory: string = '';
  modalText: string = '123';

  constructor(private fb: FormBuilder, private router: Router, private eventService: EventService) {
    this.createEventForm = this.fb.group({
      title: ['', Validators.required],
      description: ['', Validators.required],
      location: ['', Validators.required],
      is_public: [false, Validators.required],
      price: [null],
      capacity: [null, Validators.required],
      registration_end_date: [null, Validators.required],
      start_date: [null, Validators.required],
      end_date: [null, Validators.required],
      photo: [null]
    });
  }

  async ngOnInit() {
    this.categories = await this.eventService.getCategories();
  }

  async publish() {
    const formData = this.createEventForm.value;
    try{
      if (this.createEventForm.valid) {
        const newEvent = this.createEventForm.value as Event;
        newEvent.categories = this.selectedCategories;
        newEvent.created_at = new Date();
        newEvent.updated_at = new Date();
        newEvent.price = this.createEventForm.value.price.toString();
        console.log(newEvent);
        const eventId = await this.eventService.addEvent(newEvent);
        this.router.navigate(['/event'], {
          queryParams: { id: eventId }
        });
      }
      else{
        //TODO: find a way to return specific info about which fields in the form did not pass the validation
        throw new Error("something went bad");
      }
    }
    catch (e: any){
      if (e instanceof Error){
        this.modalText = e.message;
      }
      else{
        //TODO: add aption to display error messages from HTML errors
        this.modalText = 'Something went wrong, please check the required fields and try again';
      }
      document.getElementById("openModal1")?.click();
    }
  }

  addCategory(category: string) {
    if (!this.isCategorySelected(category)) {
      this.selectedCategories.push(category);
    }
  }
  
  removeSelectedCategory(categoryToRemove: string) {
    if (this.selectedCategories !== null) {
      const index = this.selectedCategories.indexOf(categoryToRemove);
      if (index !== -1) {
        this.selectedCategories.splice(index, 1);
      }
    }
  }

  isCategorySelected(category: string): boolean {
    return this.selectedCategories !== null && this.selectedCategories.includes(category);
  }

  goBack() {
    this.router.navigate(['/home']);
  }

}
