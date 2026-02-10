"use client";

import { ReactNode } from "react";
import { useRouter } from "next/navigation";
import { authClient } from "@/lib/auth";
import { CheckSquare, LogOut } from "lucide-react";

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
    <main className="min-h-screen">
      <div className="max-w-7xl mx-auto px-4 py-6 sm:px-6 sm:py-8 lg:px-8">
        <header className="flex items-center justify-between mb-6 gap-3">
          <div className="flex items-center gap-3">
            <div className="flex items-center justify-center w-10 h-10 rounded-xl bg-teal/20 border border-teal/40">
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
            <button
              type="button"
              onClick={handleSignOut}
              className="inline-flex items-center gap-2 px-4 py-2.5 rounded-xl bg-surface-glass backdrop-blur-lg border border-border-subtle text-sm font-semibold text-text-muted hover:text-danger hover:border-danger/50 cursor-pointer transition-colors duration-200 min-h-[44px]"
            >
              <LogOut className="w-4 h-4" />
              Sign Out
            </button>
          </div>
        </header>

        {children}
      </div>
    </main>
  );
}
