import React, { useState, useEffect } from 'react';
import { 
  ChartBarIcon,
  ClockIcon,
  ArrowPathIcon,
  ChevronDownIcon
} from '@heroicons/react/24/outline';
import { XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, LineChart, Line, BarChart, Bar, PieChart, Pie, Cell } from 'recharts';
import { apiService } from '../../services/apiService';
import AnalyticsPanel from '../../components/analytics/AnalyticsPanel';

const AnalyticsPage: React.FC = () => {
  const [dateRange, setDateRange] = useState('30'); // days
  const [granularity, setGranularity] = useState('weekly');
  const [priorityTrends, setPriorityTrends] = useState<any>(null);
  const [bertPerformance, setBertPerformance] = useState<any>(null);
  const [productivityMetrics, setProductivityMetrics] = useState<any>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [lastUpdated, setLastUpdated] = useState<Date | null>(null);
  const [error, setError] = useState<string | null>(null);

  const loadAnalyticsData = async () => {
    try {
      setIsLoading(true);
      setError(null);
      console.log('🔄 Loading analytics data...');
      
      const [trends, performance, productivity] = await Promise.all([
        apiService.getPriorityTrends().catch(err => {
          console.error('❌ Priority trends failed:', err);
          return null;
        }),
        apiService.getBertPerformance().catch(err => {
          console.error('❌ BERT performance failed:', err);
          return null;
        }),
        apiService.getProductivityMetrics().catch(err => {
          console.error('❌ Productivity metrics failed:', err);
          return null;
        })
      ]);

      console.log('✅ Analytics data loaded:', { trends, performance, productivity });
      
      setPriorityTrends(trends);
      setBertPerformance(performance);
      setProductivityMetrics(productivity);
      setLastUpdated(new Date());
    } catch (error) {
      console.error('❌ Error loading analytics data:', error);
      setError(error instanceof Error ? error.message : 'Failed to load analytics');
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    loadAnalyticsData();
  }, [dateRange, granularity]);

  const getTimeSeriesData = () => {
    if (!priorityTrends?.trends) {
      console.log('⚠️ No priority trends data available');
      return [];
    }
    
    return priorityTrends.trends.map((trend: any) => ({
      period: trend.period,
      totalEvents: trend.total_events,
      highPriority: trend.high_priority_percentage,
      critical: trend.critical_events,
      name: trend.period // for charts
    }));
  };

  const getProductivityData = () => {
    if (!productivityMetrics?.metrics?.patterns?.hourly_effectiveness) {
      console.log('⚠️ No productivity data available');
      return [];
    }
    
    return Object.entries(productivityMetrics.metrics.patterns.hourly_effectiveness)
      .map(([hour, score]) => ({
        hour: `${hour}:00`,
        score: score as number,
        name: `${hour}:00` // for charts
      }))
      .filter(item => item.score > 0);
  };

  const getPriorityDistribution = () => {
    if (!priorityTrends?.trends?.[0]?.priority_distribution) {
      console.log('⚠️ No priority distribution data available');
      return [];
    }
    
    const distribution = priorityTrends.trends[0].priority_distribution;
    return Object.entries(distribution)
      .filter(([_, data]: [string, any]) => data.count > 0)
      .map(([priority, data]: [string, any], index) => ({
        name: `Priority ${priority}`,
        value: data.count || 0,
        percentage: Math.round(data.percentage || 0),
        fill: ['#ef4444', '#f97316', '#eab308', '#22c55e', '#6b7280'][index % 5]
      }));
  };

  console.log('🎯 Analytics Page Render - Loading:', isLoading, 'Data:', { priorityTrends, bertPerformance, productivityMetrics });

  return (
    <div className="p-6 space-y-6 bg-gray-50 min-h-screen">
      {/* Header */}
      <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-gray-900 flex items-center">
              <ChartBarIcon className="h-6 w-6 mr-3 text-purple-600" />
              Analytics Dashboard
            </h1>
            <p className="text-gray-600 mt-1">
              Comprehensive insights and performance metrics
            </p>
          </div>
          
          <div className="flex items-center space-x-4">
            {lastUpdated && (
              <span className="text-sm text-gray-500">
                Updated {lastUpdated.toLocaleTimeString()}
              </span>
            )}
            <button
              onClick={loadAnalyticsData}
              disabled={isLoading}
              className="flex items-center space-x-2 px-4 py-2 bg-purple-600 hover:bg-purple-700 text-white rounded-lg transition-colors disabled:opacity-50"
            >
              <ArrowPathIcon className={`h-4 w-4 ${isLoading ? 'animate-spin' : ''}`} />
              <span>Refresh</span>
            </button>
          </div>
        </div>

        {/* Simple Filters */}
        <div className="mt-6 flex items-center space-x-4 p-4 bg-gray-50 rounded-lg">
          <div className="flex items-center space-x-2">
            <ClockIcon className="h-5 w-5 text-gray-500" />
            <span className="text-sm font-medium text-gray-700">Time Range:</span>
            <select
              value={dateRange}
              onChange={(e) => setDateRange(e.target.value)}
              className="border border-gray-200 rounded-md px-3 py-1 text-sm bg-white"
              aria-label="Select time range"
            >
              <option value="7">Last 7 days</option>
              <option value="30">Last 30 days</option>
              <option value="90">Last 90 days</option>
            </select>
          </div>

          <div className="flex items-center space-x-2">
            <ChevronDownIcon className="h-5 w-5 text-gray-500" />
            <span className="text-sm font-medium text-gray-700">Granularity:</span>
            <select
              value={granularity}
              onChange={(e) => setGranularity(e.target.value)}
              className="border border-gray-200 rounded-md px-3 py-1 text-sm bg-white"
              aria-label="Select granularity"
            >
              <option value="daily">Daily</option>
              <option value="weekly">Weekly</option>
              <option value="monthly">Monthly</option>
            </select>
          </div>
        </div>
      </div>

      {error && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4">
          <p className="text-red-700">Error loading analytics: {error}</p>
        </div>
      )}

      {isLoading ? (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {[...Array(4)].map((_, i) => (
            <div key={i} className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
              <div className="animate-pulse space-y-4">
                <div className="h-4 bg-gray-200 rounded w-1/3"></div>
                <div className="h-32 bg-gray-200 rounded"></div>
                <div className="space-y-2">
                  <div className="h-3 bg-gray-200 rounded"></div>
                  <div className="h-3 bg-gray-200 rounded w-2/3"></div>
                </div>
              </div>
            </div>
          ))}
        </div>
      ) : (
        <>
          {/* Enhanced Analytics Panel */}
          <AnalyticsPanel className="mb-6" />

          {/* Charts with Real Data */}
          <div className="grid grid-cols-1 xl:grid-cols-2 gap-6">
            
            {/* Priority Trends Over Time */}
            <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
              <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
                <ChartBarIcon className="h-5 w-5 mr-2 text-blue-600" />
                Priority Trends Over Time ({getTimeSeriesData().length} data points)
              </h3>
              
              {getTimeSeriesData().length > 0 ? (
                <div className="h-64">
                  <ResponsiveContainer width="100%" height="100%">
                    <LineChart data={getTimeSeriesData()}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="period" />
                      <YAxis />
                      <Tooltip />
                      <Line 
                        type="monotone" 
                        dataKey="totalEvents" 
                        stroke="#8b5cf6" 
                        strokeWidth={2}
                        name="Total Events"
                        dot={{ fill: '#8b5cf6', strokeWidth: 2, r: 4 }}
                      />
                      <Line 
                        type="monotone" 
                        dataKey="highPriority" 
                        stroke="#06b6d4" 
                        strokeWidth={2}
                        name="High Priority %"
                        dot={{ fill: '#06b6d4', strokeWidth: 2, r: 4 }}
                      />
                      <Line 
                        type="monotone" 
                        dataKey="critical" 
                        stroke="#ef4444" 
                        strokeWidth={2}
                        name="Critical Events"
                        dot={{ fill: '#ef4444', strokeWidth: 2, r: 4 }}
                      />
                    </LineChart>
                  </ResponsiveContainer>
                </div>
              ) : (
                <div className="h-64 flex items-center justify-center text-gray-500">
                  <div className="text-center">
                    <ChartBarIcon className="h-12 w-12 mx-auto mb-2 text-gray-300" />
                    <p>No trend data available</p>
                    <p className="text-sm">Priority trends: {priorityTrends ? 'Data exists but empty trends array' : 'No data loaded'}</p>
                  </div>
                </div>
              )}
            </div>

            {/* Priority Distribution */}
            <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">
                Priority Distribution ({getPriorityDistribution().length} categories)
              </h3>
              
              {getPriorityDistribution().length > 0 ? (
                <div className="h-64">
                  <ResponsiveContainer width="100%" height="100%">
                    <PieChart>
                      <Pie
                        data={getPriorityDistribution()}
                        cx="50%"
                        cy="50%"
                        outerRadius={80}
                        dataKey="value"
                        label={(entry) => `${entry.name}: ${entry.value}`}
                      >
                        {getPriorityDistribution().map((entry, index) => (
                          <Cell key={`cell-${index}`} fill={entry.fill} />
                        ))}
                      </Pie>
                      <Tooltip />
                    </PieChart>
                  </ResponsiveContainer>
                </div>
              ) : (
                <div className="h-64 flex items-center justify-center text-gray-500">
                  <p>No priority distribution data available</p>
                </div>
              )}
            </div>

            {/* Hourly Productivity */}
            <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
              <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
                <ClockIcon className="h-5 w-5 mr-2 text-green-600" />
                Hourly Productivity ({getProductivityData().length} data points)
              </h3>
              
              {getProductivityData().length > 0 ? (
                <div className="h-64">
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={getProductivityData()}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="hour" />
                      <YAxis />
                      <Tooltip />
                      <Bar dataKey="score" fill="#10b981" />
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              ) : (
                <div className="h-64 flex items-center justify-center text-gray-500">
                  <div className="text-center">
                    <ClockIcon className="h-12 w-12 mx-auto mb-2 text-gray-300" />
                    <p>No productivity patterns available</p>
                    <p className="text-sm">Productivity metrics: {productivityMetrics ? 'Data exists but no hourly patterns' : 'No data loaded'}</p>
                  </div>
                </div>
              )}
            </div>

            {/* System Overview */}
            <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
              <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
                <span className="mr-2">⚡</span>
                System Overview
              </h3>
              
              <div className="grid grid-cols-2 gap-4">
                <div className="text-center p-4 bg-blue-50 rounded-lg">
                  <div className="text-2xl font-bold text-blue-600">
                    {priorityTrends?.insights?.total_events_analyzed || 0}
                  </div>
                  <div className="text-sm text-gray-600">Total Events</div>
                </div>
                
                <div className="text-center p-4 bg-green-50 rounded-lg">
                  <div className="text-2xl font-bold text-green-600">
                    {bertPerformance?.classification_overview?.bert_adoption_rate || 0}%
                  </div>
                  <div className="text-sm text-gray-600">AI Adoption</div>
                </div>
                
                <div className="text-center p-4 bg-purple-50 rounded-lg">
                  <div className="text-2xl font-bold text-purple-600">
                    {Math.round(priorityTrends?.insights?.high_priority_rate || 0)}%
                  </div>
                  <div className="text-sm text-gray-600">High Priority</div>
                </div>
                
                <div className="text-center p-4 bg-orange-50 rounded-lg">
                  <div className="text-2xl font-bold text-orange-600">
                    {Math.round(productivityMetrics?.metrics?.overall_score || 0)}
                  </div>
                  <div className="text-sm text-gray-600">Productivity</div>
                </div>
              </div>
            </div>
          </div>
        </>
      )}
    </div>
  );
};

export default AnalyticsPage;
