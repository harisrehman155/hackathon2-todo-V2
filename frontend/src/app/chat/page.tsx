"use client";

import { ChatKit, useChatKit } from "@openai/chatkit-react";
import { MessageSquare } from "lucide-react";

import { authClient } from "@/lib/auth";

const domainKey =
  process.env.NEXT_PUBLIC_CHATKIT_API_DOMAIN_KEY ?? "domain_pk_localhost_dev";

export default function ChatPage() {
  const { control } = useChatKit({
    api: {
      url: "/api/chatkit",
      domainKey,
      fetch: async (url, init) => {
        const { data } = await authClient.token();
        const headers = new Headers(init?.headers);
        if (data?.token) {
          headers.set("Authorization", `Bearer ${data.token}`);
        }
        return fetch(url, { ...init, headers });
      },
    },
    theme: {
      colorScheme: "light",
      radius: "round",
      color: {
        accent: {
          primary: "#0f9d8a",
          level: 2,
        },
      },
    },
    header: {
      title: { enabled: true, text: "Todo AI Assistant" },
    },
    composer: {
      placeholder: "Ask me to add, update, or complete your tasks...",
    },
  });

  return (
    <main className="max-w-5xl mx-auto px-4 py-8 sm:py-12">
      <header className="mb-6 bg-white/70 backdrop-blur-lg rounded-xl border border-white/20 shadow-lg shadow-black/5 p-4 flex items-center gap-3">
        <div className="flex items-center justify-center w-10 h-10 rounded-xl bg-teal/10">
          <MessageSquare className="w-5 h-5 text-teal" />
        </div>
        <div>
          <h1 className="text-2xl font-bold font-heading text-text-primary">
            Chat Assistant
          </h1>
          <p className="text-sm text-text-muted">
            Manage your todo list with natural language.
          </p>
        </div>
      </header>

      <section className="bg-white/70 backdrop-blur-lg rounded-xl border border-white/20 shadow-lg shadow-black/5 p-3 sm:p-4 h-[70vh] min-h-[560px]">
        <ChatKit control={control} className="w-full h-full" />
      </section>
    </main>
  );
}
