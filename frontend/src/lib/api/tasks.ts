import { authClient } from "@/lib/auth";
import { forceLogoutForExpiredSession, isAuthenticationFailure } from "@/lib/api/session";

export type TaskPayload = {
  title: string;
  description?: string;
};

export type Task = {
  id: number;
  title: string;
  description: string | null;
  is_completed: boolean;
  created_at: string;
  updated_at: string;
};

const baseUrl = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";

async function getToken(): Promise<string> {
  for (let attempt = 0; attempt < 3; attempt++) {
    try {
      const { data } = await authClient.token();
      if (data?.token) return data.token;
    } catch {
      // Neon cold start can cause ETIMEDOUT — retry
    }
    if (attempt < 2) await new Promise((r) => setTimeout(r, 1000));
  }
  await forceLogoutForExpiredSession();
  throw new Error("Session expired. Redirecting to sign in.");
}

async function request<T = unknown>(
  path: string,
  init?: RequestInit
): Promise<T | null> {
  const token = await getToken();
  const headers: Record<string, string> = {
    "Content-Type": "application/json",
    Authorization: `Bearer ${token}`,
    ...(init?.headers as Record<string, string> | undefined),
  };

  const response = await fetch(`${baseUrl}${path}`, {
    ...init,
    headers,
  });

  if (!response.ok) {
    const body = await response.json().catch(() => null);
    if (isAuthenticationFailure(response.status, body)) {
      await forceLogoutForExpiredSession();
      throw new Error("Session expired. Redirecting to sign in.");
    }
    const message =
      body?.detail?.error ?? body?.detail ?? `API request failed: ${response.status}`;
    throw new Error(message);
  }

  return response.status === 204 ? null : response.json();
}

export async function listTasks(): Promise<Task[]> {
  return (await request<Task[]>("/tasks")) ?? [];
}

export async function createTask(payload: TaskPayload): Promise<Task> {
  const result = await request<Task>("/tasks", {
    method: "POST",
    body: JSON.stringify(payload),
  });
  return result!;
}

export async function updateTask(
  taskId: number,
  payload: Partial<TaskPayload>
): Promise<Task> {
  const result = await request<Task>(`/tasks/${taskId}`, {
    method: "PATCH",
    body: JSON.stringify(payload),
  });
  return result!;
}

export async function toggleTask(taskId: number): Promise<Task> {
  const result = await request<Task>(`/tasks/${taskId}/toggle-complete`, {
    method: "POST",
  });
  return result!;
}

export async function deleteTask(taskId: number): Promise<void> {
  await request(`/tasks/${taskId}`, { method: "DELETE" });
}
