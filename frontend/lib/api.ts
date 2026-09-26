import {
  ChatResponse,
  TimetableSlot,
  CalendarEvent,
  SubjectDetail,
  HealthResponse,
} from "@/types";

const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export async function checkBackendHealth(): Promise<HealthResponse> {
  const res = await fetch(`${API_BASE_URL}/api/health`, {
    cache: "no-store",
  });
  if (!res.ok) {
    throw new Error(`Failed to check health: ${res.statusText}`);
  }
  return res.json();
}

export async function sendChatMessage(message: string): Promise<ChatResponse> {
  const res = await fetch(`${API_BASE_URL}/api/chat`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ message }),
  });
  if (!res.ok) {
    const errorData = await res.json().catch(() => ({}));
    throw new Error(errorData.detail || `Server responded with ${res.status}`);
  }
  return res.json();
}

export async function fetchTimetable(): Promise<TimetableSlot[]> {
  const res = await fetch(`${API_BASE_URL}/api/timetable`, {
    cache: "no-store",
  });
  if (!res.ok) {
    throw new Error(`Failed to fetch timetable: ${res.statusText}`);
  }
  return res.json();
}

export async function fetchDayTimetable(dayOrder: string): Promise<TimetableSlot[]> {
  const res = await fetch(`${API_BASE_URL}/api/timetable/day/${encodeURIComponent(dayOrder)}`, {
    cache: "no-store",
  });
  if (!res.ok) {
    throw new Error(`Failed to fetch schedule for ${dayOrder}: ${res.statusText}`);
  }
  return res.json();
}

export async function fetchCalendarEvents(category?: string, semester?: string): Promise<CalendarEvent[]> {
  const params = new URLSearchParams();
  if (category && category !== "All") params.append("category", category);
  if (semester && semester !== "All") params.append("semester", semester);

  const url = `${API_BASE_URL}/api/calendar${params.toString() ? `?${params.toString()}` : ""}`;
  const res = await fetch(url, {
    cache: "no-store",
  });
  if (!res.ok) {
    throw new Error(`Failed to fetch calendar events: ${res.statusText}`);
  }
  return res.json();
}

export async function fetchHolidays(month?: string): Promise<CalendarEvent[]> {
  const url = month && month !== "All"
    ? `${API_BASE_URL}/api/calendar/holidays?month=${encodeURIComponent(month)}`
    : `${API_BASE_URL}/api/calendar/holidays`;
  const res = await fetch(url, {
    cache: "no-store",
  });
  if (!res.ok) {
    throw new Error(`Failed to fetch holidays: ${res.statusText}`);
  }
  return res.json();
}

export async function fetchSubjects(): Promise<SubjectDetail[]> {
  const res = await fetch(`${API_BASE_URL}/api/subjects`, {
    cache: "no-store",
  });
  if (!res.ok) {
    throw new Error(`Failed to fetch subjects: ${res.statusText}`);
  }
  return res.json();
}
