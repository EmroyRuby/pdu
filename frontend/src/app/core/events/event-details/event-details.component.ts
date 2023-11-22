import { Component } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Router } from '@angular/router';
import { EventService } from '../event.service';
import { AccountService } from '../../account/account.service';
import { Event, Comment } from '../../models';

@Component({
  selector: 'app-event-details',
  templateUrl: './event-details.component.html',
  styleUrls: ['./event-details.component.css']
})
export class EventDetailsComponent {
  eventId!: number;
  event!: Event;
  comments!: Comment[];
  isSignUpDisabled = false;
  isOrganiser = false;
  isSignedUp = false;
  isOver = false;
  newComment: string = '';

  constructor(private route: ActivatedRoute, private router: Router, private eventService: EventService, private authService: AccountService) { }

  async ngOnInit() {
    this.route.queryParamMap.subscribe(async params => {
      const eventId = params.get('id');
      if (eventId) {
        this.eventId = parseInt(eventId, 10)
        this.event = await this.eventService.getEventById(this.eventId);
        console.log(this.event);
        this.comments = await this.eventService.listComments(this.eventId);
      }
      if (!this.event.is_public && !this.authService.isLoggedIn()) {
        this.isSignUpDisabled = true;
      }
      this.isOrganiser = await this.eventService.isOrganiser(this.eventId);
      console.log(this.isOrganiser);
      this.isSignedUp = await this.eventService.isSignedUp(this.eventId);
      console.log(this.isSignedUp);
      this.isOver = this.event.end_date < new Date();
      console.log(this.isOver);
    });
  }

  goBack() {
    window.history.back();
  }

  signUp() {
    this.router.navigate(['/event/sign-up'], {
      queryParams: { id: this.eventId },
      relativeTo: this.route,
    });
  }

  async signOut() {
    await this.eventService.signOut(this.eventId);
    window.location.reload();
  }

  edit() {
    this.router.navigate(['/event/edit'], {
      queryParams: { id: this.eventId },
      relativeTo: this.route,
    });
  }

  async delete() {
    await this.eventService.deleteEvent(this.eventId);
    this.goBack();
  }

  async addComment() {
    if (this.newComment.trim() !== '' && this.isSignedUp) {
      const userId = (await this.authService.getUserData()).id;
      if(userId){
        const eventComment: Comment = {
          content: this.newComment,
          user: userId,
          event: this.eventId
        }
        await this.eventService.addComment(eventComment);
        this.newComment = '';
      }
    }
  }
}
