import React from "react";
import { cn } from "../../lib/cn";

export interface BadgeProps extends React.HTMLAttributes<HTMLSpanElement> {
  variant?: "primary" | "secondary" | "success" | "warning" | "danger" | "neutral";
  size?: "sm" | "md";
}

export const Badge: React.FC<BadgeProps> = ({
  children,
  variant = "primary",
  size = "md",
  className,
  ...props
}) => {
  const variants = {
    primary:
      "bg-primary-100 text-primary-800 dark:bg-primary-900/40 dark:text-primary-300 border border-primary-200 dark:border-primary-800",
    secondary:
      "bg-earth-100 text-earth-800 dark:bg-earth-900/40 dark:text-earth-200 border border-earth-200 dark:border-earth-800",
    success:
      "bg-success-50 text-success-700 dark:bg-success-500/10 dark:text-success-400 border border-success-200 dark:border-success-800/40",
    warning:
      "bg-warning-50 text-warning-700 dark:bg-warning-500/10 dark:text-warning-400 border border-warning-200 dark:border-warning-800/40",
    danger:
      "bg-danger-50 text-danger-700 dark:bg-danger-500/10 dark:text-danger-400 border border-danger-200 dark:border-danger-800/40",
    neutral:
      "bg-slate-100 text-slate-700 dark:bg-forest-light dark:text-slate-300 border border-slate-200 dark:border-forest-light",
  };

  const sizes = {
    sm: "px-2 py-0.5 text-[11px]",
    md: "px-2.5 py-1 text-xs",
  };

  return (
    <span
      className={cn(
        "inline-flex items-center justify-center font-medium rounded-full select-none shrink-0",
        variants[variant],
        sizes[size],
        className
      )}
      {...props}
    >
      {children}
    </span>
  );
};
