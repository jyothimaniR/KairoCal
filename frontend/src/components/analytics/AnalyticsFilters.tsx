import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  FunnelIcon,
  CalendarDaysIcon,
  ChevronDownIcon,
  AdjustmentsHorizontalIcon,
  ArrowTrendingUpIcon
} from '@heroicons/react/24/outline';

export interface FilterConfig {
  dateRange: {
    start: string;
    end: string;
    preset: string;
  };
  priority: {
    levels: number[];
    showAll: boolean;
  };
  timeGranularity: string;
  dataTypes: {
    priorityTrends: boolean;
    bertPerformance: boolean;
    productivityMetrics: boolean;
  };
  comparison: {
    enabled: boolean;
    period: string;
  };
  advanced: {
    minEventThreshold: number;
    confidenceLevel: number;
    excludeWeekends: boolean;
  };
}

interface AnalyticsFiltersProps {
  config: FilterConfig;
  onChange: (config: FilterConfig) => void;
  onReset: () => void;
  className?: string;
  variant?: 'compact' | 'expanded';
}

const AnalyticsFilters: React.FC<AnalyticsFiltersProps> = ({
  config,
  onChange,
  onReset,
  className = '',
  variant = 'compact'
}) => {
  const [isExpanded, setIsExpanded] = useState(variant === 'expanded');
  const [activeTab, setActiveTab] = useState<'basic' | 'advanced' | 'comparison'>('basic');

  const datePresets = [
    { label: 'Last 7 days', value: '7', start: -7, end: 0 },
    { label: 'Last 30 days', value: '30', start: -30, end: 0 },
    { label: 'Last 60 days', value: '60', start: -60, end: 0 },
    { label: 'Last 90 days', value: '90', start: -90, end: 0 },
    { label: 'Last 6 months', value: '180', start: -180, end: 0 },
    { label: 'Custom', value: 'custom', start: 0, end: 0 }
  ];

  const priorityLevels = [
    { label: 'Critical', value: 4, color: 'red' },
    { label: 'High', value: 3, color: 'orange' },
    { label: 'Medium', value: 2, color: 'yellow' },
    { label: 'Low', value: 1, color: 'green' },
    { label: 'None', value: 0, color: 'gray' }
  ];

  const granularityOptions = [
    { label: 'Hourly', value: 'hourly' },
    { label: 'Daily', value: 'daily' },
    { label: 'Weekly', value: 'weekly' },
    { label: 'Monthly', value: 'monthly' }
  ];

  const comparisonPeriods = [
    { label: 'Previous period', value: 'previous' },
    { label: '30 days ago', value: '30' },
    { label: '60 days ago', value: '60' },
    { label: '90 days ago', value: '90' }
  ];

  const updateConfig = (updates: Partial<FilterConfig>) => {
    onChange({ ...config, ...updates });
  };

  const updateDateRange = (preset: string) => {
    if (preset === 'custom') {
      updateConfig({
        dateRange: { ...config.dateRange, preset }
      });
      return;
    }

    const presetConfig = datePresets.find(p => p.value === preset);
    if (presetConfig) {
      const endDate = new Date();
      const startDate = new Date();
      startDate.setDate(startDate.getDate() + presetConfig.start);

      updateConfig({
        dateRange: {
          preset,
          start: startDate.toISOString().split('T')[0],
          end: endDate.toISOString().split('T')[0]
        }
      });
    }
  };

  const togglePriorityLevel = (level: number) => {
    const newLevels = config.priority.levels.includes(level)
      ? config.priority.levels.filter(l => l !== level)
      : [...config.priority.levels, level];

    updateConfig({
      priority: {
        ...config.priority,
        levels: newLevels,
        showAll: newLevels.length === priorityLevels.length
      }
    });
  };

  const resetFilters = () => {
    onReset();
    setActiveTab('basic');
  };

  const getActiveFilterCount = () => {
    let count = 0;
    
    if (config.dateRange.preset !== '30') count++;
    if (!config.priority.showAll) count++;
    if (config.timeGranularity !== 'weekly') count++;
    if (config.comparison.enabled) count++;
    if (config.advanced.minEventThreshold > 0) count++;
    if (config.advanced.excludeWeekends) count++;
    
    return count;
  };

  const activeFilterCount = getActiveFilterCount();

  return (
    <div className={`bg-white rounded-lg border border-gray-200 ${className}`}>
      {/* Header */}
      <div className="flex items-center justify-between p-4 border-b border-gray-100">
        <div className="flex items-center space-x-2">
          <FunnelIcon className="h-5 w-5 text-gray-500" />
          <span className="text-sm font-medium text-gray-900">Filters</span>
          {activeFilterCount > 0 && (
            <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
              {activeFilterCount} active
            </span>
          )}
        </div>

        <div className="flex items-center space-x-2">
          {activeFilterCount > 0 && (
            <button
              onClick={resetFilters}
              className="text-xs text-gray-500 hover:text-gray-700 transition-colors"
            >
              Reset
            </button>
          )}
          <button
            onClick={() => setIsExpanded(!isExpanded)}
            className="flex items-center space-x-1 text-sm text-gray-600 hover:text-gray-900 transition-colors"
          >
            <span>{isExpanded ? 'Collapse' : 'Expand'}</span>
            <ChevronDownIcon 
              className={`h-4 w-4 transform transition-transform ${isExpanded ? 'rotate-180' : ''}`} 
            />
          </button>
        </div>
      </div>

      <AnimatePresence>
        {isExpanded && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: 'auto', opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            transition={{ duration: 0.2 }}
          >
            {/* Tabs */}
            <div className="flex border-b border-gray-100">
              {[
                { key: 'basic', label: 'Basic', icon: CalendarDaysIcon },
                { key: 'advanced', label: 'Advanced', icon: AdjustmentsHorizontalIcon },
                { key: 'comparison', label: 'Compare', icon: ArrowTrendingUpIcon }
              ].map((tab) => {
                const Icon = tab.icon;
                return (
                  <button
                    key={tab.key}
                    onClick={() => setActiveTab(tab.key as any)}
                    className={`flex items-center space-x-2 px-4 py-2 text-sm font-medium border-b-2 transition-colors ${
                      activeTab === tab.key
                        ? 'border-blue-500 text-blue-600'
                        : 'border-transparent text-gray-500 hover:text-gray-700'
                    }`}
                  >
                    <Icon className="h-4 w-4" />
                    <span>{tab.label}</span>
                  </button>
                );
              })}
            </div>

            {/* Tab Content */}
            <div className="p-4 space-y-4">
              {activeTab === 'basic' && (
                <>
                  {/* Date Range */}
                  <div className="space-y-2">
                    <label className="text-sm font-medium text-gray-900">Date Range</label>
                    <select
                      value={config.dateRange.preset}
                      onChange={(e) => updateDateRange(e.target.value)}
                      className="w-full border border-gray-200 rounded-md px-3 py-2 text-sm bg-white"
                      aria-label="Select date range"
                    >
                      {datePresets.map((preset) => (
                        <option key={preset.value} value={preset.value}>
                          {preset.label}
                        </option>
                      ))}
                    </select>
                    
                    {config.dateRange.preset === 'custom' && (
                      <div className="grid grid-cols-2 gap-2 mt-2">
                        <input
                          type="date"
                          value={config.dateRange.start}
                          onChange={(e) => updateConfig({
                            dateRange: { ...config.dateRange, start: e.target.value }
                          })}
                          className="border border-gray-200 rounded-md px-3 py-2 text-sm"
                          aria-label="Start date"
                        />
                        <input
                          type="date"
                          value={config.dateRange.end}
                          onChange={(e) => updateConfig({
                            dateRange: { ...config.dateRange, end: e.target.value }
                          })}
                          className="border border-gray-200 rounded-md px-3 py-2 text-sm"
                          aria-label="End date"
                        />
                      </div>
                    )}
                  </div>

                  {/* Priority Levels */}
                  <div className="space-y-2">
                    <label className="text-sm font-medium text-gray-900">Priority Levels</label>
                    <div className="flex flex-wrap gap-2">
                      {priorityLevels.map((priority) => (
                        <button
                          key={priority.value}
                          onClick={() => togglePriorityLevel(priority.value)}
                          className={`flex items-center space-x-2 px-3 py-1 rounded-full text-xs font-medium transition-colors ${
                            config.priority.levels.includes(priority.value)
                              ? 'bg-blue-100 text-blue-800 ring-1 ring-blue-200'
                              : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                          }`}
                        >
                          <div className={`w-2 h-2 rounded-full ${
                            priority.color === 'red' ? 'bg-red-500' :
                            priority.color === 'orange' ? 'bg-orange-500' :
                            priority.color === 'yellow' ? 'bg-yellow-500' :
                            priority.color === 'green' ? 'bg-green-500' :
                            'bg-gray-500'
                          }`} />
                          <span>{priority.label}</span>
                        </button>
                      ))}
                    </div>
                  </div>

                  {/* Time Granularity */}
                  <div className="space-y-2">
                    <label className="text-sm font-medium text-gray-900">Time Granularity</label>
                    <select
                      value={config.timeGranularity}
                      onChange={(e) => updateConfig({ timeGranularity: e.target.value })}
                      className="w-full border border-gray-200 rounded-md px-3 py-2 text-sm bg-white"
                      aria-label="Select time granularity"
                    >
                      {granularityOptions.map((option) => (
                        <option key={option.value} value={option.value}>
                          {option.label}
                        </option>
                      ))}
                    </select>
                  </div>
                </>
              )}

              {activeTab === 'advanced' && (
                <>
                  {/* Data Types */}
                  <div className="space-y-2">
                    <label className="text-sm font-medium text-gray-900">Data Types</label>
                    <div className="space-y-2">
                      {[
                        { key: 'priorityTrends', label: 'Priority Trends', icon: '📊' },
                        { key: 'bertPerformance', label: 'BERT Performance', icon: '🤖' },
                        { key: 'productivityMetrics', label: 'Productivity Metrics', icon: '⚡' }
                      ].map((type) => (
                        <label key={type.key} className="flex items-center space-x-2">
                          <input
                            type="checkbox"
                            checked={config.dataTypes[type.key as keyof typeof config.dataTypes]}
                            onChange={(e) => updateConfig({
                              dataTypes: {
                                ...config.dataTypes,
                                [type.key]: e.target.checked
                              }
                            })}
                            className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                          />
                          <span className="text-sm text-gray-700">
                            {type.icon} {type.label}
                          </span>
                        </label>
                      ))}
                    </div>
                  </div>

                  {/* Minimum Event Threshold */}
                  <div className="space-y-2">
                    <label className="text-sm font-medium text-gray-900">
                      Minimum Events Threshold: {config.advanced.minEventThreshold}
                    </label>
                    <input
                      type="range"
                      min="0"
                      max="20"
                      value={config.advanced.minEventThreshold}
                      onChange={(e) => updateConfig({
                        advanced: {
                          ...config.advanced,
                          minEventThreshold: parseInt(e.target.value)
                        }
                      })}
                      className="w-full"
                      aria-label="Minimum events threshold"
                    />
                  </div>

                  {/* Advanced Options */}
                  <div className="space-y-2">
                    <label className="text-sm font-medium text-gray-900">Options</label>
                    <div className="space-y-2">
                      <label className="flex items-center space-x-2">
                        <input
                          type="checkbox"
                          checked={config.advanced.excludeWeekends}
                          onChange={(e) => updateConfig({
                            advanced: {
                              ...config.advanced,
                              excludeWeekends: e.target.checked
                            }
                          })}
                          className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                        />
                        <span className="text-sm text-gray-700">Exclude weekends</span>
                      </label>
                    </div>
                  </div>
                </>
              )}

              {activeTab === 'comparison' && (
                <>
                  {/* Enable Comparison */}
                  <div className="space-y-2">
                    <label className="flex items-center space-x-2">
                      <input
                        type="checkbox"
                        checked={config.comparison.enabled}
                        onChange={(e) => updateConfig({
                          comparison: {
                            ...config.comparison,
                            enabled: e.target.checked
                          }
                        })}
                        className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                      />
                      <span className="text-sm font-medium text-gray-900">Enable Period Comparison</span>
                    </label>
                  </div>

                  {config.comparison.enabled && (
                    <div className="space-y-2">
                      <label className="text-sm font-medium text-gray-900">Compare With</label>
                      <select
                        value={config.comparison.period}
                        onChange={(e) => updateConfig({
                          comparison: {
                            ...config.comparison,
                            period: e.target.value
                          }
                        })}
                        className="w-full border border-gray-200 rounded-md px-3 py-2 text-sm bg-white"
                        aria-label="Select comparison period"
                      >
                        {comparisonPeriods.map((period) => (
                          <option key={period.value} value={period.value}>
                            {period.label}
                          </option>
                        ))}
                      </select>
                    </div>
                  )}

                  <div className="bg-blue-50 p-3 rounded-lg">
                    <p className="text-sm text-blue-700">
                      💡 <strong>Tip:</strong> Comparison mode will show current period data alongside 
                      historical data to help identify trends and changes.
                    </p>
                  </div>
                </>
              )}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};

export default AnalyticsFilters;
