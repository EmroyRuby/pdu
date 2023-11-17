import { Injectable } from '@angular/core';
import { Event, Category, EventRegistration, EventsFilter } from '../models';
import { HttpClient, HttpParams } from '@angular/common/http';
import { BehaviorSubject, Observable, firstValueFrom, map } from 'rxjs';
import { AccountService } from '../account/account.service';

@Injectable({
  providedIn: 'root'
})
export class EventService {
  // Array to store categories
  private categories: string[] = [];
  // Array to store events
  private events: Event[] = [];
  // Filters for events
  filters: EventsFilter = {
    title_pattern: null,
    categories: null,
    accessibility: "All",
    start_date: new Date,
    end_date: null
  };

  constructor(private http: HttpClient, private accountService: AccountService) {
  }

  // Retrieve a list of events based on applied filters
  async listEvents(): Promise<Event[]> {
    try {
      console.log(this.filters);
      // Build HTTP params based on applied filters
      let params = new HttpParams();
      if (this.filters.title_pattern) {
        params = params.set('title', this.filters.title_pattern);
      }
      if (this.filters.categories) {
        const categoriesString = this.filters.categories.join(',');
        params = params.set('category', categoriesString);
      }
      if (this.filters.accessibility) {
        if(this.filters.accessibility === 'Public') {
          params = params.set('is_public', "True");
        }
        else if(this.filters.accessibility === 'Private') {
          params = params.set('is_public', "False");
        }
      }
      if (this.filters.start_date) {
        params = params.set('start_date', (this.filters.start_date).toISOString().slice(0,10));
      }
      if (this.filters.end_date) {
        params = params.set('end_date', (this.filters.end_date).toISOString().slice(0,10));
      }
      // Make a GET request to retrieve events
      const events = await firstValueFrom(
        this.http.get<Event[]>(`http://127.0.0.1:8000/api/events/`, { params }).pipe()
      );
      this.events = events;
      console.log('Events retrived successfully');
      return this.events;
    } catch (error) {
      console.error('Error during GET events HTTP request:', error);
      throw error;
    }
  }

  // List events for the authenticated user based on their role
  async listMyEvents(role: number): Promise<Event[]> {
    if (role === 1) {
      // as participant
      try {
        const options = {
          withCredentials: true,
        };
        const events = await firstValueFrom(
          this.http.get<EventRegistration[]>(`http://127.0.0.1:8000/api/event-registrations/`, options).pipe(
            map((data) => data.filter((item) => item.is_registered)),
            map((registrations) => registrations.map((registration) => registration.event_detail)),
            map((events) => events.filter((event) => event !== undefined) as Event[])
          )
        );
        console.log("Participant's events retrived successfully");
        return events;
      } catch (error) {
        console.error('Error during GET participant events HTTP request:', error);
        throw error;
      }
    } else if (role === 2) {
      // as organiser
      try {
        const userId = (await this.accountService.getUserData()).id;
        let params = new HttpParams();
        if (userId) {
          params = params.set('user', userId);
        }
        const events = await firstValueFrom(
          this.http.get<Event[]>(`http://127.0.0.1:8000/api/events/`, { params }).pipe()
        );
        console.log("Organiser's events retrived successfully");
        return events;
      } catch (error) {
        console.error('Error during GET organizer events HTTP request:', error);
        throw error;
      }
    }
    return this.events;
  }
  

  // Retrieve a list of categories
  async getCategories(): Promise<string[]> {
    try {
      const categories = await firstValueFrom(
        this.http.get<Category[]>(`http://127.0.0.1:8000/api/categories/`).pipe(
          map(data => data.map(item => item.name))
        )
      );
      this.categories = categories;
      console.log("Categories retrived successfully");
      return this.categories;
    }catch (error) {
      console.error('Error during GET categories HTTP request:', error);
      throw error;
    }
  }

  // Retrieve event details by ID
  async getEventById(eventId: number): Promise<Event> {
    try {
      console.log("Getting event of id=" + eventId);
      let params = new HttpParams();
      params = params.set('id', eventId);
      const event = await firstValueFrom(
        this.http.get<Event[]>(`http://127.0.0.1:8000/api/events/`, { params }).pipe()
      );
      console.log("Event ", eventId, " data: ", event);
      return event[0];
    } catch (error) {
      console.error('Error during GET event by ID HTTP request:', error);
      throw error;
    }
  }

  // Add a new event
  async addEvent(event: Event): Promise<number> {
    try {
      const newCategories = event.categories?.filter(category => !this.categories.includes(category));
      if (newCategories) {
        for (const category of newCategories) {
          await this.addCategory(category);
        }
      }
      const options = {
        withCredentials: true,
        headers: {
          'X-CSRFToken': this.accountService.getCsrfToken(),
        },
      };
      const eventResp = await firstValueFrom(
        this.http.post<Event>(`http://127.0.0.1:8000/api/events/`, event, options).pipe()
      );
      console.log("Added event: " + eventResp);
      const eventId = eventResp.id;
      return eventId;
    } catch (error) {
      console.error('Error during POST addEvent HTTP request:', error);
      throw error;
    }
  }

  async addCategory(category: string) {
    try {
      const options = {
        withCredentials: true,
        headers: {
          'X-CSRFToken': this.accountService.getCsrfToken(),
        },
      };
      const eventResp = await firstValueFrom(
        this.http.post(`http://127.0.0.1:8000/api/categories/`, { name: category }, options).pipe()
      );
      console.log("Added category: " + eventResp);
    } catch (error) {
      console.error('Error during POST addCategory HTTP request:', error);
      throw error;
    }
  }

  // Edit an existing event
  async editEvent(eventId: number, updatedEvent: Event) {
    try {
      const newCategories = updatedEvent.categories?.filter(category => !this.categories.includes(category));
      if (newCategories) {
        for (const category of newCategories) {
          await this.addCategory(category);
        }
      }
      const options = {
        withCredentials: true,
        headers: {
          'X-CSRFToken': this.accountService.getCsrfToken(),
        },
      };
      const eventResp = await firstValueFrom(
        this.http.put<Event>(`http://127.0.0.1:8000/api/events/${eventId}/`, updatedEvent, options).pipe()
      );
      console.log("Updated event " + eventId + ". New value: ", eventResp);
    } catch (error) {
      console.error('Error during PUT editEvent HTTP request:', error);
      throw error;
    }
  }

  // Delete an existing event
  async deleteEvent(eventId: number) {
    try {
      const options = {
        withCredentials: true,
        headers: {
          'X-CSRFToken': this.accountService.getCsrfToken(),
        },
      };
      await firstValueFrom(
        this.http.delete(`http://127.0.0.1:8000/api/events/${eventId}/`, options).pipe()
      );
      console.log("Deleted event " + eventId);
    } catch (error) {
      console.error('Error during DELETE deleteEvent HTTP request:', error);
      throw error;
    }
  }

  // Check if the user is signed up for an event
  async isSignedUp(eventId: number): Promise<boolean> {
    const events = await this.listMyEvents(1);
    const isSignedUp = events.some(event => event.id === eventId);
    console.log("isSignedUp: ", isSignedUp);
    return isSignedUp;
  }

  // Check if the user is the organiser of an event
  async isOrganiser(eventId: number): Promise<boolean> {
    const event = await this.getEventById(eventId);
    const userId = (await this.accountService.getUserData()).id;
    const isOrganiser = event.user === userId;
    console.log("isOrganiser: ", isOrganiser);
    return isOrganiser;
  }

  // Sign up for an event
  async signUp(eventId: number): Promise<boolean> {
    try {
      const options = {
        withCredentials: true,
        headers: {
          'X-CSRFToken': this.accountService.getCsrfToken(),
        },
      };
      const eventReg: EventRegistration = {
        event: eventId,
        is_registered: true
      };
      const resp = await firstValueFrom(
        this.http.post<EventRegistration>(`http://127.0.0.1:8000/api/event-registrations/`, eventReg, options).pipe()
      );
      return resp.is_registered === true;
    } catch (error) {
      console.error('Error during POST signUp HTTP request:', error);
      throw error;
    }
  }
  
  // Sign out from an event
  async signOut(eventId: number) {
    try {
      const options = {
        withCredentials: true,
        headers: {
          'X-CSRFToken': this.accountService.getCsrfToken(),
        },
      };
      const eventReg = await firstValueFrom(
        this.http.get<EventRegistration[]>(`http://127.0.0.1:8000/api/event-registrations/`, options).pipe(
          map((data) => data.filter((registration) => registration.event === eventId))
        )
      );
      const regId = eventReg[0].id;
      console.log(regId);
      await firstValueFrom(
        this.http.delete(`http://127.0.0.1:8000/api/event-registrations/${regId}`, options).pipe()
      );
    } catch (error) {
      console.error('Error during signOut method:', error);
      throw error;
    }
  }
}