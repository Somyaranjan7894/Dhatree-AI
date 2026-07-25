import React from "react";
import { Card } from "@/components/common";
import { LoginForm } from "@/modules/auth";
import { Sprout } from "lucide-react";
import { APP_NAME, APP_TAGLINE } from "@/config/constants";

export const Login: React.FC = () => {
  return (
    <div className="min-h-[80vh] flex flex-col items-center justify-center py-12 px-4 sm:px-6 lg:px-8 animate-fade-in">
      <div className="w-full max-w-md flex flex-col items-center mb-6 text-center">
        <div className="h-14 w-14 rounded-2xl bg-primary-600 text-white flex items-center justify-center shadow-card mb-3">
          <Sprout className="h-8 w-8" />
        </div>
        <h1 className="text-2xl font-bold tracking-tight text-slate-900 dark:text-slate-100">
          {APP_NAME}
        </h1>
        <p className="text-sm text-slate-600 dark:text-slate-400 mt-1">
          {APP_TAGLINE}
        </p>
      </div>

      <Card className="w-full max-w-md p-6 sm:p-8 shadow-modal">
        <div className="mb-6 pb-4 border-b border-slate-200 dark:border-forest-light">
          <h2 className="text-lg font-semibold text-slate-800 dark:text-slate-100">
            Platform Sign In
          </h2>
          <p className="text-xs text-slate-500 dark:text-slate-400 mt-0.5">
            Enter your authenticated credentials to access secure agricultural boundaries.
          </p>
        </div>
        <LoginForm />
      </Card>
    </div>
  );
};

export default Login;
