import { Component } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Router } from '@angular/router';

@Component({
  selector: 'app-event-details',
  templateUrl: './event-details.component.html',
  styleUrls: ['./event-details.component.css']
})
export class EventDetailsComponent {
  event: any = {
    id: 1,
      title: 'Volleyball group',
      image: '/assets/volleyball.jpg',
      dateTime: '2023-11-15T15:00:00',
      location: "Wrocław",
      tags: ['Sport', 'Volleyball', 'Beginners'],
      isPublic: false,
      description: 
      'We are a close-knit community of friends who share a passion for volleyball and are on the lookout for like-minded individuals to join us in some thrilling matches during our free time.\
      Our meetups are all about friendly competition, skill improvement, and, most importantly, having a blast on the court. \
      You can expect a supportive and encouraging atmosphere where we cheer each other on, offer tips, and celebrate every point, regardless of skill level.'
  };

  constructor(private route: ActivatedRoute, private router: Router) {
    const eventId = this.route.snapshot.paramMap.get('id');
  }

  goBackToEvents() {
    this.router.navigate(['/events']); // Assuming '/events' is the route for your events page
  }
}
