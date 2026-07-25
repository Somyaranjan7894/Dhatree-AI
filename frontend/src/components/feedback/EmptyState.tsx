import React from "react";
import { FolderOpen } from "lucide-react";
import { Button } from "../ui/Button";
import { cn } from "../../lib/cn";

export interface EmptyStateProps {
  icon?: React.ReactNode;
  title: string;
  description?: string;
  actionLabel?: string;
  onAction?: () => void;
  className?: string;
}

export const EmptyState: React.FC<EmptyStateProps> = ({
  icon,
  title,
  description,
  actionLabel,
  onAction,
  className,
}) => {
  return (
    <div
      className={cn(
        "flex flex-col items-center justify-center text-center p-8 md:p-12 border-2 border-dashed border-slate-200 dark:border-forest-light rounded-2xl bg-slate-50/50 dark:bg-forest-medium/30 select-none animate-fade-in",
        className
      )}
    >
      <div className="p-4 rounded-full bg-slate-100 dark:bg-forest-dark text-slate-400 dark:text-slate-500 mb-4">
        {icon || <FolderOpen className="w-8 h-8" />}
      </div>
      <h3 className="text-base font-semibold text-slate-800 dark:text-slate-200 mb-1">
        {title}
      </h3>
      {description && (
        <p className="text-sm text-slate-500 dark:text-slate-400 max-w-sm mb-6">
          {description}
        </p>
      )}
      {actionLabel && onAction && (
        <Button variant="primary" size="sm" onClick={onAction}>
          {actionLabel}
        </Button>
      )}
    </div>
  );
};
