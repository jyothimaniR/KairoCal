import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { 
  ChartBarIcon,
  CpuChipIcon,
  SparklesIcon,
  ClockIcon,
  ArrowTrendingUpIcon,
  ArrowPathIcon
} from '@heroicons/react/24/outline';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { apiService } from '../../services/apiService';
import { getPriorityInfo } from '../../utils/priorityUtils';

interface AnalyticsPanelProps {
  className?: string;
}

const AnalyticsPanel: React.FC<AnalyticsPanelProps> = ({ className = '' }) => {
  const [priorityTrends, setPriorityTrends] = useState<any>(null);
  const [bertPerformance, setBertPerformance] = useState<any>(null);
  const [productivityMetrics, setProductivityMetrics] = useState<any>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isRefreshing, setIsRefreshing] = useState(false);

  const loadAnalytics = async () => {
    try {
      setError(null);
      if (!isRefreshing) setIsLoading(true);

      const [trends, performance, productivity] = await Promise.all([
        apiService.getPriorityTrends(),
        apiService.getBertPerformance(),
        // Use fallback data if productivity endpoint fails
        apiService.getProductivityMetrics().catch(() => null)
      ]);

      setPriorityTrends(trends);
      setBertPerformance(performance);
      setProductivityMetrics(productivity);
    } catch (err) {
      console.error('Error loading analytics:', err);
      setError('Failed to load analytics data');
    } finally {
      setIsLoading(false);
      setIsRefreshing(false);
    }
  };

  useEffect(() => {
    loadAnalytics();
  }, []);

  const handleRefresh = async () => {
    setIsRefreshing(true);
    await loadAnalytics();
  };

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

  const getPriorityChartData = () => {
    if (!priorityTrends?.trends?.[0]?.priority_distribution) return [];
    
    const distribution = priorityTrends.trends[0].priority_distribution;
    
    return Object.entries(distribution)
      .map(([priority, data]: [string, any]) => {
        const { label, color } = getPriorityLabel(parseInt(priority));
        return {
          priority: parseInt(priority),
          label,
          count: data.count || 0,
          percentage: Math.round(data.percentage || 0),
          color: {
            red: '#ef4444',
            orange: '#f97316',
            yellow: '#eab308',
            green: '#22c55e',
            gray: '#6b7280'
          }[color] || '#6b7280'
        };
      })
      .sort((a, b) => a.priority - b.priority); // Sort by priority level instead of filtering out zeros
  };

  const getProductivityChartData = () => {
    if (!productivityMetrics?.metrics?.components) return [];
    
    const components = productivityMetrics.metrics.components;
    return [
      { name: 'Meeting Efficiency', value: components.meeting_efficiency || 0 },
      { name: 'Energy Management', value: components.energy_management || 0 },
      { name: 'Time Utilization', value: components.time_utilization || 0 },
      { name: 'Focus Score', value: components.focus_score || 0 }
    ];
  };

  const getPriorityLabel = (priority: number) => {
    // PRIORITY FIX: Use centralized priority system instead of hardcoded logic
    const priorityInfo = getPriorityInfo(priority);
    return { 
      label: priorityInfo.label, 
      color: priorityInfo.color 
    };
  };

  const priorityChartData = getPriorityChartData();
  const productivityChartData = getProductivityChartData();

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className={`bg-white rounded-xl p-6 shadow-sm border border-gray-200 ${className}`}
    >
      <div className="flex items-center justify-between mb-6">
        <h3 className="text-lg font-semibold text-gray-900 flex items-center">
          <ChartBarIcon className="h-5 w-5 mr-2" />
          📊 AI Analytics Overview
        </h3>
        <button
          onClick={handleRefresh}
          disabled={isRefreshing}
          className="flex items-center space-x-2 px-3 py-1.5 text-sm text-gray-600 hover:text-gray-900 hover:bg-gray-50 rounded-lg transition-colors"
        >
          <ArrowPathIcon className={`h-4 w-4 ${isRefreshing ? 'animate-spin' : ''}`} />
          <span>Refresh</span>
        </button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Priority Trends with Chart */}
        <div className="lg:col-span-2">
          <h4 className="text-sm font-medium text-gray-900 mb-3 flex items-center">
            <SparklesIcon className="h-4 w-4 mr-1" />
            Priority Distribution & Trends
          </h4>
          
          {priorityChartData && priorityChartData.length > 0 ? (
            <div className="space-y-4">
              {/* Chart */}
              <div className="h-64">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={priorityChartData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="label" />
                    <YAxis />
                    <Tooltip 
                      formatter={(value, name) => [value, name === 'count' ? 'Events' : name]}
                      labelFormatter={(label) => `Priority: ${label}`}
                    />
                    <Bar dataKey="count" fill="#8b5cf6" radius={[4, 4, 0, 0]} />
                  </BarChart>
                </ResponsiveContainer>
              </div>
              
              {/* Stats Cards */}
              {priorityTrends?.insights && (
                <div className="grid grid-cols-2 gap-3 text-xs">
                  <div className="bg-blue-50 p-3 rounded-lg">
                    <div className="font-medium text-blue-900">Total Events</div>
                    <div className="text-xl font-bold text-blue-600">
                      {priorityTrends.insights.total_events_analyzed}
                    </div>
                  </div>
                  <div className="bg-purple-50 p-3 rounded-lg">
                    <div className="font-medium text-purple-900">High Priority</div>
                    <div className="text-xl font-bold text-purple-600 flex items-center">
                      {Math.round(priorityTrends.insights.high_priority_rate)}%
                      <ArrowTrendingUpIcon className="h-4 w-4 ml-1" />
                    </div>
                  </div>
                </div>
              )}
            </div>
          ) : (
            <div className="text-center py-8 text-gray-500 text-sm">
              <ClockIcon className="h-12 w-12 mx-auto mb-3 text-gray-300" />
              <p className="font-medium">No priority data available yet</p>
              <p className="text-xs">Create more events to see trends and charts</p>
            </div>
          )}
        </div>

        {/* BERT Performance & Productivity */}
        <div className="space-y-6">
          {/* BERT Performance */}
          <div>
            <h4 className="text-sm font-medium text-gray-900 mb-3 flex items-center">
              <CpuChipIcon className="h-4 w-4 mr-1" />
              BERT AI Performance
            </h4>

            {bertPerformance?.classification_overview ? (
              <div className="space-y-3">
                {/* Classification Overview */}
                <div className="bg-gradient-to-r from-purple-50 to-blue-50 p-4 rounded-lg">
                  <div className="grid grid-cols-1 gap-3 text-sm">
                    <div className="flex justify-between">
                      <span className="text-gray-700">AI Classified</span>
                      <span className="font-bold text-purple-600">
                        {bertPerformance.classification_overview.bert_classified}
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-700">Adoption Rate</span>
                      <span className="font-bold text-blue-600">
                        {Math.round(bertPerformance.classification_overview.bert_adoption_rate)}%
                      </span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-2 mt-2">
                      <div 
                        className="bg-gradient-to-r from-purple-500 to-blue-500 h-2 rounded-full transition-all"
                        style={{
                          width: `${bertPerformance.classification_overview.bert_adoption_rate}%`
                        }}
                      ></div>
                    </div>
                  </div>
                </div>

                {/* Status Indicators */}
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
                  <div>
                    <div className="text-xs font-medium text-gray-700 mb-2">💡 AI Recommendations:</div>
                    <div className="space-y-1">
                      {bertPerformance.recommendations.slice(0, 2).map((rec: string, index: number) => (
                        <div key={index} className="text-xs text-gray-600 bg-yellow-50 p-2 rounded border-l-2 border-yellow-300">
                          {rec}
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            ) : (
              <div className="text-center py-4 text-gray-500 text-sm">
                <CpuChipIcon className="h-8 w-8 mx-auto mb-2 text-gray-300" />
                <p>BERT analysis loading...</p>
              </div>
            )}
          </div>

          {/* Productivity Metrics */}
          {productivityMetrics?.metrics && (
            <div>
              <h4 className="text-sm font-medium text-gray-900 mb-3 flex items-center">
                <ArrowTrendingUpIcon className="h-4 w-4 mr-1" />
                Productivity Score
              </h4>
              <div className="bg-gradient-to-r from-green-50 to-emerald-50 p-4 rounded-lg">
                <div className="text-center">
                  <div className="text-3xl font-bold text-green-600 mb-1">
                    {Math.round(productivityMetrics.metrics.overall_score)}
                  </div>
                  <div className="text-sm text-gray-600">Overall Score</div>
                  <div className="w-full bg-gray-200 rounded-full h-2 mt-3">
                    <div 
                      className="bg-gradient-to-r from-green-400 to-emerald-500 h-2 rounded-full transition-all"
                      style={{
                        width: `${productivityMetrics.metrics.overall_score}%`
                      }}
                    ></div>
                  </div>
                </div>
                
                {productivityChartData && productivityChartData.length > 0 && (
                  <div className="mt-4 grid grid-cols-2 gap-2 text-xs">
                    {productivityChartData.slice(0, 4).map((item) => (
                      <div key={item.name} className="flex items-center justify-between">
                        <span className="text-gray-600 truncate">{item.name.split(' ')[0]}</span>
                        <span className="font-medium text-gray-900">{item.value}%</span>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>
          )}
        </div>
      </div>
    </motion.div>
  );
};

export default AnalyticsPanel;
