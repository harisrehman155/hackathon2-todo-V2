"use client";

import { FormEvent, useEffect, useRef, useState } from "react";
import { Plus, X } from "lucide-react";

type CreateTaskModalProps = {
  open: boolean;
  loading?: boolean;
  onClose: () => void;
  onSubmit: (payload: { title: string; description?: string }) => Promise<void>;
};

export function CreateTaskModal({
  open,
  loading = false,
  onClose,
  onSubmit,
}: CreateTaskModalProps) {
  const titleRef = useRef<HTMLInputElement>(null);
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!open) return;
    setTitle("");
    setDescription("");
    setError(null);
    const id = window.setTimeout(() => titleRef.current?.focus(), 10);
    const onKeyDown = (event: KeyboardEvent) => {
      if (event.key === "Escape") onClose();
    };
    document.addEventListener("keydown", onKeyDown);
    document.body.style.overflow = "hidden";
    return () => {
      window.clearTimeout(id);
      document.removeEventListener("keydown", onKeyDown);
      document.body.style.overflow = "";
    };
  }, [open, onClose]);

  if (!open) return null;

  async function handleSubmit(event: FormEvent) {
    event.preventDefault();
    const trimmedTitle = title.trim();
    if (!trimmedTitle) {
      setError("Title is required.");
      return;
    }

    setError(null);
    try {
      await onSubmit({
        title: trimmedTitle,
        description: description.trim() || undefined,
      });
      onClose();
    } catch (submitError) {
      setError(
        submitError instanceof Error ? submitError.message : "Unable to create task",
      );
    }
  }

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center px-4"
      role="dialog"
      aria-modal="true"
      aria-labelledby="create-task-title"
    >
      <button
        aria-label="Close task creation modal"
        className="absolute inset-0 bg-black/70 backdrop-blur-sm cursor-pointer"
        onClick={onClose}
        type="button"
      />

      <section className="relative w-full max-w-lg rounded-2xl border border-border-glass bg-surface-glass-strong backdrop-blur-xl shadow-2xl shadow-black/45 p-5 sm:p-6">
        <header className="flex items-center justify-between gap-3 mb-5">
          <div>
            <h2 id="create-task-title" className="text-xl font-bold font-heading text-text-primary">
              New Task
            </h2>
            <p className="text-sm text-text-muted mt-1">Status will be set to pending by default.</p>
          </div>
          <button
            aria-label="Close modal"
            className="inline-flex items-center justify-center w-10 h-10 rounded-xl border border-border-subtle text-text-muted hover:text-text-primary hover:border-teal/60 transition-colors duration-200 cursor-pointer min-h-[44px] min-w-[44px]"
            onClick={onClose}
            type="button"
          >
            <X className="w-4 h-4" />
          </button>
        </header>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label htmlFor="new-task-title" className="block text-sm font-semibold text-text-primary mb-1.5">
              Title
            </label>
            <input
              id="new-task-title"
              ref={titleRef}
              type="text"
              value={title}
              onChange={(event) => setTitle(event.target.value)}
              placeholder="Write your task title..."
              className="w-full px-4 py-3 rounded-xl bg-slate-950/55 border border-border-subtle text-text-primary placeholder:text-slate-400 focus:border-teal outline-none transition-colors duration-200"
            />
          </div>

          <div>
            <label htmlFor="new-task-description" className="block text-sm font-semibold text-text-primary mb-1.5">
              Description
            </label>
            <textarea
              id="new-task-description"
              rows={4}
              value={description}
              onChange={(event) => setDescription(event.target.value)}
              placeholder="Optional details..."
              className="w-full px-4 py-3 rounded-xl bg-slate-950/55 border border-border-subtle text-text-primary placeholder:text-slate-400 focus:border-teal outline-none transition-colors duration-200 resize-none"
            />
          </div>

          {error && (
            <p className="text-sm text-danger font-medium" role="alert">
              {error}
            </p>
          )}

          <div className="flex items-center justify-end gap-2 pt-1">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2.5 rounded-xl border border-border-subtle text-sm font-semibold text-text-muted hover:text-text-primary hover:border-teal/50 transition-colors duration-200 cursor-pointer min-h-[44px]"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={loading}
              className="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-teal text-slate-950 text-sm font-bold hover:bg-teal-hover transition-colors duration-200 cursor-pointer disabled:opacity-60 disabled:cursor-not-allowed min-h-[44px]"
            >
              <Plus className="w-4 h-4" />
              {loading ? "Creating..." : "Create Task"}
            </button>
          </div>
        </form>
      </section>
    </div>
  );
}
