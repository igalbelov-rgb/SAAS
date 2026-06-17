import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext'; // 🔥 ייבוא הקונטקסט
import { authService } from '../services/api';
import { User, Mail, Lock, ArrowRight, CheckCircle2, AlertCircle } from 'lucide-react';

export default function Register() {
  const navigate = useNavigate();
  const { login } = useAuth(); // 🔥 שליפת פונקציית הלוגין הריאקטיבית מהקונטקסט
  const [formData, setFormData] = useState({ fullName: '', email: '', password: '' });
  const [status, setStatus] = useState({ loading: false, error: null, success: false });

  const handleSubmit = async (e) => {
    e.preventDefault();
    setStatus({ loading: true, error: null, success: false });

    try {
      // 1. רישום המשתמש בדאטאבייס
      await authService.register(formData.email, formData.password, formData.fullName);
      
      // 2. ביצוע לוגין אוטומטי מייד לאחר ההרשמה
      const loginData = await authService.login(formData.email, formData.password);
  
      // 3. עדכון הסטטוס המקומי
      setStatus({ loading: false, error: null, success: true });

      // 🔥 התיקון הקריטי: אם חזר טוקן, נזריק אותו לקונטקסט וננווט מייד לדשבורד
      if (loginData && loginData.access_token) {
        login(loginData.access_token, loginData.user);
        
        // השהייה קלה של חצי שנייה כדי שהמשתמש יספיק לראות מצב "הצלחה" (אופציונלי אך מומלץ ל-UX)
        setTimeout(() => {
          navigate('/dashboard');
        }, 600);
      }
      
    } catch (err) {
      const errorMsg = err.response?.data?.detail?.[0]?.msg || err.response?.data?.detail || 'משהו השתבש ברישום. נסה שוב.';
      setStatus({ loading: false, error: errorMsg, success: false });
    }
  };

  return (
    <div className="min-h-screen bg-zinc-950 text-zinc-50 flex items-center justify-center p-4 dir-rtl" style={{ direction: 'rtl' }}>
      <div className="w-full max-w-md bg-zinc-900 border border-zinc-800 rounded-xl p-8 shadow-2xl">
        
        {/* כותרת */}
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold tracking-tight">יצירת חשבון חדש</h1>
          <p className="text-sm text-zinc-400 mt-2">הצטרף לפלטפורמת ה-Affiliate AI SaaS שלנו</p>
        </div>

        {/* הודעות מערכת */}
        {status.success && (
          <div className="mb-6 p-4 bg-emerald-950/50 border border-emerald-500/30 text-emerald-400 rounded-lg flex items-center gap-3 text-sm">
            <CheckCircle2 className="w-5 h-5 flex-shrink-0" />
            <span>ההרשמה בוצעה בהצלחה! עכשיו אתה יכול להתחבר.</span>
          </div>
        )}

        {status.error && (
          <div className="mb-6 p-4 bg-rose-950/50 border border-rose-500/30 text-rose-400 rounded-lg flex items-center gap-3 text-sm">
            <AlertCircle className="w-5 h-5 flex-shrink-0" />
            <span className="truncate">{status.error}</span>
          </div>
        )}

        {/* טופס */}
        <form onSubmit={handleSubmit} className="space-y-5">
          <div>
            <label className="block text-sm font-medium text-zinc-300 mb-1.5">שם מלא</label>
            <div className="relative">
              <User className="absolute right-3 top-1/2 -translate-y-1/2 w-4 h-4 text-zinc-500" />
              <input
                type="text"
                required
                className="w-full bg-zinc-950 border border-zinc-800 rounded-lg pr-10 pl-4 py-2.5 text-zinc-100 placeholder-zinc-600 focus:outline-none focus:border-zinc-600 transition-colors"
                placeholder="ישראל ישראלי"
                value={formData.fullName}
                onChange={(e) => setFormData({ ...formData, fullName: e.target.value })}
              />
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-zinc-300 mb-1.5">כתובת אימייל</label>
            <div className="relative">
              <Mail className="absolute right-3 top-1/2 -translate-y-1/2 w-4 h-4 text-zinc-500" />
              <input
                type="email"
                required
                className="w-full bg-zinc-950 border border-zinc-800 rounded-lg pr-10 pl-4 py-2.5 text-zinc-100 placeholder-zinc-600 focus:outline-none focus:border-zinc-600 transition-colors text-left"
                placeholder="you@example.com"
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
            className="w-full bg-zinc-100 hover:bg-zinc-200 text-zinc-950 font-medium py-2.5 rounded-lg flex items-center justify-center gap-2 transition-colors disabled:opacity-50 mt-2"
          >
            {status.loading ? 'מבצע רישום...' : 'צור חשבון'}
            <ArrowRight className="w-4 h-4 rotate-180" />
          </button>
        </form>

        <div className="text-center mt-6 text-sm text-zinc-500">
          כבר יש לך חשבון? <a href="/login" className="text-zinc-300 hover:underline">התחבר כאן</a>
        </div>

      </div>
    </div>
  );
}