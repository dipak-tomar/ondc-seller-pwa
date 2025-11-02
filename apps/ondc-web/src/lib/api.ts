import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

export const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const authApi = {
  requestOTP: (data: { email?: string; phone?: string }) =>
    api.post('/auth/request-otp', data),
  verifyOTP: (data: { email?: string; phone?: string; otp: string }) =>
    api.post('/auth/verify-otp', data),
  getMe: () => api.get('/auth/me'),
};

export const productsApi = {
  list: (params?: any) => api.get('/products', { params }),
  create: (data: any) => api.post('/products', data),
  update: (id: string, data: any) => api.put(`/products/${id}`, data),
  bulkUpload: (file: File) => {
    const formData = new FormData();
    formData.append('file', file);
    return api.post('/products/bulk', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
  },
  sync: () => api.post('/products/sync'),
};

export const ordersApi = {
  list: (params?: any) => api.get('/orders', { params }),
  create: (data: any) => api.post('/orders', data),
  confirm: (id: string) => api.post(`/orders/${id}/confirm`),
  export: () => api.post('/orders/export'),
};

export const inventoryApi = {
  list: () => api.get('/inventory'),
  adjust: (data: any) => api.post('/inventory/adjust', data),
};

export const analyticsApi = {
  sales: (days?: number) => api.get('/analytics/sales', { params: { days } }),
  topProducts: (limit?: number) => api.get('/analytics/top-products', { params: { limit } }),
};

export const billingApi = {
  subscribe: (plan: string) => api.post('/billing/subscribe', { plan }),
  status: () => api.get('/billing/status'),
};
