import React from 'react';
import { AnalysisResult } from '../types';

interface MetricsDashboardProps {
  data: AnalysisResult;
}

const MetricCard: React.FC<{ 
  title: string; 
  value: string | number; 
  icon: string;
  color: string;
}> = ({ title, value, icon, color }) => (
    <div className={`p-5 bg-gradient-to-br ${color} rounded-xl shadow-lg hover:shadow-xl transition-all duration-200 transform hover:-translate-y-1`}>
        <div className="flex items-center justify-between">
          <div>
            <h3 className="text-sm font-medium text-white/80 truncate">{title}</h3>
            <p className="mt-2 text-3xl font-bold text-white">{value}</p>
          </div>
          <span className="text-5xl opacity-20">{icon}</span>
        </div>
    </div>
);

const UserCard: React.FC<{
  user: string;
  messages: number;
  words: number;
  avgLength: number;
  isTopUser: boolean;
}> = ({ user, messages, words, avgLength, isTopUser }) => (
  <div className={`p-5 bg-gradient-to-br ${isTopUser ? 'from-purple-500 to-blue-500' : 'from-gray-700 to-gray-800'} rounded-xl shadow-lg hover:shadow-xl transition-all duration-200 transform hover:-translate-y-1`}>
    <div className="flex items-start justify-between mb-3">
      <div className="flex items-center gap-2">
        <span className="text-3xl">{isTopUser ? '👑' : '👤'}</span>
        <h4 className="font-bold text-white text-lg">{user}</h4>
      </div>
      {isTopUser && <span className="text-xs bg-yellow-400 text-yellow-900 px-2 py-1 rounded-full font-semibold">Most Active</span>}
    </div>
    <div className="space-y-2">
      <div className="flex items-center justify-between text-white/90">
        <span className="text-sm flex items-center gap-2">
          💬 <span>Messages</span>
        </span>
        <span className="font-semibold text-lg">{messages.toLocaleString()}</span>
      </div>
      <div className="flex items-center justify-between text-white/90">
        <span className="text-sm flex items-center gap-2">
          📝 <span>Words</span>
        </span>
        <span className="font-semibold text-lg">{words.toLocaleString()}</span>
      </div>
      <div className="flex items-center justify-between text-white/90">
        <span className="text-sm flex items-center gap-2">
          📊 <span>Avg Length</span>
        </span>
        <span className="font-semibold text-lg">{avgLength.toFixed(1)} words</span>
      </div>
    </div>
  </div>
);

export const MetricsDashboard: React.FC<MetricsDashboardProps> = ({ data }) => {
  const { basic_stats } = data;
  const users = Object.keys(basic_stats.messages_per_user);
  const topUser = users.reduce((a, b) => 
    basic_stats.messages_per_user[a] > basic_stats.messages_per_user[b] ? a : b
  );

  return (
    <div className="p-6 bg-gradient-to-br from-gray-50 to-gray-100 rounded-xl shadow-lg dark:from-gray-900 dark:to-gray-800">
      <div className="flex items-center gap-3 mb-6">
        <span className="text-3xl">📊</span>
        <h2 className="text-3xl font-bold bg-gradient-to-r from-purple-600 to-blue-600 bg-clip-text text-transparent dark:from-purple-400 dark:to-blue-400">
          Key Metrics
        </h2>
      </div>
      
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4 mb-8">
        <MetricCard 
          title="Total Messages" 
          value={basic_stats.total_messages.toLocaleString()} 
          icon="💬"
          color="from-blue-500 to-blue-600"
        />
        <MetricCard 
          title="Total Words" 
          value={basic_stats.total_words.toLocaleString()} 
          icon="📝"
          color="from-green-500 to-green-600"
        />
        <MetricCard 
          title="Chat Duration" 
          value={`${basic_stats.chat_duration_days} days`}
          icon="📅"
          color="from-purple-500 to-purple-600"
        />
        <MetricCard 
          title="Daily Average" 
          value={Math.round(basic_stats.total_messages / Math.max(basic_stats.chat_duration_days, 1))}
          icon="⚡"
          color="from-orange-500 to-orange-600"
        />
      </div>
      
      <div className="mt-8">
        <div className="flex items-center gap-3 mb-5">
          <span className="text-2xl">👥</span>
          <h3 className="text-2xl font-bold text-gray-900 dark:text-white">Participant Activity</h3>
        </div>
        <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-2">
            {users.map(user => (
                <UserCard
                  key={user}
                  user={user}
                  messages={basic_stats.messages_per_user[user]}
                  words={basic_stats.words_per_user[user]}
                  avgLength={basic_stats.avg_message_length_per_user[user]}
                  isTopUser={user === topUser}
                />
            ))}
        </div>
      </div>
    </div>
  );
};
