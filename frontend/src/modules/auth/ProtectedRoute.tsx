import React from "react";
import { Navigate, Outlet, useLocation } from "react-router-dom";
import { useAuth } from "./useAuth";
import { Role } from "@/types";
import { Card, Button } from "@/components/common";
import { Spinner } from "@/components/feedback/Spinner";
import { ShieldAlert } from "lucide-react";

export interface ProtectedRouteProps {
  allowedRoles?: Role[];
  redirectTo?: string;
}

export const ProtectedRoute: React.FC<ProtectedRouteProps> = ({
  allowedRoles,
  redirectTo = "/login",
}) => {
  const { user, isAuthenticated, loading } = useAuth();
  const location = useLocation();

  if (loading) {
    return (
      <div className="flex min-h-[50vh] w-full items-center justify-center">
        <div className="flex flex-col items-center gap-3">
          <Spinner size="lg" />
          <span className="text-xs text-slate-500 dark:text-slate-400 font-medium">
            Verifying secure session credentials...
          </span>
        </div>
      </div>
    );
  }

  if (!isAuthenticated || !user) {
    return <Navigate to={redirectTo} replace state={{ from: location }} />;
  }

  if (allowedRoles && allowedRoles.length > 0 && !allowedRoles.includes(user.role)) {
    return (
      <div className="flex min-h-[60vh] items-center justify-center animate-fade-in p-4">
        <Card className="max-w-md text-center flex flex-col items-center gap-4 p-8">
          <div className="h-14 w-14 rounded-2xl bg-danger-100 text-danger-600 flex items-center justify-center shadow-inner">
            <ShieldAlert className="h-7 w-7" />
          </div>
          <h2 className="text-xl font-bold text-slate-800 dark:text-slate-100">
            403 - Permission Denied
          </h2>
          <p className="text-xs text-slate-600 dark:text-slate-400 leading-relaxed">
            Your current role (<span className="font-semibold uppercase text-primary-600">{user.role}</span>) does not have sufficient access privileges to view this domain boundary.
          </p>
          <div className="w-full mt-2">
            <Button
              variant="outline"
              className="w-full"
              onClick={() => window.history.back()}
            >
              Go Back
            </Button>
          </div>
        </Card>
      </div>
    );
  }

  return <Outlet />;
};
