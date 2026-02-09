import { betterAuth } from "better-auth";
import { jwt } from "better-auth/plugins";
import { nextCookies } from "better-auth/next-js";
import { Pool } from "pg";
import { SignJWT } from "jose";

const jwtSecret = new TextEncoder().encode(
  process.env.BETTER_AUTH_SECRET ?? "dev-secret"
);

export const auth = betterAuth({
  database: new Pool({
    connectionString: process.env.DATABASE_URL,
    ssl: { rejectUnauthorized: false },
    connectionTimeoutMillis: 10000,
    idleTimeoutMillis: 30000,
    max: 5,
  }),
  basePath: "/api/auth",
  emailAndPassword: {
    enabled: true,
  },
  plugins: [
    nextCookies(),
    jwt({
      jwt: {
        issuer: "better-auth",
        audience: "hackathon2",
        expirationTime: "1h",
        definePayload: ({ user }) => ({
          sub: user.id,
          email: user.email,
          name: user.name,
        }),
        sign: async (payload) => {
          return await new SignJWT(payload)
            .setProtectedHeader({ alg: "HS256", typ: "JWT" })
            .setIssuedAt()
            .setIssuer("better-auth")
            .setAudience("hackathon2")
            .setExpirationTime("1h")
            .sign(jwtSecret);
        },
      },
      jwks: {
        remoteUrl: process.env.BETTER_AUTH_URL
          ? `${process.env.BETTER_AUTH_URL}/api/auth/jwks`
          : "http://localhost:3000/api/auth/jwks",
        keyPairConfig: {
          alg: "EdDSA",
          crv: "Ed25519",
        },
      },
    }),
  ],
});
