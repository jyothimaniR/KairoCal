import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { 
  ChartBarIcon,
  CpuChipIcon,
  SparklesIcon,
  ClockIcon
} from '@heroicons/react/24/outline';
import { apiService } from '../../services/apiService';

interface AnalyticsPanelProps {
  className?: string;
}

const AnalyticsPanel: React.FC<AnalyticsPanelProps> = ({ className = '' }) => {
  const [priorityTrends, setPriorityTrends] = useState<any>(null);
  const [bertPerformance, setBertPerformance] = useState<any>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const loadAnalytics = async () => {
      try {
        setIsLoading(true);
        setError(null);

        const [trends, performance] = await Promise.all([
          apiService.getPriorityTrends(),
          apiService.getBertPerformance()
        ]);

        setPriorityTrends(trends);
        setBertPerformance(performance);
      } catch (err) {
        console.error('Error loading analytics:', err);
        setError('Failed to load analytics data');
      } finally {
        setIsLoading(false);
      }
    };

    loadAnalytics();
  }, []);

  if (isLoading) {
    return (
      <div className={`bg-white rounded-xl p-6 shadow-sm border border-gray-200 ${className}`}>
        <div className="animate-pulse space-y-4">
          <div className="h-4 bg-gray-200 rounded w-1/3"></div>
          <div className="space-y-2">
            <div className="h-3 bg-gray-200 rounded"></div>
            <div className="h-3 bg-gray-200 rounded w-2/3"></div>
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className={`bg-white rounded-xl p-6 shadow-sm border border-gray-200 ${className}`}>
        <div className="text-center text-red-600">
          <ChartBarIcon className="h-8 w-8 mx-auto mb-2" />
          <p className="text-sm">{error}</p>
        </div>
      </div>
    );
  }

  const getPriorityDistribution = () => {
    if (!priorityTrends?.trends?.[0]?.priority_distribution) return null;
    
    const distribution = priorityTrends.trends[0].priority_distribution;
    
    // Handle the new data structure where each priority has count and percentage
    return Object.entries(distribution)
      .map(([priority, data]: [string, any]) => ({
        priority: parseInt(priority),
        count: data.count || 0,
        percentage: Math.round(data.percentage || 0)
      }))
      .filter(item => item.count > 0); // Only show priorities that have events
  };

  const getPriorityLabel = (priority: number) => {
    switch (priority) {
      case 1: return { label: 'Critical', color: 'red' };
      case 2: return { label: 'High', color: 'orange' };
      case 3: return { label: 'Medium', color: 'yellow' };
      case 4: return { label: 'Low', color: 'green' };
      case 5: return { label: 'Very Low', color: 'green' };
      default: return { label: 'Unknown', color: 'gray' };
    }
  };

  const priorityDistribution = getPriorityDistribution();

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className={`bg-white rounded-xl p-6 shadow-sm border border-gray-200 ${className}`}
    >
      <h3 className="text-lg font-semibold text-gray-900 mb-6 flex items-center">
        <ChartBarIcon className="h-5 w-5 mr-2" />
        📊 AI Analytics Overview
      </h3>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Priority Trends */}
        <div>
          <h4 className="text-sm font-medium text-gray-900 mb-3 flex items-center">
            <SparklesIcon className="h-4 w-4 mr-1" />
            Priority Distribution
          </h4>
          
          {priorityDistribution && priorityDistribution.length > 0 ? (
            <div className="space-y-2">
              {priorityDistribution.map(({ priority, count, percentage }) => {
                const { label, color } = getPriorityLabel(priority);
                const bgColor = {
                  red: 'bg-red-100',
                  orange: 'bg-orange-100',
                  yellow: 'bg-yellow-100',
                  green: 'bg-green-100',
                  gray: 'bg-gray-100'
                }[color];
                
                const barColor = {
                  red: 'bg-red-500',
                  orange: 'bg-orange-500',
                  yellow: 'bg-yellow-500',
                  green: 'bg-green-500',
                  gray: 'bg-gray-500'
                }[color];

                return (
                  <div key={priority} className={`p-2 rounded ${bgColor}`}>
                    <div className="flex items-center justify-between text-xs">
                      <span className="font-medium">{label}</span>
                      <span>{count} events ({percentage}%)</span>
                    </div>
                    <div className="mt-1 w-full bg-gray-200 rounded-full h-1">
                      <div 
                        className={`h-1 rounded-full ${barColor}`}
                        style={{ width: `${percentage}%` }}
                      ></div>
                    </div>
                  </div>
                );
              })}
            </div>
          ) : (
            <div className="text-center py-4 text-gray-500 text-sm">
              <ClockIcon className="h-6 w-6 mx-auto mb-2" />
              <p>No priority data available yet</p>
              <p className="text-xs">Create more events to see trends</p>
            </div>
          )}

          {/* Summary Stats */}
          {priorityTrends?.insights && (
            <div className="mt-4 grid grid-cols-2 gap-3 text-xs">
              <div className="bg-blue-50 p-2 rounded">
                <div className="font-medium text-blue-900">Total Events</div>
                <div className="text-lg font-bold text-blue-600">
                  {priorityTrends.insights.total_events_analyzed}
                </div>
              </div>
              <div className="bg-purple-50 p-2 rounded">
                <div className="font-medium text-purple-900">High Priority</div>
                <div className="text-lg font-bold text-purple-600">
                  {Math.round(priorityTrends.insights.high_priority_rate * 100)}%
                </div>
              </div>
            </div>
          )}
        </div>

        {/* BERT Performance */}
        <div>
          <h4 className="text-sm font-medium text-gray-900 mb-3 flex items-center">
            <CpuChipIcon className="h-4 w-4 mr-1" />
            BERT AI Performance
          </h4>

          {bertPerformance?.classification_overview && (
            <div className="space-y-3">
              {/* Classification Overview */}
              <div className="bg-gradient-to-r from-purple-50 to-blue-50 p-3 rounded-lg">
                <div className="grid grid-cols-2 gap-3 text-xs">
                  <div>
                    <div className="font-medium text-gray-700">AI Classified</div>
                    <div className="text-lg font-bold text-purple-600">
                      {bertPerformance.classification_overview.bert_classified}
                    </div>
                  </div>
                  <div>
                    <div className="font-medium text-gray-700">Adoption Rate</div>
                    <div className="text-lg font-bold text-blue-600">
                      {Math.round(bertPerformance.classification_overview.bert_adoption_rate * 100)}%
                    </div>
                  </div>
                </div>
              </div>

              {/* Performance Indicators */}
              <div className="space-y-2">
                <div className="flex items-center justify-between p-2 bg-green-50 rounded">
                  <span className="text-xs font-medium text-green-900">Model Status</span>
                  <span className="text-xs text-green-600">🟢 Operational</span>
                </div>
                
                <div className="flex items-center justify-between p-2 bg-blue-50 rounded">
                  <span className="text-xs font-medium text-blue-900">Voice Integration</span>
                  <span className="text-xs text-blue-600">🎤 Active</span>
                </div>
              </div>

              {/* Recommendations */}
              {bertPerformance.recommendations && bertPerformance.recommendations.length > 0 && (
                <div className="mt-4">
                  <div className="text-xs font-medium text-gray-700 mb-2">💡 AI Recommendations:</div>
                  <div className="space-y-1">
                    {bertPerformance.recommendations.slice(0, 2).map((rec: string, index: number) => (
                      <div key={index} className="text-xs text-gray-600 bg-yellow-50 p-2 rounded">
                        {rec}
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </motion.div>
  );
};

export default AnalyticsPanel;
