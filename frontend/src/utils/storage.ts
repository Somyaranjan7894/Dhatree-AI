import { TokenPair } from "../types";

const ACCESS_TOKEN_KEY = "dhatree_access_token";
const REFRESH_TOKEN_KEY = "dhatree_refresh_token";

/**
 * TokenStorage manages JWT access and refresh tokens securely with browser storage fallback.
 */
export const TokenStorage = {
  getAccessToken(): string | null {
    try {
      return localStorage.getItem(ACCESS_TOKEN_KEY);
    } catch {
      return null;
    }
  },

  getRefreshToken(): string | null {
    try {
      return localStorage.getItem(REFRESH_TOKEN_KEY);
    } catch {
      return null;
    }
  },

  setTokens(tokens: TokenPair): void {
    try {
      localStorage.setItem(ACCESS_TOKEN_KEY, tokens.access);
      localStorage.setItem(REFRESH_TOKEN_KEY, tokens.refresh);
      window.dispatchEvent(new Event("dhatree:tokens_updated"));
    } catch (e) {
      console.error("Failed to persist tokens to storage:", e);
    }
  },

  clearTokens(): void {
    try {
      localStorage.removeItem(ACCESS_TOKEN_KEY);
      localStorage.removeItem(REFRESH_TOKEN_KEY);
      window.dispatchEvent(new Event("dhatree:tokens_cleared"));
    } catch (e) {
      console.error("Failed to clear tokens from storage:", e);
    }
  },
};
