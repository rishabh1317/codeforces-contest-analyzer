import React from 'react';
import { Link } from 'react-router-dom';
import SearchBar from '../components/SearchBar';
import { Activity, Swords } from 'lucide-react';

const HomePage = () => {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center p-6 relative overflow-hidden bg-background text-text">
      {/* Background decoration */}
      <div className="absolute top-1/4 -left-32 w-96 h-96 bg-primary/10 rounded-full blur-[100px] pointer-events-none"></div>
      <div className="absolute bottom-1/4 -right-32 w-96 h-96 bg-secondary/10 rounded-full blur-[100px] pointer-events-none"></div>
      
      <div className="text-center space-y-8 z-10 w-full max-w-3xl font-mono">
        <div className="inline-flex items-center justify-center p-4 bg-surface/50 rounded-3xl border border-white/5 mb-4 shadow-xl">
          <Activity className="h-12 w-12 text-primary" />
        </div>
        <h1 className="text-4xl md:text-6xl font-extrabold tracking-tight">
          Level Up Your <br/>
          <span className="bg-clip-text text-transparent bg-gradient-to-r from-primary to-secondary">
            Competitive Programming
          </span>
        </h1>
        <p className="text-base md:text-lg text-muted max-w-2xl mx-auto">
          Analyze your contest history, identify hidden weak areas, and get targeted problem recommendations.
        </p>
        
        <div className="pt-8 flex flex-col items-center gap-4">
          <SearchBar />
          <Link 
            to="/compare" 
            className="flex items-center gap-2 text-primary hover:text-primary/80 text-sm font-semibold transition-all hover:scale-[1.02] border border-primary/20 bg-primary/10 px-6 py-2.5 rounded-xl shadow-md"
          >
            <Swords className="h-4 w-4" /> Compare with a Rival
          </Link>
        </div>
      </div>
    </div>
  );
};

export default HomePage;
