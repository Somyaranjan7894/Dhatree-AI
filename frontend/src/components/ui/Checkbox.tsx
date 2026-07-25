import React, { forwardRef } from "react";
import { cn } from "../../lib/cn";

export interface CheckboxProps
  extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
}

export const Checkbox = forwardRef<HTMLInputElement, CheckboxProps>(
  ({ className, label, error, id, ...props }, ref) => {
    const checkboxId =
      id || (label ? label.toLowerCase().replace(/\s+/g, "-") : undefined);

    return (
      <div className="flex flex-col gap-1">
        <label
          htmlFor={checkboxId}
          className="inline-flex items-center gap-2.5 cursor-pointer select-none"
        >
          <input
            id={checkboxId}
            ref={ref}
            type="checkbox"
            className={cn(
              "h-4 w-4 rounded border-slate-300 dark:border-forest-light text-primary-600 focus:ring-primary-500/20 dark:bg-forest-dark transition-colors cursor-pointer",
              error && "border-danger-500",
              className
            )}
            {...props}
          />
          {label && (
            <span className="text-sm font-medium text-slate-700 dark:text-slate-300">
              {label}
            </span>
          )}
        </label>
        {error && (
          <span className="text-xs text-danger-600 dark:text-danger-400 font-medium">
            {error}
          </span>
        )}
      </div>
    );
  }
);

Checkbox.displayName = "Checkbox";
