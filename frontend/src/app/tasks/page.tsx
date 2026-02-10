"use client";

import { useCallback, useEffect, useMemo, useState } from "react";
import { Plus } from "lucide-react";
import { toast } from "react-toastify";

import { ChatDrawer } from "@/components/chat/ChatDrawer";
import { TaskCard } from "@/components/tasks/TaskCard";
import { TaskLayout } from "@/components/tasks/TaskLayout";
import { TaskStates } from "@/components/tasks/TaskStates";
import { CreateTaskModal } from "@/components/tasks/CreateTaskModal";
import { createTask, deleteTask, listTasks, Task, toggleTask } from "@/lib/api/tasks";

export default function TasksPage() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [pageError, setPageError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [showCreateModal, setShowCreateModal] = useState(false);

  const fetchTasks = useCallback(async () => {
    setLoading(true);
    setPageError(null);
    try {
      const data = await listTasks();
      setTasks(data);
    } catch (error) {
      setPageError(error instanceof Error ? error.message : "Failed to load tasks");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchTasks();
  }, [fetchTasks]);

  const pendingTasks = useMemo(() => tasks.filter((task) => !task.is_completed), [tasks]);
  const completedTasks = useMemo(() => tasks.filter((task) => task.is_completed), [tasks]);

  async function handleCreateTask(payload: { title: string; description?: string }) {
    setSubmitting(true);
    try {
      const newTask = await createTask(payload);
      setTasks((prev) => [...prev, newTask]);
      toast.success("Task created.");
      setShowCreateModal(false);
      setPageError(null);
    } catch (error) {
      const message = error instanceof Error ? error.message : "Failed to create task";
      setPageError(message);
      toast.error(message);
    } finally {
      setSubmitting(false);
    }
  }

  async function handleToggleTask(id: number) {
    try {
      const updated = await toggleTask(id);
      setTasks((prev) => prev.map((task) => (task.id === id ? updated : task)));
      setPageError(null);
    } catch (error) {
      const message = error instanceof Error ? error.message : "Failed to update task";
      setPageError(message);
      toast.error(message);
    }
  }

  async function handleDeleteTask(id: number) {
    try {
      await deleteTask(id);
      setTasks((prev) => prev.filter((task) => task.id !== id));
      setPageError(null);
    } catch (error) {
      const message = error instanceof Error ? error.message : "Failed to delete task";
      setPageError(message);
      toast.error(message);
    }
  }

  async function handleChatTaskAction(_toolNames: string[]) {
    await fetchTasks();
  }

  return (
    <TaskLayout>
      <section className="relative overflow-hidden rounded-3xl border border-border-glass bg-surface-glass p-4 sm:p-5 lg:p-6 backdrop-blur-2xl shadow-2xl shadow-black/40">
        <div className="pointer-events-none absolute -top-24 left-1/3 h-44 w-44 rounded-full bg-cyan-400/20 blur-3xl" />
        <div className="pointer-events-none absolute -bottom-24 right-12 h-44 w-44 rounded-full bg-red-400/20 blur-3xl" />

        <header className="relative mb-4 sm:mb-5">
          <h2 className="text-xl sm:text-2xl font-bold font-heading text-text-primary">Active Tasks</h2>
          <p className="text-sm text-text-muted mt-1">
            Manage all work from one board and use the assistant from the chat launcher.
          </p>
        </header>
        <TaskStates
          loading={loading}
          error={pageError}
          empty={!loading && !pageError && tasks.length === 0}
          onRetry={fetchTasks}
        />

        {!loading && !pageError && tasks.length > 0 && (
          <div className="relative grid grid-cols-1 lg:grid-cols-2 gap-4 sm:gap-5">
            <section className="rounded-2xl border border-border-glass bg-slate-950/35 p-3 sm:p-4">
              <div className="flex items-center justify-between mb-3">
                <h3 className="text-base font-semibold font-heading text-text-primary inline-flex items-center gap-2">
                  <span className="inline-block w-2 h-2 rounded-full bg-amber-400" />
                  Pending
                </h3>
                <span className="text-xs px-2 py-1 rounded-full bg-warning-bg text-warning-text font-semibold">
                  {pendingTasks.length}
                </span>
              </div>
              <div className="space-y-3" aria-live="polite">
                {pendingTasks.length > 0 ? (
                  pendingTasks.map((task) => (
                    <TaskCard
                      key={task.id}
                      task={task}
                      onToggle={handleToggleTask}
                      onDelete={handleDeleteTask}
                    />
                  ))
                ) : (
                  <p className="text-sm text-text-muted">No pending tasks.</p>
                )}
              </div>
            </section>

            <section className="rounded-2xl border border-border-glass bg-slate-950/35 p-3 sm:p-4">
              <div className="flex items-center justify-between mb-3">
                <h3 className="text-base font-semibold font-heading text-text-primary inline-flex items-center gap-2">
                  <span className="inline-block w-2 h-2 rounded-full bg-emerald-400" />
                  Completed
                </h3>
                <span className="text-xs px-2 py-1 rounded-full bg-success-bg text-success-text font-semibold">
                  {completedTasks.length}
                </span>
              </div>
              <div className="space-y-3" aria-live="polite">
                {completedTasks.length > 0 ? (
                  completedTasks.map((task) => (
                    <TaskCard
                      key={task.id}
                      task={task}
                      onToggle={handleToggleTask}
                      onDelete={handleDeleteTask}
                    />
                  ))
                ) : (
                  <p className="text-sm text-text-muted">No completed tasks yet.</p>
                )}
              </div>
            </section>
          </div>
        )}
      </section>

      <button
        type="button"
        onClick={() => setShowCreateModal(true)}
        aria-label="Create task"
        className="fixed z-40 bottom-24 right-6 sm:bottom-8 sm:right-28 inline-flex items-center justify-center w-14 h-14 rounded-full border border-teal/45 bg-surface-glass-strong backdrop-blur-xl text-teal shadow-lg shadow-teal/25 hover:bg-teal hover:text-slate-950 transition-colors duration-200 cursor-pointer min-h-[44px] min-w-[44px]"
      >
        <Plus className="w-6 h-6" />
      </button>

      <CreateTaskModal
        open={showCreateModal}
        onClose={() => setShowCreateModal(false)}
        onSubmit={handleCreateTask}
        loading={submitting}
      />

      <ChatDrawer onTaskAction={handleChatTaskAction} />
    </TaskLayout>
  );
}
