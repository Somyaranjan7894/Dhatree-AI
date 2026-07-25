import React, { useState, useEffect } from "react";
import { Search, X } from "lucide-react";
import { Input } from "../ui/Input";

export interface SearchBoxProps {
  placeholder?: string;
  onSearch: (query: string) => void;
  debounceMs?: number;
  initialValue?: string;
  className?: string;
}

export const SearchBox: React.FC<SearchBoxProps> = ({
  placeholder = "Search agricultural records...",
  onSearch,
  debounceMs = 300,
  initialValue = "",
  className,
}) => {
  const [value, setValue] = useState(initialValue);

  useEffect(() => {
    const timer = setTimeout(() => {
      onSearch(value);
    }, debounceMs);
    return () => clearTimeout(timer);
  }, [value, debounceMs, onSearch]);

  return (
    <Input
      className={className}
      value={value}
      onChange={(e) => setValue(e.target.value)}
      placeholder={placeholder}
      leftIcon={<Search className="w-4 h-4" />}
      rightIcon={
        value ? (
          <button
            type="button"
            onClick={() => setValue("")}
            className="p-1 text-slate-400 hover:text-slate-600 dark:hover:text-slate-200 transition-colors focus:outline-none"
            aria-label="Clear search"
          >
            <X className="w-4 h-4" />
          </button>
        ) : undefined
      }
    />
  );
};
