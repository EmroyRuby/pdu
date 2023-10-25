import { Component } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Router } from '@angular/router';

@Component({
  selector: 'app-event-details',
  templateUrl: './event-details.component.html',
  styleUrls: ['./event-details.component.css']
})
export class EventDetailsComponent {
  eventId!: number;

  event: any = {
    id: 1,
      title: 'Volleyball group',
      image: '/assets/volleyball.jpg',
      startDate: '2023-11-15T15:00:00',
      endDate: '2023-11-15T17:00:00',
      location: "Wrocław",
      price: '10.00',
      capacity: 10,
      tags: ['Sport', 'Volleyball', 'Beginners'],
      isPublic: false,
      registrationEndDate: '2023-11-14T17:00:00',
      description: 
      'We are a close-knit community of friends who share a passion for volleyball and are on the lookout for like-minded individuals to join us in some thrilling matches during our free time.\
      Our meetups are all about friendly competition, skill improvement, and, most importantly, having a blast on the court. \
      You can expect a supportive and encouraging atmosphere where we cheer each other on, offer tips, and celebrate every point, regardless of skill level.'
  };

  constructor(private route: ActivatedRoute, private router: Router) {
    this.route.params.subscribe((params) => {
      this.eventId = +params['id']; // Access the 'id' route parameter
    });
  }

  goBackToEvents() {
    this.router.navigate(['/events']); // Assuming '/events' is the route for your events page
  }
}
