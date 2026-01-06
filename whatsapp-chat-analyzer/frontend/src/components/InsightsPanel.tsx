import React from 'react';
import { AnalysisResult } from '../types';

interface InsightsPanelProps {
  data: AnalysisResult;
}

export const InsightsPanel: React.FC<InsightsPanelProps> = ({ data }) => {
  const { insights, transcriptions } = data;

  return (
    <div className="p-6 bg-gradient-to-br from-purple-50 to-blue-50 rounded-xl shadow-lg dark:from-gray-800 dark:to-gray-900 mt-6 space-y-6">
      {insights && (
        <div>
          <div className="flex items-center gap-3 mb-4">
            <span className="text-3xl">💡</span>
            <h2 className="text-2xl font-bold bg-gradient-to-r from-purple-600 to-blue-600 bg-clip-text text-transparent dark:from-purple-400 dark:to-blue-400">
              Chat Insights
            </h2>
          </div>
          <div className="p-6 bg-white rounded-xl shadow-md dark:bg-gray-800 border-l-4 border-purple-500">
            <div className="prose prose-sm max-w-none dark:prose-invert">
              <p className="text-gray-700 dark:text-gray-300 whitespace-pre-wrap leading-relaxed">
                {insights}
              </p>
            </div>
          </div>
        </div>
      )}

      {transcriptions && transcriptions.length > 0 && (
        <div>
          <div className="flex items-center gap-3 mb-4">
            <span className="text-3xl">🎙️</span>
            <h2 className="text-2xl font-bold bg-gradient-to-r from-purple-600 to-blue-600 bg-clip-text text-transparent dark:from-purple-400 dark:to-blue-400">
              Voice Note Transcriptions
            </h2>
          </div>
          <div className="space-y-4">
            {transcriptions.map((t, index) => (
              <div key={index} className="p-5 bg-white rounded-xl shadow-md dark:bg-gray-800 hover:shadow-lg transition-shadow duration-200 border-l-4 border-blue-400">
                <div className="flex justify-between items-center mb-3">
                    <div className="flex items-center gap-2">
                      <span className="text-2xl">👤</span>
                      <span className="font-semibold text-blue-600 dark:text-blue-400 text-lg">{t.sender}</span>
                    </div>
                    <span className="text-xs text-gray-500 dark:text-gray-400 bg-gray-100 dark:bg-gray-700 px-3 py-1 rounded-full">
                      {new Date(t.timestamp).toLocaleString()}
                    </span>
                </div>
                <p className="mt-2 text-gray-700 dark:text-gray-300 leading-relaxed italic">"{t.message}"</p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};
