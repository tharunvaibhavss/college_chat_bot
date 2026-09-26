import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import Navbar from "@/components/Navbar";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "MCA Academic Assistant | PSG College of Arts & Science",
  description:
    "NLP-powered College Academic Assistant Chatbot for MCA Semester III Timetable & Academic Calendar 2026-2027",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html
      lang="en"
      className={`${geistSans.variable} ${geistMono.variable} h-full antialiased`}
    >
      <body className="min-h-full flex flex-col bg-slate-50 dark:bg-slate-950 text-slate-800 dark:text-slate-100 font-sans transition-colors">
        <Navbar />
        <main className="flex-1 max-w-7xl w-full mx-auto p-4 sm:p-6 lg:p-8">
          {children}
        </main>
        <footer className="border-t border-slate-200 dark:border-slate-800 bg-white/70 dark:bg-slate-900/70 py-6 text-center text-xs text-slate-500 dark:text-slate-400">
          <div className="max-w-7xl mx-auto px-4 space-y-1">
            <p className="font-medium text-slate-700 dark:text-slate-300">
              Department of Computer Applications (MCA) • PSG College of Arts & Science
            </p>
            <p>
              Academic Calendar 2026–2027 & Semester III Timetable • Powered by FastAPI & NLP
            </p>
          </div>
        </footer>
      </body>
    </html>
  );
}
