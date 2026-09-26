export interface ChatMessage {
  id: string;
  sender: "user" | "bot";
  text: string;
  timestamp: string;
  intent?: string;
  sources?: string[];
  error?: boolean;
}

export interface ChatResponse {
  answer: string;
  intent: string;
  sources: string[];
}

export interface TimetableSlot {
  id: number;
  day_order: string;
  start_time: string;
  end_time: string;
  subject: string;
  room?: string | null;
  faculty?: string | null;
  class_type: string;
  subject_id?: number | null;
}

export interface CalendarEvent {
  id: number;
  date: string;
  day: string;
  event: string;
  category: string;
  semester?: string | null;
  is_holiday: boolean;
  description?: string | null;
}

export interface SubjectScheduleSlot {
  day_order: string;
  start_time: string;
  end_time: string;
  room?: string | null;
  faculty?: string | null;
  class_type: string;
}

export interface SubjectDetail {
  id: number;
  code: string;
  name: string;
  description?: string | null;
  class_type: string;
  faculty?: string | null;
  schedules: SubjectScheduleSlot[];
}

export interface HealthResponse {
  status: string;
  message: string;
  version: string;
}
