import React from 'react';
import { motion } from 'framer-motion';
import { generateRecentActivities, formatTimeAgo, type RecentActivityItem } from '../../utils/recentActivityGenerator';
import type { Event } from '../../services/apiService';

interface RecentActivityProps {
  events: Event[];
  isLoading?: boolean;
}

const ActivityItem: React.FC<{ activity: RecentActivityItem; index: number }> = ({ activity, index }) => {
  const colorClasses = {
    green: 'bg-green-500',
    blue: 'bg-blue-500',
    purple: 'bg-purple-500',
    orange: 'bg-orange-500',
    red: 'bg-red-500'
  };

  return (
    <motion.div
      initial={{ opacity: 0, x: -20 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ delay: index * 0.1 }}
      className="flex items-center space-x-3 p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors"
    >
      <div className={`w-2 h-2 rounded-full ${colorClasses[activity.color as keyof typeof colorClasses]}`}></div>
      <div className="flex-1 min-w-0">
        <p className="text-sm font-medium text-gray-900 truncate">
          <span className="mr-2">{activity.icon}</span>
          {activity.description}
        </p>
        <p className="text-xs text-gray-500">
          {formatTimeAgo(activity.timestamp)}
        </p>
      </div>
    </motion.div>
  );
};

export const RecentActivity: React.FC<RecentActivityProps> = ({ events, isLoading = false }) => {
  const activities = generateRecentActivities(events, 5);

  if (isLoading) {
    return (
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.3 }}
        className="bg-white rounded-xl p-6 shadow-sm border border-gray-200"
      >
        <h2 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
          ⚡ Recent Activity
        </h2>
        
        <div className="space-y-4">
          {[1, 2, 3].map((i) => (
            <div key={i} className="flex items-center space-x-3 p-3 bg-gray-50 rounded-lg animate-pulse">
              <div className="w-2 h-2 bg-gray-300 rounded-full"></div>
              <div className="flex-1">
                <div className="h-4 bg-gray-300 rounded mb-2"></div>
                <div className="h-3 bg-gray-200 rounded w-20"></div>
              </div>
            </div>
          ))}
        </div>
      </motion.div>
    );
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.3 }}
      className="bg-white rounded-xl p-6 shadow-sm border border-gray-200"
    >
      <h2 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
        ⚡ Recent Activity
      </h2>
      
      <div className="space-y-4">
        {activities.length > 0 ? (
          activities.map((activity: RecentActivityItem, index: number) => (
            <ActivityItem key={activity.id} activity={activity} index={index} />
          ))
        ) : (
          <div className="text-center py-8 text-gray-500">
            <div className="text-4xl mb-2">📋</div>
            <p className="text-sm">No recent activity to show</p>
            <p className="text-xs text-gray-400 mt-1">Activity will appear when you create events</p>
          </div>
        )}
      </div>
      
      {activities.length > 0 && (
        <div className="mt-4 pt-4 border-t border-gray-100">
          <p className="text-xs text-gray-400 text-center">
            Showing recent activity from your events
          </p>
        </div>
      )}
    </motion.div>
  );
};
