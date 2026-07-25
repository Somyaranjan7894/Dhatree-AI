import React from "react";
import { cn } from "../../lib/cn";

export interface SpinnerProps {
  size?: "sm" | "md" | "lg" | "xl";
  text?: string;
  className?: string;
}

export const Spinner: React.FC<SpinnerProps> = ({
  size = "md",
  text,
  className,
}) => {
  const sizeClasses = {
    sm: "h-5 w-5 border-2",
    md: "h-8 w-8 border-3",
    lg: "h-12 w-12 border-4",
    xl: "h-16 w-16 border-4",
  };

  return (
    <div
      className={cn(
        "flex flex-col items-center justify-center gap-3 py-6 select-none",
        className
      )}
    >
      <div
        className={cn(
          "animate-spin rounded-full border-primary-600 dark:border-primary-400 border-t-transparent",
          sizeClasses[size]
        )}
      />
      {text && (
        <span className="text-sm font-medium text-slate-600 dark:text-slate-300 animate-pulse">
          {text}
        </span>
      )}
    </div>
  );
};

export const Loader = Spinner;
