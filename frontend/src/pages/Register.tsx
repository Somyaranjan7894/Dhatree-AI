import React from "react";
import { Card } from "@/components/common";
import { RegisterForm } from "@/modules/auth";
import { Sprout } from "lucide-react";
import { APP_NAME, APP_TAGLINE } from "@/config/constants";

export const Register: React.FC = () => {
  return (
    <div className="min-h-[85vh] flex flex-col items-center justify-center py-10 px-4 sm:px-6 lg:px-8 animate-fade-in">
      <div className="w-full max-w-xl flex flex-col items-center mb-6 text-center">
        <div className="h-14 w-14 rounded-2xl bg-primary-600 text-white flex items-center justify-center shadow-card mb-3">
          <Sprout className="h-8 w-8" />
        </div>
        <h1 className="text-2xl font-bold tracking-tight text-slate-900 dark:text-slate-100">
          Join {APP_NAME}
        </h1>
        <p className="text-sm text-slate-600 dark:text-slate-400 mt-1">
          {APP_TAGLINE}
        </p>
      </div>

      <Card className="w-full max-w-xl p-6 sm:p-8 shadow-modal">
        <div className="mb-6 pb-4 border-b border-slate-200 dark:border-forest-light">
          <h2 className="text-lg font-semibold text-slate-800 dark:text-slate-100">
            Create User Profile
          </h2>
          <p className="text-xs text-slate-500 dark:text-slate-400 mt-0.5">
            Register your role boundary (Farmer, Agronomist, or Researcher) to initialize workspace access.
          </p>
        </div>
        <RegisterForm />
      </Card>
    </div>
  );
};

export default Register;
