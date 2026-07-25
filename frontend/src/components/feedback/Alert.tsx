import React from "react";
import { AlertCircle, CheckCircle2, Info, AlertTriangle, X } from "lucide-react";
import { cn } from "../../lib/cn";

export interface AlertProps {
  variant?: "info" | "success" | "warning" | "danger";
  title?: string;
  children: React.ReactNode;
  onClose?: () => void;
  className?: string;
}

export const Alert: React.FC<AlertProps> = ({
  variant = "info",
  title,
  children,
  onClose,
  className,
}) => {
  const icons = {
    info: <Info className="w-5 h-5 text-primary-600 dark:text-primary-400 shrink-0" />,
    success: <CheckCircle2 className="w-5 h-5 text-success-600 dark:text-success-400 shrink-0" />,
    warning: <AlertTriangle className="w-5 h-5 text-warning-600 dark:text-warning-400 shrink-0" />,
    danger: <AlertCircle className="w-5 h-5 text-danger-600 dark:text-danger-400 shrink-0" />,
  };

  const styles = {
    info: "bg-primary-50 border-primary-200 text-primary-900 dark:bg-primary-950/40 dark:border-primary-800 dark:text-primary-200",
    success: "bg-success-50 border-success-200 text-success-900 dark:bg-success-950/40 dark:border-success-800 dark:text-success-200",
    warning: "bg-warning-50 border-warning-200 text-warning-900 dark:bg-warning-950/40 dark:border-warning-800 dark:text-warning-200",
    danger: "bg-danger-50 border-danger-200 text-danger-900 dark:bg-danger-950/40 dark:border-danger-800 dark:text-danger-200",
  };

  return (
    <div
      className={cn(
        "relative flex items-start gap-3 p-4 rounded-xl border select-none transition-all animate-fade-in",
        styles[variant],
        className
      )}
      role="alert"
    >
      <div className="mt-0.5">{icons[variant]}</div>
      <div className="flex-1 text-sm leading-relaxed">
        {title && <h5 className="font-semibold mb-0.5">{title}</h5>}
        <div>{children}</div>
      </div>
      {onClose && (
        <button
          type="button"
          onClick={onClose}
          className="p-1 rounded-lg opacity-70 hover:opacity-100 transition-opacity focus:outline-none"
          aria-label="Dismiss alert"
        >
          <X className="w-4 h-4" />
        </button>
      )}
    </div>
  );
};
