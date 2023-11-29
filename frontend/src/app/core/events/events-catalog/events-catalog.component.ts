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
  recommended: Event[] = [];
  categories: string[] = [];
  accessibility: any[] = ['All', 'Public', 'Private'];
  filters: EventsFilter = {
    title_pattern: null,
    categories: null,
    accessibility: null,
    start_date: null,
    end_date: null,
    only_available: null,
    price_less_than: null,
    price_greater_than: null

  };
  isDropdownOpen = false;
  availabilityFilter: string = 'All';

  constructor(private router: Router, private route: ActivatedRoute, private eventService: EventService) { 
  }

  async ngOnInit() {
    this.categories = await this.eventService.getCategories();
    this.filters = this.eventService.filters;
    this.events = await this.eventService.listEvents();
    this.recommended = await this.eventService.listRecommended();
  }  

  onCardClick(event: any) {
    const eventId = event.id;
    this.router.navigate(['/event'], {
      queryParams: { id: eventId },
      relativeTo: this.route,
    });
  }

  async applyFilter() {
    this.eventService.filters = this.filters;
    this.events = await this.eventService.listEvents();
    this.recommended = await this.eventService.listRecommended();
    console.log(this.events);
  }

  filterbyTitle(searchTitle: string) {
    this.filters.title_pattern = searchTitle;
    this.applyFilter();
  }

  filterByCategory(category: string) {
    if (this.filters) {
      if (this.isCategorySelected(category)) {
        this.filters.categories = this.filters.categories?.filter(selectedCategory => selectedCategory !== category) ?? [];
      } else {
        this.filters.categories = this.filters.categories ?? [];
        this.filters.categories.push(category);
      }
      this.applyFilter();
    }
  }

  filterByDates(start_date: string, end_date: string) {
    if (start_date) {
      if (new Date(start_date) < new Date()) {
        start_date = new Date().toISOString();
      }
      this.filters.start_date = new Date(start_date);
    }
    if (end_date) {
      this.filters.end_date = new Date(end_date);
    }
    this.applyFilter();
  }

  filterByAccessibility(acc: string) {
    if (this.filters) {
        this.filters.accessibility = acc;
      this.applyFilter();
    }
  }

  filterByAvailability(only_available: boolean) {
    if (this.filters) {
        this.filters.only_available = only_available;
      this.applyFilter();
    }
  }

  filterByPrice(price_greater_than: string, price_less_than: string) {
    if (this.filters) {
      if (price_greater_than) {
        this.filters.price_greater_than = price_greater_than;
      }
      if (price_less_than) {
        this.filters.price_less_than = price_less_than;
      }
      this.applyFilter();
    }
  }

  removeSelectedCategory(categoryToRemove: string) {
    if (this.filters.categories !== null) {
      const index = this.filters.categories.indexOf(categoryToRemove);
      if (index !== -1) {
        this.filters.categories.splice(index, 1);
      }
      this.applyFilter();
    }
  }

  removeSelectedAcc() {
    if (this.filters.accessibility !== null) {
        this.filters.accessibility = "All";
      }
      this.applyFilter();
  }

  clearStartDateFilter() {
    this.filters.start_date = new Date();
    this.applyFilter();
  }

  clearEndDateFilter() {
    this.filters.end_date = null;
    this.applyFilter();
  }

  clearAvailabilityFilter() {
    this.filters.only_available = false;
    this.availabilityFilter = "All"
    this.applyFilter();
  }

  clearPriceGreaterThanFilter() {
    this.filters.price_greater_than = null;
    this.applyFilter();
  }

  clearPriceLessThanFilter() {
    this.filters.price_less_than = null;
    this.applyFilter();
  }

  clearAll() {
    this.filters.categories = null;
    this.filters.accessibility = "All";
    this.filters.start_date = new Date();
    this.filters.end_date = null;
    this.filters.only_available = false;
    this.availabilityFilter = "All"
    this.filters.price_greater_than = null;
    this.filters.price_less_than = null;
    this.applyFilter();
  } 

  isCategorySelected(category: string): boolean {
    return this.filters.categories !== null && this.filters.categories.includes(category);
  }

  toggleDropdown() {
    this.isDropdownOpen = !this.isDropdownOpen;
  }
}
