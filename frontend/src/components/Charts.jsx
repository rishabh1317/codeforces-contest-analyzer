import React from 'react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  Radar,
  LineChart,
  Line,
  Legend,
  AreaChart,
  Area,
} from 'recharts';

const chartTooltipStyle = {
  backgroundColor: '#161b22',
  borderColor: '#30363d',
  color: '#f0f6fc',
  borderRadius: '8px',
};

export const WeakTopicsChart = ({ data }) => {
  return (
    <div className="h-80 w-full fade-in">
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={data} margin={{ top: 20, right: 30, left: 20, bottom: 35 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#30363d" vertical={false} />
          <XAxis
            dataKey="topic"
            stroke="#8b949e"
            tick={{ fill: '#8b949e', fontSize: 10 }}
            interval={0}
            angle={-25}
            textAnchor="end"
            height={60}
          />
          <YAxis stroke="#8b949e" tick={{ fill: '#8b949e', fontSize: 11 }} />
          <Tooltip contentStyle={chartTooltipStyle} itemStyle={{ color: '#00d4ff' }} />
          <Bar dataKey="attempted" name="Attempts" fill="#9d4edd" radius={[4, 4, 0, 0]} />
          <Bar dataKey="solved" name="Solved" fill="#00d4ff" radius={[4, 4, 0, 0]} />
          <Legend />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};

export const SuccessRateRadar = ({ data }) => {
  return (
    <div className="h-80 w-full fade-in">
      <ResponsiveContainer width="100%" height="100%">
        <RadarChart cx="50%" cy="50%" outerRadius="70%" data={data}>
          <PolarGrid stroke="#30363d" />
          <PolarAngleAxis dataKey="topic" tick={{ fill: '#8b949e', fontSize: 10 }} />
          <PolarRadiusAxis angle={30} domain={[0, 1]} tick={{ fill: '#8b949e', fontSize: 9 }} stroke="#30363d" />
          <Radar
            name="Success Rate"
            dataKey="success_rate"
            stroke="#00d4ff"
            fill="#00d4ff"
            fillOpacity={0.4}
          />
          <Tooltip contentStyle={chartTooltipStyle} itemStyle={{ color: '#00d4ff' }} />
        </RadarChart>
      </ResponsiveContainer>
    </div>
  );
};

export const RatingTimelineChart = ({ data }) => {
  if (!data?.length) return null;
  const chartData = data.map((d) => ({
    name: d.contest_name?.slice(0, 20) || 'Contest',
    rating: d.rating,
    change: d.rating_change,
  }));

  return (
    <div className="h-80 w-full fade-in">
      <ResponsiveContainer width="100%" height="100%">
        <AreaChart data={chartData} margin={{ top: 10, right: 20, left: 0, bottom: 40 }}>
          <defs>
            <linearGradient id="ratingGrad" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="#00d4ff" stopOpacity={0.4} />
              <stop offset="95%" stopColor="#00d4ff" stopOpacity={0} />
            </linearGradient>
          </defs>
          <CartesianGrid strokeDasharray="3 3" stroke="#30363d" vertical={false} />
          <XAxis
            dataKey="name"
            stroke="#8b949e"
            tick={{ fill: '#8b949e', fontSize: 9 }}
            angle={-30}
            textAnchor="end"
            height={50}
          />
          <YAxis stroke="#8b949e" tick={{ fill: '#8b949e', fontSize: 11 }} domain={['auto', 'auto']} />
          <Tooltip contentStyle={chartTooltipStyle} />
          <Area type="monotone" dataKey="rating" stroke="#00d4ff" fill="url(#ratingGrad)" name="Rating" />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  );
};

export const RankTimelineChart = ({ data }) => {
  if (!data?.length) return null;
  const chartData = data.map((d) => ({
    name: d.contest_name?.slice(0, 20) || 'Contest',
    rank: d.rank,
  }));

  return (
    <div className="h-80 w-full fade-in">
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={chartData} margin={{ top: 10, right: 20, left: 0, bottom: 40 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#30363d" vertical={false} />
          <XAxis
            dataKey="name"
            stroke="#8b949e"
            tick={{ fill: '#8b949e', fontSize: 9 }}
            angle={-30}
            textAnchor="end"
            height={50}
          />
          <YAxis
            stroke="#8b949e"
            tick={{ fill: '#8b949e', fontSize: 11 }}
            reversed
            domain={['auto', 'auto']}
          />
          <Tooltip contentStyle={chartTooltipStyle} />
          <Line type="monotone" dataKey="rank" stroke="#9d4edd" strokeWidth={2} dot={{ r: 3 }} name="Rank" />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};

export const RatingChangeChart = ({ data }) => {
  if (!data?.length) return null;
  const chartData = data.map((d) => ({
    name: d.contest_name?.slice(0, 15) || 'C',
    change: d.rating_change,
  }));

  return (
    <div className="h-64 w-full fade-in">
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={chartData} margin={{ top: 10, right: 20, left: 0, bottom: 30 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#30363d" vertical={false} />
          <XAxis dataKey="name" stroke="#8b949e" tick={{ fill: '#8b949e', fontSize: 9 }} />
          <YAxis stroke="#8b949e" tick={{ fill: '#8b949e', fontSize: 11 }} />
          <Tooltip contentStyle={chartTooltipStyle} />
          <Bar
            dataKey="change"
            name="Rating Change"
            fill="#00d4ff"
            radius={[4, 4, 0, 0]}
          />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};

export const GrowthCompareChart = ({ rival1, rival2 }) => {
  const data = [
    { metric: 'Rating', [rival1.handle]: rival1.rating || 0, [rival2.handle]: rival2.rating || 0 },
    { metric: 'Max Rating', [rival1.handle]: rival1.max_rating || 0, [rival2.handle]: rival2.max_rating || 0 },
    { metric: 'Growth', [rival1.handle]: rival1.rating_growth || 0, [rival2.handle]: rival2.rating_growth || 0 },
    { metric: 'Solved', [rival1.handle]: rival1.problems_solved || 0, [rival2.handle]: rival2.problems_solved || 0 },
    { metric: 'Contests', [rival1.handle]: rival1.total_contests || 0, [rival2.handle]: rival2.total_contests || 0 },
  ];

  return (
    <div className="h-80 w-full fade-in">
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={data} margin={{ top: 10, right: 20, left: 0, bottom: 10 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#30363d" vertical={false} />
          <XAxis dataKey="metric" stroke="#8b949e" tick={{ fill: '#8b949e', fontSize: 11 }} />
          <YAxis stroke="#8b949e" tick={{ fill: '#8b949e', fontSize: 11 }} />
          <Tooltip contentStyle={chartTooltipStyle} />
          <Bar dataKey={rival1.handle} fill="#00d4ff" radius={[4, 4, 0, 0]} />
          <Bar dataKey={rival2.handle} fill="#9d4edd" radius={[4, 4, 0, 0]} />
          <Legend />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};
