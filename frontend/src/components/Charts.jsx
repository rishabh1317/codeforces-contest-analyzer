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
  Legend
} from 'recharts';

export const WeakTopicsChart = ({ data }) => {
  return (
    <div className="h-80 w-full fade-in">
      <ResponsiveContainer width="100%" height="100%">
        <BarChart
          data={data}
          margin={{ top: 20, right: 30, left: 20, bottom: 20 }}
        >
          <CartesianGrid strokeDasharray="3 3" stroke="#334155" vertical={false} />
          <XAxis dataKey="topic" stroke="#94a3b8" tick={{fill: '#94a3b8'}} />
          <YAxis stroke="#94a3b8" tick={{fill: '#94a3b8'}} />
          <Tooltip 
            contentStyle={{ backgroundColor: '#1e293b', borderColor: '#334155', color: '#f8fafc' }}
            itemStyle={{ color: '#38bdf8' }}
          />
          <Bar dataKey="attempted" name="Attempts" fill="#818cf8" radius={[4, 4, 0, 0]} />
          <Bar dataKey="solved" name="Solved" fill="#38bdf8" radius={[4, 4, 0, 0]} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};

export const SuccessRateRadar = ({ data }) => {
  return (
    <div className="h-80 w-full fade-in">
      <ResponsiveContainer width="100%" height="100%">
        <RadarChart cx="50%" cy="50%" outerRadius="80%" data={data}>
          <PolarGrid stroke="#334155" />
          <PolarAngleAxis dataKey="topic" tick={{ fill: '#94a3b8', fontSize: 12 }} />
          <PolarRadiusAxis angle={30} domain={[0, 1]} tick={false} axisLine={false} />
          <Radar
            name="Success Rate"
            dataKey="success_rate"
            stroke="#38bdf8"
            fill="#38bdf8"
            fillOpacity={0.6}
          />
          <Tooltip 
             contentStyle={{ backgroundColor: '#1e293b', borderColor: '#334155', color: '#f8fafc' }}
             itemStyle={{ color: '#38bdf8' }}
          />
        </RadarChart>
      </ResponsiveContainer>
    </div>
  );
};
