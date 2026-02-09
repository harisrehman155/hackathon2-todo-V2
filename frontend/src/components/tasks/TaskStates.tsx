"use client";

import { AlertCircle, Inbox, Loader2 } from "lucide-react";

type TaskStatesProps = {
  loading?: boolean;
  error?: string | null;
  empty?: boolean;
  onRetry?: () => void;
};

export function TaskStates({ loading, error, empty, onRetry }: TaskStatesProps) {
  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center py-12 text-text-muted">
        <Loader2 className="w-8 h-8 animate-spin text-teal mb-3" />
        <p className="text-sm font-medium">Loading tasks...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex flex-col items-center justify-center py-12 text-center">
        <AlertCircle className="w-8 h-8 text-danger mb-3" />
        <p className="text-sm font-medium text-danger mb-3">{error}</p>
        {onRetry && (
          <button
            onClick={onRetry}
            className="px-4 py-2 rounded-xl bg-teal text-white text-sm font-semibold cursor-pointer hover:bg-teal-hover transition-colors duration-200 min-h-[44px]"
          >
            Try Again
          </button>
        )}
      </div>
    );
  }

  if (empty) {
    return (
      <div className="flex flex-col items-center justify-center py-12 text-text-muted">
        <Inbox className="w-10 h-10 mb-3 opacity-50" />
        <p className="text-sm font-medium">No tasks yet</p>
        <p className="text-xs mt-1">Create your first task to get started.</p>
      </div>
    );
  }

  return null;
}
