import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { compareRivals } from '../api/api';
import { ArrowLeft, Swords, Award, AlertCircle, Lightbulb } from 'lucide-react';
import SkeletonLoader from '../components/SkeletonLoader';
import { GrowthCompareChart } from '../components/Charts';

const ComparePage = () => {
  const [handle1, setHandle1] = useState('');
  const [handle2, setHandle2] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [data, setData] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!handle1.trim() || !handle2.trim()) return;

    setLoading(true);
    setError(null);
    setData(null);

    try {
      const result = await compareRivals(handle1.trim(), handle2.trim());
      setData(result);
    } catch (err) {
      const errorMsg = err.response?.data?.detail || err.message || 'An error occurred';
      if (errorMsg.includes('not found') || errorMsg.includes('404')) {
        setError('Handle not found. Please verify the usernames and try again.');
      } else {
        setError(errorMsg);
      }
    } finally {
      setLoading(false);
    }
  };

  const renderStatsRow = (label, val1, val2, highBetter = true) => {
    const isNum1 = typeof val1 === 'number';
    const isNum2 = typeof val2 === 'number';
    
    let is1Better = false;
    let is2Better = false;

    if (isNum1 && isNum2) {
      if (val1 !== val2) {
        if (highBetter) {
          is1Better = val1 > val2;
          is2Better = val2 > val1;
        } else {
          is1Better = val1 < val2;
          is2Better = val2 < val1;
        }
      }
    }

    return (
      <div className="border-b border-white/5 py-4 flex items-center justify-between font-mono text-sm">
        <span className={`text-left w-1/3 truncate px-2 ${is1Better ? 'text-primary font-bold' : 'text-muted'}`}>
          {val1 !== null && val1 !== undefined ? val1 : 'N/A'}
        </span>
        <span className="text-center text-xs text-muted w-1/3 uppercase tracking-wider font-semibold">
          {label}
        </span>
        <span className={`text-right w-1/3 truncate px-2 ${is2Better ? 'text-primary font-bold' : 'text-muted'}`}>
          {val2 !== null && val2 !== undefined ? val2 : 'N/A'}
        </span>
      </div>
    );
  };

  return (
    <div className="min-h-screen flex flex-col relative overflow-hidden bg-background text-text">
      {/* Background gradients */}
      <div className="absolute top-0 left-1/4 w-96 h-96 bg-primary/5 rounded-full blur-[120px] pointer-events-none"></div>
      <div className="absolute bottom-0 right-1/4 w-96 h-96 bg-secondary/5 rounded-full blur-[120px] pointer-events-none"></div>

      <header className="w-full border-b border-white/10 bg-surface/50 backdrop-blur-md sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
          <Link to="/" className="flex items-center gap-2 text-muted hover:text-text transition-colors font-mono text-sm">
            <ArrowLeft className="h-5 w-5" />
            <span>Back to Search</span>
          </Link>
          <div className="flex items-center gap-2 font-mono text-sm font-bold text-primary">
            <Swords className="h-5 w-5" />
            <span>RIVAL DUEL</span>
          </div>
        </div>
      </header>

      <main className="flex-1 max-w-7xl w-full mx-auto p-4 sm:p-8 lg:p-12 space-y-10">
        {/* Setup duel inputs */}
        <div className="glass-panel p-6 sm:p-8 max-w-2xl mx-auto border border-white/10">
          <h2 className="text-2xl font-bold font-mono text-center mb-6 text-primary flex items-center justify-center gap-3">
            <Swords className="h-6 w-6" /> Prepare Comparison
          </h2>
          <form onSubmit={handleSubmit} className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="space-y-2">
                <label className="text-xs text-muted uppercase tracking-wider font-semibold font-mono block">Handle 1</label>
                <input
                  type="text"
                  placeholder="e.g. Tourist"
                  value={handle1}
                  onChange={(e) => setHandle1(e.target.value)}
                  className="w-full bg-surface border border-white/10 rounded-xl px-4 py-3 text-text placeholder-muted focus:outline-none focus:border-primary transition-colors font-mono"
                  required
                />
              </div>
              <div className="space-y-2">
                <label className="text-xs text-muted uppercase tracking-wider font-semibold font-mono block">Handle 2</label>
                <input
                  type="text"
                  placeholder="e.g. Benq"
                  value={handle2}
                  onChange={(e) => setHandle2(e.target.value)}
                  className="w-full bg-surface border border-white/10 rounded-xl px-4 py-3 text-text placeholder-muted focus:outline-none focus:border-primary transition-colors font-mono"
                  required
                />
              </div>
            </div>
            <button
              type="submit"
              disabled={loading}
              className="w-full bg-primary hover:bg-primary/80 disabled:bg-primary/50 text-background font-bold font-mono py-3 rounded-xl transition-all shadow-lg shadow-primary/20 hover:scale-[1.01] flex items-center justify-center gap-2"
            >
              {loading ? 'Analyzing...' : 'Execute Duel'}
            </button>
          </form>
        </div>

        {/* Loading state */}
        {loading && (
          <div className="max-w-4xl mx-auto mt-8">
            <SkeletonLoader />
          </div>
        )}

        {/* Error state */}
        {error && (
          <div className="max-w-md mx-auto flex flex-col items-center justify-center text-center space-y-4 p-8 glass-panel border border-rose-500/20 mt-8">
            <AlertCircle className="h-12 w-12 text-rose-500" />
            <h3 className="text-xl font-bold font-mono text-rose-500">Analysis Error</h3>
            <p className="text-sm font-mono text-muted">{error}</p>
          </div>
        )}

        {/* Results Panel */}
        {!loading && !error && data && (
          <div className="max-w-4xl mx-auto space-y-8 fade-in">
            {/* Headers Side by Side */}
            <div className="grid grid-cols-3 items-center justify-between glass-panel p-6 border border-white/10 text-center">
              <div className="flex flex-col items-center">
                <h3 className="text-2xl sm:text-3xl font-extrabold font-mono text-primary truncate max-w-[200px]">
                  {data.rival1.handle}
                </h3>
                <span className="text-xs text-muted font-mono mt-1 capitalize">{data.rival1.rank || 'Unrated'}</span>
              </div>
              <div className="flex flex-col items-center justify-center">
                <div className="bg-primary/20 text-primary border border-primary/30 h-12 w-12 rounded-full flex items-center justify-center font-bold font-mono">
                  VS
                </div>
              </div>
              <div className="flex flex-col items-center">
                <h3 className="text-2xl sm:text-3xl font-extrabold font-mono text-secondary truncate max-w-[200px]">
                  {data.rival2.handle}
                </h3>
                <span className="text-xs text-muted font-mono mt-1 capitalize">{data.rival2.rank || 'Unrated'}</span>
              </div>
            </div>

            {/* Split statistics */}
            <div className="glass-panel p-6 border border-white/10">
              <h4 className="text-lg font-bold font-mono text-primary text-center mb-6 border-b border-white/10 pb-4">
                Head-to-Head Comparison
              </h4>
              <div className="flex flex-col">
                {renderStatsRow('Current Rating', data.rival1.rating, data.rival2.rating)}
                {renderStatsRow('Max Rating', data.rival1.max_rating, data.rival2.max_rating)}
                {renderStatsRow('Total Contests', data.rival1.total_contests, data.rival2.total_contests)}
                {renderStatsRow('Problems Solved', data.rival1.problems_solved, data.rival2.problems_solved)}
                {renderStatsRow('Rating Growth', data.rival1.rating_growth, data.rival2.rating_growth)}
                {renderStatsRow('Consistency', data.rival1.consistency_score, data.rival2.consistency_score)}
              </div>
            </div>

            {/* Insights */}
            {data.insights?.length > 0 && (
              <div className="glass-panel p-6 border border-white/10">
                <h4 className="text-lg font-bold font-mono text-primary flex items-center gap-2 mb-4">
                  <Lightbulb className="h-5 w-5" /> Key Insights
                </h4>
                <ul className="space-y-2 text-sm text-muted font-mono">
                  {data.insights.map((insight, i) => (
                    <li key={i} className="flex gap-2">
                      <span className="text-primary">•</span> {insight}
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {/* Growth comparison chart */}
            <div className="glass-panel p-6 border border-white/10">
              <h4 className="text-lg font-bold font-mono text-primary text-center mb-6">
                Performance Comparison
              </h4>
              <GrowthCompareChart rival1={data.rival1} rival2={data.rival2} />
            </div>

            {/* Split tags (Strongest & Weakest) */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
              {/* Strongest Tags */}
              <div className="glass-panel p-6 border border-white/10 space-y-4">
                <h4 className="text-md font-bold font-mono text-green-400 flex items-center gap-2 border-b border-white/10 pb-3">
                  <Award className="h-5 w-5" /> Strongest Tags
                </h4>
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <h5 className="text-xs text-muted font-mono mb-2 uppercase">{data.rival1.handle}</h5>
                    <div className="space-y-2">
                      {data.rival1.strongest_tags.map((t, idx) => (
                        <div key={idx} className="bg-white/5 border border-white/5 p-2 rounded-lg text-xs font-mono flex justify-between">
                          <span className="truncate max-w-[100px]">{t.tag}</span>
                          <span className="text-green-400 font-bold">{Math.round(t.ac_rate * 100)}%</span>
                        </div>
                      ))}
                    </div>
                  </div>
                  <div className="border-l border-white/5 pl-4">
                    <h5 className="text-xs text-muted font-mono mb-2 uppercase">{data.rival2.handle}</h5>
                    <div className="space-y-2">
                      {data.rival2.strongest_tags.map((t, idx) => (
                        <div key={idx} className="bg-white/5 border border-white/5 p-2 rounded-lg text-xs font-mono flex justify-between">
                          <span className="truncate max-w-[100px]">{t.tag}</span>
                          <span className="text-green-400 font-bold">{Math.round(t.ac_rate * 100)}%</span>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              </div>

              {/* Weakest Tags */}
              <div className="glass-panel p-6 border border-white/10 space-y-4">
                <h4 className="text-md font-bold font-mono text-rose-400 flex items-center gap-2 border-b border-white/10 pb-3">
                  <AlertCircle className="h-5 w-5" /> Weakest Tags
                </h4>
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <h5 className="text-xs text-muted font-mono mb-2 uppercase">{data.rival1.handle}</h5>
                    <div className="space-y-2">
                      {data.rival1.weakest_tags.map((t, idx) => (
                        <div key={idx} className="bg-white/5 border border-white/5 p-2 rounded-lg text-xs font-mono flex justify-between">
                          <span className="truncate max-w-[100px]">{t.tag}</span>
                          <span className="text-rose-400 font-bold">{Math.round(t.ac_rate * 100)}%</span>
                        </div>
                      ))}
                    </div>
                  </div>
                  <div className="border-l border-white/5 pl-4">
                    <h5 className="text-xs text-muted font-mono mb-2 uppercase">{data.rival2.handle}</h5>
                    <div className="space-y-2">
                      {data.rival2.weakest_tags.map((t, idx) => (
                        <div key={idx} className="bg-white/5 border border-white/5 p-2 rounded-lg text-xs font-mono flex justify-between">
                          <span className="truncate max-w-[100px]">{t.tag}</span>
                          <span className="text-rose-400 font-bold">{Math.round(t.ac_rate * 100)}%</span>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  );
};

export default ComparePage;
