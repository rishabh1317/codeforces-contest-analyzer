import React from 'react';
import SearchBar from '../components/SearchBar';
import { Activity } from 'lucide-react';

const HomePage = () => {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center p-6 relative overflow-hidden">
      {/* Background decoration */}
      <div className="absolute top-1/4 -left-32 w-96 h-96 bg-primary/20 rounded-full blur-[100px] pointer-events-none"></div>
      <div className="absolute bottom-1/4 -right-32 w-96 h-96 bg-secondary/20 rounded-full blur-[100px] pointer-events-none"></div>
      
      <div className="text-center space-y-8 z-10 w-full max-w-3xl">
        <div className="inline-flex items-center justify-center p-4 bg-surface/50 rounded-3xl border border-white/5 mb-4 shadow-xl">
          <Activity className="h-12 w-12 text-primary" />
        </div>
        <h1 className="text-5xl md:text-6xl font-extrabold tracking-tight">
          Level Up Your <br/>
          <span className="bg-clip-text text-transparent bg-gradient-to-r from-primary to-secondary">
            Competitive Programming
          </span>
        </h1>
        <p className="text-lg md:text-xl text-muted max-w-2xl mx-auto">
          Analyze your contest history, identify hidden weak areas, and get targeted problem recommendations.
        </p>
        
        <div className="pt-8">
          <SearchBar />
        </div>
      </div>
    </div>
  );
};

export default HomePage;
