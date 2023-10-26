import { Component } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Router } from '@angular/router';
import { EventService } from '../event.service';

@Component({
  selector: 'app-event-details',
  templateUrl: './event-details.component.html',
  styleUrls: ['./event-details.component.css']
})
export class EventDetailsComponent {
  eventId!: number;
  event: any;

  constructor(private route: ActivatedRoute, private router: Router, private eventService: EventService) { }

  ngOnInit() {
    this.route.queryParamMap.subscribe(params => {
      const eventId = params.get('id');
      if (eventId) {
        this.eventId = parseInt(eventId, 10)
        this.event = this.eventService.getEventById(this.eventId);
      }
    });
  }

  goBackToEvents() {
    this.router.navigate(['/events']);
  }
}
