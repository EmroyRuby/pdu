import { Component, OnInit, ViewChild } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-events-catalog',
  templateUrl: './events-catalog.component.html',
  styleUrls: ['./events-catalog.component.css']
})
export class EventsCatalogComponent implements OnInit {
  events: any[] = [
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
  tags: any[] = ['Sport', 'Volleyball', 'Beginners', 'Dance', 'Ballet']
  visibility: any[] = ['Public', 'Private']
  filters = {
    searchTitle: '',
    selectedTags: [] as string[],
    selectedVisibility: [] as string[],
    startDate: '',
    endDate: ''
  }
  isDropdownOpen = false;

  constructor(private router: Router, private route: ActivatedRoute) { }

  ngOnInit() {
  }  

  onCardClick(event: any) {
    console.log('Card clicked', event);
    const eventId = event.id;
    this.router.navigate(['/events/event'], {
      queryParams: { id: eventId },
      relativeTo: this.route,
    });
  }

  filterbyTitle(searchTitle: string) {
    if (searchTitle) {
      this.filters.searchTitle = searchTitle;
    }
    this.applyFilter();
  }

  filterByTag(tag: string) {
    if (this.isTagSelected(tag)) {
      this.filters.selectedTags = this.filters.selectedTags.filter(selectedTag => selectedTag !== tag);
    } else {
      this.filters.selectedTags.push(tag);
    }
    this.applyFilter();
  }

  filterByDates(startDate: string, endDate: string) {
    if (startDate) {
      this.filters.startDate = startDate;
    }
    if (endDate) {
      this.filters.startDate = endDate;
    }
    this.applyFilter();
  }

  filterByVisibility(vis: string) {
    if (this.isVisSelected(vis)) {
      this.filters.selectedVisibility = this.filters.selectedVisibility.filter(selectedVis => selectedVis !== vis);
    } else {
      this.filters.selectedVisibility.push(vis);
    }
    this.applyFilter();
  }


  applyFilter() {
    // if (this.filters.selectedTags.length === 0) {
    //   this.events = this.events;
    // } else {
    //   this.events = this.events.filter(event =>
    //     this.filters.selectedTags.every(tag => event.tags.includes(tag))
    //   );
    // }
  }

  removeSelectedTag(tagToRemove: string) {
    const index = this.filters.selectedTags.indexOf(tagToRemove);
    if (index !== -1) {
      this.filters.selectedTags.splice(index, 1);
    }
  }

  removeSelectedVis(visToRemove: string) {
    const index = this.filters.selectedVisibility.indexOf(visToRemove);
    if (index !== -1) {
      this.filters.selectedVisibility.splice(index, 1);
    }
  }

  isTagSelected(tag: string): boolean {
    return this.filters.selectedTags.includes(tag);
  }

  isVisSelected(vis: string): boolean {
    return this.filters.selectedVisibility.includes(vis);
  }

  toggleDropdown() {
    this.isDropdownOpen = !this.isDropdownOpen;
  }
}
