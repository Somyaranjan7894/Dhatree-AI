/**
 * Standardized API response envelopes and error definitions matching Dhatree AI backend contract.
 */
export interface ApiResponse<T = unknown> {
  success: boolean;
  message: string;
  data: T;
  errors?: Record<string, string[]>;
  code?: string;
}

export interface PaginatedData<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

export type PaginatedResponse<T> = ApiResponse<PaginatedData<T>>;

export interface ApiError {
  success: false;
  message: string;
  errors?: Record<string, string[]>;
  code?: string;
  status?: number;
}

export type ApiErrorResponse = ApiError;

