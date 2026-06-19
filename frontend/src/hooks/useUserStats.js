import { useState, useEffect } from 'react';
import { getDashboard } from '../api/api';

export const useUserStats = (platform, handle) => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!platform || !handle) {
      setLoading(false);
      return;
    }

    const fetchData = async () => {
      setLoading(true);
      setError(null);
      try {
        const dashboard = await getDashboard(handle);
        setData({
          ...dashboard.analysis,
          rating: dashboard.rating,
          max_rating: dashboard.max_rating,
          tagAnalysis: dashboard.tag_analysis,
          percentile: dashboard.percentile,
          contestAnalytics: dashboard.contest_analytics,
          problemRecommendations: dashboard.problem_recommendations,
          ratingPrediction: dashboard.rating_prediction,
          strongest_topics: dashboard.analysis.strongest_topics,
          weakest_topics: dashboard.analysis.weakest_topics,
          topic_recommendations: dashboard.analysis.topic_recommendations,
        });
      } catch (err) {
        setError(err.response?.data?.detail || err.message || 'An error occurred');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [platform, handle]);

  return { data, loading, error };
};
