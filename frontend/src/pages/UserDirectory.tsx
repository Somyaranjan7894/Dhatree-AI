import React from "react";
import { Card, Button } from "@/components/common";
import { EmptyState } from "@/components/feedback/EmptyState";
import { Users, UserPlus } from "lucide-react";

export const UserDirectory: React.FC = () => {
  return (
    <div className="flex flex-col gap-6 animate-fade-in">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-slate-800 dark:text-slate-100 flex items-center gap-2">
            <Users className="h-6 w-6 text-primary-600 dark:text-primary-400" />
            RBAC User Directory Management
          </h1>
          <p className="text-sm text-slate-600 dark:text-slate-400">
            Admin console for managing platform users, role assignments, and account statuses.
          </p>
        </div>
        <Button
          variant="primary"
          leftIcon={<UserPlus className="w-4 h-4" />}
          disabled
          title="Scheduled for Admin Portal Implementation"
        >
          Invite Platform User
        </Button>
      </div>

      <Card className="p-6">
        <div className="mb-4 pb-4 border-b border-slate-100 dark:border-forest-light flex items-center justify-between">
          <span className="text-sm font-semibold text-slate-700 dark:text-slate-200">
            Users Module Boundary (`backend/modules/users`)
          </span>
          <span className="text-xs text-primary-600 dark:text-primary-400 font-medium">
            REST API: `/api/v1/users/`
          </span>
        </div>

        <EmptyState
          icon={<Users className="w-8 h-8" />}
          title="Admin Directory Access Secured"
          description="You are viewing the administrative boundary for user identity and Role-Based Access Control (RBAC). Complete user table management and audit logs will be enabled in future admin iterations."
          actionLabel="RBAC Specifications"
          onAction={() => window.open("/api/v1/docs/", "_blank")}
        />
      </Card>
    </div>
  );
};

export default UserDirectory;
