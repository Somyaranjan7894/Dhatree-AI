/**
 * Global application constants.
 */
export const APP_NAME = "Dhatree AI";
export const APP_TAGLINE = "AI-Powered Digital Agriculture Platform";
export const DEFAULT_PAGE_SIZE = 10;
export const REQUEST_TIMEOUT_MS = 30000;

export const LOCAL_STORAGE_KEYS = {
  AUTH_TOKEN: "dhatree_access_token",
  REFRESH_TOKEN: "dhatree_refresh_token",
  USER_PREFERENCES: "dhatree_user_prefs",
} as const;
