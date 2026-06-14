import React, { useState } from 'react';
import { 
  Link2, Sparkles, SendHorizontal, Share2, Image, 
  Layers, Loader2, LogOut, AlertCircle 
} from 'lucide-react';
// 1. ייבוא שירות ה-API
import { productService } from '../services/api';

export default function Dashboard() {
  // --- System States ---
  const [productUrl, setProductUrl] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [activeTab, setActiveTab] = useState('telegram'); 
  const [errorMessage, setErrorMessage] = useState(''); // State חדש להצגת שגיאות מהשרת

  // ה-Mock Data המקור שלך משמש כעת כברירת מחדל אסתטית עד הסריקה הראשונה
  const [scrapedData, setScrapedData] = useState({
    title: "Sony WH-1000XM5 Wireless Noise Canceling Headphones - High-Res Audio",
    imageUrl: "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=500&q=80",
    aiCopy: {
      telegram: "🔥 CRAZY DEAL ALERT! 🔥\n\n🎧 Sony WH-1000XM5 Flagship Headphones at rock-bottom price!\n✔️ World-class Active Noise Canceling (ANC)\n✔️ Up to 30 hours of non-stop battery life\n\n📌 Get yours here: https://amzn.to/example",
      facebook: "Ready to elevate your audio experience? 🎧\n\nSony is changing the game again with the WH-1000XM5. We tested the new noise canceling and the results are absolutely mind-blowing. Perfect for travel, remote work, or just tuning out the world.\n\n👇 Full review & discount link in the comments!",
      pinterest: "Sony WH-1000XM5 Review - The King of ANC Headphones. Best wireless headphones for travel, office setup, and audiophiles in 2026."
    }
  });

  // 2. חיבור פונקציית הסריקה ל-FastAPI האמיתי שלך
  const handleScrapeSubmit = async (e) => {
    e.preventDefault();
    if (!productUrl) return;
    
    setIsLoading(true);
    setErrorMessage('');
    
    try {
      const data = await productService.scrapeProduct(productUrl);
      
      if (data.success) {
        setScrapedData({
          title: data.title,
          imageUrl: data.imageUrl,
          aiCopy: data.aiCopy // מקבל את ה-Telegram, Facebook, Pinterest מהשרת
        });
      } else {
        setErrorMessage(data.error || 'Failed to extract product data.');
      }
    } catch (err) {
      console.error('Scraping connection error:', err);
      setErrorMessage('Connection to backend failed. Please check your docker logs.');
    } finally {
      setIsLoading(false);
    }
  };

  // 3. עדכון פונקציית השיגור שתקרא לשרת (ומשם ל-n8n)
  const handlePublish = async (platform) => {
    if (!scrapedData) return;
    try {
      alert(`⚡ Pushing content to ${platform.toUpperCase()} pipeline via n8n...`);
      await productService.publishToPlatform(platform, {
        title: scrapedData.title,
        imageUrl: scrapedData.imageUrl,
        content: scrapedData.aiCopy[platform]
      });
    } catch (err) {
      console.error(`Publishing to ${platform} failed:`, err);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    window.location.href = '/login';
  };

  return (
    /* --- Main Background: Styled like warm sand with a subtle tech grid pattern --- */
    <div 
      className="min-h-screen bg-amber-50/60 text-slate-800 font-sans antialiased selection:bg-amber-200 relative" 
      style={{ 
        direction: 'ltr',
        backgroundImage: 'radial-gradient(#f59e0b 0.75px, transparent 0.75px)',
        backgroundSize: '24px 24px',
      }}
    >
      
      {/* --- Top Dynamic Navbar --- */}
      <header className="border-b-2 border-sky-950 bg-white sticky top-0 z-50 px-6 py-4 flex items-center justify-between shadow-sm">
        <div className="flex items-center gap-3">
          <div className="bg-sky-500 text-white p-2 border-2 border-sky-950 rounded-xl font-black text-2xl rotate-[-3deg] shadow-[2px_2px_0px_0px_rgba(8,47,73,1)]">
            AI
          </div>
          <h1 className="text-2xl font-black tracking-tight text-slate-900">
            SaaS<span className="text-sky-600">Sourcing</span>
          </h1>
        </div>
        
        <div className="flex items-center gap-6">
          <div className="hidden sm:flex items-center gap-2 bg-amber-100 border-2 border-amber-500 px-3 py-1.5 rounded-lg text-xs font-bold text-amber-800">
            <span className="w-2 h-2 bg-emerald-500 rounded-full animate-ping"></span>
            System Active
          </div>
          <button 
            onClick={handleLogout}
            className="flex items-center gap-2 bg-rose-50 hover:bg-rose-100 text-rose-700 font-bold text-xs px-3 py-2 border-2 border-rose-300 rounded-lg transition-all transform hover:translate-y-[-2px] cursor-pointer"
          >
            <LogOut className="w-3.5 h-3.5" />
            Logout
          </button>
        </div>
      </header>

      {/* --- Main Workspace (Split-Screen) --- */}
      <main className="max-w-7xl mx-auto p-6 grid grid-cols-1 lg:grid-cols-12 gap-8 my-6">
        
        {/* ================= LEFT SIDE: INPUT & CONFIGURATION ================= */}
        <section className="lg:col-span-5 space-y-6">
          <div className="bg-white border-2 border-sky-600 rounded-2xl p-6 shadow-[6px_6px_0px_0px_rgba(2,132,199,0.15)] transition-transform hover:scale-[1.01]">
            <div className="flex items-center gap-2 mb-3">
              <div className="p-2 bg-sky-50 border border-sky-200 rounded-lg">
                <Link2 className="w-5 h-5 text-sky-600" />
              </div>
              <h2 className="text-xl font-black text-slate-900">Product Link Sourcing</h2>
            </div>
            <p className="text-sm text-slate-500 mb-6">Drop any e-commerce product URL below. Our smart bots will instantly scrape the technical specs, analyze parameters, and feed the AI copy engine.</p>
            
            <form onSubmit={handleScrapeSubmit} className="space-y-5">
              <div>
                <label className="block text-xs font-black uppercase tracking-wider text-slate-600 mb-2">Product Target URL</label>
                <div className="relative">
                  <input
                    type="url"
                    required
                    placeholder="https://www.amazon.com/dp/B09XS7JWHH..."
                    className="w-full bg-slate-50 border-2 border-slate-200 rounded-xl pl-4 pr-4 py-3.5 text-sm font-medium text-slate-900 placeholder-slate-400 focus:outline-none focus:ring-4 focus:ring-sky-100 focus:border-sky-500 transition-all shadow-inner"
                    value={productUrl}
                    onChange={(e) => setProductUrl(e.target.value)}
                  />
                </div>
              </div>

              {/* Action Button */}
              <button
                type="submit"
                disabled={isLoading}
                className="w-full bg-amber-400 hover:bg-amber-500 text-slate-900 font-black py-4 rounded-xl flex items-center justify-center gap-2 border-2 border-amber-600 transition-all shadow-[4px_4px_0px_0px_rgba(245,158,11,0.2)] active:translate-x-[2px] active:translate-y-[2px] active:shadow-none disabled:opacity-50 text-base cursor-pointer"
              >
                {isLoading ? (
                  <>
                    <Loader2 className="w-5 h-5 animate-spin" />
                    🤖 Bots Extracting Data...
                  </>
                ) : (
                  <>
                    <Sparkles className="w-5 h-5" />
                    Analyze & Generate Copy
                  </>
                )}
              </button>
            </form>

            {/* הצגת תיבת שגיאה אסתטית במידה ומשהו נכשל ב-Backend */}
            {errorMessage && (
              <div className="mt-4 bg-rose-50 border border-rose-200 text-rose-700 p-4 rounded-xl flex items-start gap-2 text-xs font-semibold">
                <AlertCircle className="w-4 h-4 mt-0.5 flex-shrink-0" />
                <div>{errorMessage}</div>
              </div>
            )}
          </div>

          {/* Guidelines Box */}
          <div className="bg-indigo-50 border border-indigo-200 rounded-xl p-5 text-xs text-indigo-950 flex gap-4">
            <div className="w-8 h-8 rounded-full bg-indigo-600 text-white flex items-center justify-center font-bold flex-shrink-0">
              AI
            </div>
            <div>
              <span className="font-extrabold block text-sm text-indigo-900 mb-1">How it works:</span>
              Once clicked, our system triggers an asynchronous background process that populates the preview deck on the right. You can tweak everything live before blasting to social media channels.
            </div>
          </div>
        </section>

        {/* ================= RIGHT SIDE: LIVE DYNAMIC PREVIEW DECK ================= */}
        <section className="lg:col-span-7">
          <div className="bg-white border-2 border-sky-600 rounded-2xl shadow-[6px_6px_0px_0px_rgba(2,132,199,0.15)] overflow-hidden h-full flex flex-col">
            
            {/* Header */}
            <div className="px-6 py-4 bg-indigo-600 text-white flex items-center justify-between">
              <div className="flex items-center gap-2">
                <Layers className="w-5 h-5 text-amber-300" />
                <h3 className="font-black text-base tracking-wide">Live Multi-Channel Content Preview</h3>
              </div>
              <span className="text-xs bg-slate-900/30 text-amber-300 font-bold px-3 py-1 rounded-full border border-indigo-400">
                AI Pipeline Active
              </span>
            </div>

            {/* Inner Content Area */}
            <div className="p-6 flex-1 flex flex-col justify-between space-y-6">
              
              {/* Product Scraped Header Widget */}
              <div className="flex flex-col sm:flex-row gap-4 bg-slate-50 border border-slate-200 p-4 rounded-xl">
                <div className="w-full sm:w-28 h-28 bg-white rounded-lg overflow-hidden flex-shrink-0 border border-slate-300 relative group">
                  {scrapedData.imageUrl && (
                    <img src={scrapedData.imageUrl} alt="Target Product" className="w-full h-full object-cover transition-transform group-hover:scale-110" />
                  )}
                </div>
                <div className="flex flex-col justify-center">
                  <span className="text-[10px] font-black uppercase tracking-widest text-sky-600 mb-1">Target Identified</span>
                  <h4 className="text-base font-bold text-slate-900 leading-snug line-clamp-2">{scrapedData.title}</h4>
                </div>
              </div>

              {/* Tab Navigation */}
              <div className="flex-1 flex flex-col">
                <div className="flex flex-wrap border-b border-slate-200 gap-1">
                  {['telegram', 'facebook', 'pinterest'].map((tab) => (
                    <button
                      key={tab}
                      onClick={() => setActiveTab(tab)}
                      className={`pb-3 pt-1 text-sm font-black px-4 capitalize transition-all border-b-2 cursor-pointer ${
                        activeTab === tab 
                          ? 'border-sky-500 text-sky-600' 
                          : 'border-transparent text-slate-400 hover:text-slate-600'
                      }`}
                    >
                      {tab} Post
                    </button>
                  ))}
                </div>

                {/* Workspace Textarea */}
                <div className="mt-4 flex-1">
                  <textarea
                    rows={6}
                    className="w-full bg-slate-50 border border-slate-200 rounded-xl p-4 text-sm text-slate-800 font-mono leading-relaxed focus:outline-none focus:ring-4 focus:ring-indigo-50 focus:border-indigo-500 resize-none"
                    value={scrapedData.aiCopy[activeTab] || ''}
                    onChange={(e) => {
                      const updatedCopy = { ...scrapedData.aiCopy, [activeTab]: e.target.value };
                      setScrapedData({ ...scrapedData, aiCopy: updatedCopy });
                    }}
                  />
                </div>
              </div>

              {/* --- Dedicated Action Distribution Buttons --- */}
              <div className="pt-4 border-t border-slate-100">
                <span className="block text-xs font-black uppercase tracking-wider text-slate-500 mb-3">
                  Instant Channel Dispatch (Via n8n Automation Engine)
                </span>
                
                <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
                  
                  {/* Telegram Trigger */}
                  <button 
                    onClick={() => handlePublish('telegram')}
                    className="bg-white hover:bg-sky-50 border border-slate-200 hover:border-sky-400 text-slate-900 text-xs font-black py-3.5 px-4 rounded-xl flex items-center justify-center gap-2 transition-all shadow-sm hover:translate-y-[-1px] cursor-pointer"
                  >
                    <SendHorizontal className="w-4 h-4 text-sky-500" />
                    Push Telegram
                  </button>

                  {/* Facebook Trigger */}
                  <button 
                    onClick={() => handlePublish('facebook')}
                    className="bg-white hover:bg-indigo-50 border border-slate-200 hover:border-indigo-400 text-slate-900 text-xs font-black py-3.5 px-4 rounded-xl flex items-center justify-center gap-2 transition-all shadow-sm hover:translate-y-[-1px] cursor-pointer"
                  >
                    <Share2 className="w-4 h-4 text-indigo-600" />
                    Publish Facebook
                  </button>

                  {/* Pinterest Trigger */}
                  <button 
                    onClick={() => handlePublish('pinterest')}
                    className="bg-white hover:bg-rose-50 border border-slate-200 hover:border-rose-400 text-slate-900 text-xs font-black py-3.5 px-4 rounded-xl flex items-center justify-center gap-2 transition-all shadow-sm hover:translate-y-[-1px] cursor-pointer"
                  >
                    <Image className="w-4 h-4 text-rose-500" />
                    Pin to Pinterest
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