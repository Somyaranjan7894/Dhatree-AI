import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";

/**
 * Merges CSS class names dynamically, combining clsx conditions and tailwind-merge deduplication.
 */
export function cn(...inputs: ClassValue[]): string {
  return twMerge(clsx(inputs));
}
