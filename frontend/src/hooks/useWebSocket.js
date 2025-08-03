/**
 * React Hook for WebSocket Integration
 * Provides easy WebSocket access in React components
 */

import { useState, useEffect, useRef, useCallback } from 'react';
import { webSocketClient, MESSAGE_TYPES, CONNECTION_STATES } from '../services/webSocketClient';

export const useWebSocket = (options = {}) => {
    const [connectionState, setConnectionState] = useState(CONNECTION_STATES.DISCONNECTED);
    const [isConnected, setIsConnected] = useState(false);
    const [metrics, setMetrics] = useState({});
    const [lastMessage, setLastMessage] = useState(null);
    const handlersRef = useRef(new Map());

    // Auto-connect option
    const { autoConnect = true, userId = null, authToken = null } = options;

    /**
     * Connect to WebSocket
     */
    const connect = useCallback(async (userIdParam = null, authTokenParam = null) => {
        try {
            const finalUserId = userIdParam || userId;
            const finalAuthToken = authTokenParam || authToken;
            
            await webSocketClient.connect(finalAuthToken, finalUserId);
        } catch (error) {
            console.error('❌ useWebSocket: Connection failed', error);
        }
    }, [userId, authToken]);

    /**
     * Disconnect from WebSocket
     */
    const disconnect = useCallback(() => {
        webSocketClient.disconnect();
    }, []);

    /**
     * Send message
     */
    const sendMessage = useCallback(async (messageType, payload, callback) => {
        return await webSocketClient.sendMessage(messageType, payload, callback);
    }, []);

    /**
     * Subscribe to message type
     */
    const subscribe = useCallback((messageType, handler) => {
        // Store handler reference for cleanup
        if (!handlersRef.current.has(messageType)) {
            handlersRef.current.set(messageType, []);
        }
        handlersRef.current.get(messageType).push(handler);

        // Register with WebSocket client
        webSocketClient.on(messageType, handler);

        // Return unsubscribe function
        return () => {
            const handlers = handlersRef.current.get(messageType) || [];
            const index = handlers.indexOf(handler);
            if (index > -1) {
                handlers.splice(index, 1);
            }
            webSocketClient.off(messageType, handler);
        };
    }, []);

    /**
     * Send voice transcription
     */
    const sendVoiceTranscription = useCallback(async (audioBlob, options = {}) => {
        return await webSocketClient.sendVoiceTranscription(audioBlob, options);
    }, []);

    /**
     * Send event creation
     */
    const sendEventCreation = useCallback(async (eventData) => {
        return await webSocketClient.sendEventCreation(eventData);
    }, []);

    /**
     * Send event update
     */
    const sendEventUpdate = useCallback(async (eventId, updates) => {
        return await webSocketClient.sendEventUpdate(eventId, updates);
    }, []);

    /**
     * Update presence
     */
    const updatePresence = useCallback(async (status, activity = null) => {
        return await webSocketClient.updatePresence(status, activity);
    }, []);

    /**
     * Request user presence
     */
    const requestUserPresence = useCallback(async (userIds = []) => {
        return await webSocketClient.requestUserPresence(userIds);
    }, []);

    // Set up connection state monitoring
    useEffect(() => {
        const handleConnectionStateChange = (stateData) => {
            setConnectionState(stateData.state);
            setIsConnected(stateData.state === CONNECTION_STATES.CONNECTED);
            setMetrics(stateData.metrics);
        };

        webSocketClient.on('connection_state_change', handleConnectionStateChange);

        // Initial state
        setConnectionState(webSocketClient.getConnectionState());
        setIsConnected(webSocketClient.isConnected());
        setMetrics(webSocketClient.getMetrics());

        return () => {
            webSocketClient.off('connection_state_change', handleConnectionStateChange);
        };
    }, []);

    // Auto-connect on mount
    useEffect(() => {
        if (autoConnect && !isConnected && connectionState === CONNECTION_STATES.DISCONNECTED) {
            connect();
        }
    }, [autoConnect, isConnected, connectionState, connect]);

    // Cleanup on unmount
    useEffect(() => {
        return () => {
            // Clean up all registered handlers
            handlersRef.current.forEach((handlers, messageType) => {
                handlers.forEach(handler => {
                    webSocketClient.off(messageType, handler);
                });
            });
            handlersRef.current.clear();
        };
    }, []);

    return {
        // Connection management
        connect,
        disconnect,
        isConnected,
        connectionState,
        metrics,

        // Messaging
        sendMessage,
        subscribe,
        lastMessage,

        // Specialized methods
        sendVoiceTranscription,
        sendEventCreation,
        sendEventUpdate,
        updatePresence,
        requestUserPresence
    };
};

/**
 * Hook for listening to specific message types
 */
export const useWebSocketMessage = (messageType, handler, dependencies = []) => {
    const { subscribe } = useWebSocket({ autoConnect: false });

    useEffect(() => {
        if (!messageType || !handler) return;

        const unsubscribe = subscribe(messageType, handler);
        return unsubscribe;
    }, [messageType, subscribe, ...dependencies]);
};

/**
 * Hook for real-time event updates
 */
export const useRealtimeEvents = () => {
    const [events, setEvents] = useState([]);
    const [conflicts, setConflicts] = useState([]);
    const [reminders, setReminders] = useState([]);
    const [priorityAlerts, setPriorityAlerts] = useState([]);

    const { subscribe } = useWebSocket();

    useEffect(() => {
        // Event created
        const unsubscribeEventCreated = subscribe(MESSAGE_TYPES.EVENT_CREATED, (data) => {
            setEvents(prev => [data.payload.event, ...prev]);
            console.log('📅 Real-time: Event created', data.payload.event);
        });

        // Event updated
        const unsubscribeEventUpdated = subscribe(MESSAGE_TYPES.EVENT_UPDATED, (data) => {
            setEvents(prev => prev.map(event => 
                event.id === data.payload.event.id ? data.payload.event : event
            ));
            console.log('📝 Real-time: Event updated', data.payload.event);
        });

        // Event deleted
        const unsubscribeEventDeleted = subscribe(MESSAGE_TYPES.EVENT_DELETED, (data) => {
            setEvents(prev => prev.filter(event => event.id !== data.payload.event_id));
            console.log('🗑️ Real-time: Event deleted', data.payload.event_id);
        });

        // Conflict detected
        const unsubscribeConflict = subscribe(MESSAGE_TYPES.CONFLICT_DETECTED, (data) => {
            setConflicts(prev => [data.payload.conflict, ...prev]);
            console.log('⚠️ Real-time: Conflict detected', data.payload.conflict);
        });

        // Reminder notification
        const unsubscribeReminder = subscribe(MESSAGE_TYPES.REMINDER_NOTIFICATION, (data) => {
            setReminders(prev => [data.payload.reminder, ...prev]);
            console.log('🔔 Real-time: Reminder', data.payload.reminder);
        });

        // Priority alert
        const unsubscribePriorityAlert = subscribe(MESSAGE_TYPES.PRIORITY_ALERT, (data) => {
            setPriorityAlerts(prev => [data.payload.alert, ...prev]);
            console.log('🚨 Real-time: Priority alert', data.payload.alert);
        });

        return () => {
            unsubscribeEventCreated();
            unsubscribeEventUpdated();
            unsubscribeEventDeleted();
            unsubscribeConflict();
            unsubscribeReminder();
            unsubscribePriorityAlert();
        };
    }, [subscribe]);

    // Clear notifications
    const clearConflicts = useCallback(() => setConflicts([]), []);
    const clearReminders = useCallback(() => setReminders([]), []);
    const clearPriorityAlerts = useCallback(() => setPriorityAlerts([]), []);

    return {
        events,
        conflicts,
        reminders,
        priorityAlerts,
        clearConflicts,
        clearReminders,
        clearPriorityAlerts
    };
};

/**
 * Hook for user presence tracking
 */
export const useUserPresence = (userIds = []) => {
    const [userPresence, setUserPresence] = useState({});
    const [onlineUsers, setOnlineUsers] = useState([]);

    const { subscribe, requestUserPresence } = useWebSocket();

    useEffect(() => {
        // Subscribe to presence updates
        const unsubscribe = subscribe(MESSAGE_TYPES.USER_PRESENCE, (data) => {
            const { user_id, presence } = data.payload;
            
            setUserPresence(prev => ({
                ...prev,
                [user_id]: presence
            }));

            // Update online users list
            if (presence.status === 'online') {
                setOnlineUsers(prev => [...new Set([...prev, user_id])]);
            } else {
                setOnlineUsers(prev => prev.filter(id => id !== user_id));
            }

            console.log('👤 Real-time: User presence updated', { user_id, presence });
        });

        return unsubscribe;
    }, [subscribe]);

    // Request presence for specific users
    useEffect(() => {
        if (userIds.length > 0) {
            requestUserPresence(userIds);
        }
    }, [userIds, requestUserPresence]);

    return {
        userPresence,
        onlineUsers,
        isUserOnline: (userId) => onlineUsers.includes(userId),
        getUserPresence: (userId) => userPresence[userId] || { status: 'unknown' }
    };
};

/**
 * Hook for voice transcription
 */
export const useVoiceTranscription = () => {
    const [isRecording, setIsRecording] = useState(false);
    const [transcriptionResult, setTranscriptionResult] = useState(null);
    const [error, setError] = useState(null);
    const mediaRecorderRef = useRef(null);
    const chunksRef = useRef([]);

    const { sendVoiceTranscription, subscribe } = useWebSocket();

    useEffect(() => {
        // Subscribe to transcription results
        const unsubscribe = subscribe(MESSAGE_TYPES.VOICE_TRANSCRIPTION, (data) => {
            setTranscriptionResult(data.payload.transcription);
            setIsRecording(false);
            console.log('🎤 Real-time: Voice transcription result', data.payload.transcription);
        });

        return unsubscribe;
    }, [subscribe]);

    const startRecording = useCallback(async () => {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            
            mediaRecorderRef.current = new MediaRecorder(stream, {
                mimeType: 'audio/webm;codecs=opus'
            });
            
            chunksRef.current = [];
            
            mediaRecorderRef.current.ondataavailable = (event) => {
                if (event.data.size > 0) {
                    chunksRef.current.push(event.data);
                }
            };

            mediaRecorderRef.current.onstop = async () => {
                const audioBlob = new Blob(chunksRef.current, { type: 'audio/webm' });
                
                // Send to WebSocket
                await sendVoiceTranscription(audioBlob, {
                    format: 'webm',
                    enhanced: true
                });

                // Clean up
                stream.getTracks().forEach(track => track.stop());
            };

            mediaRecorderRef.current.start();
            setIsRecording(true);
            setError(null);
            setTranscriptionResult(null);

        } catch (err) {
            setError(err.message);
            console.error('❌ Voice recording failed:', err);
        }
    }, [sendVoiceTranscription]);

    const stopRecording = useCallback(() => {
        if (mediaRecorderRef.current && isRecording) {
            mediaRecorderRef.current.stop();
        }
    }, [isRecording]);

    return {
        isRecording,
        transcriptionResult,
        error,
        startRecording,
        stopRecording
    };
};

export default useWebSocket;
