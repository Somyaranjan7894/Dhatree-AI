/**
 * Core User identity, roles, and authentication interfaces matching the Django Phase 2 backend.
 */
export type Role = "farmer" | "agronomist" | "researcher" | "admin";

export type AccountStatus = "active" | "suspended" | "pending_verification";

export interface User {
  id: string;
  email: string;
  username: string;
  full_name: string;
  phone_number?: string | null;
  role: Role;
  account_status: AccountStatus;
  is_verified: boolean;
  created_at?: string;
  updated_at?: string;
}

export interface TokenPair {
  access: string;
  refresh: string;
}

export interface AuthResponseData {
  user: User;
  tokens: TokenPair;
}

export interface LoginPayload {
  identifier: string;
  password: string;
}

export interface RegisterPayload {
  email: string;
  username: string;
  password: string;
  password_confirm: string;
  full_name?: string;
  phone_number?: string;
  role?: Role;
}

export interface UpdateProfilePayload {
  full_name?: string;
  phone_number?: string;
}

export interface ChangePasswordPayload {
  old_password: string;
  new_password: string;
  new_password_confirm: string;
}
