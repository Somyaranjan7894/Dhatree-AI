import { apiClient } from "./client";
import { ENDPOINTS } from "./endpoints";
import {
  ApiResponse,
  AuthResponseData,
  LoginPayload,
  RegisterPayload,
  TokenPair,
  User,
} from "@/types";

/**
 * Service class encapsulating authentication and user profile API operations.
 */
export class AuthService {
  /**
   * Authenticate user with credentials (email/username + password).
   */
  static async login(payload: LoginPayload): Promise<ApiResponse<AuthResponseData>> {
    return apiClient.post(ENDPOINTS.AUTH.LOGIN, payload);
  }

  /**
   * Register a new user account and receive initial session tokens.
   */
  static async register(payload: RegisterPayload): Promise<ApiResponse<AuthResponseData>> {
    return apiClient.post(ENDPOINTS.AUTH.REGISTER, payload);
  }

  /**
   * Blacklist refresh token and terminate session on server.
   */
  static async logout(refreshToken: string): Promise<ApiResponse<{ message: string }>> {
    return apiClient.post(ENDPOINTS.AUTH.LOGOUT, { refresh: refreshToken });
  }

  /**
   * Rotate access and refresh tokens using valid refresh token.
   */
  static async refreshTokens(refreshToken: string): Promise<ApiResponse<TokenPair>> {
    return apiClient.post(ENDPOINTS.AUTH.REFRESH, { refresh: refreshToken });
  }

  /**
   * Retrieve current authenticated user profile.
   */
  static async getCurrentUser(): Promise<ApiResponse<User>> {
    return apiClient.get(ENDPOINTS.USERS.PROFILE);
  }
}
