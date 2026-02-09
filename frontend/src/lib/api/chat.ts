import { authClient } from "@/lib/auth";

const baseUrl = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";

export type ChatRequest = {
  message: string;
  conversation_id?: string;
};

export type ChatResponse = {
  response: string;
  conversation_id: string;
};

async function getToken(): Promise<string> {
  const { data } = await authClient.token();
  if (!data?.token) {
    throw new Error("Unable to get auth token. Please sign in again.");
  }
  return data.token;
}

export async function sendChatMessage(payload: ChatRequest): Promise<ChatResponse> {
  const token = await getToken();
  const response = await fetch(`${baseUrl}/api/chat`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify(payload),
  });

  const body = await response.json().catch(() => null);
  if (!response.ok) {
    const message = body?.detail?.error ?? body?.detail ?? `API request failed: ${response.status}`;
    throw new Error(message);
  }

  return body as ChatResponse;
}
