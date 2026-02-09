import { randomUUID } from "crypto";
import { NextRequest, NextResponse } from "next/server";

type ChatMessage = {
  role?: string;
  content?: string;
  metadata?: Record<string, unknown>;
};

const baseUrl = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";
const conversationByThread = new Map<string, string>();

function extractConversationId(payload: any, lastUserMessage?: ChatMessage): string | undefined {
  const fromPayload =
    payload?.conversation_id ??
    payload?.conversationId ??
    payload?.metadata?.conversation_id ??
    payload?.metadata?.conversationId;
  if (typeof fromPayload === "string" && fromPayload) return fromPayload;

  const fromMessage =
    lastUserMessage?.metadata?.conversation_id ??
    lastUserMessage?.metadata?.conversationId;
  if (typeof fromMessage === "string" && fromMessage) return fromMessage;

  const threadId = payload?.thread_id ?? payload?.threadId ?? payload?.thread?.id;
  if (typeof threadId === "string" && threadId) {
    return conversationByThread.get(threadId);
  }
  return undefined;
}

export async function POST(request: NextRequest) {
  try {
    const payload = await request.json();
    const messages = (payload?.messages ?? []) as ChatMessage[];
    const lastUser = [...messages].reverse().find((m) => m.role === "user");
    const userContent =
      typeof lastUser?.content === "string" ? lastUser.content.trim() : "";

    if (!userContent) {
      return NextResponse.json(
        { error: "No user message found in request" },
        { status: 400 },
      );
    }

    const conversation_id = extractConversationId(payload, lastUser);
    const authHeader = request.headers.get("authorization");

    const upstream = await fetch(`${baseUrl}/api/chat`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        ...(authHeader ? { Authorization: authHeader } : {}),
      },
      body: JSON.stringify({ message: userContent, conversation_id }),
    });

    const upstreamBody = await upstream.json().catch(() => null);
    if (!upstream.ok) {
      const message =
        upstreamBody?.detail?.error ??
        upstreamBody?.error ??
        "Chat backend request failed";
      return NextResponse.json({ error: message }, { status: upstream.status });
    }

    const threadId = payload?.thread_id ?? payload?.threadId ?? payload?.thread?.id;
    if (typeof threadId === "string" && upstreamBody?.conversation_id) {
      conversationByThread.set(threadId, upstreamBody.conversation_id);
    }

    return NextResponse.json({
      id: `chatcmpl-${randomUUID()}`,
      object: "chat.completion",
      choices: [
        {
          index: 0,
          message: {
            role: "assistant",
            content: upstreamBody?.response ?? "",
          },
          finish_reason: "stop",
        },
      ],
      conversation_id: upstreamBody?.conversation_id,
    });
  } catch {
    return NextResponse.json(
      { error: "Unable to process chat request" },
      { status: 500 },
    );
  }
}
