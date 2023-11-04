import { Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
import { EventService } from '../event.service';
import { Event, EventsFilter } from '../../models';

@Component({
  selector: 'app-my-events',
  templateUrl: './my-events.component.html',
  styleUrls: ['./my-events.component.css']
})
export class MyEventsComponent implements OnInit {
  events: Event[] = [];
  isDropdownOpen = false;

  constructor(private router: Router, private route: ActivatedRoute, private eventService: EventService) { 
  }

  ngOnInit() {
    this.events = this.eventService.listMyEvents(1);
  }  

  onCardClick(event: any) {
    const eventId = event.id;
    this.router.navigate(['/event'], {
      queryParams: { id: eventId },
      relativeTo: this.route,
    });
  }

  filterbyRole(role: number) {
    if (role === 1) {
      this.events = this.eventService.listMyEvents(1);
    } else if (role === 2) {
      this.events = this.eventService.listMyEvents(2);
    }
  }
  

}
