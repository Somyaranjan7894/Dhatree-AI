import { apiClient } from "./client";

export const reportService = {
  getAnalytics: async () => {
    const response = await apiClient.get<any>("/reports/analytics/");
    const res = response as any;
    return res.data || res;
  }
};
