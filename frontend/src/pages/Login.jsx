import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom'; // 🔥 שינוי 1: ייבוא הניווט של React Router
import { useAuth } from '../contexts/AuthContext'; // 🔥 שינוי 2: ייבוא ה-Hook של האותנטיקציה שהקמנו
import { authService } from '../services/api';
import { Mail, Lock, LogIn, AlertCircle } from 'lucide-react';

export default function Login() {
  const navigate = useNavigate(); // 🔥 שינוי 3: הגדרת פונקציית הניווט
  const { login } = useAuth(); // 🔥 שינוי 4: שליפת פונקציית הלוגין הריאקטיבית מהקונטקסט
  
  const [formData, setFormData] = useState({ email: '', password: '' });
  const [status, setStatus] = useState({ loading: false, error: null });

  const handleSubmit = async (e) => {
    e.preventDefault();
    setStatus({ loading: true, error: null });

    try {
      const data = await authService.login(formData.email, formData.password);
      
      if (data.access_token) {
        // 🔥 שינוי 5: במקום לשמור ידנית ולרענן את הדף, מפעילים את פונקציית ה-login של הקונטקסט.
        // הפונקציה הזו שומרת את הטוקן, מעדכנת את ה-user ומעדכנת את ה-State של כל האפליקציה בבת אחת.
        login(data.access_token, data.user);
        
        // 🔥 שינוי 6: ניווט ריאקטיבי פנימי לדשבורד - מונע את באג ההקפצה חזרה ללוגין!
        navigate('/dashboard');
      }
    } catch (err) {
      setStatus({ 
        loading: false, 
        error: err.response?.status === 401 ? 'אימייל או סיסמה שגויים' : 'שגיאת שרת פנימית'
      });
    }
  };

  return (
    <div className="min-h-screen bg-zinc-950 text-zinc-50 flex items-center justify-center p-4" style={{ direction: 'rtl' }}>
      <div className="w-full max-w-md bg-zinc-900 border border-zinc-800 rounded-xl p-8 shadow-2xl">
        
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold tracking-tight">ברוך הבא חזרה</h1>
          <p className="text-sm text-zinc-400 mt-2">התחבר כדי לנהל את קמפייני ה-AI שלך</p>
        </div>

        {status.error && (
          <div className="mb-6 p-4 bg-rose-950/50 border border-rose-500/30 text-rose-400 rounded-lg flex items-center gap-3 text-sm">
            <AlertCircle className="w-5 h-5 flex-shrink-0" />
            <span>{status.error}</span>
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-5">
          <div>
            <label className="block text-sm font-medium text-zinc-300 mb-1.5">אימייל</label>
            <div className="relative">
              <Mail className="absolute right-3 top-1/2 -translate-y-1/2 w-4 h-4 text-zinc-500" />
              <input
                type="email"
                required
                className="w-full bg-zinc-950 border border-zinc-800 rounded-lg pr-10 pl-4 py-2.5 text-zinc-100 placeholder-zinc-600 focus:outline-none focus:border-zinc-600 transition-colors text-left"
                placeholder="name@company.com"
                value={formData.email}
                onChange={(e) => setFormData({ ...formData, email: e.target.value })}
              />
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-zinc-300 mb-1.5">סיסמה</label>
            <div className="relative">
              <Lock className="absolute right-3 top-1/2 -translate-y-1/2 w-4 h-4 text-zinc-500" />
              <input
                type="password"
                required
                className="w-full bg-zinc-950 border border-zinc-800 rounded-lg pr-10 pl-4 py-2.5 text-zinc-100 placeholder-zinc-600 focus:outline-none focus:border-zinc-600 transition-colors text-left"
                placeholder="••••••••"
                value={formData.password}
                onChange={(e) => setFormData({ ...formData, password: e.target.value })}
              />
            </div>
          </div>

          <button
            type="submit"
            disabled={status.loading}
            className="w-full bg-zinc-100 hover:bg-zinc-200 text-zinc-950 font-medium py-2.5 rounded-lg flex items-center justify-center gap-2 transition-colors disabled:opacity-50"
          >
            {status.loading ? 'מתחבר...' : 'התחברות'}
            <LogIn className="w-4 h-4" />
          </button>
        </form>

        <div className="text-center mt-6 text-sm text-zinc-500">
          אין לך חשבון עדיין? <a href="/register" className="text-zinc-300 hover:underline">להרשמה מהירה</a>
        </div>

      </div>
    </div>
  );
}