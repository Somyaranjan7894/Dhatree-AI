/**
 * Environment configuration reader and validator using Zod schemas.
 * Ensures type-safe access to Vite environment variables.
 */
import { z } from "zod";

const envSchema = z.object({
  VITE_API_BASE_URL: z
    .string()
    .url()
    .default("http://localhost:8000/api/v1"),
  VITE_APP_ENV: z
    .enum(["development", "production", "test"])
    .default("development"),
  VITE_ENABLE_MOCK_API: z
    .string()
    .transform((val) => val === "true")
    .default("false"),
});

const parseEnv = () => {
  const result = envSchema.safeParse((import.meta as unknown as { env: Record<string, unknown> }).env);
  if (!result.success) {
    console.error("Invalid environment variables:", result.error.format());
    // Fallback to default safe schema values during SSR or test harness build
    return envSchema.parse({});
  }
  return result.data;
};

export const env = parseEnv();
