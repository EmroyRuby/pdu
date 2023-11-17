  export interface Category {
    name: string,
    id: number
  }

  export interface EventRegistration {
    id?: number;
    event: number;
    event_detail?: Event;
    is_registered: boolean;
  }
  
  export interface Event {
    id: number;
    title: string;
    description: string;
    location: string;
    is_public: boolean;
    price?: string;
    capacity?: number;
    remaining_slots?: number;
    registration_end_date: Date;
    start_date: Date;
    end_date: Date;
    created_at?: Date;
    updated_at?: Date;
    user?: number;
    user_email?: string;
    categories?: string[];
    photo?: string;
  }
  
  export interface User {
    id?: number,
    username?: string;
    email: string;
    password?: string;
  }

  export interface EventsFilter {
    title_pattern: string | null,
    categories: string[] | null,
    accessibility: string | null,
    start_date: Date | null,
    end_date: Date | null
  }