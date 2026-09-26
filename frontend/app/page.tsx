"use client";

import { useState, useRef, useEffect, Suspense } from "react";
import { useSearchParams } from "next/navigation";
import {
  Send,
  Bot,
  User,
  Sparkles,
  RotateCcw,
  Tag,
  CheckCircle2,
} from "lucide-react";
import { ChatMessage } from "@/types";
import { sendChatMessage } from "@/lib/api";

const SUGGESTED_QUESTIONS = [
  "What is my schedule today?",
  "Where is ML Lab?",
  "When does the semester start?",
  "When are the CA tests?",
  "Show my Day III schedule",
  "What is my next class?",
  "When is AI on Day III?",
  "Who handles AM/SQA?",
  "When is Christmas holiday?",
  "When is the examination fee payment deadline?",
];

function ChatContent() {
  const searchParams = useSearchParams();
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      id: "initial-welcome",
      sender: "bot",
      text: "👋 Welcome! I am your MCA Academic Assistant for PSG College of Arts & Science (Semester III).\n\nAsk me anything about your timetable, lab classrooms, faculty schedules, CA test dates, exam fee deadlines, holidays, or academic calendar events for 2026-2027.",
      timestamp: "Just now",
      intent: "general_welcome",
      sources: ["PSG College of Arts & Science Academic Calendar 2026-2027", "MCA Semester III Timetable"],
    },
  ]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    const q = searchParams.get("q");
    if (q) {
      setInput(q);
      handleSend(q);
    }
  }, [searchParams]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading]);

  const handleSend = async (textToSend?: string) => {
    const question = (textToSend || input).trim();
    if (!question || isLoading) return;

    const userMessage: ChatMessage = {
      id: `user-${Date.now()}`,
      sender: "user",
      text: question,
      timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setIsLoading(true);

    try {
      const response = await sendChatMessage(question);
      const botMessage: ChatMessage = {
        id: `bot-${Date.now()}`,
        sender: "bot",
        text: response.answer,
        timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
        intent: response.intent,
        sources: response.sources,
      };
      setMessages((prev) => [...prev, botMessage]);
    } catch (err: unknown) {
      const errorText =
        err instanceof Error
          ? err.message
          : "Unable to reach the assistant server. Please ensure the backend is running.";
      const errorMessage: ChatMessage = {
        id: `err-${Date.now()}`,
        sender: "bot",
        text: `⚠️ ${errorText}`,
        timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
        error: true,
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
      setTimeout(() => inputRef.current?.focus(), 50);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const handleReset = () => {
    setMessages([
      {
        id: "initial-welcome-reset",
        sender: "bot",
        text: "Conversation reset. How can I help you today with your MCA Semester III schedule or academic calendar?",
        timestamp: "Just now",
        intent: "general_welcome",
        sources: ["PSG College of Arts & Science Academic Calendar 2026-2027", "MCA Semester III Timetable"],
      },
    ]);
  };

  return (
    <div className="flex flex-col h-[calc(100vh-10.5rem)] min-h-[550px] max-w-5xl mx-auto bg-white dark:bg-slate-900 rounded-2xl shadow-xl border border-slate-200/80 dark:border-slate-800 overflow-hidden">
      {/* Page Header */}
      <div className="px-5 py-4 border-b border-slate-200 dark:border-slate-800 bg-gradient-to-r from-blue-50/50 via-indigo-50/30 to-white dark:from-slate-800/60 dark:to-slate-900 flex items-center justify-between">
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 rounded-xl bg-blue-600 text-white flex items-center justify-center shadow-md shadow-blue-500/20">
            <Bot className="w-6 h-6" />
          </div>
          <div>
            <h1 className="text-base sm:text-lg font-bold text-slate-900 dark:text-white flex items-center space-x-2">
              <span>🎓 MCA Academic Assistant</span>
              <span className="text-xs px-2 py-0.5 rounded-full bg-blue-100 text-blue-800 dark:bg-blue-900/60 dark:text-blue-300 font-semibold">
                NLP Powered
              </span>
            </h1>
            <p className="text-xs text-slate-500 dark:text-slate-400">
              PSG College of Arts & Science • Semester III (2026–2027)
            </p>
          </div>
        </div>

        <div className="flex items-center space-x-2">
          <button
            onClick={handleReset}
            className="flex items-center space-x-1.5 px-3 py-1.5 rounded-lg text-xs font-medium text-slate-600 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
            title="Reset conversation"
          >
            <RotateCcw className="w-3.5 h-3.5" />
            <span className="hidden sm:inline">Reset</span>
          </button>
        </div>
      </div>

      {/* Suggested Questions Carousel / Chip Row */}
      <div className="px-4 py-2.5 bg-slate-50/80 dark:bg-slate-800/40 border-b border-slate-200/60 dark:border-slate-800 overflow-x-auto no-scrollbar flex items-center space-x-2">
        <span className="text-xs font-semibold text-slate-500 dark:text-slate-400 flex items-center space-x-1 flex-shrink-0 pr-1">
          <Sparkles className="w-3.5 h-3.5 text-amber-500" />
          <span>Suggestions:</span>
        </span>
        {SUGGESTED_QUESTIONS.map((q, idx) => (
          <button
            key={idx}
            onClick={() => handleSend(q)}
            disabled={isLoading}
            className="flex-shrink-0 px-3 py-1 text-xs rounded-full bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 hover:border-blue-500 dark:hover:border-blue-400 hover:text-blue-600 dark:hover:text-blue-400 hover:bg-blue-50/50 dark:hover:bg-slate-700/50 transition-all duration-150 text-slate-700 dark:text-slate-300 font-medium shadow-2xs"
          >
            {q}
          </button>
        ))}
      </div>

      {/* Chat Messages Container */}
      <div className="flex-1 overflow-y-auto p-4 sm:p-6 space-y-4 sm:space-y-6">
        {messages.map((msg) => {
          const isUser = msg.sender === "user";
          return (
            <div
              key={msg.id}
              className={`flex items-start gap-3 ${isUser ? "flex-row-reverse" : "flex-row"}`}
            >
              {/* Avatar */}
              <div
                className={`w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0 text-white shadow-sm ${
                  isUser
                    ? "bg-slate-700 dark:bg-slate-600"
                    : "bg-gradient-to-tr from-blue-600 to-indigo-600"
                }`}
              >
                {isUser ? <User className="w-4 h-4" /> : <Bot className="w-4 h-4" />}
              </div>

              {/* Message Bubble */}
              <div className={`flex flex-col max-w-[85%] sm:max-w-[75%] ${isUser ? "items-end" : "items-start"}`}>
                <div
                  className={`px-4 py-3 rounded-2xl text-sm leading-relaxed shadow-xs ${
                    isUser
                      ? "bg-blue-600 text-white rounded-tr-xs"
                      : msg.error
                      ? "bg-rose-50 dark:bg-rose-950/40 text-rose-900 dark:text-rose-200 border border-rose-200 dark:border-rose-900 rounded-tl-xs"
                      : "bg-slate-100 dark:bg-slate-800 text-slate-800 dark:text-slate-100 border border-slate-200/60 dark:border-slate-700/60 rounded-tl-xs"
                  }`}
                >
                  <p className="whitespace-pre-wrap">{msg.text}</p>
                </div>

                {/* Intent & Source Badges for Bot */}
                {!isUser && !msg.error && (
                  <div className="flex flex-wrap items-center gap-1.5 mt-1.5 px-1">
                    {msg.intent && msg.intent !== "general_welcome" && (
                      <span className="inline-flex items-center space-x-1 px-2 py-0.5 rounded-md text-[10px] font-medium bg-slate-200/80 dark:bg-slate-700/60 text-slate-600 dark:text-slate-300">
                        <Tag className="w-2.5 h-2.5" />
                        <span>{msg.intent}</span>
                      </span>
                    )}
                    {msg.sources && msg.sources.length > 0 && (
                      <span className="inline-flex items-center space-x-1 px-2 py-0.5 rounded-md text-[10px] font-medium bg-blue-50 dark:bg-blue-950/60 text-blue-700 dark:text-blue-300 border border-blue-200/50 dark:border-blue-900/50">
                        <CheckCircle2 className="w-2.5 h-2.5 text-blue-500" />
                        <span>{msg.sources[0]}</span>
                      </span>
                    )}
                    <span className="text-[10px] text-slate-400 dark:text-slate-500 ml-1">
                      {msg.timestamp}
                    </span>
                  </div>
                )}

                {isUser && (
                  <span className="text-[10px] text-slate-400 dark:text-slate-500 mt-1 px-1">
                    {msg.timestamp}
                  </span>
                )}
              </div>
            </div>
          );
        })}

        {/* Loading Indicator */}
        {isLoading && (
          <div className="flex items-start gap-3">
            <div className="w-8 h-8 rounded-full bg-gradient-to-tr from-blue-600 to-indigo-600 flex items-center justify-center text-white flex-shrink-0">
              <Bot className="w-4 h-4" />
            </div>
            <div className="px-4 py-3 rounded-2xl rounded-tl-xs bg-slate-100 dark:bg-slate-800 border border-slate-200/60 dark:border-slate-700/60 shadow-xs">
              <div className="flex items-center space-x-1.5">
                <span className="w-2 h-2 rounded-full bg-blue-600 animate-bounce" style={{ animationDelay: "0ms" }} />
                <span className="w-2 h-2 rounded-full bg-indigo-600 animate-bounce" style={{ animationDelay: "150ms" }} />
                <span className="w-2 h-2 rounded-full bg-sky-500 animate-bounce" style={{ animationDelay: "300ms" }} />
                <span className="text-xs text-slate-500 dark:text-slate-400 ml-2 font-medium">Processing query...</span>
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input Form */}
      <div className="p-3 sm:p-4 bg-white dark:bg-slate-900 border-t border-slate-200 dark:border-slate-800">
        <form
          onSubmit={(e) => {
            e.preventDefault();
            handleSend();
          }}
          className="flex items-center gap-2"
        >
          <input
            ref={inputRef}
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Ask about timetable, ML Lab, AI schedule, CA tests, holidays, exam fee deadlines..."
            className="flex-1 px-4 py-3 text-sm rounded-xl bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-slate-900 dark:text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all shadow-inner"
            disabled={isLoading}
          />
          <button
            type="submit"
            disabled={!input.trim() || isLoading}
            className="px-5 py-3 rounded-xl bg-blue-600 hover:bg-blue-700 disabled:opacity-50 disabled:hover:bg-blue-600 text-white font-medium text-sm flex items-center space-x-1.5 shadow-md shadow-blue-500/20 transition-all cursor-pointer disabled:cursor-not-allowed"
          >
            <span>Send</span>
            <Send className="w-4 h-4" />
          </button>
        </form>
      </div>
    </div>
  );
}

export default function ChatbotPage() {
  return (
    <Suspense
      fallback={
        <div className="flex items-center justify-center h-64 text-sm text-slate-500">
          Loading Academic Assistant...
        </div>
      }
    >
      <ChatContent />
    </Suspense>
  );
}
