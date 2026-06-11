import React, { useState } from 'react';
import { 
  Link2, Sparkles, SendHorizontal, Share2, Image, 
  Layers, Loader2, AlertTriangle 
} from 'lucide-react';

export default function Dashboard() {
  // --- States למערכת ---
  const [productUrl, setProductUrl] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [activeTab, setActiveTab] = useState('telegram'); // טאב פעיל בתצוגה המקדימה

  // דאטה פיקטיבי (Mock Data) לצורך בדיקת העיצוב, עד שנחבר את קריאות ה-API מהרשת
  const [mockScrapedData, setMockScrapedData] = useState({
    title: "אוזניות אלחוטיות Sony WH-1000XM5 עם סינון רעשים אקטיבי",
    imageUrl: "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=500&q=80",
    aiCopy: {
      telegram: "🔥 דיל מטורף בערוץ! 🔥\n\n🎧 אוזניות הדגל של סוני Sony WH-1000XM5 במחיר רצפה!\n✔️ סינון רעשים אקטיבי (ANC) מהטובים בעולם\n✔️ סוללה לעד 30 שעות עבודה ברצף\n\n📌 לפרטים ורכישה ישירה: https://amzn.to/example",
      facebook: "מחפשים את חוויית הסאונד המושלמת? 🎧\n\nסוני שוב שוברת את השוק עם ה-WH-1000XM5. בדקנו את סינון הרעשים החדש שלהן והתוצאות פשוט מדהימות. מושלם לטיסות, עבודה מהמשרד או סתם ניתוק מהעולם.\n\n👇 קישור לסקירה המלאה והטבת רכישה בתגובה הראשונה!",
      pinterest: "Sony WH-1000XM5 Review - The King of ANC Headphones. Best wireless headphones for travel, office setup, and audiophiles in 2026."
    }
  });

  const handleScrapeSubmit = (e) => {
    e.preventDefault();
    if (!productUrl) return;
    
    setIsLoading(true);
    // סימולציה של סריקה מה-Backend (נחליף את זה ב-Axios בהמשך)
    setTimeout(() => {
      setIsLoading(false);
    }, 2500);
  };

  const handlePublish = (platform) => {
    alert(`משלח את התוכן לפלטפורמת: ${platform} דרך הצינור של n8n...`);
  };

  return (
    <div className="min-h-screen bg-zinc-950 text-zinc-50 font-sans antialiased" style={{ direction: 'rtl' }}>
      
      {/* --- Top Navbar --- */}
      <header className="border-b border-zinc-800 bg-zinc-900/50 backdrop-blur sticky top-0 z-50 px-6 py-4 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="bg-zinc-100 text-zinc-950 p-1.5 rounded-lg font-bold text-xl">S</div>
          <h1 className="text-xl font-bold tracking-tight">SaaS AI Sourcing</h1>
        </div>
        <div className="flex items-center gap-4 text-sm text-zinc-400">
          <span>מחובר כגירסה ראשונה</span>
          <div className="w-2.5 h-2.5 bg-emerald-500 rounded-full animate-pulse"></div>
        </div>
      </header>

      {/* --- Dashboard Layout Split-Screen --- */}
      <main className="max-w-7xl mx-auto p-6 grid grid-cols-1 lg:grid-cols-12 gap-6">
        
        {/* ================= צד ימין: טופס קלט ואפשרויות ================= */}
        <section className="lg:col-span-5 space-y-6">
          <div className="bg-zinc-900 border border-zinc-800 rounded-xl p-6 shadow-xl">
            <div className="flex items-center gap-2 mb-4">
              <Sparkles className="w-5 h-5 text-zinc-400" />
              <h2 className="text-lg font-semibold">איתור וניתוח מוצר</h2>
            </div>
            <p className="text-sm text-zinc-400 mb-6">הזן לינק של מוצר מאתרים נבחרים (Amazon, AliExpress וכו') ומנוע ה-AI שלנו ישלוף את הנתונים ויכתוב עבורך את הקופי המושלם.</p>
            
            <form onSubmit={handleScrapeSubmit} className="space-y-4">
              <div>
                <label className="block text-xs font-medium text-zinc-400 mb-2">כתובת ה-URL של המוצר</label>
                <div className="relative">
                  <Link2 className="absolute right-3 top-1/2 -translate-y-1/2 w-4 h-4 text-zinc-500" />
                  <input
                    type="url"
                    required
                    placeholder="https://www.amazon.com/dp/B09XS7JWHH..."
                    className="w-full bg-zinc-950 border border-zinc-800 rounded-lg pr-10 pl-4 py-3 text-sm text-zinc-100 placeholder-zinc-600 focus:outline-none focus:border-zinc-600 transition-colors text-left"
                    value={productUrl}
                    onChange={(e) => setProductUrl(e.target.value)}
                  />
                </div>
              </div>

              <button
                type="submit"
                disabled={isLoading}
                className="w-full bg-zinc-100 hover:bg-zinc-200 text-zinc-950 font-medium py-3 rounded-lg flex items-center justify-center gap-2 transition-all disabled:opacity-50 text-sm shadow"
              >
                {isLoading ? (
                  <>
                    <Loader2 className="w-4 h-4 animate-spin" />
                    סורק ומנתח באמצעות AI...
                  </>
                ) : (
                  <>
                    <Sparkles className="w-4 h-4" />
                    סרוק והפק קמפיין שיווקי
                  </>
                )}
              </button>
            </form>
          </div>

          {/* תיבת סטטוס/הנחיות מערכת */}
          <div className="bg-zinc-900/40 border border-zinc-800/60 rounded-xl p-5 text-xs text-zinc-500 flex gap-3">
            <AlertTriangle className="w-4 h-4 text-zinc-500 flex-shrink-0 mt-0.5" />
            <div>
              <span className="font-semibold text-zinc-400 block mb-1">הנחיות הפצה:</span>
              לאחר סיום הניתוח, הטקסטים יופיעו בצד שמאל. תוכל לערוך אותם באופן מקומי או ללחוץ ישירות על אחד מכפתורי ה-Publish כדי לשגר אותם אוטומטית לערוצים שלך.
            </div>
          </div>
        </section>

        {/* ================= צד שמאל: תצוגה מקדימה וניהול קופי ================= */}
        <section className="lg:col-span-7">
          <div className="bg-zinc-900 border border-zinc-800 rounded-xl shadow-xl overflow-hidden h-full flex flex-col">
            
            {/* כותרת האזור הדינמי */}
            <div className="px-6 py-4 border-b border-zinc-800 bg-zinc-900/80 flex items-center justify-between">
              <div className="flex items-center gap-2">
                <Layers className="w-4 h-4 text-zinc-400" />
                <h3 className="text-sm font-medium">קמפיין מוצר מוכן (Live AI Preview)</h3>
              </div>
              <span className="text-xs bg-zinc-800 text-zinc-300 px-2.5 py-1 rounded-full border border-zinc-700">תצוגת סימולציה</span>
            </div>

            {/* תוכן התצוגה המקדימה */}
            <div className="p-6 flex-1 space-y-6">
              
              {/* כרטיסיית מוצר עליונה (תמונה + כותרת שנשלפה) */}
              <div className="flex flex-col md:flex-row gap-4 bg-zinc-950 p-4 border border-zinc-800 rounded-lg">
                <div className="w-full md:w-32 h-32 bg-zinc-900 rounded-md overflow-hidden flex-shrink-0 border border-zinc-800 relative">
                  {mockScrapedData.imageUrl ? (
                    <img src={mockScrapedData.imageUrl} alt="product" className="w-full h-full object-cover" />
                  ) : (
                    <Image className="w-6 h-6 text-zinc-700 absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2" />
                  )}
                </div>
                <div className="flex flex-col justify-center">
                  <span className="text-xs text-zinc-500 uppercase tracking-wider mb-1 font-mono">Scraped Title</span>
                  <h4 className="text-base font-semibold text-zinc-200 leading-snug">{mockScrapedData.title}</h4>
                </div>
              </div>

              {/* ניווט בין כרטיסיות ה-AI Copywriting (Tabs) */}
              <div>
                <div className="flex border-b border-zinc-800 gap-2">
                  <button 
                    onClick={() => setActiveTab('telegram')}
                    className={`pb-3 text-sm font-medium px-4 border-b-2 transition-all ${activeTab === 'telegram' ? 'border-zinc-100 text-zinc-100' : 'border-transparent text-zinc-500 hover:text-zinc-300'}`}
                  >
                    טקסט לטלגרם
                  </button>
                  <button 
                    onClick={() => setActiveTab('facebook')}
                    className={`pb-3 text-sm font-medium px-4 border-b-2 transition-all ${activeTab === 'facebook' ? 'border-zinc-100 text-zinc-100' : 'border-transparent text-zinc-500 hover:text-zinc-300'}`}
                  >
                    פוסט לפייסבוק
                  </button>
                  <button 
                    onClick={() => setActiveTab('pinterest')}
                    className={`pb-3 text-sm font-medium px-4 border-b-2 transition-all ${activeTab === 'pinterest' ? 'border-zinc-100 text-zinc-100' : 'border-transparent text-zinc-500 hover:text-zinc-300'}`}
                  >
                    תיאור לפינטרסט
                  </button>
                </div>

                {/* תיבת תוכן הטאב הניתנת לעריכה */}
                <div className="mt-4">
                  <textarea
                    rows={6}
                    className="w-full bg-zinc-950 border border-zinc-800 rounded-lg p-4 text-sm text-zinc-300 font-mono leading-relaxed focus:outline-none focus:border-zinc-700 resize-none whitespace-pre-wrap"
                    value={mockScrapedData.aiCopy[activeTab]}
                    onChange={(e) => {
                      const updatedCopy = { ...mockScrapedData.aiCopy, [activeTab]: e.target.value };
                      setMockScrapedData({ ...mockScrapedData, aiCopy: updatedCopy });
                    }}
                  />
                </div>
              </div>

              {/* --- 3 כפתורי הפצה ייעודיים (Milestone A Action Points) --- */}
              <div className="pt-2">
                <label className="block text-xs font-medium text-zinc-500 mb-3">שגר לערוצי שיווק אוטומטיים (Publish Via n8n):</label>
                <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
                  
                  {/* כפתור טלגרם */}
                  <button 
                    onClick={() => handlePublish('telegram')}
                    className="bg-zinc-950 hover:bg-zinc-900 border border-zinc-800 hover:border-zinc-700 text-zinc-200 text-xs py-3 px-4 rounded-lg flex items-center justify-center gap-2 transition-colors font-medium"
                  >
                    <SendHorizontal className="w-3.5 h-3.5 text-sky-400" />
                    העלאה לטלגרם
                  </button>

                  {/* כפתור פייסבוק */}
                  <button 
                    onClick={() => handlePublish('facebook')}
                    className="bg-zinc-950 hover:bg-zinc-900 border border-zinc-800 hover:border-zinc-700 text-zinc-200 text-xs py-3 px-4 rounded-lg flex items-center justify-center gap-2 transition-colors font-medium"
                  >
                    <Share2 className="w-3.5 h-3.5 text-blue-500" />
                    העלאה לפייסבוק
                  </button>

                  {/* כפתור פינטרסט */}
                  <button 
                    onClick={() => handlePublish('pinterest')}
                    className="bg-zinc-950 hover:bg-zinc-900 border border-zinc-800 hover:border-zinc-700 text-zinc-200 text-xs py-3 px-4 rounded-lg flex items-center justify-center gap-2 transition-colors font-medium"
                  >
                    <Image className="w-3.5 h-3.5 text-rose-500" />
                    העלאה לפינטרסט
                  </button>

                </div>
              </div>

            </div>

          </div>
        </section>

      </main>
    </div>
  );
}