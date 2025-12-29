import React, { useEffect, useState } from 'react';
import { CheckCircle, AlertCircle, Info } from 'lucide-react';

interface ActivityItem {
  id: number;
  time: string;
  message: string;
  type: 'success' | 'error' | 'info';
}

export const LiveActivity: React.FC = () => {
  const [activities, setActivities] = useState<ActivityItem[]>([
    {
      id: 1,
      time: new Date().toLocaleTimeString('en-US', {
        hour: '2-digit',
        minute: '2-digit',
        hour12: true,
      }),
      message: 'Connected to Local Server',
      type: 'success',
    },
  ]);

  // Function to add new activity (for demo purposes)
  useEffect(() => {
    const interval = setInterval(() => {
      const messages = [
        'New signal received from channel',
        'Trade executed successfully',
        'Broker connection verified',
        'Signal parsed and validated',
      ];

      const newActivity: ActivityItem = {
        id: Date.now(),
        time: new Date().toLocaleTimeString('en-US', {
          hour: '2-digit',
          minute: '2-digit',
          hour12: true,
        }),
        message: messages[Math.floor(Math.random() * messages.length)],
        type: Math.random() > 0.2 ? 'success' : 'info',
      };

      setActivities((prev) => [newActivity, ...prev].slice(0, 10)); // Keep only last 10
    }, 30000); // Add new activity every 30 seconds

    return () => clearInterval(interval);
  }, []);

  const getIcon = (type: ActivityItem['type']) => {
    switch (type) {
      case 'success':
        return <CheckCircle className="h-4 w-4 text-success-500" />;
      case 'error':
        return <AlertCircle className="h-4 w-4 text-danger-500" />;
      case 'info':
        return <Info className="h-4 w-4 text-primary-500" />;
    }
  };

  return (
    <div className="bg-dark-card border border-dark-border rounded-xl p-6">
      {/* Header */}
      <div className="flex items-center gap-2 mb-4">
        <div className="w-2 h-2 bg-success-500 rounded-full animate-pulse"></div>
        <h3 className="text-lg font-semibold text-white">Live Activity</h3>
      </div>

      {/* Activity Feed */}
      <div className="space-y-3">
        {activities.map((activity) => (
          <div
            key={activity.id}
            className="flex items-start gap-3 p-3 rounded-lg bg-dark-surface hover:bg-dark-hover transition-colors"
          >
            <div className="mt-0.5">{getIcon(activity.type)}</div>
            <div className="flex-1 min-w-0">
              <p className="text-sm text-gray-200 leading-relaxed">
                {activity.message}
              </p>
              <p className="text-xs text-gray-500 mt-1">{activity.time}</p>
            </div>
          </div>
        ))}
      </div>

      {/* View All Link */}
      <button className="w-full mt-4 text-sm text-primary-400 hover:text-primary-300 font-medium transition-colors">
        View All Activity →
      </button>
    </div>
  );
};
