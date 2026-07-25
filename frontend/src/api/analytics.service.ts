import { apiClient } from './client';

export interface DiseaseFrequency {
  predicted_class: string;
  count: number;
}

export interface MonthlyScan {
  month: string;
  count: number;
}

export interface AnalyticsResponse {
  disease_frequency: DiseaseFrequency[];
  monthly_scans: MonthlyScan[];
  insights: string[];
}

export const analyticsService = {
  getAnalytics: async (): Promise<AnalyticsResponse> => {
    const response = await apiClient.get('/reports/analytics/');
    const res = response as any;
    return res.data || res;
  }
};
