import axios from 'axios';

// משתמשים בנתיב יחסי כי ה-Nginx Proxy מנתב את /api ל-Backend
const api = axios.create({
  baseURL: '/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

// הגדרת פונקציות ה-Auth
export const authService = {
  register: async (email, password, fullName) => {
    const response = await api.post('/auth/register', {
      email,
      password,
      full_name: fullName,
    });
    return response.data;
  },

  login: async (email, password) => {
    const response = await api.post('/auth/login', {
      email,
      password,
    });
    return response.data;
  },
};

export default api;