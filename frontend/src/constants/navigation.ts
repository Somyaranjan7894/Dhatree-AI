import {
  Home,
  Sprout,
  ScanLine,
  Lightbulb,
  CloudSun,
  FileSpreadsheet,
  Bell,
  Bot,
  UserCheck,
  Users,
} from "lucide-react";
import { Role } from "../types";

export interface NavItem {
  label: string;
  href: string;
  icon: React.ComponentType<{ className?: string }>;
  allowedRoles?: Role[];
  badge?: string;
}

export const SIDEBAR_NAV_ITEMS: NavItem[] = [
  {
    label: "Dashboard",
    href: "/dashboard",
    icon: Home,
  },
  {
    label: "My Farms",
    href: "/farms",
    icon: Sprout,
    allowedRoles: ["farmer", "agronomist", "admin"],
  },
  {
    label: "Disease Detection",
    href: "/disease-detection",
    icon: ScanLine,
    allowedRoles: ["farmer", "agronomist", "researcher", "admin"],
  },
  {
    label: "Recommendation",
    href: "/recommendations",
    icon: Lightbulb,
    allowedRoles: ["farmer", "agronomist", "admin"],
  },
  {
    label: "Weather Intelligence",
    href: "/weather",
    icon: CloudSun,
  },
  {
    label: "AI Assistant",
    href: "/ai-assistant",
    icon: Bot,
    badge: "AI",
  },
  {
    label: "Reports",
    href: "/reports",
    icon: FileSpreadsheet,
  },
  {
    label: "Notifications",
    href: "/notifications",
    icon: Bell,
  },
  {
    label: "User Directory",
    href: "/admin/users",
    icon: Users,
    allowedRoles: ["admin"],
  },
  {
    label: "Profile Settings",
    href: "/profile",
    icon: UserCheck,
  },
];

export const ROLE_OPTIONS = [
  { label: "Farmer (Primary Agricultural User)", value: "farmer" },
  { label: "Agronomist (Advisory & Crop Specialist)", value: "agronomist" },
  { label: "Researcher (Analytics & Data Scientist)", value: "researcher" },
];
