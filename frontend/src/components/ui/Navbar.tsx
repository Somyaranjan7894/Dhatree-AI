import React from "react";
import { Link } from "react-router-dom";
import { Sprout, Bell, Menu, Sun, Moon, LogOut } from "lucide-react";
import { Avatar } from "./Avatar";
import { formatRole } from "../../utils/formatters";
import { Role } from "../../types";

export interface NavbarProps {
  onToggleSidebar?: () => void;
  isDarkMode?: boolean;
  onToggleTheme?: () => void;
  user?: {
    full_name: string;
    email: string;
    role: Role;
  } | null;
  onLogout?: () => void;
}

export const Navbar: React.FC<NavbarProps> = ({
  onToggleSidebar,
  isDarkMode = false,
  onToggleTheme,
  user,
  onLogout,
}) => {
  return (
    <header className="sticky top-0 z-40 flex h-16 w-full items-center justify-between border-b border-slate-200 dark:border-forest-light bg-white/95 dark:bg-forest-medium/95 backdrop-blur-md px-4 sm:px-6 shadow-sm select-none transition-colors">
      <div className="flex items-center gap-3">
        {onToggleSidebar && (
          <button
            onClick={onToggleSidebar}
            className="lg:hidden rounded-xl p-2 text-slate-600 hover:bg-slate-100 dark:text-slate-300 dark:hover:bg-forest-light focus:outline-none transition-colors"
            aria-label="Toggle Navigation Sidebar"
          >
            <Menu className="h-5 w-5" />
          </button>
        )}
        <Link to="/dashboard" className="flex items-center gap-2.5 group">
          <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-primary-600 text-white shadow-sm group-hover:bg-primary-700 transition-colors">
            <Sprout className="h-6 w-6" />
          </div>
          <div className="flex flex-col">
            <div className="flex items-center gap-2">
              <span className="text-lg font-bold tracking-tight text-slate-900 dark:text-slate-100 font-sans">
                Dhatree AI
              </span>
              <span className="hidden sm:inline-block rounded-full bg-primary-100 dark:bg-primary-900/50 px-2 py-0.5 text-[10px] font-semibold tracking-wide uppercase text-primary-800 dark:text-primary-300 border border-primary-200 dark:border-primary-800">
                Phase 3
              </span>
            </div>
            <span className="text-[10px] text-slate-500 dark:text-slate-400 font-medium hidden sm:block">
              Agriculture Intelligence Platform
            </span>
          </div>
        </Link>
      </div>

      <div className="flex items-center gap-2 sm:gap-3">
        {onToggleTheme && (
          <button
            onClick={onToggleTheme}
            className="rounded-xl p-2 text-slate-600 hover:bg-slate-100 dark:text-slate-300 dark:hover:bg-forest-light transition-colors focus:outline-none"
            aria-label="Toggle color mode"
            title={isDarkMode ? "Switch to light mode" : "Switch to dark mode"}
          >
            {isDarkMode ? <Sun className="h-5 w-5 text-warning-500" /> : <Moon className="h-5 w-5" />}
          </button>
        )}

        <Link
          to="/notifications"
          className="relative rounded-xl p-2 text-slate-600 hover:bg-slate-100 dark:text-slate-300 dark:hover:bg-forest-light transition-colors focus:outline-none"
          aria-label="Notifications"
          title="View notifications"
        >
          <Bell className="h-5 w-5" />
          <span className="absolute top-1.5 right-1.5 h-2 w-2 rounded-full bg-primary-500 ring-2 ring-white dark:ring-forest-medium" />
        </Link>

        {user ? (
          <div className="flex items-center gap-3 border-l border-slate-200 dark:border-forest-light pl-3 sm:pl-4">
            <Link to="/profile" className="flex items-center gap-2.5 group">
              <Avatar name={user.full_name} size="md" />
              <div className="hidden md:flex flex-col text-left">
                <span className="text-xs font-semibold text-slate-800 dark:text-slate-200 group-hover:text-primary-600 dark:group-hover:text-primary-400 transition-colors truncate max-w-[130px]">
                  {user.full_name}
                </span>
                <span className="text-[10px] text-primary-700 dark:text-primary-300 font-medium">
                  {formatRole(user.role)}
                </span>
              </div>
            </Link>
            {onLogout && (
              <button
                onClick={onLogout}
                className="rounded-xl p-2 text-slate-500 hover:bg-danger-50 hover:text-danger-600 dark:hover:bg-danger-500/10 dark:hover:text-danger-400 transition-colors focus:outline-none"
                title="Log out"
                aria-label="Log out"
              >
                <LogOut className="h-4 w-4" />
              </button>
            )}
          </div>
        ) : (
          <div className="flex items-center gap-2 border-l border-slate-200 dark:border-forest-light pl-3">
            <Link
              to="/login"
              className="text-xs font-semibold text-primary-600 dark:text-primary-400 hover:underline px-2 py-1"
            >
              Sign In
            </Link>
          </div>
        )}
      </div>
    </header>
  );
};
