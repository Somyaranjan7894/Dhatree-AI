import React, { forwardRef } from "react";
import { cn } from "../../lib/cn";

export interface RadioProps
  extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
}

export const Radio = forwardRef<HTMLInputElement, RadioProps>(
  ({ className, label, id, ...props }, ref) => {
    const radioId =
      id || (label ? label.toLowerCase().replace(/\s+/g, "-") : undefined);

    return (
      <label
        htmlFor={radioId}
        className="inline-flex items-center gap-2.5 cursor-pointer select-none"
      >
        <input
          id={radioId}
          ref={ref}
          type="radio"
          className={cn(
            "h-4 w-4 rounded-full border-slate-300 dark:border-forest-light text-primary-600 focus:ring-primary-500/20 dark:bg-forest-dark transition-colors cursor-pointer",
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
    );
  }
);

Radio.displayName = "Radio";
