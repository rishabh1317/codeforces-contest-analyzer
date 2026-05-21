import React from 'react';
import { WeakTopicsChart, SuccessRateRadar } from './Charts';
import { Target, AlertTriangle, Code2 } from 'lucide-react';


const Dashboard = ({ handle, data }) => {
  const { total_submissions, weak_topics = [], recommendations = [] } = data;

  const hasWeakTopics = weak_topics && weak_topics.length > 0;

  return (
    <div className="w-full max-w-7xl mx-auto space-y-12 fade-in p-4 sm:p-8 lg:p-12">
      {/* Header section */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-end gap-6 mb-12">
        <div>
          <h1 className="text-4xl md:text-5xl font-extrabold bg-gradient-to-r from-primary to-secondary bg-clip-text text-transparent drop-shadow-xl animate-fade-in">
            {handle}'s Analysis
          </h1>
          <p className="text-lg text-muted mt-3 font-medium">Based on <span className="text-primary font-bold">{total_submissions}</span> Codeforces submissions</p>
        </div>
        <div className="glass-panel px-8 py-4 flex items-center gap-4 rounded-2xl shadow-xl border border-primary/30 bg-gradient-to-r from-primary/20 to-secondary/20 animate-fade-in">
          <Code2 className="text-primary h-8 w-8" />
          <span className="font-bold text-lg">{weak_topics.length} Weak Areas Identified</span>
        </div>
      </div>

      {/* Top Level Stats */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-12">
        {/* Card 1: Total Submissions */}
        <div className="glass-panel p-8 relative overflow-hidden group rounded-2xl shadow-xl bg-gradient-to-br from-primary/20 to-white/10 hover:scale-[1.03] hover:shadow-2xl transition-all duration-300">
          <div className="absolute -right-6 -top-6 w-32 h-32 bg-primary/30 rounded-full blur-2xl group-hover:bg-primary/40 transition-all"></div>
          <div className="flex flex-col items-start">
            <p className="text-muted text-base font-semibold mb-2">Total Submissions</p>
            <h3 className="text-4xl font-extrabold text-primary drop-shadow animate-fade-in">{total_submissions}</h3>
          </div>
          <Target className="text-primary h-10 w-10 absolute right-4 top-4 opacity-60" />
        </div>
        {/* Card 2: Most Weak Topic */}
        <div className="glass-panel p-8 relative overflow-hidden group rounded-2xl shadow-xl bg-gradient-to-br from-rose-500/20 to-white/10 hover:scale-[1.03] hover:shadow-2xl transition-all duration-300">
          <div className="absolute -right-6 -top-6 w-32 h-32 bg-rose-500/30 rounded-full blur-2xl group-hover:bg-rose-500/40 transition-all"></div>
          <div className="flex flex-col items-start">
            <p className="text-muted text-base font-semibold mb-2">Most Weak Topic</p>
            <h3 className="text-2xl font-bold text-rose-500 truncate max-w-[180px] animate-fade-in" title={weak_topics[0]?.topic}>
              {hasWeakTopics ? weak_topics[0].topic : 'None'}
            </h3>
          </div>
          <AlertTriangle className="text-rose-400 h-10 w-10 absolute right-4 top-4 opacity-60" />
        </div>
        {/* Card 3: Next Recommended Action */}
        <div className="glass-panel p-8 relative overflow-hidden group flex flex-col justify-center rounded-2xl shadow-xl bg-gradient-to-br from-secondary/20 to-white/10 hover:scale-[1.03] hover:shadow-2xl transition-all duration-300">
          <h3 className="text-xl font-bold mb-3 text-secondary">Next Recommended Action</h3>
          {hasWeakTopics && recommendations && recommendations.length > 0 ? (
            <div className="flex flex-col gap-2 max-h-48 overflow-y-auto">
              {recommendations.slice(0, 3).map((rec, idx) => (
                <a
                  key={idx}
                  href={rec.suggested_url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="block px-4 py-2 rounded-lg bg-primary/10 hover:bg-primary/20 text-primary font-semibold transition-colors border border-primary/20 shadow-md animate-fade-in"
                >
                  {rec.action}
                </a>
              ))}
            </div>
          ) : (
            <p className="text-base text-muted">No weak topics detected. <span className="text-green-500 font-semibold">Great job!</span></p>
          )}
        </div>
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-10">
        <div className="glass-panel p-8 rounded-2xl shadow-md">
          <h3 className="text-2xl font-bold mb-6 text-primary">Attempt vs Solve by Topic</h3>
          {hasWeakTopics ? (
            <WeakTopicsChart data={weak_topics} />
          ) : (
            <div className="text-center text-muted py-16">No weak topic data to display.</div>
          )}
        </div>
        <div className="glass-panel p-8 rounded-2xl shadow-md">
          <h3 className="text-2xl font-bold mb-6 text-secondary">Topic Success Rates</h3>
          {hasWeakTopics ? (
            <SuccessRateRadar data={weak_topics} />
          ) : (
            <div className="text-center text-muted py-16">No weak topic data to display.</div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
