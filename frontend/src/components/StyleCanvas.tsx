'use client';

import { useState } from 'react';
import { UploadCloud, CheckCircle2, Loader2 } from 'lucide-react';

export default function StyleCanvas() {
  const [dragActive, setDragActive] = useState(false);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);

  const handleFileAction = async (e: any) => {
    e.preventDefault();
    setDragActive(false);
    
    // Check if files exist
    const files = e.dataTransfer ? e.dataTransfer.files : e.target.files;
    if (!files || !files[0]) return;

    setLoading(true);
    
    // Simulate API call to FastAPI backend
    setTimeout(() => {
      setResult({
        shoe_color_name: 'Slate Blue',
        shoe_color_hex: '#6a5acd',
        recommendations: {
          bold_ss26: [
            { top: 'Mustard Yellow Cotton Tee', bottom: 'Olive Trousers', hex: '#FFDB58' }
          ]
        }
      });
      setLoading(false);
    }, 2000);
  };

  return (
    <div className="w-full flex justify-center mt-10">
      {!result ? (
        <label
          className={`relative flex flex-col items-center justify-center w-full max-w-3xl h-80 rounded-3xl border-2 border-dashed transition-all duration-300 cursor-pointer overflow-hidden backdrop-blur-md bg-white/5
            ${dragActive ? 'border-primary bg-primary/10 scale-[1.02]' : 'border-neutral-700 hover:border-neutral-500 hover:bg-white/10'}`}
          onDragOver={(e) => { e.preventDefault(); setDragActive(true); }}
          onDragLeave={() => setDragActive(false)}
          onDrop={handleFileAction}
        >
          <input type="file" className="hidden" onChange={handleFileAction} accept="image/*" />
          
          <div className="flex flex-col items-center justify-center space-y-4 text-center p-6">
            {loading ? (
              <>
                <Loader2 className="w-12 h-12 text-primary animate-spin" />
                <h3 className="text-xl font-medium tracking-tight text-white">Extracting CAM16-UCS...</h3>
                <p className="text-neutral-400 text-sm">Processing via SAM 3 Segmentation</p>
              </>
            ) : (
              <>
                <div className="p-4 rounded-full bg-neutral-800/50 mb-2">
                  <UploadCloud className="w-10 h-10 text-neutral-400" />
                </div>
                <h3 className="text-2xl font-semibold tracking-tight text-white">Upload Footwear Protocol</h3>
                <p className="text-neutral-400 mb-2 text-sm max-w-md">Drag & drop your shoe photo here. Raw data is processed strictly in-memory.</p>
              </>
            )}
          </div>
        </label>
      ) : (
        <div className="w-full max-w-4xl grid md:grid-cols-2 gap-8 animate-in fade-in slide-in-from-bottom-8 duration-700">
          {/* Shoe Color Pillar */}
          <div className="flex flex-col items-center justify-center p-8 rounded-3xl bg-neutral-900 border border-neutral-800 shadow-2xl">
            <h2 className="text-neutral-400 uppercase tracking-widest text-xs mb-6 font-semibold">Extracted Base</h2>
            <div 
              className="w-32 h-32 rounded-full shadow-[0_0_50px_rgba(106,90,205,0.4)] mb-8"
              style={{ backgroundColor: result.shoe_color_hex }}
            />
            <h3 className="text-3xl font-bold text-white mb-2">{result.shoe_color_name}</h3>
            <span className="font-mono text-neutral-500 text-sm">{result.shoe_color_hex}</span>
          </div>

          {/* Recommendation Matrix */}
          <div className="flex flex-col justify-center space-y-6">
             <div className="flex items-center space-x-3 mb-2">
                <CheckCircle2 className="text-emerald-500 w-6 h-6" />
                <h2 className="text-xl font-medium text-white tracking-tight">SS26 Bold Recommendation</h2>
             </div>
             
             {result.recommendations.bold_ss26.map((rec: any, idx: number) => (
                <div key={idx} className="group relative p-6 rounded-2xl bg-gradient-to-br from-neutral-900 to-neutral-800/50 border border-neutral-800 hover:border-neutral-600 transition-colors">
                  <div className="flex justify-between items-start">
                    <div>
                      <h4 className="text-white font-medium text-lg mb-1">{rec.top}</h4>
                      <p className="text-neutral-400 text-sm">{rec.bottom}</p>
                    </div>
                    <div 
                      className="w-10 h-10 rounded-full border-2 border-neutral-800 group-hover:scale-110 transition-transform shadow-lg"
                      style={{ backgroundColor: rec.hex }}
                    />
                  </div>
                </div>
             ))}
             
             <button 
                onClick={() => setResult(null)}
                className="self-start mt-4 px-6 py-3 rounded-full text-sm font-semibold bg-white text-black hover:bg-neutral-200 transition-colors"
             >
               Process New Variant
             </button>
          </div>
        </div>
      )}
    </div>
  );
}
