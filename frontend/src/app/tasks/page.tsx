"use client";

import { FormEvent, useCallback, useEffect, useState } from "react";
import { Plus } from "lucide-react";

import { TaskLayout } from "@/components/tasks/TaskLayout";
import { TaskStates } from "@/components/tasks/TaskStates";
import { TaskCard } from "@/components/tasks/TaskCard";
import {
  listTasks,
  createTask,
  toggleTask,
  deleteTask,
  Task,
} from "@/lib/api/tasks";

export default function TasksPage() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [formError, setFormError] = useState<string | null>(null);
  const [pageError, setPageError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);

  const fetchTasks = useCallback(async () => {
    setLoading(true);
    setPageError(null);
    try {
      const data = await listTasks();
      setTasks(data);
    } catch (err) {
      setPageError(
        err instanceof Error ? err.message : "Failed to load tasks"
      );
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchTasks();
  }, [fetchTasks]);

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();
    const trimmed = title.trim();
    if (!trimmed) {
      setFormError("Title is required.");
      return;
    }

    setFormError(null);
    setSubmitting(true);
    try {
      const newTask = await createTask({
        title: trimmed,
        description: description.trim() || undefined,
      });
      setTasks((prev) => [...prev, newTask]);
      setTitle("");
      setDescription("");
    } catch (err) {
      setFormError(
        err instanceof Error ? err.message : "Failed to create task"
      );
    } finally {
      setSubmitting(false);
    }
  }

  async function handleToggle(id: number) {
    try {
      const updated = await toggleTask(id);
      setTasks((prev) =>
        prev.map((t) => (t.id === id ? updated : t))
      );
    } catch (err) {
      setPageError(
        err instanceof Error ? err.message : "Failed to toggle task"
      );
    }
  }

  async function handleDelete(id: number) {
    try {
      await deleteTask(id);
      setTasks((prev) => prev.filter((t) => t.id !== id));
    } catch (err) {
      setPageError(
        err instanceof Error ? err.message : "Failed to delete task"
      );
    }
  }

  return (
    <TaskLayout>
      {/* Create Task Form */}
      <section className="bg-white/70 backdrop-blur-lg rounded-xl border border-white/20 shadow-lg shadow-black/5 p-5">
        <h2 className="text-lg font-bold font-heading text-text-primary mb-4">
          New Task
        </h2>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label
              htmlFor="task-title"
              className="block text-sm font-semibold text-text-primary mb-1.5"
            >
              Title
            </label>
            <input
              id="task-title"
              type="text"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              placeholder="What needs to be done?"
              className="w-full px-4 py-3 rounded-xl bg-white/80 border border-border-subtle focus:border-teal focus:ring-2 focus:ring-teal/20 outline-none transition-colors duration-200 text-text-primary placeholder:text-text-muted/50"
            />
          </div>
          <div>
            <label
              htmlFor="task-desc"
              className="block text-sm font-semibold text-text-primary mb-1.5"
            >
              Description
            </label>
            <textarea
              id="task-desc"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              placeholder="Optional details..."
              rows={3}
              className="w-full px-4 py-3 rounded-xl bg-white/80 border border-border-subtle focus:border-teal focus:ring-2 focus:ring-teal/20 outline-none transition-colors duration-200 text-text-primary placeholder:text-text-muted/50 resize-none"
            />
          </div>

          {formError && (
            <p className="text-sm text-danger font-medium" role="alert">
              {formError}
            </p>
          )}

          <button
            type="submit"
            disabled={submitting}
            className="inline-flex items-center gap-2 px-5 py-3 rounded-xl bg-teal text-white font-bold text-sm cursor-pointer hover:bg-teal-hover focus:ring-2 focus:ring-teal/20 focus:outline-none transition-colors duration-200 disabled:opacity-50 disabled:cursor-not-allowed min-h-[44px]"
          >
            <Plus className="w-4 h-4" />
            {submitting ? "Adding..." : "Add Task"}
          </button>
        </form>
      </section>

      {/* Task List */}
      <section className="bg-white/70 backdrop-blur-lg rounded-xl border border-white/20 shadow-lg shadow-black/5 p-5">
        <h2 className="text-lg font-bold font-heading text-text-primary mb-4">
          Your Tasks
        </h2>

        <TaskStates
          loading={loading}
          error={pageError}
          empty={!loading && !pageError && tasks.length === 0}
          onRetry={fetchTasks}
        />

        <div className="space-y-3" aria-live="polite">
          {tasks.map((task) => (
            <TaskCard
              key={task.id}
              task={task}
              onToggle={handleToggle}
              onDelete={handleDelete}
            />
          ))}
        </div>
      </section>
    </TaskLayout>
  );
}
