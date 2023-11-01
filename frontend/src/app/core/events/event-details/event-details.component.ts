import { Component } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Router } from '@angular/router';
import { EventService } from '../event.service';
import { AccountService } from '../../account/account.service';

@Component({
  selector: 'app-event-details',
  templateUrl: './event-details.component.html',
  styleUrls: ['./event-details.component.css']
})
export class EventDetailsComponent {
  eventId!: number;
  event: any;
  isSignUpDisabled = false;

  constructor(private route: ActivatedRoute, private router: Router, private eventService: EventService, private authService: AccountService) { }

  ngOnInit() {
    this.route.queryParamMap.subscribe(params => {
      const eventId = params.get('id');
      if (eventId) {
        this.eventId = parseInt(eventId, 10)
        this.event = this.eventService.getEventById(this.eventId);
      }
    });
    console.log(this.event.isPublic)
    console.log(this.authService.isLoggedIn())
    if (!this.event.isPublic && !this.authService.isLoggedIn()) {
      this.isSignUpDisabled = true;
    }
  }

  goBackToEvents() {
    this.router.navigate(['/events']);
  }

  signUp() {
    console.log('Sign up');
    this.router.navigate(['/events/event/sign-up'], {
      queryParams: { id: this.eventId },
      relativeTo: this.route,
    });
  }
}
