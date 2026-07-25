/**
 * Axios HTTP client configuration with request/response interceptors,
 * JWT authentication injection, and standardized error unwrapping.
 */
import axios, { AxiosError, InternalAxiosRequestConfig } from "axios";
import { env } from "@/config/env";
import { LOCAL_STORAGE_KEYS, REQUEST_TIMEOUT_MS } from "@/config/constants";
import { TokenStorage } from "@/utils/storage";
import { ApiErrorResponse } from "@/types";

export const apiClient = axios.create({
  baseURL: env.VITE_API_BASE_URL,
  timeout: REQUEST_TIMEOUT_MS,
  headers: {
    "Content-Type": "application/json",
  },
});

// Request Interceptor: Attach JWT Authorization Header
apiClient.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    const token = localStorage.getItem(LOCAL_STORAGE_KEYS.AUTH_TOKEN);
    if (token && config.headers) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error: AxiosError) => Promise.reject(error)
);

// Response Interceptor: Unwarp standardized Django Rest Framework API responses and handle errors
apiClient.interceptors.response.use(
  (response) => response.data,
  (error: AxiosError<ApiErrorResponse>) => {
    if (error.response?.status === 401) {
      // Clear expired credentials
      TokenStorage.clearTokens();
    }
    const apiError = error.response?.data || {
      status: "error",
      code: "NETWORK_ERROR",
      message: error.message || "A network communication error occurred.",
      details: null,
    };
    return Promise.reject(apiError);
  }
);
