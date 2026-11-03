// Backend location. Override with VITE_API_BASE_URL (e.g. in frontend/.env.local).
export const API_BASE_URL = (import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000').replace(
  /\/+$/,
  '',
)

export const ENDPOINTS = {
  health: `${API_BASE_URL}/`,
  predict: `${API_BASE_URL}/api/predict`,
}
