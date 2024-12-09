import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { EventService } from '../event.service';
import { Event } from '../../models';

@Component({
  selector: 'app-edit-event',
  templateUrl: './edit-event.component.html',
  styleUrls: ['./edit-event.component.css']
})
export class EditEventComponent implements OnInit {
  editEventForm!: FormGroup;
  categories: string[] = [];
  selectedCategories: string[] = [];
  newCategory: string = '';
  eventId!: number;
  event!: Event;
  modalText = '';
  errors = '';
  selectedFile = undefined;

  constructor(private fb: FormBuilder, private route: ActivatedRoute, private router: Router, private eventService: EventService) {
    this.editEventForm = this.fb.group({
      title: ['', Validators.required],
      description: ['', Validators.required],
      location: ['', Validators.required],
      is_public: [false, Validators.required],
      price: [null, Validators.required],
      capacity: [null],
      registration_end_date: [null, Validators.required],
      start_date: [null, Validators.required],
      end_date: [null, Validators.required],
      created_at: [null],
      updated_at: [null],
      user: [null],
      user_email: [null],
      categories: [null],
      photo: [null],
    });
  }

  async ngOnInit() {
    this.categories = await this.eventService.getCategories();
    this.route.queryParamMap.subscribe(async params => {
      const eventId = params.get('id');
      if (eventId) {
        this.eventId = parseInt(eventId, 10)
        this.event = await this.eventService.getEventById(this.eventId);
        console.log(this.event.location)
        let eventData = {
          title: this.event.title,
          description: this.event.description,
          location: this.event.description,
          is_public: this.event.is_public,
          price: Number(this.event.price),
          capacity: this.event.capacity,
          remaining_slots: this.event.remaining_slots,
          registration_end_date: new Date(this.event.registration_end_date).toISOString().replace('Z', ''),
          start_date: new Date(this.event.start_date).toISOString().replace('Z', ''),
          end_date: new Date(this.event.end_date).toISOString().replace('Z', ''),
          created_at: this.event.created_at,
          updated_at: this.event.updated_at,
          user: this.event.user,
          user_email: this.event.user_email,
          photo: this.event.photo,
        }
        console.log(eventData);
        this.editEventForm.patchValue(eventData);
        /*
        this.editEventForm = this.fb.group({
          title: [this.event.title, Validators.required],
          description: this.event.description,
          location: this.event.description,
          is_public: this.event.is_public,
          price: Number(this.event.price),
          capacity: this.event.capacity,
          remaining_slots: this.event.remaining_slots,
          registration_end_date: new Date(this.event.registration_end_date),
          start_date: new Date(this.event.start_date),
          end_date: new Date(this.event.end_date),
          created_at: this.event.created_at,
          updated_at: this.event.updated_at,
          user: this.event.user,
          user_email: this.event.user_email,
          photo: this.event.photo,
        });
        */
        if(this.event.categories){
          this.selectedCategories = this.event.categories;
        }
      }
    });
    
  }

  async publish() {
    const formData = this.editEventForm.value;
    try{
      if (this.editEventForm.valid) {
        let newEvent = this.editEventForm.value as Event;
        console.log("ala:" + newEvent.location);
        console.log("formData: " + formData);
        console.log("magda: " + formData.location);
        newEvent.categories = this.selectedCategories;
        newEvent.updated_at = new Date();
        newEvent.price = this.editEventForm.value.price.toString();
        newEvent.photo = this.selectedFile;
        await this.eventService.editEvent(this.eventId, newEvent);
        this.router.navigate(['/event'], {
          queryParams: { id: this.eventId }
        });
      }
      else{
        this.errors = "";
        Object.keys(this.editEventForm.controls).forEach(controlName => {
          const control = this.editEventForm.get(controlName);
          if (control && control.invalid){
            this.errors += controlName + " is required\n"
          }
        });
        throw new Error(this.errors);
      }
    }
    catch (e: any){
      if (e instanceof Error){
        this.modalText = e.message;
      }
      else{
        this.modalText = '';
        e.error.forEach((element: any) => {
          element.forEach((error_message: any) =>{
            this.modalText += error_message + '\n';
          });
        });
      }
      document.getElementById("openModal1")?.click();
    }
  }

  onFileSelected(event: any){
    this.selectedFile = event.target.files[0];
    console.log(this.selectedFile);
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

  goBackToEvent() {
    this.router.navigate(['/event'], {
      queryParams: { id: this.eventId }
    });
  }
}
