import { Injectable } from '@angular/core';
import { EventsFilter } from '../models';
import { Event} from '../models';

@Injectable({
  providedIn: 'root'
})
export class EventService {
  private tags: string[] = ['Sports', 'Competition', 'Volleyball', 'Dance', 'Performance', 'Education', 'Tutoring', 'Art', 'Crafts'];
  private events: Event[] = [
    {
      id: 1,
      title: 'Volleyball group',
      organiser: 'Volleyball Club A',
      description: 'Join our exciting volleyball group.',
      location: 'Sports Arena 1',
      isPublic: true,
      price: 10,
      capacity: 100,
      registrationEndDate: new Date('2023-12-15T12:00:00'),
      startDate: new Date('2024-01-20T09:00:00'),
      endDate: new Date('2024-01-22T18:00:00'),
      image: '/assets/volleyball.jpg',
      tags: ['Sports', 'Competition', 'Volleyball'],
    },
    {
      id: 2,
      title: 'Ballet class',
      organiser: 'Ballet School B',
      description: 'Learn the art of ballet and prepare for an enchanting ballet performance.',
      location: 'Dance Studio 2',
      isPublic: true,
      price: 20,
      capacity: 50,
      registrationEndDate: new Date('2023-11-30T12:00:00'),
      startDate: new Date('2024-02-15T10:30:00'),
      endDate: new Date('2024-02-17T16:00:00'),
      image: '/assets/ballet.jpg',
      tags: ['Dance', 'Performance'],
    },
    {
      id: 3,
      title: 'Math Tutoring Session',
      organiser: 'Math Tutors C',
      description: 'Improve your math skills with our expert math tutoring sessions. All levels welcome!',
      location: 'Library 3',
      isPublic: false,
      capacity: 20,
      registrationEndDate: new Date('2024-01-25T14:00:00'),
      startDate: new Date('2024-03-10T17:30:00'),
      endDate: new Date('2024-03-12T19:30:00'),
      image: 'math.jpg',
      tags: ['Education', 'Tutoring'],
    },
    {
      id: 4,
      title: 'Pottery Workshop',
      organiser: 'Pottery Studio D',
      description: 'Unleash your creativity with our hands-on pottery workshop. Create unique clay art!',
      location: 'Art Studio 4',
      isPublic: true,
      price: 15,
      capacity: 40,
      registrationEndDate: new Date('2024-02-28T12:00:00'),
      startDate: new Date('2024-04-15T10:00:00'),
      endDate: new Date('2024-04-17T16:30:00'),
      image: 'pottery.jpg',
      tags: ['Art', 'Crafts'],
    },
  ];

  listEvents(filters: EventsFilter): Event[] {
    return this.events;
  }

  getTags(): string[] {
    return this.tags;
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
