"use client";

import { Check, Circle, Trash2 } from "lucide-react";
import type { Task } from "@/lib/api/tasks";

type TaskCardProps = {
  task: Task;
  onToggle: (id: number) => void;
  onDelete: (id: number) => void;
};

export function TaskCard({ task, onToggle, onDelete }: TaskCardProps) {
  return (
    <article className="bg-surface-glass border border-border-glass backdrop-blur-xl rounded-2xl p-4 transition-colors duration-200 hover:border-teal/40">
      <header className="flex items-start justify-between gap-3 mb-2">
        <h2
          className={`text-base font-semibold font-heading leading-snug ${
            task.is_completed
              ? "line-through text-slate-400"
              : "text-text-primary"
          }`}
        >
          {task.title}
        </h2>
        <span
          className={`shrink-0 inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-semibold ${
            task.is_completed
              ? "bg-success-bg text-success-text"
              : "bg-warning-bg text-warning-text"
          }`}
        >
          {task.is_completed ? (
            <>
              <Check className="w-3 h-3" /> Completed
            </>
          ) : (
            <>
              <Circle className="w-3 h-3" /> Pending
            </>
          )}
        </span>
      </header>

      {task.description && (
        <p className="text-sm text-text-muted mb-3 leading-relaxed">
          {task.description}
        </p>
      )}

      <div className="flex items-center gap-2 mt-3">
        <button
          type="button"
          onClick={() => onToggle(task.id)}
          className="inline-flex items-center gap-1.5 px-3 py-2 rounded-lg bg-teal text-slate-950 text-sm font-semibold cursor-pointer hover:bg-teal-hover transition-colors duration-200 min-h-[44px]"
        >
          {task.is_completed ? (
            <>
              <Circle className="w-4 h-4" /> Mark Pending
            </>
          ) : (
            <>
              <Check className="w-4 h-4" /> Mark Complete
            </>
          )}
        </button>
        <button
          type="button"
          onClick={() => onDelete(task.id)}
          className="inline-flex items-center gap-1.5 px-3 py-2 rounded-lg bg-danger text-slate-950 text-sm font-semibold cursor-pointer hover:bg-danger-hover transition-colors duration-200 min-h-[44px]"
        >
          <Trash2 className="w-4 h-4" /> Delete
        </button>
      </div>
    </article>
  );
}
