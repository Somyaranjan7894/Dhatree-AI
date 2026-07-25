import React from "react";
import { NavLink } from "react-router-dom";
import { SIDEBAR_NAV_ITEMS } from "../../constants/navigation";
import { Role } from "../../types";
import { cn } from "../../lib/cn";

export interface SidebarProps {
  isOpen?: boolean;
  onClose?: () => void;
  userRole?: Role;
}

export const Sidebar: React.FC<SidebarProps> = ({
  isOpen = false,
  onClose,
  userRole = "farmer",
}) => {
  const filteredNavItems = SIDEBAR_NAV_ITEMS.filter((item) => {
    if (!item.allowedRoles) return true;
    return item.allowedRoles.includes(userRole);
  });

  return (
    <>
      {/* Mobile Backdrop */}
      {isOpen && onClose && (
        <div
          className="fixed inset-0 z-40 bg-slate-900/60 dark:bg-slate-950/80 backdrop-blur-sm lg:hidden transition-opacity animate-fade-in"
          onClick={onClose}
        />
      )}

      {/* Sidebar Aside */}
      <aside
        className={cn(
          "fixed top-16 bottom-0 left-0 z-40 w-64 border-r border-slate-200 dark:border-forest-light bg-white dark:bg-forest-medium flex flex-col justify-between p-4 transition-transform duration-200 lg:static lg:translate-x-0 lg:h-[calc(100vh-4rem)] shrink-0 overflow-y-auto select-none",
          isOpen ? "translate-x-0 shadow-xl" : "-translate-x-full lg:shadow-none"
        )}
      >
        <nav className="flex flex-col gap-1">
          <div className="px-3.5 py-2 text-[11px] font-semibold uppercase tracking-wider text-slate-400 dark:text-slate-400">
            Navigation Modules
          </div>
          {filteredNavItems.map((item) => {
            const Icon = item.icon;
            return (
              <NavLink
                key={item.href}
                to={item.href}
                onClick={() => onClose && onClose()}
                className={({ isActive }) =>
                  cn(
                    "flex items-center justify-between rounded-xl px-3.5 py-2.5 text-sm font-medium transition-all duration-150 group",
                    isActive
                      ? "bg-primary-600 text-white shadow-sm dark:bg-primary-600"
                      : "text-slate-600 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-forest-light hover:text-slate-900 dark:hover:text-white"
                  )
                }
              >
                {({ isActive }) => (
                  <>
                    <div className="flex items-center gap-3 truncate">
                      <Icon
                        className={cn(
                          "h-4 w-4 shrink-0 transition-transform group-hover:scale-110",
                          isActive ? "text-white" : "text-slate-500 dark:text-slate-400 group-hover:text-primary-600 dark:group-hover:text-primary-300"
                        )}
                      />
                      <span className="truncate">{item.label}</span>
                    </div>
                    {item.badge && (
                      <span
                        className={cn(
                          "px-2 py-0.5 rounded-full text-[10px] font-semibold uppercase shrink-0",
                          isActive
                            ? "bg-white/20 text-white"
                            : "bg-primary-100 text-primary-800 dark:bg-primary-900/50 dark:text-primary-300"
                        )}
                      >
                        {item.badge}
                      </span>
                    )}
                  </>
                )}
              </NavLink>
            );
          })}
        </nav>

        <div className="mt-6 rounded-xl bg-earth-100 dark:bg-forest-dark/70 p-4 border border-earth-200 dark:border-forest-light">
          <div className="flex items-center justify-between text-xs font-semibold text-slate-800 dark:text-slate-200 mb-1">
            <span>Platform Status</span>
            <span className="flex items-center gap-1.5 text-primary-700 dark:text-primary-400 font-bold">
              <span className="h-2 w-2 rounded-full bg-primary-500 animate-pulse" />
              Online
            </span>
          </div>
          <p className="text-[11px] text-slate-600 dark:text-slate-400 leading-relaxed">
            AI Engine connected to Dhatree Phase 2 REST API endpoints (`v0.1.0`).
          </p>
        </div>
      </aside>
    </>
  );
};
