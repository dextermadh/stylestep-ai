import StyleCanvas from '@/components/StyleCanvas';

export default function Home() {
  return (
    <main className="min-h-screen flex flex-col items-center justify-center p-8 bg-gradient-to-br from-black to-[#0a0a0a]">
      <div className="absolute top-0 w-full h-[500px] bg-gradient-to-b from-primary/10 to-transparent pointer-events-none" />
      
      <div className="z-10 w-full max-w-4xl text-center space-y-6 mb-16">
        <h1 className="text-5xl md:text-7xl font-extrabold tracking-tighter text-transparent bg-clip-text bg-gradient-to-r from-white to-neutral-500">
          StyleStep AI
        </h1>
        <p className="text-lg md:text-xl text-neutral-400 max-w-2xl mx-auto font-light leading-relaxed">
          Eradicate Safe Choice Fatigue. Upload your footwear to extract precise CAM16-UCS color matrices and instantly generate high-contrast, fashion-forward 2026 outfit architecture.
        </p>
      </div>

      <div className="z-10 w-full max-w-5xl">
        <StyleCanvas />
      </div>

      <footer className="z-10 mt-24 text-neutral-600 text-sm tracking-wide">
        Powered by SAM 3 Segmentation & CIEDE2000 Precision Engine.
      </footer>
    </main>
  );
}
