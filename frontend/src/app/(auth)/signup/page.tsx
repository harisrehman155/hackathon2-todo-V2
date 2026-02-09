"use client";

import { FormEvent, useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { authClient } from "@/lib/auth";
import { UserPlus } from "lucide-react";

export default function SignUpPage() {
  const router = useRouter();
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();
    setError(null);

    if (password.length < 8) {
      setError("Password must be at least 8 characters.");
      return;
    }

    setLoading(true);

    const { error: authError } = await authClient.signUp.email({
      name,
      email,
      password,
    });

    if (authError) {
      setError(authError.message ?? "Sign up failed. Please try again.");
      setLoading(false);
      return;
    }

    router.push("/tasks");
  }

  return (
    <main className="min-h-screen flex items-center justify-center px-4 py-12">
      <div className="w-full max-w-md bg-white/70 backdrop-blur-lg rounded-2xl border border-white/20 shadow-lg shadow-black/5 p-8">
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-12 h-12 rounded-xl bg-teal/10 mb-4">
            <UserPlus className="w-6 h-6 text-teal" />
          </div>
          <h1 className="text-2xl font-bold font-heading text-text-primary">
            Create Account
          </h1>
          <p className="mt-2 text-text-muted">
            Sign up to start managing your tasks
          </p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-5">
          <div>
            <label
              htmlFor="name"
              className="block text-sm font-semibold text-text-primary mb-1.5"
            >
              Name
            </label>
            <input
              id="name"
              type="text"
              required
              value={name}
              onChange={(e) => setName(e.target.value)}
              placeholder="Your name"
              className="w-full px-4 py-3 rounded-xl bg-white/80 border border-border-subtle focus:border-teal focus:ring-2 focus:ring-teal/20 outline-none transition-colors duration-200 text-text-primary placeholder:text-text-muted/50"
            />
          </div>

          <div>
            <label
              htmlFor="email"
              className="block text-sm font-semibold text-text-primary mb-1.5"
            >
              Email
            </label>
            <input
              id="email"
              type="email"
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="you@example.com"
              className="w-full px-4 py-3 rounded-xl bg-white/80 border border-border-subtle focus:border-teal focus:ring-2 focus:ring-teal/20 outline-none transition-colors duration-200 text-text-primary placeholder:text-text-muted/50"
            />
          </div>

          <div>
            <label
              htmlFor="password"
              className="block text-sm font-semibold text-text-primary mb-1.5"
            >
              Password
            </label>
            <input
              id="password"
              type="password"
              required
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="At least 8 characters"
              className="w-full px-4 py-3 rounded-xl bg-white/80 border border-border-subtle focus:border-teal focus:ring-2 focus:ring-teal/20 outline-none transition-colors duration-200 text-text-primary placeholder:text-text-muted/50"
            />
          </div>

          {error && (
            <p className="text-sm text-danger font-medium" role="alert">
              {error}
            </p>
          )}

          <button
            type="submit"
            disabled={loading}
            className="w-full py-3 px-4 rounded-xl bg-teal text-white font-bold text-base cursor-pointer hover:bg-teal-hover focus:ring-2 focus:ring-teal/20 focus:outline-none transition-colors duration-200 disabled:opacity-50 disabled:cursor-not-allowed min-h-[44px]"
          >
            {loading ? "Creating account..." : "Sign Up"}
          </button>
        </form>

        <p className="mt-6 text-center text-sm text-text-muted">
          Already have an account?{" "}
          <Link
            href="/signin"
            className="text-teal font-semibold hover:text-teal-hover transition-colors duration-200"
          >
            Sign in
          </Link>
        </p>
      </div>
    </main>
  );
}
