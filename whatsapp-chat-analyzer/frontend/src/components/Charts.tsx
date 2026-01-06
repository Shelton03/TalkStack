import React from 'react';
import { BarChart, Bar, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, Cell } from 'recharts';
import { AnalysisResult } from '../types';

interface ChartsProps {
  data: AnalysisResult;
}

const ChartContainer: React.FC<{ title: string; icon: string; children: React.ReactNode }> = ({ title, icon, children }) => (
    <div className="p-6 bg-white rounded-xl shadow-lg dark:bg-gray-800 hover:shadow-xl transition-shadow duration-200">
        <div className="flex items-center gap-3 mb-4">
            <span className="text-2xl">{icon}</span>
            <h3 className="text-lg font-bold text-gray-900 dark:text-white">{title}</h3>
        </div>
        <div className="h-72">
            {children}
        </div>
    </div>
);

const COLORS = ['#8b5cf6', '#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#ec4899', '#14b8a6', '#f97316'];

const CustomTooltip = ({ active, payload, label }: any) => {
  if (active && payload && payload.length) {
    return (
      <div className="bg-gray-900 text-white p-3 rounded-lg shadow-lg border border-gray-700">
        <p className="font-semibold">{label}</p>
        {payload.map((entry: any, index: number) => (
          <p key={index} style={{ color: entry.color }}>
            {entry.name}: {entry.value}
          </p>
        ))}
      </div>
    );
  }
  return null;
};


export const Charts: React.FC<ChartsProps> = ({ data }) => {
  const { temporal_stats, linguistic_stats } = data;

  return (
    <div className="p-6 bg-gradient-to-br from-gray-50 to-gray-100 rounded-xl shadow-lg dark:from-gray-900 dark:to-gray-800 mt-6">
        <div className="flex items-center gap-3 mb-6">
            <span className="text-3xl">📈</span>
            <h2 className="text-3xl font-bold bg-gradient-to-r from-purple-600 to-blue-600 bg-clip-text text-transparent dark:from-purple-400 dark:to-blue-400">
                Visualizations
            </h2>
        </div>
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <ChartContainer title="Message Volume Over Time" icon="📅">
                <ResponsiveContainer width="100%" height="100%">
                    <LineChart data={temporal_stats.message_volume_over_time} margin={{ top: 5, right: 20, left: -10, bottom: 5 }}>
                        <CartesianGrid strokeDasharray="3 3" stroke="#374151" opacity={0.3} />
                        <XAxis 
                          dataKey="date" 
                          stroke="#6b7280"
                          tick={{ fontSize: 12 }}
                        />
                        <YAxis stroke="#6b7280" />
                        <Tooltip content={<CustomTooltip />} />
                        <Legend />
                        <Line 
                          type="monotone" 
                          dataKey="message_count" 
                          name="Messages" 
                          stroke="#8b5cf6" 
                          strokeWidth={3}
                          dot={{ fill: '#8b5cf6', r: 4 }}
                          activeDot={{ r: 6 }}
                        />
                    </LineChart>
                </ResponsiveContainer>
            </ChartContainer>

            <ChartContainer title="Activity by Hour of Day" icon="🕐">
                <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={temporal_stats.activity_by_hour} margin={{ top: 5, right: 20, left: -10, bottom: 5 }}>
                        <CartesianGrid strokeDasharray="3 3" stroke="#374151" opacity={0.3} />
                        <XAxis 
                          dataKey="hour" 
                          stroke="#6b7280"
                          tick={{ fontSize: 12 }}
                        />
                        <YAxis stroke="#6b7280" />
                        <Tooltip content={<CustomTooltip />} />
                        <Legend />
                        <Bar dataKey="message_count" name="Messages" radius={[8, 8, 0, 0]}>
                          {temporal_stats.activity_by_hour.map((_entry: any, index: number) => (
                            <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                          ))}
                        </Bar>
                    </BarChart>
                </ResponsiveContainer>
            </ChartContainer>

            <ChartContainer title="Activity by Day of Week" icon="📆">
                <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={temporal_stats.activity_by_day_of_week} margin={{ top: 5, right: 20, left: -10, bottom: 5 }}>
                        <CartesianGrid strokeDasharray="3 3" stroke="#374151" opacity={0.3} />
                        <XAxis 
                          dataKey="day" 
                          stroke="#6b7280"
                          tick={{ fontSize: 12 }}
                        />
                        <YAxis stroke="#6b7280" />
                        <Tooltip content={<CustomTooltip />} />
                        <Legend />
                        <Bar dataKey="message_count" name="Messages" fill="#10b981" radius={[8, 8, 0, 0]}>
                          {temporal_stats.activity_by_day_of_week.map((_entry: any, index: number) => (
                            <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                          ))}
                        </Bar>
                    </BarChart>
                </ResponsiveContainer>
            </ChartContainer>
            
            <ChartContainer title="Most Common Words" icon="🔤">
                <ResponsiveContainer width="100%" height="100%">
                    <BarChart 
                      layout="vertical" 
                      data={linguistic_stats.most_common_words.slice(0, 10).reverse()} 
                      margin={{ top: 5, right: 20, left: 60, bottom: 5 }}
                    >
                         <CartesianGrid strokeDasharray="3 3" stroke="#374151" opacity={0.3} />
                         <XAxis type="number" stroke="#6b7280" />
                         <YAxis 
                           type="category" 
                           dataKey="word" 
                           stroke="#6b7280"
                           tick={{ fontSize: 12 }}
                         />
                         <Tooltip content={<CustomTooltip />} />
                         <Legend />
                         <Bar dataKey="count" name="Frequency" radius={[0, 8, 8, 0]}>
                           {linguistic_stats.most_common_words.slice(0, 10).map((_entry: any, index: number) => (
                             <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                           ))}
                         </Bar>
                    </BarChart>
                </ResponsiveContainer>
            </ChartContainer>

        </div>
    </div>
  );
};
