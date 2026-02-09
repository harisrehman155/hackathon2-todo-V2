"use client";

import { ReactNode } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { authClient } from "@/lib/auth";
import { LogOut, CheckSquare, MessageSquare } from "lucide-react";

type TaskLayoutProps = {
  children: ReactNode;
};

export function TaskLayout({ children }: TaskLayoutProps) {
  const router = useRouter();
  const { data: session } = authClient.useSession();

  async function handleSignOut() {
    await authClient.signOut({
      fetchOptions: {
        onSuccess: () => router.push("/signin"),
      },
    });
  }

  return (
    <main className="max-w-5xl mx-auto px-4 py-8 sm:py-12">
      <header className="flex items-center justify-between mb-8 gap-3">
        <div className="flex items-center gap-3">
          <div className="flex items-center justify-center w-10 h-10 rounded-xl bg-teal/10">
            <CheckSquare className="w-5 h-5 text-teal" />
          </div>
          <div>
            <h1 className="text-2xl font-bold font-heading text-text-primary">
              Task Board
            </h1>
            {session?.user && (
              <p className="text-sm text-text-muted">{session.user.email}</p>
            )}
          </div>
        </div>

        <div className="flex items-center gap-2">
          <Link
            href="/chat"
            className="inline-flex items-center gap-2 px-4 py-2.5 rounded-xl bg-white/70 backdrop-blur-lg border border-border-subtle text-sm font-semibold text-text-muted hover:text-teal hover:border-teal/30 cursor-pointer transition-colors duration-200 min-h-[44px]"
          >
            <MessageSquare className="w-4 h-4" />
            AI Chat
          </Link>
          <button
            onClick={handleSignOut}
            className="inline-flex items-center gap-2 px-4 py-2.5 rounded-xl bg-white/70 backdrop-blur-lg border border-border-subtle text-sm font-semibold text-text-muted hover:text-danger hover:border-danger/30 cursor-pointer transition-colors duration-200 min-h-[44px]"
          >
            <LogOut className="w-4 h-4" />
            Sign Out
          </button>
        </div>
      </header>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">{children}</div>
    </main>
  );
}
