import React, { forwardRef } from "react";
import { cn } from "../../lib/cn";

export interface SwitchProps
  extends Omit<React.InputHTMLAttributes<HTMLInputElement>, "type"> {
  label?: string;
}

export const Switch = forwardRef<HTMLInputElement, SwitchProps>(
  ({ className, label, id, checked, ...props }, ref) => {
    const switchId =
      id || (label ? label.toLowerCase().replace(/\s+/g, "-") : undefined);

    return (
      <label
        htmlFor={switchId}
        className="inline-flex items-center gap-3 cursor-pointer select-none"
      >
        <div className="relative">
          <input
            id={switchId}
            ref={ref}
            type="checkbox"
            checked={checked}
            className="sr-only peer"
            {...props}
          />
          <div
            className={cn(
              "w-11 h-6 bg-slate-200 dark:bg-forest-light rounded-full peer peer-focus:ring-2 peer-focus:ring-primary-500/20 transition-colors duration-200 peer-checked:bg-primary-600 dark:peer-checked:bg-primary-500",
              className
            )}
          />
          <div className="absolute left-1 top-1 bg-white w-4 h-4 rounded-full transition-transform duration-200 peer-checked:translate-x-5 shadow-sm" />
        </div>
        {label && (
          <span className="text-sm font-medium text-slate-700 dark:text-slate-300">
            {label}
          </span>
        )}
      </label>
    );
  }
);

Switch.displayName = "Switch";
