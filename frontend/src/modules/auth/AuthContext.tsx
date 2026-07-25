/* eslint-disable react-refresh/only-export-components */
import React, { createContext, useCallback, useEffect, useMemo, useState } from "react";
import { AuthService } from "@/api/auth.service";
import { TokenStorage } from "@/utils/storage";
import { LoginPayload, RegisterPayload, User } from "@/types";

export interface AuthContextType {
  user: User | null;
  isAuthenticated: boolean;
  loading: boolean;
  error: string | null;
  login: (payload: LoginPayload) => Promise<void>;
  register: (payload: RegisterPayload) => Promise<void>;
  logout: () => Promise<void>;
  updateUser: (updatedUser: Partial<User>) => void;
  clearError: () => void;
}

export const AuthContext = createContext<AuthContextType | undefined>(undefined);

export interface AuthProviderProps {
  children: React.ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const clearError = useCallback(() => {
    setError(null);
  }, []);

  const updateUser = useCallback((updatedUser: Partial<User>) => {
    setUser((prev) => (prev ? { ...prev, ...updatedUser } : null));
  }, []);

  // Initialize session on mount
  useEffect(() => {
    let isMounted = true;

    const initializeAuth = async () => {
      const accessToken = TokenStorage.getAccessToken();
      const refreshToken = TokenStorage.getRefreshToken();

      if (!accessToken && !refreshToken) {
        if (isMounted) setLoading(false);
        return;
      }

      try {
        const response = await AuthService.getCurrentUser();
        if (isMounted && response.data) {
          setUser(response.data);
        }
      } catch {
        // If getting profile with access token fails, try refreshing tokens
        if (refreshToken) {
          try {
            const refreshRes = await AuthService.refreshTokens(refreshToken);
            if (refreshRes.data) {
              TokenStorage.setTokens(refreshRes.data);
              const retryRes = await AuthService.getCurrentUser();
              if (isMounted && retryRes.data) {
                setUser(retryRes.data);
              }
            }
          } catch {
            if (isMounted) {
              TokenStorage.clearTokens();
              setUser(null);
            }
          }
        } else {
          if (isMounted) {
            TokenStorage.clearTokens();
            setUser(null);
          }
        }
      } finally {
        if (isMounted) setLoading(false);
      }
    };

    initializeAuth();

    const handleTokensCleared = () => {
      if (isMounted) setUser(null);
    };

    window.addEventListener("dhatree:tokens_cleared", handleTokensCleared);

    return () => {
      isMounted = false;
      window.removeEventListener("dhatree:tokens_cleared", handleTokensCleared);
    };
  }, []);

  const login = useCallback(async (payload: LoginPayload) => {
    setLoading(true);
    setError(null);
    try {
      const response = await AuthService.login(payload);
      const { user: userData, tokens } = response.data;
      TokenStorage.setTokens(tokens);
      setUser(userData);
    } catch (err: unknown) {
      const errObj = err as { message?: string; errors?: { detail?: string[] } };
      const errorMessage =
        errObj?.message || errObj?.errors?.detail?.[0] || "Authentication failed. Please check your credentials.";
      setError(errorMessage);
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  const register = useCallback(async (payload: RegisterPayload) => {
    setLoading(true);
    setError(null);
    try {
      const response = await AuthService.register(payload);
      const { user: userData, tokens } = response.data;
      TokenStorage.setTokens(tokens);
      setUser(userData);
    } catch (err: unknown) {
      const errObj = err as { message?: string; errors?: { detail?: string[] } };
      const errorMessage =
        errObj?.message || errObj?.errors?.detail?.[0] || "Registration failed. Please check your input details.";
      setError(errorMessage);
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  const logout = useCallback(async () => {
    const refreshToken = TokenStorage.getRefreshToken();
    try {
      if (refreshToken) {
        await AuthService.logout(refreshToken);
      }
    } catch (e) {
      console.error("Server-side logout failed:", e);
    } finally {
      TokenStorage.clearTokens();
      setUser(null);
    }
  }, []);

  const value = useMemo(
    () => ({
      user,
      isAuthenticated: !!user,
      loading,
      error,
      login,
      register,
      logout,
      updateUser,
      clearError,
    }),
    [user, loading, error, login, register, logout, updateUser, clearError]
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};
