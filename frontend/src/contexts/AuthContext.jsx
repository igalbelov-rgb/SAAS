// 1. לוגיקת האותנטיקציה והגנת הדפים (Auth Flow)
// מנהל את מצב ההתחברות הגלובלי בתוך ה-React.

// הקבצים שעובדים יחד:
// backend/app/api/auth.py (מנפיק את הטוקן ב-Login).

// frontend/src/contexts/AuthContext.jsx (שומר ומפיץ את מצב המשתמש לכל האפליקציה).

// frontend/src/App.jsx (חוסם או מאפשר גישה לדשבורד).

// 💻 איך הקוד נראה בפועל?
// מנהל את מצב ההתחברות הגלובלי בתוך ה-React.
// משתמש ב-LocalStorage כדי לשמור את הטוקן והמידע על המשתמש, כך שהמצב נשמר גם אחרי רענון הדף.
// מייצר פונקציות login ו-logout שמעדכנות את ה-LocalStorage ואת מצב המשתמש ב-React.
// מספק את המידע הזה לכל הרכיבים דרך Context
// 🔐 ב-App.jsx, יש קומפוננטת ProtectedRoute שמוודאת שיש טוקן לפני שמאפשרת גישה לדשבורד. אם אין טוקן, המשתמש מועבר לדף הלוגין   
// ב-App.jsx, יש גם נתיב ברירת מחדל שמפנה את המשתמש לדשבורד אם הוא מחובר, או לדף הלוגין אם לא.          

import { createContext, useContext, useState, useEffect } from 'react';

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // בדיקה בטעינה האם המשתמש כבר מחובר
    const storedUser = localStorage.getItem('user');
    const token = localStorage.getItem('access_token');
    if (storedUser && token) {
      setUser(JSON.parse(storedUser));
    }
    setLoading(false);
  }, []);

  const login = (token, userData) => {
    localStorage.setItem('access_token', token);
    localStorage.setItem('user', JSON.stringify(userData));
    setUser(userData);
  };

  const logout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('user');
    setUser(null);
    window.location.href = '/login';
  };

  return (
    <AuthContext.Provider value={{ user, login, logout, isAuthenticated: !!user, loading }}>
      {!loading && children}
    </AuthContext.Provider>
  );
}

export const useAuth = () => useContext(AuthContext);