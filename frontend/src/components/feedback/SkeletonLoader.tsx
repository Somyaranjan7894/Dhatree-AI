import React from "react";
import { cn } from "../../lib/cn";

export interface SkeletonLoaderProps
  extends React.HTMLAttributes<HTMLDivElement> {
  variant?: "text" | "rectangular" | "circular" | "card";
  width?: string | number;
  height?: string | number;
}

export const SkeletonLoader: React.FC<SkeletonLoaderProps> = ({
  variant = "rectangular",
  width,
  height,
  className,
  ...props
}) => {
  if (variant === "card") {
    return (
      <div
        className={cn(
          "w-full rounded-2xl border border-slate-200 dark:border-forest-light p-6 bg-white dark:bg-forest-medium space-y-4 animate-pulse select-none",
          className
        )}
        {...props}
      >
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-full bg-slate-200 dark:bg-forest-light shrink-0" />
          <div className="space-y-2 flex-1">
            <div className="h-4 bg-slate-200 dark:bg-forest-light rounded w-1/3" />
            <div className="h-3 bg-slate-200 dark:bg-forest-light rounded w-1/4" />
          </div>
        </div>
        <div className="space-y-2 pt-2">
          <div className="h-4 bg-slate-200 dark:bg-forest-light rounded w-full" />
          <div className="h-4 bg-slate-200 dark:bg-forest-light rounded w-5/6" />
          <div className="h-4 bg-slate-200 dark:bg-forest-light rounded w-2/3" />
        </div>
      </div>
    );
  }

  const variants = {
    text: "h-4 rounded w-3/4",
    rectangular: "rounded-xl",
    circular: "rounded-full",
  };

  return (
    <div
      className={cn(
        "animate-pulse bg-slate-200 dark:bg-forest-light select-none",
        variants[variant],
        className
      )}
      style={{
        width: typeof width === "number" ? `${width}px` : width,
        height: typeof height === "number" ? `${height}px` : height,
      }}
      {...props}
    />
  );
};
