const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';

export async function apiFetch(endpoint: string, options: RequestInit = {}) {
  const token = typeof window !== 'undefined' ? localStorage.getItem('token') : null;

  const headers = {
    'Content-Type': 'application/json',
    ...(token ? { 'Authorization': `Bearer ${token}` } : {}),
    ...options.headers,
  };

  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    headers,
  });

  if (!response.ok) {
    if (response.status === 401) {
      if (typeof window !== 'undefined') {
        localStorage.removeItem('token');
        window.location.href = '/login';
      }
    }
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.detail || 'API request failed');
  }

  return response.json();
}

export const api = {
  login: (credentials: any) =>
    apiFetch('/users/login', {
      method: 'POST',
      body: JSON.stringify(credentials),
    }),

  getDashboardSummary: () =>
    apiFetch('/dashboard/summary'),

  getDevices: (limit = 10, offset = 0) =>
    apiFetch(`/devices?limit=${limit}&offset=${offset}`),

  createDevice: (data: any) =>
    apiFetch('/devices', {
      method: 'POST',
      body: JSON.stringify(data),
    }),

  getTrafficLogs: (limit = 100, offset = 0) =>
    apiFetch(`/logs?limit=${limit}&offset=${offset}`),


  register: (data: {
    username: string;
    email: string;
    password: string;
  }) =>
    apiFetch('/users/register', {
      method: 'POST',
      body: JSON.stringify(data),
    }),
};

