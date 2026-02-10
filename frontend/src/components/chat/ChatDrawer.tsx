"use client";

import { FormEvent, useEffect, useMemo, useRef, useState } from "react";
import { Bot, Loader2, MessageCircle, Send, X } from "lucide-react";
import { toast } from "react-toastify";
import { authClient } from "@/lib/auth";
import { sendChatMessage } from "@/lib/api/chat";

type ChatMessage = {
  id: string;
  role: "user" | "assistant";
  content: string;
};

type ChatDrawerProps = {
  onTaskAction?: (toolNames: string[]) => void | Promise<void>;
};

export function ChatDrawer({ onTaskAction }: ChatDrawerProps) {
  const { data: session } = authClient.useSession();
  const [open, setOpen] = useState(false);
  const [input, setInput] = useState("");
  const [sending, setSending] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [conversationId, setConversationId] = useState<string | undefined>();
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      id: "assistant-welcome",
      role: "assistant",
      content: "Ask me to add, complete, update, or delete your tasks.",
    },
  ]);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const storageKey = useMemo(() => {
    const userKey = session?.user?.id ?? session?.user?.email ?? "anonymous";
    return `hackathon2:chat:conversation:${userKey}`;
  }, [session?.user?.id, session?.user?.email]);

  useEffect(() => {
    if (typeof window === "undefined") return;
    const storedId = window.localStorage.getItem(storageKey);
    if (storedId) setConversationId(storedId);
  }, [storageKey]);

  useEffect(() => {
    if (typeof window === "undefined") return;
    if (!conversationId) {
      window.localStorage.removeItem(storageKey);
      return;
    }
    window.localStorage.setItem(storageKey, conversationId);
  }, [conversationId, storageKey]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, open]);

  async function handleSubmit(event: FormEvent) {
    event.preventDefault();
    const message = input.trim();
    if (!message || sending) return;

    setError(null);
    setSending(true);
    setInput("");

    const userMessage: ChatMessage = {
      id: `user-${Date.now()}`,
      role: "user",
      content: message,
    };
    setMessages((prev) => [...prev, userMessage]);

    try {
      const result = await sendChatMessage({
        message,
        conversation_id: conversationId,
      });

      setConversationId(result.conversation_id);
      setMessages((prev) => [
        ...prev,
        {
          id: `assistant-${Date.now()}`,
          role: "assistant",
          content: result.response,
        },
      ]);

      const toolNames = (result.tool_names ?? []).filter((name) => name !== "unknown_tool");
      await onTaskAction?.(toolNames);
      if (toolNames.length > 0) {
        toast.success(`AI updated tasks: ${toolNames.join(", ")}`);
      } else {
        toast.info("Assistant replied. Task board refreshed.");
      }
    } catch (submitError) {
      const message =
        submitError instanceof Error ? submitError.message : "Unable to send chat message";
      setError(message);
      toast.error(message);
    } finally {
      setSending(false);
    }
  }

  return (
    <>
      <button
        type="button"
        onClick={() => setOpen(true)}
        aria-label="Open AI assistant chat"
        className="fixed z-40 bottom-6 right-6 sm:bottom-8 sm:right-8 inline-flex items-center justify-center w-14 h-14 rounded-full border border-cyan-200/40 bg-surface-glass-strong backdrop-blur-xl text-teal shadow-lg shadow-cyan-500/30 hover:text-white hover:bg-cyan-500/70 transition-colors duration-200 cursor-pointer min-h-[44px] min-w-[44px]"
      >
        <MessageCircle className="w-6 h-6" />
      </button>

      {open && (
        <div className="fixed inset-0 z-50">
          <button
            type="button"
            aria-label="Close chat drawer"
            className="absolute inset-0 bg-black/60 backdrop-blur-sm cursor-pointer"
            onClick={() => setOpen(false)}
          />

          <aside className="absolute right-0 top-0 h-full w-full sm:max-w-md border-l border-border-glass bg-surface-glass-strong backdrop-blur-xl shadow-2xl shadow-black/40 flex flex-col">
            <header className="flex items-center justify-between p-4 border-b border-border-subtle">
              <div className="flex items-center gap-2">
                <div className="w-9 h-9 rounded-xl bg-teal/20 border border-teal/40 inline-flex items-center justify-center">
                  <Bot className="w-5 h-5 text-teal" />
                </div>
                <div>
                  <h2 className="text-base font-bold font-heading text-text-primary">Task Assistant</h2>
                  <p className="text-xs text-text-muted">Same-page AI chat</p>
                </div>
              </div>
              <button
                type="button"
                aria-label="Close chat"
                onClick={() => setOpen(false)}
                className="inline-flex items-center justify-center w-10 h-10 rounded-xl border border-border-subtle text-text-muted hover:text-text-primary hover:border-teal/50 transition-colors duration-200 cursor-pointer min-h-[44px] min-w-[44px]"
              >
                <X className="w-4 h-4" />
              </button>
            </header>

            <div className="flex-1 overflow-y-auto p-4 space-y-3" aria-live="polite">
              {messages.map((message) => (
                <div
                  key={message.id}
                  className={`max-w-[88%] rounded-2xl px-3.5 py-2.5 text-sm leading-relaxed border ${
                    message.role === "user"
                      ? "ml-auto bg-chat-user-bg border-teal/35 text-cyan-100"
                      : "mr-auto bg-chat-assistant-bg border-slate-600/45 text-slate-100"
                  }`}
                >
                  {message.content}
                </div>
              ))}

              {sending && (
                <div className="mr-auto inline-flex items-center gap-2 rounded-xl border border-slate-600/50 bg-chat-assistant-bg px-3 py-2 text-sm text-text-muted">
                  <Loader2 className="w-4 h-4 animate-spin" />
                  Thinking...
                </div>
              )}
              <div ref={messagesEndRef} />
            </div>

            <footer className="p-4 border-t border-border-subtle">
              {error && (
                <p className="text-sm text-danger mb-2" role="alert">
                  {error}
                </p>
              )}
              <form onSubmit={handleSubmit} className="flex items-end gap-2">
                <label htmlFor="chat-input" className="sr-only">
                  Chat message
                </label>
                <textarea
                  id="chat-input"
                  rows={4}
                  value={input}
                  onChange={(event) => setInput(event.target.value)}
                  placeholder="Ask me to manage your tasks..."
                  className="flex-1 px-3 py-2.5 min-h-[110px] rounded-xl bg-slate-950/60 border border-border-subtle text-text-primary placeholder:text-slate-400 focus:border-teal outline-none resize-y"
                />
                <button
                  type="submit"
                  disabled={sending || !input.trim()}
                  className="inline-flex items-center justify-center w-11 h-11 rounded-xl bg-teal text-slate-950 font-bold hover:bg-teal-hover transition-colors duration-200 cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed min-h-[44px] min-w-[44px]"
                  aria-label="Send message"
                >
                  <Send className="w-4 h-4" />
                </button>
              </form>
            </footer>
          </aside>
        </div>
      )}
    </>
  );
}
