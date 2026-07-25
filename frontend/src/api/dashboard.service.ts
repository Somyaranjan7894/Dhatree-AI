import { apiClient } from './client';

export interface DashboardMetrics {
  active_farms: number;
  total_disease_predictions: number;
  unread_alerts: number;
}

export interface DashboardInsight {
  type: 'info' | 'warning' | 'critical' | 'success';
  message: string;
}

export interface DashboardActivity {
  diseases: { id: string, disease: string, confidence: number, date: string }[];
  crop_recommendations: { id: string, crop: string, confidence: number, date: string }[];
  fertilizer_recommendations: { id: string, crop: string, fertilizer: string, date: string }[];
}

export interface DashboardOverviewResponse {
  metrics: DashboardMetrics;
  insights: DashboardInsight[];
  recent_activity: DashboardActivity;
}

export const dashboardService = {
  getOverview: async (): Promise<DashboardOverviewResponse> => {
    const response = await apiClient.get('/dashboard/overview/');
    const res = response as any;
    return res.data || res;
  }
};
