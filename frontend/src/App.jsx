import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Login from './pages/Login';
import Register from './pages/Register';

// קומפוננטת דשבורד זמנית עד שנמלא את src/pages/Dashboard.jsx
const TempDashboard = () => {
  const token = localStorage.getItem('token');
  
  // הגנה בסיסית על הנתיב - אם אין טוקן, זורק חזרה ל-Login
  if (!token) {
    return <Navigate to="/login" replace />;
  }

  return (
    <div className="min-h-screen bg-zinc-950 text-zinc-50 flex flex-col items-center justify-center p-4" style={{ direction: 'rtl' }}>
      <div className="w-full max-w-2xl bg-zinc-900 border border-zinc-800 rounded-xl p-8 text-center shadow-2xl">
        <h1 className="text-3xl font-bold mb-2 text-emerald-400">👋 ברוך הבא לדשבורד!</h1>
        <p className="text-zinc-400 mb-6">התחברת בהצלחה למערכת האוטומציה של ה-SaaS.</p>
        <button 
          onClick={() => {
            localStorage.removeItem('token');
            window.location.href = '/login';
          }}
          className="px-4 py-2 bg-zinc-800 hover:bg-zinc-700 border border-zinc-700 rounded-lg text-sm transition-colors"
        >
          התנתקות
        </button>
      </div>
    </div>
  );
};

export default function App() {
  return (
    <Router>
      <Routes>
        {/* נתיבי המערכת המרכזיים */}
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/dashboard" element={<TempDashboard />} />

        {/* ברירת מחדל: אם מגיעים לנתיב הראשי (/), נבדוק אם המשתמש מחובר */}
        <Route 
          path="/" 
          element={
            localStorage.getItem('token') ? 
            <Navigate to="/dashboard" replace /> : 
            <Navigate to="/login" replace />
          } 
        />

        {/* Fallback - כל נתיב לא מוכר אחר יזרוק לעמוד הבית */}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </Router>
  );
}
