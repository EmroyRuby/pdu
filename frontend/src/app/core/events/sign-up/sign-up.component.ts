import { Component } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Router } from '@angular/router';
import { EventService } from '../event.service';
import { AccountService } from '../../account/account.service';
import { Event } from '../../models';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';

@Component({
  selector: 'app-sign-up',
  templateUrl: './sign-up.component.html',
  styleUrls: ['./sign-up.component.css']
})
export class SignUpComponent {
  eventId!: number;
  event!: Event;
  signUpForm: FormGroup;
  isLoggedIn: boolean = false;

  constructor(private fb: FormBuilder, private route: ActivatedRoute, private router: Router, private eventService: EventService, private authService: AccountService) {
    this.signUpForm = this.fb.group({
      email: ['', Validators.required]
    });
   }

  async ngOnInit() {
    this.route.queryParamMap.subscribe(params => {
      const eventId = params.get('id');
      if (eventId) {
        this.eventId = parseInt(eventId, 10)
      }
    });
    this.event = await this.eventService.getEventById(this.eventId);
    this.isLoggedIn = this.authService.isLoggedIn();

    if (!this.event || (!this.event.is_public && !this.isLoggedIn)) {
      this.router.navigate(['/login']);
    }
  }

  goBackToEvent() {
    this.router.navigate(['/event'], {
      queryParams: { id: this.eventId }
    });
  }

  signUp() {
    this.eventService.signUp(this.eventId);
    this.goBackToEvent();
  }
}
