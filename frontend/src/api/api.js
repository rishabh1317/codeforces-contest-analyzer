import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const getDashboard = async (handle) => {
  const response = await apiClient.get(`/api/users/${handle}/dashboard`);
  return response.data;
};

export const getAnalysis = async (platform, handle) => {
  const response = await apiClient.get(`/analysis/${platform}/${handle}`);
  return response.data;
};

export const getTagAnalysis = async (handle) => {
  const response = await apiClient.get(`/api/users/${handle}/tag-analysis`);
  return response.data;
};

export const getPercentile = async (handle) => {
  const response = await apiClient.get(`/api/users/${handle}/percentile`);
  return response.data;
};

export const getContestAnalytics = async (handle) => {
  const response = await apiClient.get(`/api/users/${handle}/contest-analytics`);
  return response.data;
};

export const getRecommendations = async (handle, limit = 10) => {
  const response = await apiClient.get(`/api/users/${handle}/recommendations?limit=${limit}`);
  return response.data;
};

export const getRatingPrediction = async (handle) => {
  const response = await apiClient.get(`/api/users/${handle}/rating-prediction`);
  return response.data;
};

export const compareRivals = async (handle1, handle2) => {
  const response = await apiClient.get(`/api/compare?handle1=${handle1}&handle2=${handle2}`);
  return response.data;
};
