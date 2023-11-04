import { Component, OnInit, ViewChild } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
import { EventService } from '../event.service';
import { Event, EventsFilter } from '../../models';

@Component({
  selector: 'app-events-catalog',
  templateUrl: './events-catalog.component.html',
  styleUrls: ['./events-catalog.component.css']
})
export class EventsCatalogComponent implements OnInit {
  events: Event[] = [];
  filteredEvents: Event[] = [];
  tags: string[] = [];
  accessibility: any[] = ['Public', 'Private']
  filters: EventsFilter = {
    titlePattern: null,
    tags: null,
    accessibility: null,
    startDate: null,
    endDate: null
  };
  isDropdownOpen = false;

  constructor(private router: Router, private route: ActivatedRoute, private eventService: EventService) { 
  }

  ngOnInit() {
    this.filters = this.eventService.filters;
    this.events = this.eventService.listEvents();
    this.filteredEvents = this.events;
    this.tags = this.eventService.getTags();
  }  

  onCardClick(event: any) {
    const eventId = event.id;
    this.router.navigate(['/event'], {
      queryParams: { id: eventId },
      relativeTo: this.route,
    });
  }

  filterbyTitle(searchTitle: string) {
    this.filters.titlePattern = searchTitle;
    this.applyFilter();
  }

  filterByTag(tag: string) {
    if (this.filters) {
      if (this.isTagSelected(tag)) {
        this.filters.tags = this.filters.tags?.filter(selectedTag => selectedTag !== tag) ?? [];
      } else {
        this.filters.tags = this.filters.tags ?? [];
        this.filters.tags.push(tag);
      }
      this.applyFilter();
    }
  }

  filterByDates(startDate: string, endDate: string) {
      if (startDate) {
        this.filters.startDate = new Date(startDate);
      }
      if (endDate) {
        this.filters.endDate = new Date(endDate);
    }
    this.applyFilter();
  }

  filterByAccessibility(acc: string) {
    if (this.filters) {
      if (this.isAccSelected(acc)) {
        this.filters.accessibility = this.filters.accessibility?.filter(selectedAcc => selectedAcc !== acc) ?? [];
      } else {
        this.filters.accessibility = this.filters.accessibility ?? [];
        this.filters.accessibility.push(acc);
      }
      this.applyFilter();
    }
  }


  applyFilter() {
    this.eventService.filters = this.filters;
    this.events = this.eventService.listEvents();
  }

  removeSelectedTag(tagToRemove: string) {
    if (this.filters.tags !== null) {
      const index = this.filters.tags.indexOf(tagToRemove);
      if (index !== -1) {
        this.filters.tags.splice(index, 1);
      }
      this.applyFilter();
    }
  }

  removeSelectedAcc(accToRemove: string) {
    if (this.filters.accessibility !== null) {
      const index = this.filters.accessibility.indexOf(accToRemove);
      if (index !== -1) {
        this.filters.accessibility.splice(index, 1);
      }
      this.applyFilter();
    }
  }

  clearStartDateFilter() {
    this.filters.startDate = null;
    this.applyFilter();
  }

  clearEndDateFilter() {
    this.filters.endDate = null;
    this.applyFilter();
  }

  isTagSelected(tag: string): boolean {
    return this.filters.tags !== null && this.filters.tags.includes(tag);
  }

  isAccSelected(acc: string): boolean {
    return this.filters.accessibility !== null && this.filters.accessibility.includes(acc);
  }  

  toggleDropdown() {
    this.isDropdownOpen = !this.isDropdownOpen;
  }
}
