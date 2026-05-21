import React from 'react';

const SkeletonLoader = () => {
  return (
    <div className="w-full max-w-6xl mx-auto space-y-8 animate-pulse p-6">
      <div className="h-12 bg-surface rounded-xl w-1/3 mb-10"></div>
      
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        {[1, 2, 3].map((i) => (
          <div key={i} className="h-32 bg-surface rounded-2xl border border-white/5"></div>
        ))}
      </div>
      
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <div className="h-96 bg-surface rounded-2xl border border-white/5"></div>
        <div className="h-96 bg-surface rounded-2xl border border-white/5"></div>
      </div>
    </div>
  );
};

export default SkeletonLoader;
