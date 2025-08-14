import { useState, useEffect, useCallback } from 'react';
import { apiService } from '../services/apiService';

export interface SystemHealthSummary {
  voice: {
    status: 'healthy' | 'unavailable' | 'error';
    services?: Record<string, string>;
  };
  analytics: {
    status: 'healthy' | 'unavailable' | 'error';
    details?: Record<string, unknown>;
  };
  bert: {
    status: 'healthy' | 'unavailable' | 'error';
    details?: Record<string, unknown>;
  };
}

/**
 * UNIFIED SYSTEM HEALTH HOOK
 * Single source of truth for all system status indicators
 * Ensures consistent BERT status across ALL UI components
 */
export function useSystemHealth() {
  const [systemHealth, setSystemHealth] = useState<SystemHealthSummary | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const refreshSystemHealth = useCallback(async () => {
    try {
      setError(null);
      const health = await apiService.getSystemHealth();
      
      // Ensure consistent structure across all components
      const normalizedHealth: SystemHealthSummary = {
        voice: {
          status: health.voice?.status || 'error'
        },
        analytics: {
          status: health.analytics?.status || 'error'
        },
        // BERT status mirrors analytics since they're the same service
        bert: {
          status: health.bert?.status || health.analytics?.status || 'error'
        }
      };
      
      setSystemHealth(normalizedHealth);
      console.log('🔧 System Health Updated:', normalizedHealth);
    } catch (err) {
      console.error('❌ System Health Check Failed:', err);
      setError(err instanceof Error ? err.message : 'Health check failed');
      
      // Fallback status when API fails
      setSystemHealth({
        voice: { status: 'error' },
        analytics: { status: 'error' },
        bert: { status: 'error' }
      });
    } finally {
      setIsLoading(false);
    }
  }, []);

  // Auto-refresh every 30 seconds for real-time status
  useEffect(() => {
    refreshSystemHealth();
    const interval = setInterval(refreshSystemHealth, 30000);
    return () => clearInterval(interval);
  }, [refreshSystemHealth]);

  return {
    systemHealth,
    isLoading,
    error,
    refreshSystemHealth,
    // Convenience getters for consistent status across components
    isVoiceHealthy: systemHealth?.voice?.status === 'healthy',
    isBertHealthy: systemHealth?.bert?.status === 'healthy',
    isAnalyticsHealthy: systemHealth?.analytics?.status === 'healthy'
  };
}
