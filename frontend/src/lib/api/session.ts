import { authClient } from "@/lib/auth";

let redirectInProgress = false;

const AUTH_ERROR_CODES = new Set([
  "not_authenticated",
  "invalid_token",
  "token_expired",
  "auth_error",
]);

function clearChatConversationCache() {
  if (typeof window === "undefined") return;
  const keys = Object.keys(window.localStorage);
  for (const key of keys) {
    if (key.startsWith("hackathon2:chat:conversation:")) {
      window.localStorage.removeItem(key);
    }
  }
}

export function isAuthenticationFailure(status: number, body: unknown): boolean {
  if (status === 401) return true;
  if (status !== 403 || typeof body !== "object" || body === null) return false;

  const code =
    (body as { detail?: { code?: string } }).detail?.code ??
    (body as { code?: string }).code;
  return typeof code === "string" && AUTH_ERROR_CODES.has(code);
}

export async function forceLogoutForExpiredSession(): Promise<void> {
  if (redirectInProgress) return;
  redirectInProgress = true;

  clearChatConversationCache();

  try {
    await authClient.signOut();
  } catch {
    // Best effort sign-out; redirect is the hard guarantee.
  }

  if (typeof window !== "undefined") {
    const target = `/signin?reason=session_expired&callbackUrl=${encodeURIComponent("/tasks")}`;
    window.location.replace(target);
  }
}
