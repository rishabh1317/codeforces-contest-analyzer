import { useState, useEffect } from 'react';
import { getAnalysis } from '../api/api';

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
        const result = await getAnalysis(platform, handle);
        setData(result);
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
