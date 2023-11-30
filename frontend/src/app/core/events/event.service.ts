import { Injectable } from '@angular/core';
import { Event, Category, EventRegistration, EventsFilter, Comment } from '../models';
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
    end_date: null,
    only_available: false,
    price_less_than: null,
    price_greater_than: null
  };

  constructor(private http: HttpClient, private accountService: AccountService) {
  }
  async listEvents(): Promise<Event[]> {
    return await this.listEventsAndRecommended(`http://127.0.0.1:8000/api/events/`);
  }
  async listRecommended(): Promise<Event[]> {
    if(!this.accountService.isLoggedIn()){
      return [];
    }
    return await this.listEventsAndRecommended(`http://127.0.0.1:8000/api/user-recommendation/`);
  }
  // Retrieve a list of events based on applied filters
  async listEventsAndRecommended(url: string): Promise<Event[]> {
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
      if (this.filters.price_greater_than) {
        params = params.set('price_gte', this.filters.price_greater_than);
      }
      if (this.filters.price_less_than) {
        params = params.set('price_lte', this.filters.price_less_than);
      }
      // Make a GET request to retrieve events
      const options = {
        withCredentials: true,
        params: params
      };
      const events = await firstValueFrom(
        this.http.get<Event[]>(url, options).pipe(
          map((items) => {
            if (this.filters.only_available) {
              return items.filter((item) => item.remaining_slots && item.remaining_slots > 0);
            } else {
              return items;
            }
          })
        )
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
      // Create FormData object and append form data
      // const formData = new FormData();

      // formData.append('title', event.title);
      // formData.append('description', event.description);
      // formData.append('location', event.location);
      // formData.append('is_public', event.is_public.toString());
      // formData.append('price', event.price || '');
      // formData.append('capacity', event.capacity?.toString() || '');
      // formData.append('registration_end_date', new Date(event.registration_end_date).toISOString());
      // formData.append('start_date', new Date(event.start_date).toISOString());
      // formData.append('end_date', new Date(event.end_date).toISOString());
      // if(event.created_at && event.updated_at){
      //   formData.append('created_at', new Date(event.created_at).toISOString() || '');
      //   formData.append('updated_at', new Date(event.updated_at).toISOString() || '');
      // }
      // if (event.categories) {
      //   event.categories.forEach((category, index) => {
      //     formData.append(`categories[${index}]`, category);
      //   });
      // }
      // if (event.photo instanceof File) {
      //   formData.append('photo', event.photo);
      // }
      const options = {
        withCredentials: true,
        headers: {
          'X-CSRFToken': this.accountService.getCsrfToken(), 
          // 'Content-Type': 'multipart/form-data'
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
      // Create FormData object and append form data
      // const formData = new FormData();

      // formData.append('title', updatedEvent.title);
      // formData.append('description', updatedEvent.description);
      // formData.append('location', updatedEvent.location);
      // formData.append('is_public', updatedEvent.is_public.toString());
      // formData.append('price', updatedEvent.price || '');
      // formData.append('capacity', updatedEvent.capacity?.toString() || '');
      // formData.append('registration_end_date', new Date(updatedEvent.registration_end_date).toISOString());
      // formData.append('start_date', new Date(updatedEvent.start_date).toISOString());
      // formData.append('end_date', new Date(updatedEvent.end_date).toISOString());
      // if(updatedEvent.updated_at){
      //   formData.append('updated_at', new Date(updatedEvent.updated_at).toISOString() || '');
      // }
      // if (updatedEvent.categories) {
      //   updatedEvent.categories.forEach((category, index) => {
      //     formData.append(`categories[${index}]`, category);
      //   });
      // }
      // if (updatedEvent.photo instanceof File) {
      //   formData.append('photo', updatedEvent.photo);
      // }
      const options = {
        withCredentials: true,
        headers: {
          'X-CSRFToken': this.accountService.getCsrfToken(), 
          // 'Content-Type': 'multipart/form-data'
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
    let isSignedUp = false;
    if(this.accountService.isLoggedIn()){
      const events = await this.listMyEvents(1);
      isSignedUp = events.some(event => event.id === eventId);
    }
    console.log("isSignedUp: ", isSignedUp);
    return isSignedUp;
  }

  // Check if the user is the organiser of an event
  async isOrganiser(eventId: number): Promise<boolean> {
    let isOrganiser = false;
    if(this.accountService.isLoggedIn()){
      const event = await this.getEventById(eventId);
      const userId = (await this.accountService.getUserData()).id;
      isOrganiser = event.user === userId;
    }
    console.log("isOrganiser: ", isOrganiser);
    return isOrganiser;
  }

  // Sign up for an event
  async signUp(eventId: number, email: string = ''): Promise<boolean> {
    if(this.accountService.isLoggedIn()){
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
    else{
      try{
        const resp = await firstValueFrom(
          this.http.post(`http://127.0.0.1:8000/api/register-guest/`,{email: email, event: eventId}).pipe()
        );
        return true;
      } catch (error) {
        console.error('Error during POST signUp HTTP request:', error);
        throw error;
      }
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
        this.http.delete(`http://127.0.0.1:8000/api/event-registrations/${regId}/`, options).pipe()
      );
    } catch (error) {
      console.error('Error during signOut method:', error);
      throw error;
    }
  }

  async listComments(eventId: number): Promise<Comment[]> {
    try {
      let params = new HttpParams();
      params = params.set('event', eventId);
      // Make a GET request to retrieve comments
      const comments = await firstValueFrom(
        this.http.get<Comment[]>(`http://127.0.0.1:8000/api/comments/`, {params} ).pipe()
      );
      console.log('Comments retrived successfully');
      return comments;
    } catch (error) {
      console.error('Error during GET comments HTTP request:', error);
      throw error;
    }
  }

  async addComment(comment: Comment) {
    try {
      const options = {
        withCredentials: true,
        headers: {
          'X-CSRFToken': this.accountService.getCsrfToken(),
        },
      };
      const commentResp = await firstValueFrom(
        this.http.post(`http://127.0.0.1:8000/api/comments/`, comment, options).pipe()
      );
      console.log("Added comment: " + commentResp);
    } catch (error) {
      console.error('Error during POST addComment HTTP request:', error);
      throw error;
    }
  }
}
