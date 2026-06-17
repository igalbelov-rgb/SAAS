// עטיפת AuthProvider: עכשיו היא נמצאת בנקודה הגבוהה ביותר באפליקציה
// ומאפשרת לכל הדפים (כולל הראוטר עצמו) לגשת למידע האותנטיקציה בצורה נקייה

// ניהול מצב טעינה (loading):
//  כשמשתמש מרענן את הדף, לוקח ל-React כמה מילישניות לקרוא מה-localStorage ולעדכן את ה-State. שימוש ב-loading מונע באג קלאסי שבו המערכת מעיפה בטעות משתמש מחובר חזרה ל-/login לשבריר שנייה רק כי ה-State עדיין לא הספיק להתעדכן.

import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './contexts/AuthContext';
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard'; // 🔥 ייבוא הדשבורד החדש והמתקדם

// 🔐 קומפוננטת מעטפת להגנה על נתיבים (Protected Route) על בסיס ה-Context
const ProtectedRoute = ({ children }) => {
  const { isAuthenticated, loading } = useAuth();
  
  // אם ה-Context עדיין בודק את מצב הטוקן בטעינה הראשונית - נציג אינדיקטור טעינה זמני
  if (loading) {
    return <div className="min-h-screen bg-slate-900 flex items-center justify-center text-white font-semibold">Loading App...</div>;
  }
  
  // אם הבדיקה הסתיימה ואין משתמש מחובר - זורק את המשתמש חזרה לדף הלוגין
  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  // אם יש משתמש מחובר - מאפשר לו להמשיך לקומפוננטה המבוקשת
  return children;
};

// 🏠 רכיב עזר לניהול דף הבית (/) בצורה ריאקטיבית
const HomeRedirect = () => {
  const { isAuthenticated, loading } = useAuth();

  if (loading) return null; // מונע קפיצות מסך בזמן בדיקת הטוקן
  return isAuthenticated ? <Navigate to="/dashboard" replace /> : <Navigate to="/login" replace />;
};

export default function App() {
  return (
    // 🔥 העטיפה הקריטית: ה-Provider עוטף את כל האפליקציה ומזריק את ה-Auth State לכולם
    <AuthProvider>
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

          {/* ברירת מחדל: אם מגיעים לנתיב הראשי (/), נבדוק בצורה ריאקטיבית לאן להעביר אותו */}
          <Route path="/" element={<HomeRedirect />} />

          {/* Fallback - כל נתיב לא מוכר אחר יזרוק לעמוד הבית */}
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </Router>
    </AuthProvider>
  );
}