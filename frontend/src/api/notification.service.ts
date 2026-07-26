import { apiClient } from './client';

export interface Notification {
  id: string;
  title: string;
  description: string;
  notification_type: 'information' | 'success' | 'warning' | 'critical';
  category: 'prediction' | 'recommendation' | 'system' | 'alert';
  is_read: boolean;
  created_at: string;
}

export const notificationService = {
  getNotifications: async (): Promise<Notification[]> => {
    const response = await apiClient.get('/notifications/');
    const res = response as any;
    return res.data || res.results || res;
  },

  markAsRead: async (id: string): Promise<Notification> => {
    const response = await apiClient.post(`/notifications/${id}/mark_read/`);
    const res = response as any;
    return res.data || res;
  },

  markAllAsRead: async (): Promise<void> => {
    await apiClient.post('/notifications/mark_all_read/');
  },

  deleteNotification: async (id: string): Promise<void> => {
    await apiClient.delete(`/notifications/${id}/`);
  }
};
