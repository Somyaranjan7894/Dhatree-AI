import { useContext } from "react";
import { AuthContext, AuthContextType } from "./AuthContext";

/**
 * Hook to access current authentication state and actions.
 * Must be used inside an `<AuthProvider>` component hierarchy.
 */
export const useAuth = (): AuthContextType => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
};
