import React from "react";
import { X } from "lucide-react";
import { cn } from "../../lib/cn";

export interface ChipProps extends React.HTMLAttributes<HTMLDivElement> {
  label: string;
  onRemove?: () => void;
  variant?: "primary" | "neutral";
}

export const Chip: React.FC<ChipProps> = ({
  label,
  onRemove,
  variant = "neutral",
  className,
  ...props
}) => {
  const variants = {
    primary:
      "bg-primary-50 border-primary-200 text-primary-800 dark:bg-primary-900/40 dark:border-primary-800 dark:text-primary-200",
    neutral:
      "bg-slate-100 border-slate-200 text-slate-700 dark:bg-forest-light dark:border-forest-light dark:text-slate-300",
  };

  return (
    <div
      className={cn(
        "inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-medium border select-none transition-colors",
        variants[variant],
        className
      )}
      {...props}
    >
      <span>{label}</span>
      {onRemove && (
        <button
          type="button"
          onClick={onRemove}
          className="p-0.5 rounded-full hover:bg-black/10 dark:hover:bg-white/10 transition-colors focus:outline-none"
          aria-label={`Remove ${label}`}
        >
          <X className="w-3 h-3" />
        </button>
      )}
    </div>
  );
};
