"use client";

import { useState, useEffect } from "react";
import {
  Calendar as CalendarIcon,
  Tag,
  Search,
  Sparkles,
  Flame,
  CheckCircle,
  Clock,
  CalendarDays,
  FileCheck,
  CreditCard,
} from "lucide-react";
import { CalendarEvent } from "@/types";
import { fetchCalendarEvents } from "@/lib/api";

const CATEGORIES = [
  "All",
  "Holiday",
  "CA Test",
  "Examination",
  "Fee Payment",
  "Semester Date",
  "Academic Event",
];

const MONTHS = [
  "All",
  "June 2026",
  "July 2026",
  "August 2026",
  "September 2026",
  "October 2026",
  "November 2026",
  "December 2026",
  "January 2026",
  "February 2026",
  "March 2026",
  "April 2026",
  "April 2027",
];

export default function CalendarPage() {
  const [events, setEvents] = useState<CalendarEvent[]>([]);
  const [selectedCategory, setSelectedCategory] = useState("All");
  const [selectedMonth, setSelectedMonth] = useState("All");
  const [searchQuery, setSearchQuery] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const loadEvents = async () => {
      try {
        setLoading(true);
        const data = await fetchCalendarEvents();
        setEvents(data);
      } catch (err: unknown) {
        setError(err instanceof Error ? err.message : "Failed to load calendar events.");
      } finally {
        setLoading(false);
      }
    };
    loadEvents();
  }, []);

  const filteredEvents = events.filter((ev) => {
    const matchesCategory =
      selectedCategory === "All" ||
      (selectedCategory === "Holiday" ? ev.is_holiday : ev.category === selectedCategory);

    let matchesMonth = true;
    if (selectedMonth !== "All") {
      const [mName, yNum] = selectedMonth.split(" ");
      const mCodes: Record<string, string> = {
        January: "01",
        February: "02",
        March: "03",
        April: "04",
        May: "05",
        June: "06",
        July: "07",
        August: "08",
        September: "09",
        October: "10",
        November: "11",
        December: "12",
      };
      const code = mCodes[mName];
      matchesMonth = ev.date.startsWith(yNum) && ev.date.includes(`-${code}-`);
    }

    const matchesSearch =
      searchQuery === "" ||
      ev.event.toLowerCase().includes(searchQuery.toLowerCase()) ||
      ev.date.includes(searchQuery) ||
      (ev.description && ev.description.toLowerCase().includes(searchQuery.toLowerCase()));

    return matchesCategory && matchesMonth && matchesSearch;
  });

  const formatDate = (dateStr: string, dayStr: string) => {
    try {
      const parts = dateStr.split("-");
      if (parts.length === 3) {
        const year = parts[0];
        const monthIndex = parseInt(parts[1], 10) - 1;
        const day = parseInt(parts[2], 10);
        const monthNames = [
          "January", "February", "March", "April", "May", "June",
          "July", "August", "September", "October", "November", "December"
        ];
        return `${dayStr}, ${day} ${monthNames[monthIndex]} ${year}`;
      }
    } catch {
      // fallback
    }
    return `${dayStr}, ${dateStr}`;
  };

  const holidaysCount = events.filter((e) => e.is_holiday).length;
  const caTestsCount = events.filter((e) => e.category === "CA Test").length;
  const examCount = events.filter((e) => e.category === "Examination").length;

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-white dark:bg-slate-900 p-6 rounded-2xl border border-slate-200 dark:border-slate-800 shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center space-x-2">
            <span className="p-2 rounded-lg bg-indigo-100 dark:bg-indigo-900/50 text-indigo-700 dark:text-indigo-300">
              <CalendarIcon className="w-5 h-5" />
            </span>
            <h1 className="text-xl sm:text-2xl font-bold text-slate-900 dark:text-white">
              Academic Calendar 2026–2027
            </h1>
          </div>
          <p className="text-sm text-slate-500 dark:text-slate-400 mt-1">
            Authoritative Calendar • PSG College of Arts & Science
          </p>
        </div>

        {/* Search */}
        <div className="relative w-full md:w-72">
          <Search className="w-4 h-4 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search events, holidays, dates..."
            className="w-full pl-9 pr-4 py-2 text-sm rounded-xl bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-slate-900 dark:text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-indigo-500"
          />
        </div>
      </div>

      {/* Metrics Row */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
        <div className="p-4 rounded-xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-xs">
          <span className="text-xs font-semibold text-slate-500 dark:text-slate-400">Total Calendar Events</span>
          <p className="text-2xl font-bold text-slate-900 dark:text-white mt-1">{events.length}</p>
        </div>
        <div className="p-4 rounded-xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-xs">
          <span className="text-xs font-semibold text-rose-600 dark:text-rose-400">Declared Holidays</span>
          <p className="text-2xl font-bold text-rose-600 dark:text-rose-400 mt-1">{holidaysCount}</p>
        </div>
        <div className="p-4 rounded-xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-xs">
          <span className="text-xs font-semibold text-blue-600 dark:text-blue-400">CA Test Schedules</span>
          <p className="text-2xl font-bold text-blue-600 dark:text-blue-400 mt-1">{caTestsCount}</p>
        </div>
        <div className="p-4 rounded-xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-xs">
          <span className="text-xs font-semibold text-indigo-600 dark:text-indigo-400">Comprehensive Exams</span>
          <p className="text-2xl font-bold text-indigo-600 dark:text-indigo-400 mt-1">{examCount}</p>
        </div>
      </div>

      {/* Key Milestones Quick Banner */}
      <div className="p-5 rounded-2xl bg-gradient-to-r from-blue-900 via-indigo-900 to-slate-900 text-white shadow-md">
        <h2 className="text-sm font-bold uppercase tracking-wider text-blue-200 mb-3 flex items-center space-x-2">
          <Sparkles className="w-4 h-4 text-amber-400" />
          <span>Core Semester Milestones</span>
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
          <div className="p-3 rounded-xl bg-white/10 backdrop-blur-xs space-y-1">
            <span className="font-bold text-blue-300">Odd Semester 2026:</span>
            <p>• Commencement: <strong className="text-white">15 June 2026</strong></p>
            <p>• Last Working Day: <strong className="text-white">23 October 2026</strong></p>
            <p>• Comprehensive Exams: <strong className="text-white">30 October 2026</strong></p>
          </div>
          <div className="p-3 rounded-xl bg-white/10 backdrop-blur-xs space-y-1">
            <span className="font-bold text-indigo-300">Even Semester 2026–2027:</span>
            <p>• Commencement: <strong className="text-white">2 December 2026</strong></p>
            <p>• Last Working Day: <strong className="text-white">16 April 2026 / 16 April 2027</strong></p>
            <p>• Comprehensive Exams: <strong className="text-white">20 April 2026 / 23 April 2027</strong></p>
          </div>
        </div>
      </div>

      {/* Filters (Categories & Months) */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3">
        {/* Category Chips */}
        <div className="flex items-center space-x-1.5 overflow-x-auto w-full sm:w-auto pb-1">
          {CATEGORIES.map((cat) => {
            const isActive = selectedCategory === cat;
            return (
              <button
                key={cat}
                onClick={() => setSelectedCategory(cat)}
                className={`px-3 py-1.5 rounded-lg text-xs font-semibold whitespace-nowrap transition-all ${
                  isActive
                    ? "bg-indigo-600 text-white shadow-sm"
                    : "bg-white dark:bg-slate-900 text-slate-600 dark:text-slate-300 border border-slate-200 dark:border-slate-800 hover:bg-slate-100 dark:hover:bg-slate-800"
                }`}
              >
                {cat}
              </button>
            );
          })}
        </div>

        {/* Month Selector */}
        <div className="flex items-center space-x-2 w-full sm:w-auto">
          <span className="text-xs font-semibold text-slate-500 dark:text-slate-400">Month:</span>
          <select
            value={selectedMonth}
            onChange={(e) => setSelectedMonth(e.target.value)}
            className="px-3 py-1.5 text-xs font-medium rounded-lg bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 text-slate-800 dark:text-slate-200 focus:outline-none focus:ring-2 focus:ring-indigo-500"
          >
            {MONTHS.map((m) => (
              <option key={m} value={m}>
                {m}
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* Events List */}
      {loading ? (
        <div className="text-center py-16 bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800">
          <div className="inline-block w-8 h-8 border-4 border-indigo-600 border-t-transparent rounded-full animate-spin mb-3"></div>
          <p className="text-sm text-slate-500 dark:text-slate-400">Loading academic calendar...</p>
        </div>
      ) : error ? (
        <div className="p-6 text-center bg-rose-50 dark:bg-rose-950/30 rounded-2xl border border-rose-200 dark:border-rose-900 text-rose-700 dark:text-rose-300">
          <p className="font-semibold">{error}</p>
        </div>
      ) : filteredEvents.length === 0 ? (
        <div className="text-center py-12 bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 text-slate-500">
          No calendar events match your filter criteria.
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {filteredEvents.map((ev) => {
            const isHoliday = ev.is_holiday;
            const isExam = ev.category === "Examination";
            const isCA = ev.category === "CA Test";
            const isFee = ev.category === "Fee Payment";

            return (
              <div
                key={ev.id}
                className={`p-5 rounded-2xl border transition-all duration-200 flex flex-col justify-between ${
                  isHoliday
                    ? "bg-rose-50/40 dark:bg-rose-950/20 border-rose-200 dark:border-rose-900/60 hover:border-rose-400"
                    : isExam
                    ? "bg-indigo-50/40 dark:bg-indigo-950/20 border-indigo-200 dark:border-indigo-900/60"
                    : isCA
                    ? "bg-blue-50/40 dark:bg-blue-950/20 border-blue-200 dark:border-blue-900/60"
                    : isFee
                    ? "bg-emerald-50/40 dark:bg-emerald-950/20 border-emerald-200 dark:border-emerald-900/60"
                    : "bg-white dark:bg-slate-900 border-slate-200 dark:border-slate-800 hover:shadow-md"
                }`}
              >
                <div>
                  {/* Category & Semester tags */}
                  <div className="flex items-center justify-between gap-2 mb-2">
                    <span
                      className={`px-2.5 py-0.5 rounded-full text-[10px] font-bold uppercase tracking-wider ${
                        isHoliday
                          ? "bg-rose-100 text-rose-800 dark:bg-rose-900/60 dark:text-rose-300"
                          : isExam
                          ? "bg-indigo-100 text-indigo-800 dark:bg-indigo-900/60 dark:text-indigo-300"
                          : isCA
                          ? "bg-blue-100 text-blue-800 dark:bg-blue-900/60 dark:text-blue-300"
                          : isFee
                          ? "bg-emerald-100 text-emerald-800 dark:bg-emerald-900/60 dark:text-emerald-300"
                          : "bg-slate-100 text-slate-800 dark:bg-slate-800 dark:text-slate-300"
                      }`}
                    >
                      {ev.category}
                    </span>

                    {ev.semester && (
                      <span className="text-[11px] font-medium text-slate-500 dark:text-slate-400">
                        {ev.semester}
                      </span>
                    )}
                  </div>

                  {/* Event Title */}
                  <h3 className="text-base font-bold text-slate-900 dark:text-white">
                    {ev.event}
                  </h3>

                  {ev.description && (
                    <p className="text-xs text-slate-600 dark:text-slate-400 mt-2 leading-relaxed">
                      {ev.description}
                    </p>
                  )}
                </div>

                {/* Date footer */}
                <div className="mt-4 pt-3 border-t border-slate-200/60 dark:border-slate-800 flex items-center justify-between text-xs font-semibold text-slate-700 dark:text-slate-300">
                  <span className="flex items-center space-x-1.5">
                    <CalendarDays className="w-4 h-4 text-indigo-500" />
                    <span>{formatDate(ev.date, ev.day)}</span>
                  </span>
                  {isHoliday && (
                    <span className="text-[10px] text-rose-600 dark:text-rose-400 font-bold uppercase">
                      Holiday
                    </span>
                  )}
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
