// Centralized API base configuration for frontend services
// Use Vite env var if provided, otherwise default to backend-in-Docker on localhost:8000

type ViteEnv = { VITE_API_BASE?: string } | undefined;
const viteEnv: ViteEnv = (import.meta as unknown as { env?: { VITE_API_BASE?: string } }).env;
export const API_BASE: string = viteEnv?.VITE_API_BASE || 'http://127.0.0.1:8000';
export const API_V1: string = `${API_BASE}/api/v1`;
