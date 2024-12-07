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
  upcomingEvents: Event[] = [];
  pastEvents: Event[] = [];
  isDropdownOpen = false;
  role = 1;

  constructor(private router: Router, private route: ActivatedRoute, private eventService: EventService) { 
  }

  async ngOnInit() {
    this.filterbyRole(1);

  }  

  onCardClick(event: any) {
    const eventId = event.id;
    this.router.navigate(['/event'], {
      queryParams: { id: eventId },
      relativeTo: this.route,
    });
  }

  async filterbyRole(role: number) {
      this.role = role;
      const events = await this.eventService.listMyEvents(role);
      this.upcomingEvents = events.filter(event => new Date(event.start_date) > new Date());
      this.upcomingEvents.sort((a, b) => new Date(a.start_date).getTime() - new Date(b.start_date).getTime());
      this.pastEvents = events.filter(event => new Date(event.start_date) <= new Date());
      this.pastEvents.sort((a, b) => new Date(b.start_date).getTime() - new Date(a.start_date).getTime());

  }
  

}
