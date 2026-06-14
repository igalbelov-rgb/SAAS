// הקומפוננטה הזו מבודדת את 3 כפתורי השיגור (הצינורות ל-n8n). היא מקבלת פונקציה מהאבא (onPublish) ומעבירה לה את שם הפלטפורמה שנבחרה ברגע הלחיצה.

import React from 'react';
import { SendHorizontal, Share2, Image } from 'lucide-react';

export default function PublishControl({ onPublish }) {
  return (
    <div className="pt-4 border-t border-slate-100">
      <span className="block text-xs font-black uppercase tracking-wider text-slate-500 mb-3">
        Instant Channel Dispatch (Via n8n Automation Engine)
      </span>
      
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        
        {/* Telegram Push Button */}
        <button 
          onClick={() => onPublish('telegram')}
          className="bg-white hover:bg-sky-50 border border-slate-200 hover:border-sky-400 text-slate-900 text-xs font-black py-3.5 px-4 rounded-xl flex items-center justify-center gap-2 transition-all shadow-sm hover:translate-y-[-1px] cursor-pointer"
        >
          <SendHorizontal className="w-4 h-4 text-sky-500" />
          Push Telegram
        </button>

        {/* Facebook Publish Button */}
        <button 
          onClick={() => onPublish('facebook')}
          className="bg-white hover:bg-indigo-50 border border-slate-200 hover:border-indigo-400 text-slate-900 text-xs font-black py-3.5 px-4 rounded-xl flex items-center justify-center gap-2 transition-all shadow-sm hover:translate-y-[-1px] cursor-pointer"
        >
          <Share2 className="w-4 h-4 text-indigo-600" />
          Publish Facebook
        </button>

        {/* Pinterest Pin Button */}
        <button 
          onClick={() => onPublish('pinterest')}
          className="bg-white hover:bg-rose-50 border border-slate-200 hover:border-rose-400 text-slate-900 text-xs font-black py-3.5 px-4 rounded-xl flex items-center justify-center gap-2 transition-all shadow-sm hover:translate-y-[-1px] cursor-pointer"
        >
          <Image className="w-4 h-4 text-rose-500" />
          Pin to Pinterest
        </button>

      </div>
    </div>
  );
}