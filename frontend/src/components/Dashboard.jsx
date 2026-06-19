import React from 'react';
import {
  WeakTopicsChart,
  SuccessRateRadar,
  RatingTimelineChart,
  RankTimelineChart,
  RatingChangeChart,
} from './Charts';
import {
  Target,
  AlertTriangle,
  Code2,
  Trophy,
  TrendingUp,
  BookOpen,
  Zap,
  Award,
  BarChart3,
} from 'lucide-react';

const progressionColors = {
  foundation: 'text-blue-400 bg-blue-400/10 border-blue-400/30',
  comfortable: 'text-green-400 bg-green-400/10 border-green-400/30',
  growth: 'text-yellow-400 bg-yellow-400/10 border-yellow-400/30',
  challenge: 'text-rose-400 bg-rose-400/10 border-rose-400/30',
};

const TagHeatmap = ({ data }) => {
  if (!data || data.length === 0) return null;
  return (
    <div className="glass-panel p-6 sm:p-8 rounded-2xl">
      <h3 className="text-xl font-bold mb-2 text-primary">Topic Performance Heatmap</h3>
      <p className="text-muted text-sm mb-6">Red = weak, green = strong. Hover for details.</p>
      <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-3">
        {data.map((item, idx) => {
          const hue = item.ac_rate * 120;
          return (
            <div
              key={idx}
              className="relative group p-3 rounded-xl border border-white/10 transition-all hover:scale-[1.03]"
              style={{
                background: `linear-gradient(135deg, hsla(${hue}, 80%, 25%, 0.1) 0%, hsla(${hue}, 80%, 15%, 0.3) 100%)`,
                borderColor: `hsla(${hue}, 80%, 40%, 0.25)`,
              }}
            >
              <h4 className="font-bold text-xs truncate" title={item.tag}>{item.tag}</h4>
              <p className="text-[10px] text-muted mt-1">{item.total} attempts</p>
              <span className="text-sm font-extrabold" style={{ color: `hsl(${hue}, 90%, 55%)` }}>
                {Math.round(item.ac_rate * 100)}%
              </span>
            </div>
          );
        })}
      </div>
    </div>
  );
};

const TopicList = ({ title, topics, variant = 'weak' }) => {
  if (!topics?.length) return null;
  const color = variant === 'strong' ? 'text-green-400' : 'text-rose-400';
  return (
    <div className="glass-panel p-6 rounded-2xl">
      <h3 className={`text-lg font-bold mb-4 flex items-center gap-2 ${color}`}>
        {variant === 'strong' ? <Award className="h-5 w-5" /> : <AlertTriangle className="h-5 w-5" />}
        {title}
      </h3>
      <div className="space-y-2">
        {topics.map((t, i) => (
          <div key={i} className="flex justify-between items-center bg-white/5 rounded-lg px-3 py-2 text-sm">
            <span className="truncate font-medium">{t.topic}</span>
            <div className="flex gap-3 text-xs text-muted">
              <span>{Math.round(t.success_rate * 100)}% AC</span>
              {t.relative_performance_score != null && (
                <span className="text-primary">Score: {t.relative_performance_score}</span>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

const Dashboard = ({ handle, data }) => {
  const {
    total_submissions,
    weak_topics = [],
    strongest_topics = [],
    weakest_topics = [],
    recommendations = [],
    topic_recommendations = [],
    percentile = [],
    contestAnalytics,
    problemRecommendations = [],
    ratingPrediction,
    rating,
    max_rating,
  } = data;

  const hasWeakTopics = weak_topics.length > 0;
  const timeline = contestAnalytics?.rating_timeline || [];

  let topPercentage = null;
  if (percentile?.length) {
    const avgPercentile = percentile.reduce((a, c) => a + c.percentile, 0) / percentile.length;
    topPercentage = (100 - avgPercentile).toFixed(1);
  }

  const trendLabels = {
    strong_growth: 'Strong Growth',
    growing: 'Growing',
    stable: 'Stable',
    declining: 'Declining',
    insufficient_data: 'Need More Data',
  };

  return (
    <div className="w-full max-w-7xl mx-auto space-y-10 fade-in p-4 sm:p-8 lg:p-12">
      {/* Header */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-end gap-6">
        <div>
          <h1 className="text-3xl md:text-5xl font-extrabold bg-gradient-to-r from-primary to-secondary bg-clip-text text-transparent">
            {handle}
          </h1>
          <p className="text-muted mt-2">
            {rating != null ? (
              <span>
                Rating <span className="text-primary font-bold">{rating}</span>
                {max_rating != null && (
                  <span className="ml-3">Max <span className="text-secondary font-bold">{max_rating}</span></span>
                )}
              </span>
            ) : (
              'Unrated'
            )}
            <span className="ml-3">· {total_submissions} submissions analyzed</span>
          </p>
        </div>
      </div>

      {/* Stats cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="glass-panel p-6 rounded-2xl relative">
          <p className="text-muted text-sm mb-1">Total Submissions</p>
          <h3 className="text-3xl font-extrabold text-primary">{total_submissions}</h3>
          <Code2 className="h-8 w-8 text-primary/40 absolute right-4 top-4" />
        </div>
        <div className="glass-panel p-6 rounded-2xl relative">
          <p className="text-muted text-sm mb-1">Weak Areas</p>
          <h3 className="text-2xl font-bold text-rose-400">{weak_topics.length}</h3>
          <AlertTriangle className="h-8 w-8 text-rose-400/40 absolute right-4 top-4" />
        </div>
        <div className="glass-panel p-6 rounded-2xl relative">
          <p className="text-muted text-sm mb-1">Contest Performance</p>
          <h3 className="text-2xl font-extrabold text-yellow-400">
            {topPercentage != null ? `Top ${topPercentage}%` : 'N/A'}
          </h3>
          <Trophy className="h-8 w-8 text-yellow-400/40 absolute right-4 top-4" />
        </div>
        <div className="glass-panel p-6 rounded-2xl relative">
          <p className="text-muted text-sm mb-1">Consistency</p>
          <h3 className="text-2xl font-extrabold text-secondary">
            {contestAnalytics?.consistency_score ?? '—'}
          </h3>
          <BarChart3 className="h-8 w-8 text-secondary/40 absolute right-4 top-4" />
        </div>
      </div>

      {/* Rating prediction */}
      {ratingPrediction && (
        <div className="glass-panel p-6 sm:p-8 rounded-2xl border border-primary/20">
          <h2 className="text-xl font-bold text-primary flex items-center gap-2 mb-4">
            <TrendingUp className="h-5 w-5" /> Rating Growth Predictor
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div>
              <p className="text-muted text-sm">Predicted Range (3 contests)</p>
              <p className="text-2xl font-bold mt-1">
                {ratingPrediction.predicted_rating_low} – {ratingPrediction.predicted_rating_high}
              </p>
              <p className="text-sm text-muted mt-1">
                Mid estimate: <span className="text-primary font-bold">{ratingPrediction.predicted_rating_mid}</span>
              </p>
            </div>
            <div>
              <p className="text-muted text-sm">Confidence</p>
              <p className="text-2xl font-bold mt-1">{Math.round(ratingPrediction.confidence_score * 100)}%</p>
              <p className="text-sm text-muted mt-1">
                Trend: {trendLabels[ratingPrediction.trend] || ratingPrediction.trend}
              </p>
            </div>
            <div>
              <p className="text-muted text-sm mb-2">Suggested Improvements</p>
              <ul className="text-sm space-y-1">
                {ratingPrediction.suggested_improvements?.slice(0, 3).map((s, i) => (
                  <li key={i} className="text-muted flex gap-2">
                    <Zap className="h-3 w-3 text-primary shrink-0 mt-0.5" />
                    {s}
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </div>
      )}

      {/* Contest analytics */}
      {contestAnalytics && contestAnalytics.total_contests > 0 && (
        <div className="space-y-6">
          <h2 className="text-xl font-bold text-primary flex items-center gap-2">
            <Trophy className="h-5 w-5" /> Contest Performance Analytics
          </h2>
          <p className="text-muted text-sm">{contestAnalytics.summary}</p>
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
            <div className="glass-panel p-4 rounded-xl text-center">
              <p className="text-xs text-muted">Total Growth</p>
              <p className="text-xl font-bold text-primary">{contestAnalytics.total_rating_growth}</p>
            </div>
            <div className="glass-panel p-4 rounded-xl text-center">
              <p className="text-xs text-muted">Avg Change</p>
              <p className="text-xl font-bold">{contestAnalytics.avg_rating_change}</p>
            </div>
            <div className="glass-panel p-4 rounded-xl text-center">
              <p className="text-xs text-muted">Upsolves</p>
              <p className="text-xl font-bold">{contestAnalytics.upsolve_count}</p>
            </div>
            <div className="glass-panel p-4 rounded-xl text-center">
              <p className="text-xs text-muted">Contest Freq (days)</p>
              <p className="text-xl font-bold">{contestAnalytics.avg_days_between_contests}</p>
            </div>
          </div>
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div className="glass-panel p-6 rounded-2xl">
              <h3 className="font-bold mb-4">Rating Timeline</h3>
              <RatingTimelineChart data={timeline} />
            </div>
            <div className="glass-panel p-6 rounded-2xl">
              <h3 className="font-bold mb-4">Rank Trends</h3>
              <RankTimelineChart data={contestAnalytics.rank_timeline} />
            </div>
          </div>
          <div className="glass-panel p-6 rounded-2xl">
            <h3 className="font-bold mb-4">Per-Contest Rating Changes</h3>
            <RatingChangeChart data={timeline} />
          </div>
        </div>
      )}

      {/* Topic strength / weakness */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <TopicList title="Strongest Topics" topics={strongest_topics} variant="strong" />
        <TopicList title="Weakest Topics" topics={weakest_topics} variant="weak" />
      </div>

      {/* Weak topic charts */}
      {hasWeakTopics && (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div className="glass-panel p-6 rounded-2xl">
            <h3 className="font-bold mb-4 text-primary">Attempts vs Solves</h3>
            <WeakTopicsChart data={weak_topics} />
          </div>
          <div className="glass-panel p-6 rounded-2xl">
            <h3 className="font-bold mb-4 text-secondary">Success Rate Radar</h3>
            <SuccessRateRadar data={weak_topics} />
          </div>
        </div>
      )}

      {/* Problem recommendations */}
      {problemRecommendations?.length > 0 && (
        <div className="glass-panel p-6 sm:p-8 rounded-2xl">
          <h2 className="text-xl font-bold text-primary flex items-center gap-2 mb-6">
            <BookOpen className="h-5 w-5" /> Recommended Problems
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {problemRecommendations.map((p, i) => (
              <a
                key={i}
                href={p.url}
                target="_blank"
                rel="noopener noreferrer"
                className="block p-4 rounded-xl bg-white/5 border border-white/10 hover:border-primary/40 transition-colors"
              >
                <div className="flex justify-between items-start gap-2">
                  <div>
                    <p className="font-bold text-sm">{p.name}</p>
                    {p.contest_id && p.index && (
                      <p className="text-xs text-muted">{p.contest_id}{p.index}</p>
                    )}
                  </div>
                  <div className="flex items-center gap-2">
                    {p.rating && <span className="text-primary font-bold text-sm">{p.rating}</span>}
                    <span className={`text-[10px] px-2 py-0.5 rounded border ${progressionColors[p.difficulty_progression] || ''}`}>
                      {p.difficulty_progression}
                    </span>
                  </div>
                </div>
                <p className="text-xs text-muted mt-2">{p.reason}</p>
                {p.tags?.length > 0 && (
                  <div className="flex flex-wrap gap-1 mt-2">
                    {p.tags.slice(0, 3).map((tag) => (
                      <span key={tag} className="text-[10px] bg-white/5 px-2 py-0.5 rounded">{tag}</span>
                    ))}
                  </div>
                )}
              </a>
            ))}
          </div>
        </div>
      )}

      {/* Topic improvement recommendations */}
      {topic_recommendations?.length > 0 && (
        <div className="glass-panel p-6 rounded-2xl">
          <h3 className="font-bold text-secondary flex items-center gap-2 mb-4">
            <Target className="h-5 w-5" /> Improvement Recommendations
          </h3>
          <ul className="space-y-2 text-sm text-muted">
            {topic_recommendations.map((rec, i) => (
              <li key={i} className="flex gap-2">
                <span className="text-primary">→</span> {rec}
              </li>
            ))}
          </ul>
        </div>
      )}

      {data.tagAnalysis && <TagHeatmap data={data.tagAnalysis} />}
    </div>
  );
};

export default Dashboard;
