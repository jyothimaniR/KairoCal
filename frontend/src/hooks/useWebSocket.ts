import { useState, useEffect, useRef, useCallback } from 'react';
import type { Event } from '../services/apiService';

export interface WebSocketMessage {
  type: 'event_created' | 'event_updated' | 'event_deleted' | 'conflict_detected' | 'system_status';
  data: any;
  timestamp: string;
  user_id?: string;
}

export interface WebSocketOptions {
  url: string;
  reconnectInterval?: number;
  maxReconnectAttempts?: number;
  onMessage?: (message: WebSocketMessage) => void;
  onError?: (error: Event) => void;
  onStatusChange?: (status: 'connecting' | 'connected' | 'disconnected' | 'error') => void;
}

export interface UseWebSocketReturn {
  connectionStatus: 'connecting' | 'connected' | 'disconnected' | 'error';
  sendMessage: (message: WebSocketMessage) => void;
  lastMessage: WebSocketMessage | null;
  isConnected: boolean;
  reconnect: () => void;
  disconnect: () => void;
}

// Default WebSocket URL - can be overridden
const DEFAULT_WS_URL = process.env.NODE_ENV === 'production' 
  ? 'wss://api.kairocal.com/ws'
  : 'ws://localhost:8000/ws';

export const useWebSocket = (options: Partial<WebSocketOptions> = {}): UseWebSocketReturn => {
  const {
    url = DEFAULT_WS_URL,
    reconnectInterval = 3000,
    maxReconnectAttempts = 5,
    onMessage,
    onError,
    onStatusChange,
  } = options;

  const [connectionStatus, setConnectionStatus] = useState<'connecting' | 'connected' | 'disconnected' | 'error'>('disconnected');
  const [lastMessage, setLastMessage] = useState<WebSocketMessage | null>(null);
  
  const ws = useRef<WebSocket | null>(null);
  const reconnectAttempts = useRef(0);
  const reconnectTimeoutRef = useRef<NodeJS.Timeout | null>(null);
  const shouldReconnect = useRef(true);

  const updateStatus = useCallback((status: typeof connectionStatus) => {
    setConnectionStatus(status);
    onStatusChange?.(status);
  }, [onStatusChange]);

  const connect = useCallback(() => {
    if (ws.current?.readyState === WebSocket.OPEN) {
      return;
    }

    updateStatus('connecting');
    
    try {
      // Add user identification to WebSocket URL
      const wsUrl = `${url}?user_id=frontend-test-user&client=calendar`;
      ws.current = new WebSocket(wsUrl);

      ws.current.onopen = () => {
        console.log('📡 WebSocket connected');
        updateStatus('connected');
        reconnectAttempts.current = 0;
        
        // Send connection acknowledgment
        const ackMessage: WebSocketMessage = {
          type: 'system_status',
          data: { action: 'connect', client: 'calendar', timestamp: new Date().toISOString() },
          timestamp: new Date().toISOString(),
        };
        
        ws.current?.send(JSON.stringify(ackMessage));
      };

      ws.current.onmessage = (event) => {
        try {
          const message: WebSocketMessage = JSON.parse(event.data);
          console.log('📡 WebSocket message received:', message);
          
          setLastMessage(message);
          onMessage?.(message);
        } catch (error) {
          console.error('Error parsing WebSocket message:', error);
        }
      };

      ws.current.onclose = (event) => {
        console.log('📡 WebSocket disconnected:', event.code, event.reason);
        updateStatus('disconnected');
        
        // Attempt to reconnect if it wasn't intentional
        if (shouldReconnect.current && reconnectAttempts.current < maxReconnectAttempts) {
          console.log(`📡 Reconnecting WebSocket (attempt ${reconnectAttempts.current + 1}/${maxReconnectAttempts})...`);
          
          reconnectTimeoutRef.current = setTimeout(() => {
            reconnectAttempts.current++;
            connect();
          }, reconnectInterval);
        }
      };

      ws.current.onerror = (error) => {
        console.error('📡 WebSocket error:', error);
        updateStatus('error');
        onError?.(error as any);
      };

    } catch (error) {
      console.error('Failed to create WebSocket connection:', error);
      updateStatus('error');
    }
  }, [url, updateStatus, onMessage, onError, maxReconnectAttempts, reconnectInterval]);

  const disconnect = useCallback(() => {
    shouldReconnect.current = false;
    
    if (reconnectTimeoutRef.current) {
      clearTimeout(reconnectTimeoutRef.current);
    }
    
    if (ws.current) {
      ws.current.close(1000, 'Client disconnect');
      ws.current = null;
    }
    
    updateStatus('disconnected');
  }, [updateStatus]);

  const reconnect = useCallback(() => {
    disconnect();
    shouldReconnect.current = true;
    reconnectAttempts.current = 0;
    setTimeout(connect, 100);
  }, [disconnect, connect]);

  const sendMessage = useCallback((message: WebSocketMessage) => {
    if (ws.current?.readyState === WebSocket.OPEN) {
      try {
        ws.current.send(JSON.stringify(message));
        console.log('📡 WebSocket message sent:', message);
      } catch (error) {
        console.error('Error sending WebSocket message:', error);
      }
    } else {
      console.warn('Cannot send message: WebSocket not connected');
    }
  }, []);

  // Initialize connection
  useEffect(() => {
    connect();
    
    return () => {
      disconnect();
    };
  }, [connect, disconnect]);

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      if (reconnectTimeoutRef.current) {
        clearTimeout(reconnectTimeoutRef.current);
      }
    };
  }, []);

  return {
    connectionStatus,
    sendMessage,
    lastMessage,
    isConnected: connectionStatus === 'connected',
    reconnect,
    disconnect,
  };
};

// Real-time calendar updates hook
export const useCalendarWebSocket = (onEventUpdate?: () => void) => {
  const handleMessage = useCallback((message: WebSocketMessage) => {
    switch (message.type) {
      case 'event_created':
      case 'event_updated':
      case 'event_deleted':
        console.log('📅 Calendar event update received via WebSocket:', message.type);
        onEventUpdate?.();
        break;
      case 'conflict_detected':
        console.log('⚠️ Conflict detected via WebSocket:', message.data);
        // Could trigger a toast notification here
        break;
      case 'system_status':
        console.log('📊 System status update:', message.data);
        break;
      default:
        console.log('📡 Unknown WebSocket message type:', message.type);
    }
  }, [onEventUpdate]);

  const webSocket = useWebSocket({
    onMessage: handleMessage,
  });

  return webSocket;
};
