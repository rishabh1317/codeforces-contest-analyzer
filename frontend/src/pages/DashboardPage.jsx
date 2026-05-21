import React from 'react';
import { useParams, Link } from 'react-router-dom';
import { useUserStats } from '../hooks/useUserStats';
import Dashboard from '../components/Dashboard';
import SkeletonLoader from '../components/SkeletonLoader';
import { ArrowLeft, AlertCircle } from 'lucide-react';
import SearchBar from '../components/SearchBar';

const DashboardPage = () => {
  const { platform, handle } = useParams();
  const { data, loading, error } = useUserStats(platform, handle);

  return (
    <div className="min-h-screen flex flex-col relative overflow-hidden">
      {/* Background decoration */}
      <div className="absolute top-0 -left-64 w-96 h-96 bg-primary/10 rounded-full blur-[120px] pointer-events-none"></div>

      <header className="w-full border-b border-white/10 bg-surface/50 backdrop-blur-md sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
          <Link to="/" className="flex items-center gap-2 text-muted hover:text-text transition-colors">
            <ArrowLeft className="h-5 w-5" />
            <span className="font-medium hidden sm:inline">Back to Search</span>
          </Link>
          <div className="w-full max-w-xs">
             <SearchBar initialHandle={handle} />
          </div>
        </div>
      </header>

      <main className="flex-1 flex flex-col">
        {loading && (
          <div className="mt-8">
            <SkeletonLoader />
          </div>
        )}
        
        {error && (
          <div className="m-auto flex flex-col items-center justify-center text-center space-y-4 p-8 glass-panel max-w-lg mt-20">
            <AlertCircle className="h-16 w-16 text-rose-500" />
            <h2 className="text-2xl font-bold">Analysis Failed</h2>
            <p className="text-muted">{error}</p>
            <Link to="/" className="text-primary hover:underline mt-4">Try another handle</Link>
          </div>
        )}

        {!loading && !error && data && (
          <div className="mt-8">
            <Dashboard handle={handle} data={data} />
          </div>
        )}
      </main>
    </div>
  );
};

export default DashboardPage;
