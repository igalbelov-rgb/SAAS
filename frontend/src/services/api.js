import axios from 'axios';

// משתמשים בנתיב יחסי כי ה-Nginx Proxy מנתב את /api ל-Backend
const api = axios.create({
  baseURL: '/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

// 🔥 Interceptor: מזרק אוטומטית את ה-JWT Token לכל בקשה שיוצאת לשרת
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
}, (error) => {
  return Promise.reject(error);
});


// 🔐 הגדרת פונקציות ה-Auth
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


// 🚀 שירות חדש: טיפול במוצרים, סריקה והפצה (Milestone A)
export const productService = {
  /**
   * שולח URL של מוצר ל-Backend כדי לסרוק נתונים ולהפיק קופי עם AI
   */
  scrapeProduct: async (productUrl) => {
    const response = await api.post('/products/scrape', { url: productUrl });
    return response.data;
  },

  /**
   * משגר את התוכן המעובד לפלטפורמת הפצה ספציפית (telegram, facebook, pinterest)
   */
  publishToPlatform: async (platform, productData) => {
    const response = await api.post(`/products/publish/${platform}`, productData);
    return response.data;
  },
};

export default api;