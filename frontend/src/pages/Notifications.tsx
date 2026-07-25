import React, { useEffect, useState } from "react";
import { Card, Button } from "@/components/common";
import { EmptyState } from "@/components/feedback/EmptyState";
import { Bell, CheckCircle, Trash2 } from "lucide-react";
import { notificationService } from "@/api/notification.service";
import { Notification } from "@/types";

export const Notifications: React.FC = () => {
  const [notifications, setNotifications] = useState<Notification[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchNotifications();
  }, []);

  const fetchNotifications = async () => {
    try {
      const data = await notificationService.getNotifications();
      setNotifications(data);
    } catch (error) {
      console.error("Failed to fetch notifications", error);
    } finally {
      setLoading(false);
    }
  };

  const handleMarkRead = async (id: string) => {
    try {
      await notificationService.markAsRead(id);
      setNotifications(notifications.map(n => n.id === id ? { ...n, is_read: true } : n));
    } catch (error) {
      console.error("Failed to mark notification as read", error);
    }
  };

  const handleDelete = async (id: string) => {
    try {
      await notificationService.deleteNotification(id);
      setNotifications(notifications.filter(n => n.id !== id));
    } catch (error) {
      console.error("Failed to delete notification", error);
    }
  };

  if (loading) return <div className="p-8 text-center">Loading notifications...</div>;

  return (
    <div className="flex flex-col gap-6 animate-fade-in max-w-4xl mx-auto w-full">
      <div className="flex items-center gap-2">
        <Bell className="h-6 w-6 text-amber-500" />
        <h1 className="text-2xl font-bold text-slate-800 dark:text-slate-100">
          Notifications
        </h1>
      </div>

      {notifications.length === 0 ? (
        <Card className="p-6">
          <EmptyState
            icon={<Bell className="w-8 h-8" />}
            title="All Caught Up"
            description="You have no notifications at this time."
          />
        </Card>
      ) : (
        <div className="flex flex-col gap-4">
          {notifications.map((notification) => (
            <Card key={notification.id} className={`p-5 flex flex-col sm:flex-row gap-4 items-start sm:items-center justify-between ${notification.is_read ? 'opacity-70 bg-slate-50 dark:bg-slate-800/50' : 'border-l-4 border-l-primary-500'}`}>
              <div className="flex-1">
                <div className="flex items-center gap-2 mb-1">
                  <h3 className="font-semibold text-slate-800 dark:text-slate-100">{notification.title}</h3>
                  <span className="text-[10px] uppercase font-bold px-2 py-0.5 rounded-full bg-slate-200 text-slate-600 dark:bg-slate-700 dark:text-slate-300">
                    {notification.notification_type}
                  </span>
                </div>
                <p className="text-sm text-slate-600 dark:text-slate-300 mb-2">
                  {notification.description}
                </p>
                <div className="text-xs text-slate-400">
                  {new Date(notification.created_at).toLocaleString()}
                </div>
              </div>
              <div className="flex items-center gap-2">
                {!notification.is_read && (
                  <Button variant="outline" size="sm" onClick={() => handleMarkRead(notification.id)} title="Mark as read">
                    <CheckCircle className="w-4 h-4" />
                  </Button>
                )}
                <Button variant="danger" size="sm" onClick={() => handleDelete(notification.id)} title="Delete">
                  <Trash2 className="w-4 h-4" />
                </Button>
              </div>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
};

export default Notifications;
