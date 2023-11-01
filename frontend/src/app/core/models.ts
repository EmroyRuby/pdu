export interface Event {
    id: number;
    title: string;
    organiser: string;
    description: string;
    location: string;
    isPublic: boolean;
    price?: number;
    capacity?: number;
    registrationEndDate?: Date;
    startDate?: Date;
    endDate?: Date;
    image?: string;
    tags: string[]
  }
  
  export interface User {
    username: string;
    email: string;
    password: string;
  }

  export interface EventsFilter {
    titlePattern: string | null,
    tags: string[] | null,
    accessibility: string[] | null,
    startDate: Date | null,
    endDate: Date | null
  }