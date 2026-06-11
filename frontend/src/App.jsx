import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard'; // 🔥 ייבוא הדשבורד החדש והמתקדם

// 🔐 קומפוננטת מעטפת להגנה על נתיבים (Protected Route)
const ProtectedRoute = ({ children }) => {
  const token = localStorage.getItem('token');
  
  // אם אין טוקן - זורק את המשתמש חזרה לדף הלוגין
  if (!token) {
    return <Navigate to="/login" replace />;
  }

  // אם יש טוקן - מאפשר לו להמשיך לקומפוננטה המבוקשת
  return children;
};

export default function App() {
  return (
    <Router>
      <Routes>
        {/* נתיבי המערכת המרכזיים */}
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        
        {/* דשבורד מוגן - רק משתמשים עם טוקן יכולים להיכנס */}
        <Route 
          path="/dashboard" 
          element={
            <ProtectedRoute>
              <Dashboard />
            </ProtectedRoute>
          } 
        />

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