import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class EventService {

  private events: any[] = [
    {
      id: 1,
      title: 'Volleyball group',
      image: '/assets/volleyball.jpg',
      dateTime: '2023-11-15T15:00:00',
      location: "Wrocław",
      tags: ['Sport', 'Volleyball', 'Beginners'],
      isPublic: false
    },
    {
      id: 2,
      title: 'Ballet class',
      image: '/assets/ballet.jpg',
      dateTime: '2023-11-05T18:30:00',
      location: "Wrocław",
      tags: ['Dance', 'Ballet', 'Beginners'],
      isPublic: true
    }
  ];

  listEvents(): any[] {
    return this.events;
  }

  getEventById(eventId: number): any {
    return this.events.find(event => event.id === eventId);
  }

  addEvent(event: any): number {
    return 3;
  }

  editEvent(eventId: number, updatedEvent: any): void {

  }

  deleteEvent(eventId: number): void {
  
  }
}
