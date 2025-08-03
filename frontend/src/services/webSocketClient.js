/**
 * Enterprise WebSocket Client for KairoCal Frontend
 * Auto-reconnection, message queuing, and real-time event handling
 */

import { io, Socket } from 'socket.io-client';

// Message types enum
export const MESSAGE_TYPES = {
    EVENT_CREATED: 'event_created',
    EVENT_UPDATED: 'event_updated',
    EVENT_DELETED: 'event_deleted',
    REMINDER_NOTIFICATION: 'reminder_notification',
    CONFLICT_DETECTED: 'conflict_detected',
    USER_PRESENCE: 'user_presence',
    SYSTEM_BROADCAST: 'system_broadcast',
    PRIORITY_ALERT: 'priority_alert',
    VOICE_TRANSCRIPTION: 'voice_transcription'
};

// Connection states
export const CONNECTION_STATES = {
    CONNECTING: 'connecting',
    CONNECTED: 'connected',
    DISCONNECTED: 'disconnected',
    RECONNECTING: 'reconnecting',
    ERROR: 'error'
};

class WebSocketClient {
    constructor(options = {}) {
        this.config = {
            url: options.url || 'ws://localhost:8000',
            autoConnect: options.autoConnect !== false,
            reconnection: options.reconnection !== false,
            reconnectionDelay: options.reconnectionDelay || 1000,
            reconnectionDelayMax: options.reconnectionDelayMax || 5000,
            maxReconnectionAttempts: options.maxReconnectionAttempts || 5,
            timeout: options.timeout || 20000,
            forceNew: options.forceNew || true,
            transports: options.transports || ['websocket', 'polling']
        };

        this.socket = null;
        this.connectionState = CONNECTION_STATES.DISCONNECTED;
        this.messageQueue = [];
        this.eventHandlers = new Map();
        this.reconnectAttempts = 0;
        this.latencyHistory = [];
        this.maxLatencyHistory = 100;
        
        // User and device information
        this.userId = null;
        this.deviceInfo = null;
        this.authToken = null;
        
        // Metrics
        this.metrics = {
            messagesReceived: 0,
            messagesSent: 0,
            reconnections: 0,
            connectionErrors: 0,
            averageLatency: 0
        };

        // Auto-initialize if configured
        if (this.config.autoConnect) {
            this.connect();
        }
    }

    /**
     * Connect to WebSocket server
     */
    async connect(authToken = null, userId = null) {
        try {
            this.authToken = authToken;
            this.userId = userId;
            this.connectionState = CONNECTION_STATES.CONNECTING;
            
            // Gather device information
            this.deviceInfo = this._getDeviceInfo();
            
            // Socket.IO options
            const socketOptions = {
                ...this.config,
                auth: {
                    token: this.authToken,
                    userId: this.userId,
                    deviceInfo: this.deviceInfo
                },
                query: {
                    userId: this.userId,
                    deviceId: this.deviceInfo.deviceId
                }
            };

            // Create socket connection
            this.socket = io(this.config.url, socketOptions);

            // Set up event listeners
            this._setupEventListeners();

            console.log('🔌 WebSocket: Connecting...', {
                url: this.config.url,
                userId: this.userId,
                deviceId: this.deviceInfo.deviceId
            });

        } catch (error) {
            console.error('❌ WebSocket: Connection failed', error);
            this.connectionState = CONNECTION_STATES.ERROR;
            this._notifyConnectionStateChange();
            throw error;
        }
    }

    /**
     * Disconnect from WebSocket server
     */
    disconnect() {
        if (this.socket) {
            this.socket.disconnect();
            this.socket = null;
        }
        this.connectionState = CONNECTION_STATES.DISCONNECTED;
        this._notifyConnectionStateChange();
        console.log('👋 WebSocket: Disconnected');
    }

    /**
     * Send message to server
     */
    async sendMessage(messageType, payload = {}, callback = null) {
        try {
            if (!this.isConnected()) {
                // Queue message if not connected
                this.messageQueue.push({ messageType, payload, callback, timestamp: Date.now() });
                console.warn('📦 WebSocket: Message queued (not connected)', messageType);
                return false;
            }

            const message = {
                type: messageType,
                payload: payload,
                timestamp: Date.now(),
                messageId: this._generateMessageId()
            };

            // Send message with latency tracking
            const startTime = performance.now();
            
            if (callback) {
                this.socket.emit(messageType, message, (response) => {
                    const latency = performance.now() - startTime;
                    this._updateLatency(latency);
                    callback(response);
                });
            } else {
                this.socket.emit(messageType, message);
            }

            this.metrics.messagesSent++;
            console.log('📤 WebSocket: Message sent', messageType, payload);
            return true;

        } catch (error) {
            console.error('❌ WebSocket: Send message failed', error);
            return false;
        }
    }

    /**
     * Subscribe to message type
     */
    on(messageType, handler) {
        if (!this.eventHandlers.has(messageType)) {
            this.eventHandlers.set(messageType, []);
        }
        this.eventHandlers.get(messageType).push(handler);

        // If socket is connected, also register with socket
        if (this.socket) {
            this.socket.on(messageType, handler);
        }

        console.log('📝 WebSocket: Handler registered for', messageType);
    }

    /**
     * Unsubscribe from message type
     */
    off(messageType, handler = null) {
        if (handler) {
            const handlers = this.eventHandlers.get(messageType) || [];
            const index = handlers.indexOf(handler);
            if (index > -1) {
                handlers.splice(index, 1);
            }
            if (this.socket) {
                this.socket.off(messageType, handler);
            }
        } else {
            this.eventHandlers.delete(messageType);
            if (this.socket) {
                this.socket.off(messageType);
            }
        }
    }

    /**
     * Check if connected
     */
    isConnected() {
        return this.socket && this.socket.connected && this.connectionState === CONNECTION_STATES.CONNECTED;
    }

    /**
     * Get connection state
     */
    getConnectionState() {
        return this.connectionState;
    }

    /**
     * Get connection metrics
     */
    getMetrics() {
        return {
            ...this.metrics,
            connectionState: this.connectionState,
            queuedMessages: this.messageQueue.length,
            reconnectAttempts: this.reconnectAttempts,
            latencyHistory: this.latencyHistory.slice(-10) // Last 10 latency measurements
        };
    }

    /**
     * Send voice transcription request
     */
    async sendVoiceTranscription(audioBlob, options = {}) {
        try {
            // Convert audio blob to base64
            const audioData = await this._blobToBase64(audioBlob);
            
            return await this.sendMessage('voice_transcription', {
                audio_data: audioData,
                audio_format: options.format || 'webm',
                language: options.language || 'en',
                enhanced_processing: options.enhanced || true
            });
        } catch (error) {
            console.error('❌ WebSocket: Voice transcription failed', error);
            return false;
        }
    }

    /**
     * Send event creation
     */
    async sendEventCreation(eventData) {
        return await this.sendMessage(MESSAGE_TYPES.EVENT_CREATED, {
            event: eventData,
            timestamp: new Date().toISOString()
        });
    }

    /**
     * Send event update
     */
    async sendEventUpdate(eventId, updates) {
        return await this.sendMessage(MESSAGE_TYPES.EVENT_UPDATED, {
            event_id: eventId,
            updates: updates,
            timestamp: new Date().toISOString()
        });
    }

    /**
     * Request user presence information
     */
    async requestUserPresence(userIds = []) {
        return await this.sendMessage('get_user_presence', {
            user_ids: userIds
        });
    }

    /**
     * Update own presence
     */
    async updatePresence(status, activity = null) {
        return await this.sendMessage('update_presence', {
            status: status,
            activity: activity,
            timestamp: new Date().toISOString()
        });
    }

    /**
     * Set up socket event listeners
     */
    _setupEventListeners() {
        if (!this.socket) return;

        // Connection events
        this.socket.on('connect', () => {
            console.log('✅ WebSocket: Connected successfully');
            this.connectionState = CONNECTION_STATES.CONNECTED;
            this.reconnectAttempts = 0;
            this._notifyConnectionStateChange();
            this._processMessageQueue();
        });

        this.socket.on('disconnect', (reason) => {
            console.log('💔 WebSocket: Disconnected', reason);
            this.connectionState = CONNECTION_STATES.DISCONNECTED;
            this._notifyConnectionStateChange();
        });

        this.socket.on('connect_error', (error) => {
            console.error('❌ WebSocket: Connection error', error);
            this.connectionState = CONNECTION_STATES.ERROR;
            this.metrics.connectionErrors++;
            this._notifyConnectionStateChange();
            this._handleReconnection();
        });

        // Reconnection events
        this.socket.on('reconnect', (attemptNumber) => {
            console.log('🔄 WebSocket: Reconnected after', attemptNumber, 'attempts');
            this.metrics.reconnections++;
            this.reconnectAttempts = 0;
        });

        this.socket.on('reconnect_attempt', (attemptNumber) => {
            console.log('🔄 WebSocket: Reconnection attempt', attemptNumber);
            this.connectionState = CONNECTION_STATES.RECONNECTING;
            this.reconnectAttempts = attemptNumber;
            this._notifyConnectionStateChange();
        });

        this.socket.on('reconnect_failed', () => {
            console.error('❌ WebSocket: Reconnection failed');
            this.connectionState = CONNECTION_STATES.ERROR;
            this._notifyConnectionStateChange();
        });

        // Pong event for latency measurement
        this.socket.on('pong', (latency) => {
            this._updateLatency(latency);
        });

        // Register custom event handlers
        this.eventHandlers.forEach((handlers, messageType) => {
            handlers.forEach(handler => {
                this.socket.on(messageType, (data) => {
                    this.metrics.messagesReceived++;
                    handler(data);
                });
            });
        });

        // Auto-ping for latency measurement
        setInterval(() => {
            if (this.isConnected()) {
                this.socket.emit('ping');
            }
        }, 30000); // Every 30 seconds
    }

    /**
     * Handle reconnection logic
     */
    _handleReconnection() {
        if (this.reconnectAttempts >= this.config.maxReconnectionAttempts) {
            console.error('❌ WebSocket: Max reconnection attempts reached');
            this.connectionState = CONNECTION_STATES.ERROR;
            this._notifyConnectionStateChange();
            return;
        }

        const delay = Math.min(
            this.config.reconnectionDelay * Math.pow(2, this.reconnectAttempts),
            this.config.reconnectionDelayMax
        );

        setTimeout(() => {
            if (this.socket && !this.socket.connected) {
                this.socket.connect();
            }
        }, delay);
    }

    /**
     * Process queued messages
     */
    _processMessageQueue() {
        while (this.messageQueue.length > 0) {
            const { messageType, payload, callback } = this.messageQueue.shift();
            this.sendMessage(messageType, payload, callback);
        }
    }

    /**
     * Update latency metrics
     */
    _updateLatency(latency) {
        this.latencyHistory.push(latency);
        if (this.latencyHistory.length > this.maxLatencyHistory) {
            this.latencyHistory.shift();
        }
        
        // Calculate average latency
        const sum = this.latencyHistory.reduce((a, b) => a + b, 0);
        this.metrics.averageLatency = sum / this.latencyHistory.length;
    }

    /**
     * Get device information
     */
    _getDeviceInfo() {
        const navigator = window.navigator;
        const screen = window.screen;
        
        return {
            deviceId: this._getDeviceId(),
            deviceType: this._getDeviceType(),
            userAgent: navigator.userAgent,
            platform: navigator.platform,
            language: navigator.language,
            timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
            screenResolution: screen ? `${screen.width}x${screen.height}` : null,
            cookieEnabled: navigator.cookieEnabled,
            onLine: navigator.onLine
        };
    }

    /**
     * Get or generate device ID
     */
    _getDeviceId() {
        let deviceId = localStorage.getItem('kairo_device_id');
        if (!deviceId) {
            deviceId = 'device_' + Math.random().toString(36).substr(2, 16);
            localStorage.setItem('kairo_device_id', deviceId);
        }
        return deviceId;
    }

    /**
     * Detect device type
     */
    _getDeviceType() {
        const userAgent = navigator.userAgent.toLowerCase();
        
        if (/tablet|ipad|playbook|silk|(android(?!.*mobile))/.test(userAgent)) {
            return 'tablet';
        }
        if (/mobile|iphone|ipod|android|blackberry|opera|mini|windows\sce|palm|smartphone|iemobile/.test(userAgent)) {
            return 'mobile';
        }
        return 'desktop';
    }

    /**
     * Convert blob to base64
     */
    _blobToBase64(blob) {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.onloadend = () => {
                const base64 = reader.result.split(',')[1]; // Remove data:audio/webm;base64, prefix
                resolve(base64);
            };
            reader.onerror = reject;
            reader.readAsDataURL(blob);
        });
    }

    /**
     * Generate unique message ID
     */
    _generateMessageId() {
        return `msg_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    }

    /**
     * Notify connection state change
     */
    _notifyConnectionStateChange() {
        const stateChangeHandlers = this.eventHandlers.get('connection_state_change') || [];
        stateChangeHandlers.forEach(handler => {
            try {
                handler({
                    state: this.connectionState,
                    reconnectAttempts: this.reconnectAttempts,
                    metrics: this.getMetrics()
                });
            } catch (error) {
                console.error('❌ WebSocket: State change handler error', error);
            }
        });
    }
}

// Create global instance
export const webSocketClient = new WebSocketClient();

// Export default class
export default WebSocketClient;
