export interface Event {
    title: string;
    description: string;
    location: string;
    isPublic: boolean;
    price?: number | null;
    capacity?: number | null;
    registrationEndDate?: Date | null;
    startDate?: Date | null;
    endDate?: Date | null;
    image?: string | null;
  }