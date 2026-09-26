"use client";

import { useState, useEffect } from "react";
import {
  Clock,
  MapPin,
  User,
  Coffee,
  Utensils,
  FlaskConical,
  BookOpen,
  Sparkles,
  Calendar,
  Search,
} from "lucide-react";
import { TimetableSlot } from "@/types";
import { fetchTimetable } from "@/lib/api";

const DAYS = ["All Days", "Day I", "Day II", "Day III", "Day IV", "Day V", "Day VI"];

export default function TimetablePage() {
  const [timetable, setTimetable] = useState<TimetableSlot[]>([]);
  const [selectedDay, setSelectedDay] = useState("All Days");
  const [searchQuery, setSearchQuery] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const loadTimetable = async () => {
      try {
        setLoading(true);
        const data = await fetchTimetable();
        setTimetable(data);
      } catch (err: unknown) {
        setError(err instanceof Error ? err.message : "Failed to load timetable.");
      } finally {
        setLoading(false);
      }
    };
    loadTimetable();
  }, []);

  const filteredSlots = timetable.filter((slot) => {
    const matchesDay = selectedDay === "All Days" || slot.day_order === selectedDay;
    const matchesSearch =
      searchQuery === "" ||
      slot.subject.toLowerCase().includes(searchQuery.toLowerCase()) ||
      (slot.room && slot.room.toLowerCase().includes(searchQuery.toLowerCase())) ||
      (slot.faculty && slot.faculty.toLowerCase().includes(searchQuery.toLowerCase()));
    return matchesDay && matchesSearch;
  });

  // Group slots by Day Order
  const groupedDays = ["Day I", "Day II", "Day III", "Day IV", "Day V", "Day VI"].reduce(
    (acc, day) => {
      acc[day] = filteredSlots.filter((s) => s.day_order === day);
      return acc;
    },
    {} as Record<string, TimetableSlot[]>
  );

  return (
    <div className="space-y-6">
      {/* Page Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 bg-white dark:bg-slate-900 p-6 rounded-2xl border border-slate-200 dark:border-slate-800 shadow-sm">
        <div>
          <div className="flex items-center space-x-2">
            <span className="p-2 rounded-lg bg-blue-100 dark:bg-blue-900/50 text-blue-700 dark:text-blue-300">
              <Clock className="w-5 h-5" />
            </span>
            <h1 className="text-xl sm:text-2xl font-bold text-slate-900 dark:text-white">
              MCA Semester III Timetable
            </h1>
          </div>
          <p className="text-sm text-slate-500 dark:text-slate-400 mt-1">
            Department of Computer Applications • PSG College of Arts & Science
          </p>
        </div>

        {/* Search input */}
        <div className="relative w-full sm:w-64">
          <Search className="w-4 h-4 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search subject, room, faculty..."
            className="w-full pl-9 pr-4 py-2 text-sm rounded-xl bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-slate-900 dark:text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
      </div>

      {/* Break & Lunch Timing Notice Banner */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="flex items-center space-x-4 p-4 rounded-xl bg-gradient-to-r from-amber-50 to-orange-50 dark:from-amber-950/30 dark:to-orange-950/20 border border-amber-200 dark:border-amber-800/60 shadow-xs">
          <div className="w-10 h-10 rounded-xl bg-amber-500 text-white flex items-center justify-center shadow-sm">
            <Coffee className="w-5 h-5" />
          </div>
          <div>
            <span className="text-xs font-bold uppercase tracking-wider text-amber-800 dark:text-amber-300">
              Morning Break
            </span>
            <p className="text-base font-bold text-amber-950 dark:text-amber-100">
              12:00 PM – 12:15 PM
            </p>
            <p className="text-xs text-amber-700 dark:text-amber-400">15-minute inter-period interval</p>
          </div>
        </div>

        <div className="flex items-center space-x-4 p-4 rounded-xl bg-gradient-to-r from-emerald-50 to-teal-50 dark:from-emerald-950/30 dark:to-teal-950/20 border border-emerald-200 dark:border-emerald-800/60 shadow-xs">
          <div className="w-10 h-10 rounded-xl bg-emerald-600 text-white flex items-center justify-center shadow-sm">
            <Utensils className="w-5 h-5" />
          </div>
          <div>
            <span className="text-xs font-bold uppercase tracking-wider text-emerald-800 dark:text-emerald-300">
              Lunch Break
            </span>
            <p className="text-base font-bold text-emerald-950 dark:text-emerald-100">
              1:15 PM – 2:00 PM
            </p>
            <p className="text-xs text-emerald-700 dark:text-emerald-400">45-minute afternoon recess</p>
          </div>
        </div>
      </div>

      {/* Day Order Filter Tabs */}
      <div className="flex items-center space-x-2 overflow-x-auto pb-2">
        {DAYS.map((day) => {
          const isActive = selectedDay === day;
          return (
            <button
              key={day}
              onClick={() => setSelectedDay(day)}
              className={`px-4 py-2 rounded-xl text-sm font-semibold transition-all whitespace-nowrap ${
                isActive
                  ? "bg-blue-600 text-white shadow-md shadow-blue-500/20"
                  : "bg-white dark:bg-slate-900 text-slate-600 dark:text-slate-300 border border-slate-200 dark:border-slate-800 hover:bg-slate-100 dark:hover:bg-slate-800"
              }`}
            >
              {day}
            </button>
          );
        })}
      </div>

      {/* Timetable Display */}
      {loading ? (
        <div className="text-center py-16 bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800">
          <div className="inline-block w-8 h-8 border-4 border-blue-600 border-t-transparent rounded-full animate-spin mb-3"></div>
          <p className="text-sm text-slate-500 dark:text-slate-400">Loading MCA Semester III timetable...</p>
        </div>
      ) : error ? (
        <div className="p-6 text-center bg-rose-50 dark:bg-rose-950/30 rounded-2xl border border-rose-200 dark:border-rose-900 text-rose-700 dark:text-rose-300">
          <p className="font-semibold">{error}</p>
        </div>
      ) : (
        <div className="space-y-6">
          {Object.entries(groupedDays).map(([day, slots]) => {
            if (slots.length === 0) return null;
            return (
              <div
                key={day}
                className="bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 shadow-sm overflow-hidden"
              >
                {/* Day Header */}
                <div className="px-6 py-4 bg-slate-50 dark:bg-slate-800/60 border-b border-slate-200 dark:border-slate-800 flex items-center justify-between">
                  <div className="flex items-center space-x-2">
                    <span className="w-2.5 h-2.5 rounded-full bg-blue-600"></span>
                    <h2 className="text-lg font-bold text-slate-900 dark:text-white">{day}</h2>
                  </div>
                  <span className="text-xs font-semibold px-2.5 py-1 rounded-full bg-slate-200 dark:bg-slate-700 text-slate-700 dark:text-slate-300">
                    {slots.length} Slots
                  </span>
                </div>

                {/* Periods Grid */}
                <div className="p-4 sm:p-6 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                  {slots.map((slot) => {
                    const isLab = slot.class_type === "Lab" || slot.subject.includes("Lab");
                    const isBreak = slot.class_type === "Break" || slot.class_type === "Lunch";
                    const isElective = slot.subject.includes("AM/SQA");

                    return (
                      <div
                        key={slot.id}
                        className={`p-4 rounded-xl border transition-all duration-200 ${
                          isLab
                            ? "bg-teal-50/50 dark:bg-teal-950/20 border-teal-200 dark:border-teal-800 hover:shadow-md hover:border-teal-400"
                            : isBreak
                            ? "bg-amber-50/40 dark:bg-amber-950/20 border-amber-200 dark:border-amber-800"
                            : isElective
                            ? "bg-purple-50/40 dark:bg-purple-950/20 border-purple-200 dark:border-purple-800 hover:shadow-md"
                            : "bg-slate-50/60 dark:bg-slate-800/40 border-slate-200 dark:border-slate-700 hover:shadow-md"
                        }`}
                      >
                        {/* Time & Badge */}
                        <div className="flex items-center justify-between mb-2">
                          <span className="text-xs font-bold text-slate-500 dark:text-slate-400 flex items-center space-x-1">
                            <Clock className="w-3.5 h-3.5 text-blue-500" />
                            <span>
                              {slot.start_time} - {slot.end_time}
                            </span>
                          </span>

                          <span
                            className={`px-2 py-0.5 rounded-md text-[10px] font-bold uppercase tracking-wider ${
                              isLab
                                ? "bg-teal-100 text-teal-800 dark:bg-teal-900/60 dark:text-teal-300"
                                : isBreak
                                ? "bg-amber-100 text-amber-800 dark:bg-amber-900/60 dark:text-amber-300"
                                : isElective
                                ? "bg-purple-100 text-purple-800 dark:bg-purple-900/60 dark:text-purple-300"
                                : "bg-blue-100 text-blue-800 dark:bg-blue-900/60 dark:text-blue-300"
                            }`}
                          >
                            {slot.class_type}
                          </span>
                        </div>

                        {/* Subject Title */}
                        <h3 className="text-base font-bold text-slate-900 dark:text-white flex items-center space-x-2">
                          {isLab && <FlaskConical className="w-4 h-4 text-teal-600 dark:text-teal-400" />}
                          {!isLab && !isBreak && (
                            <BookOpen className="w-4 h-4 text-blue-600 dark:text-blue-400" />
                          )}
                          <span>{slot.subject}</span>
                        </h3>

                        {/* Room and Faculty details */}
                        <div className="mt-3 pt-3 border-t border-slate-200/60 dark:border-slate-700/60 space-y-1.5 text-xs">
                          {slot.room && (
                            <div className="flex items-center space-x-1.5 text-slate-600 dark:text-slate-300">
                              <MapPin className="w-3.5 h-3.5 text-rose-500 flex-shrink-0" />
                              <span className="font-semibold text-slate-900 dark:text-white">
                                {slot.room}
                              </span>
                            </div>
                          )}

                          {slot.faculty && (
                            <div className="flex items-center space-x-1.5 text-slate-600 dark:text-slate-300">
                              <User className="w-3.5 h-3.5 text-indigo-500 flex-shrink-0" />
                              <span className="truncate">{slot.faculty}</span>
                            </div>
                          )}
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
