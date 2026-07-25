/**
 * Centralized API endpoints registry.
 * Ensures strict decoupling between UI components and backend route URLs.
 */
export const ENDPOINTS = {
  AUTH: {
    LOGIN: "/auth/login/",
    REGISTER: "/auth/register/",
    LOGOUT: "/auth/logout/",
    REFRESH: "/auth/refresh/",
  },
  USERS: {
    PROFILE: "/users/me/",
  },
  FARMS: {
    LIST: "/farms/",
    DETAIL: (id: string) => `/farms/${id}/`,
    CROPS: (id: string) => `/farms/${id}/crops/`,
    IMAGES: (id: string) => `/farms/${id}/images/`,
    HISTORY: (id: string) => `/farms/${id}/history/`,
    SOIL_SAMPLES: (id: string) => `/farms/${id}/soil-samples/`,
    WEATHER_SNAPSHOTS: (id: string) => `/farms/${id}/weather-snapshots/`,
  },
  CROPS: {
    LIST: "/crops/",
    DETAIL: (id: string) => `/crops/${id}/`,
  },
  SOIL_ANALYSIS: {
    LIST: "/soil-samples/",
    DETAIL: (id: string) => `/soil-samples/${id}/`,
  },
  WEATHER: {
    LIST: "/weather-snapshots/",
    DETAIL: (id: string) => `/weather-snapshots/${id}/`,
  },
  NOTIFICATIONS: {
    LIST: "/notifications/",
    DETAIL: (id: string) => `/notifications/${id}/`,
    MARK_READ: (id: string) => `/notifications/${id}/mark_read/`,
  },
  AI: {
    CROP_RECOMMENDATION: "/crop-recommendation/predict/",
    DISEASE_DETECTION: "/disease-detection/analyze/",
    FERTILIZER_RECOMMENDATION: "/fertilizer-recommendation/predict/",
  },
} as const;
