import { useState, useEffect, useCallback, useRef } from 'react';
import { apiService } from '../services/apiService';

export interface RefreshConfig {
  enabled: boolean;
  interval: number; // in milliseconds
  onError?: (error: Error) => void;
  onSuccess?: (data: any) => void;
}

export interface UseRealTimeDataOptions {
  refreshConfig?: RefreshConfig;
  initialLoad?: boolean;
}

export const useRealTimeData = (options: UseRealTimeDataOptions = {}) => {
  const {
    refreshConfig = { enabled: false, interval: 30000 },
    initialLoad = true
  } = options;

  const [priorityTrends, setPriorityTrends] = useState<any>(null);
  const [bertPerformance, setBertPerformance] = useState<any>(null);
  const [productivityMetrics, setProductivityMetrics] = useState<any>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [lastUpdated, setLastUpdated] = useState<Date | null>(null);
  
  const intervalRef = useRef<NodeJS.Timeout | null>(null);
  const isComponentMounted = useRef(true);

  const loadAnalyticsData = useCallback(async (isAutoRefresh = false) => {
    if (!isComponentMounted.current) return;

    try {
      if (!isAutoRefresh) setIsLoading(true);
      setError(null);

      const [trends, performance, productivity] = await Promise.all([
        apiService.getPriorityTrends(),
        apiService.getBertPerformance(),
        apiService.getProductivityMetrics().catch(() => null)
      ]);

      if (isComponentMounted.current) {
        setPriorityTrends(trends);
        setBertPerformance(performance);
        setProductivityMetrics(productivity);
        setLastUpdated(new Date());

        // Call success callback if provided
        refreshConfig.onSuccess?.({
          priorityTrends: trends,
          bertPerformance: performance,
          productivityMetrics: productivity
        });
      }
    } catch (err) {
      console.error('Error loading analytics data:', err);
      const errorMessage = err instanceof Error ? err.message : 'Failed to load analytics data';
      
      if (isComponentMounted.current) {
        setError(errorMessage);
        refreshConfig.onError?.(err instanceof Error ? err : new Error(errorMessage));
      }
    } finally {
      if (isComponentMounted.current && !isAutoRefresh) {
        setIsLoading(false);
      }
    }
  }, [refreshConfig]);

  const startAutoRefresh = useCallback(() => {
    if (intervalRef.current) {
      clearInterval(intervalRef.current);
    }

    if (refreshConfig.enabled && refreshConfig.interval > 0) {
      intervalRef.current = setInterval(() => {
        loadAnalyticsData(true);
      }, refreshConfig.interval);
    }
  }, [refreshConfig.enabled, refreshConfig.interval, loadAnalyticsData]);

  const stopAutoRefresh = useCallback(() => {
    if (intervalRef.current) {
      clearInterval(intervalRef.current);
      intervalRef.current = null;
    }
  }, []);

  const manualRefresh = useCallback(() => {
    loadAnalyticsData(false);
  }, [loadAnalyticsData]);

  // Initial load
  useEffect(() => {
    if (initialLoad) {
      loadAnalyticsData();
    }
  }, [loadAnalyticsData, initialLoad]);

  // Auto refresh management
  useEffect(() => {
    if (refreshConfig.enabled) {
      startAutoRefresh();
    } else {
      stopAutoRefresh();
    }

    return stopAutoRefresh;
  }, [refreshConfig.enabled, startAutoRefresh, stopAutoRefresh]);

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      isComponentMounted.current = false;
      stopAutoRefresh();
    };
  }, [stopAutoRefresh]);

  return {
    // Data
    priorityTrends,
    bertPerformance,
    productivityMetrics,
    
    // State
    isLoading,
    error,
    lastUpdated,
    isAutoRefreshEnabled: refreshConfig.enabled,
    refreshInterval: refreshConfig.interval,
    
    // Actions
    refresh: manualRefresh,
    startAutoRefresh,
    stopAutoRefresh
  };
};

// Hook for managing refresh intervals with different presets
export const useRefreshInterval = (initialInterval = 30000) => {
  const [interval, setInterval] = useState(initialInterval);
  const [enabled, setEnabled] = useState(false);

  const presets = [
    { label: '15 seconds', value: 15000, description: 'Very frequent updates' },
    { label: '30 seconds', value: 30000, description: 'Frequent updates' },
    { label: '1 minute', value: 60000, description: 'Regular updates' },
    { label: '5 minutes', value: 300000, description: 'Periodic updates' },
    { label: '15 minutes', value: 900000, description: 'Occasional updates' },
    { label: 'Manual only', value: 0, description: 'No automatic updates' }
  ];

  const getCurrentPreset = () => {
    return presets.find(preset => preset.value === interval) || presets[1];
  };

  const setPreset = (presetValue: number) => {
    setInterval(presetValue);
    setEnabled(presetValue > 0);
  };

  return {
    interval,
    enabled,
    presets,
    currentPreset: getCurrentPreset(),
    setInterval,
    setEnabled,
    setPreset
  };
};

// Hook for comparing different time periods
export const useComparisonPeriods = () => {
  const [primaryPeriod, setPrimaryPeriod] = useState('30'); // days
  const [comparisonPeriod, setComparisonPeriod] = useState('60'); // days
  const [comparisonEnabled, setComparisonEnabled] = useState(false);

  const periodOptions = [
    { label: '7 days', value: '7' },
    { label: '30 days', value: '30' },
    { label: '60 days', value: '60' },
    { label: '90 days', value: '90' },
    { label: '6 months', value: '180' },
    { label: '1 year', value: '365' }
  ];

  const calculateDateRange = (days: string) => {
    const endDate = new Date();
    const startDate = new Date();
    startDate.setDate(startDate.getDate() - parseInt(days));
    
    return {
      startDate: startDate.toISOString().split('T')[0],
      endDate: endDate.toISOString().split('T')[0],
      days: parseInt(days)
    };
  };

  const primaryRange = calculateDateRange(primaryPeriod);
  const comparisonRange = comparisonEnabled ? calculateDateRange(comparisonPeriod) : null;

  return {
    primaryPeriod,
    comparisonPeriod,
    comparisonEnabled,
    periodOptions,
    primaryRange,
    comparisonRange,
    setPrimaryPeriod,
    setComparisonPeriod,
    setComparisonEnabled
  };
};
