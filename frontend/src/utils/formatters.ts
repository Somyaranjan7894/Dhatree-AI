/**
 * Helper formatting utilities across Dhatree AI frontend.
 */

export function formatDate(dateString?: string | null): string {
  if (!dateString) return "N/A";
  try {
    return new Intl.DateTimeFormat("en-IN", {
      year: "numeric",
      month: "short",
      day: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    }).format(new Date(dateString));
  } catch {
    return dateString;
  }
}

export function formatRole(role?: string): string {
  switch (role) {
    case "farmer":
      return "Farmer";
    case "agronomist":
      return "Agronomist";
    case "researcher":
      return "Researcher";
    case "admin":
      return "Platform Admin";
    default:
      return "User";
  }
}

export function truncateText(text: string, maxLength = 60): string {
  if (!text || text.length <= maxLength) return text;
  return text.substring(0, maxLength) + "...";
}
