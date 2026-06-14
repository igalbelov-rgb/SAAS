// הקומפוננטה הזו אחראית להציג בצורה נקייה ומקצועית את מה שהבוטים יגרדו מהלינק: תמונת המוצר, הכותרת שלו, ומערך של תגיות מפרט טכני (specs).

import React from 'react';

export default function ProductPreview({ title, imageUrl, specs = [] }) {
  return (
    <div className="flex flex-col sm:flex-row gap-4 bg-slate-50 border border-slate-200 p-4 rounded-xl shadow-[4px_4px_0px_0px_rgba(15,23,42,0.05)]">
      
      {/* Product Image Box */}
      <div className="w-full sm:w-28 h-28 bg-white rounded-lg overflow-hidden flex-shrink-0 border border-slate-300 relative group">
        {imageUrl ? (
          <img 
            src={imageUrl} 
            alt="Target Product" 
            className="w-full h-full object-cover transition-transform group-hover:scale-110" 
          />
        ) : (
          <div className="w-full h-full bg-slate-100 flex items-center justify-center text-xs text-slate-400">
            No Image Found
          </div>
        )}
      </div>

      {/* Product Text Details & Technical Specs */}
      <div className="flex flex-col justify-center flex-1">
        <span className="text-[10px] font-black uppercase tracking-widest text-sky-600 mb-1">
          Target Identified
        </span>
        <h4 className="text-base font-bold text-slate-900 leading-snug line-clamp-2 mb-2">
          {title || "Waiting for product URL..."}
        </h4>
        
        {/* Technical Specs Badges (Rendered dynamically) */}
        {specs && specs.length > 0 && (
          <div className="flex flex-wrap gap-1.5 mt-1">
            {specs.map((spec, index) => (
              <span 
                key={index} 
                className="bg-sky-50 text-sky-700 text-[10px] font-bold px-2 py-0.5 rounded border border-sky-100 animate-fade-in"
              >
                {spec}
              </span>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}