"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import {
  BookOpen,
  FlaskConical,
  Clock,
  MapPin,
  User,
  Search,
  MessageSquare,
  Sparkles,
  Layers,
} from "lucide-react";
import { SubjectDetail } from "@/types";
import { fetchSubjects } from "@/lib/api";

export default function SubjectsPage() {
  const [subjects, setSubjects] = useState<SubjectDetail[]>([]);
  const [searchQuery, setSearchQuery] = useState("");
  const [filterType, setFilterType] = useState("All");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const loadSubjects = async () => {
      try {
        setLoading(true);
        const data = await fetchSubjects();
        setSubjects(data);
      } catch (err: unknown) {
        setError(err instanceof Error ? err.message : "Failed to load subjects.");
      } finally {
        setLoading(false);
      }
    };
    loadSubjects();
  }, []);

  const filteredSubjects = subjects.filter((s) => {
    const matchesType =
      filterType === "All" ||
      (filterType === "Lab" ? s.class_type === "Lab" : s.class_type.includes(filterType));
    const matchesSearch =
      searchQuery === "" ||
      s.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      s.code.toLowerCase().includes(searchQuery.toLowerCase()) ||
      (s.faculty && s.faculty.toLowerCase().includes(searchQuery.toLowerCase()));
    return matchesType && matchesSearch;
  });

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-white dark:bg-slate-900 p-6 rounded-2xl border border-slate-200 dark:border-slate-800 shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center space-x-2">
            <span className="p-2 rounded-lg bg-blue-100 dark:bg-blue-900/50 text-blue-700 dark:text-blue-300">
              <BookOpen className="w-5 h-5" />
            </span>
            <h1 className="text-xl sm:text-2xl font-bold text-slate-900 dark:text-white">
              Subjects & Course Schedules
            </h1>
          </div>
          <p className="text-sm text-slate-500 dark:text-slate-400 mt-1">
            Department of Computer Applications • MCA Semester III
          </p>
        </div>

        {/* Search */}
        <div className="relative w-full md:w-72">
          <Search className="w-4 h-4 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search subjects by name, code, faculty..."
            className="w-full pl-9 pr-4 py-2 text-sm rounded-xl bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-slate-900 dark:text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
      </div>

      {/* Filter Tabs */}
      <div className="flex items-center space-x-2">
        {["All", "Theory", "Lab", "Major Elective"].map((t) => (
          <button
            key={t}
            onClick={() => setFilterType(t)}
            className={`px-3.5 py-1.5 rounded-lg text-xs font-semibold transition-all ${
              filterType === t
                ? "bg-blue-600 text-white shadow-sm"
                : "bg-white dark:bg-slate-900 text-slate-600 dark:text-slate-300 border border-slate-200 dark:border-slate-800 hover:bg-slate-100 dark:hover:bg-slate-800"
            }`}
          >
            {t}
          </button>
        ))}
      </div>

      {/* Subjects Grid */}
      {loading ? (
        <div className="text-center py-16 bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800">
          <div className="inline-block w-8 h-8 border-4 border-blue-600 border-t-transparent rounded-full animate-spin mb-3"></div>
          <p className="text-sm text-slate-500 dark:text-slate-400">Loading course curriculum...</p>
        </div>
      ) : error ? (
        <div className="p-6 text-center bg-rose-50 dark:bg-rose-950/30 rounded-2xl border border-rose-200 dark:border-rose-900 text-rose-700 dark:text-rose-300">
          <p className="font-semibold">{error}</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {filteredSubjects.map((sub) => {
            const isLab = sub.class_type === "Lab";
            const isElective = sub.class_type === "Major Elective";

            return (
              <div
                key={sub.id}
                className="bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 shadow-sm p-6 flex flex-col justify-between hover:shadow-md transition-shadow"
              >
                <div>
                  {/* Top Bar: Code & Type */}
                  <div className="flex items-center justify-between gap-2 mb-3">
                    <span className="font-mono text-xs font-bold px-2.5 py-1 rounded-md bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 border border-slate-200 dark:border-slate-700">
                      {sub.code}
                    </span>
                    <span
                      className={`px-2.5 py-0.5 rounded-full text-[10px] font-bold uppercase tracking-wider ${
                        isLab
                          ? "bg-teal-100 text-teal-800 dark:bg-teal-900/60 dark:text-teal-300"
                          : isElective
                          ? "bg-purple-100 text-purple-800 dark:bg-purple-900/60 dark:text-purple-300"
                          : "bg-blue-100 text-blue-800 dark:bg-blue-900/60 dark:text-blue-300"
                      }`}
                    >
                      {sub.class_type}
                    </span>
                  </div>

                  {/* Title */}
                  <h2 className="text-lg font-bold text-slate-900 dark:text-white flex items-center space-x-2">
                    {isLab ? (
                      <FlaskConical className="w-5 h-5 text-teal-600 dark:text-teal-400" />
                    ) : (
                      <BookOpen className="w-5 h-5 text-blue-600 dark:text-blue-400" />
                    )}
                    <span>{sub.name}</span>
                  </h2>

                  {/* Description */}
                  {sub.description && (
                    <p className="text-xs text-slate-600 dark:text-slate-400 mt-2 leading-relaxed">
                      {sub.description}
                    </p>
                  )}

                  {/* Faculty */}
                  {sub.faculty && (
                    <div className="mt-3 flex items-center space-x-2 text-xs text-slate-700 dark:text-slate-300">
                      <User className="w-3.5 h-3.5 text-indigo-500 flex-shrink-0" />
                      <span>
                        <strong className="text-slate-900 dark:text-white">Faculty:</strong> {sub.faculty}
                      </span>
                    </div>
                  )}

                  {/* Schedule Slots */}
                  <div className="mt-4 pt-4 border-t border-slate-200/60 dark:border-slate-800">
                    <span className="text-xs font-bold uppercase tracking-wider text-slate-500 dark:text-slate-400 block mb-2">
                      Scheduled Timetable Periods:
                    </span>
                    {sub.schedules && sub.schedules.length > 0 ? (
                      <div className="space-y-1.5">
                        {sub.schedules.map((slot, idx) => (
                          <div
                            key={idx}
                            className="flex flex-col sm:flex-row sm:items-center justify-between p-2 rounded-lg bg-slate-50 dark:bg-slate-800/50 text-xs border border-slate-100 dark:border-slate-800 gap-1"
                          >
                            <span className="font-semibold text-blue-600 dark:text-blue-400">
                              {slot.day_order}
                            </span>
                            <span className="text-slate-600 dark:text-slate-300 font-mono">
                              {slot.start_time} - {slot.end_time}
                            </span>
                            {slot.room && (
                              <span className="inline-flex items-center space-x-1 text-slate-700 dark:text-slate-300">
                                <MapPin className="w-3 h-3 text-rose-500" />
                                <span className="font-semibold">{slot.room}</span>
                              </span>
                            )}
                          </div>
                        ))}
                      </div>
                    ) : (
                      <p className="text-xs text-slate-400 italic">No scheduled timetable slots found.</p>
                    )}
                  </div>
                </div>

                {/* Card footer CTA to chatbot */}
                <div className="mt-5 pt-3 border-t border-slate-200/60 dark:border-slate-800 flex items-center justify-end">
                  <Link
                    href={`/?q=${encodeURIComponent(`When do I have ${sub.name}?`)}`}
                    className="inline-flex items-center space-x-1.5 text-xs font-semibold text-blue-600 dark:text-blue-400 hover:text-blue-700 hover:underline"
                  >
                    <MessageSquare className="w-3.5 h-3.5" />
                    <span>Ask Assistant about this course</span>
                  </Link>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
