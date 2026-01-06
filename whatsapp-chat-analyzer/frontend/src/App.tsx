import React, { useState } from 'react';
import { AnalysisResult, LLMProvider } from './types';
import { uploadAndAnalyzeChat } from './api/client';
import { UploadForm } from './components/UploadForm';
import { MetricsDashboard } from './components/MetricsDashboard';
import { Charts } from './components/Charts';
import { InsightsPanel } from './components/InsightsPanel';

const App: React.FC = () => {
  const [analysisResult, setAnalysisResult] = useState<AnalysisResult | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleAnalyze = async (
    file: File,
    enableTranscription: boolean,
    enableAiInsights: boolean,
    llmProvider?: LLMProvider,
    llmApiKeyOrUrl?: string
  ) => {
    setIsLoading(true);
    setError(null);
    setAnalysisResult(null);
    try {
      const result = await uploadAndAnalyzeChat(file, enableTranscription, enableAiInsights, llmProvider, llmApiKeyOrUrl);
      setAnalysisResult(result);
    } catch (err: any) {
      setError(err.message || 'An unknown error occurred.');
    } finally {
      setIsLoading(false);
    }
  };
  
  const handleReset = () => {
    setAnalysisResult(null);
    setError(null);
    setIsLoading(false);
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 via-blue-50 to-purple-50 dark:from-gray-900 dark:via-gray-900 dark:to-gray-800 text-gray-900 dark:text-gray-100 p-4 sm:p-6 lg:p-8">
      <div className="max-w-7xl mx-auto">
        <header className="text-center mb-12">
          <div className="mb-4">
            <span className="text-6xl inline-block animate-bounce">💬</span>
          </div>
          <h1 className="text-5xl font-extrabold tracking-tight sm:text-6xl bg-gradient-to-r from-purple-600 via-blue-600 to-purple-600 bg-clip-text text-transparent mb-4">
            WhatsApp Chat Analyzer
          </h1>
          <p className="mt-4 text-xl text-gray-600 dark:text-gray-400 max-w-2xl mx-auto">
            Discover hidden insights, relationship dynamics, and communication patterns in your conversations
          </p>
        </header>
        
        <main>
          {!analysisResult && (
            <div className="flex justify-center">
              <UploadForm onAnalyze={handleAnalyze} isLoading={isLoading} />
            </div>
          )}

          {isLoading && (
            <div className="text-center py-12">
              <div className="inline-block">
                <svg className="animate-spin h-16 w-16 text-purple-600 dark:text-purple-400 mb-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                <p className="text-xl font-semibold text-gray-700 dark:text-gray-300">Analyzing your chat...</p>
                <p className="text-sm text-gray-500 dark:text-gray-400 mt-2">This may take a moment</p>
              </div>
            </div>
          )}
          
          {error && (
            <div className="max-w-md mx-auto my-8 p-6 text-center bg-red-50 dark:bg-red-900/20 border-2 border-red-200 dark:border-red-800 rounded-xl shadow-lg">
              <span className="text-5xl mb-4 inline-block">⚠️</span>
              <p className="font-bold text-xl text-red-700 dark:text-red-400 mb-2">Analysis Failed</p>
              <p className="text-red-600 dark:text-red-300 mb-4">{error}</p>
              <button 
                onClick={handleReset} 
                className="mt-4 px-6 py-3 bg-gradient-to-r from-red-600 to-red-700 text-white font-semibold rounded-lg hover:from-red-700 hover:to-red-800 transform hover:scale-105 transition-all duration-200 shadow-lg"
              >
                Try Again
              </button>
            </div>
          )}

          {analysisResult && (
            <div className="space-y-8 animate-fadeIn">
              <div className="flex justify-between items-center bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6">
                <div className="flex items-center gap-3">
                  <span className="text-3xl">✨</span>
                  <div>
                    <h2 className="text-2xl font-bold text-gray-900 dark:text-white">Analysis Complete!</h2>
                    <p className="text-sm text-gray-600 dark:text-gray-400">Scroll down to explore your insights</p>
                  </div>
                </div>
                <button 
                  onClick={handleReset} 
                  className="px-6 py-3 bg-gradient-to-r from-purple-600 to-blue-600 text-white font-semibold rounded-lg hover:from-purple-700 hover:to-blue-700 transform hover:scale-105 transition-all duration-200 shadow-lg flex items-center gap-2"
                >
                  <span>🔄</span>
                  Analyze Another Chat
                </button>
              </div>
              <MetricsDashboard data={analysisResult} />
              <Charts data={analysisResult} />
              <InsightsPanel data={analysisResult} />
            </div>
          )}
        </main>
        
        <footer className="mt-16 text-center text-sm text-gray-500 dark:text-gray-400 pb-8">
          <p>Made with 💜 for understanding conversations better</p>
        </footer>
      </div>
    </div>
  );
};

export default App;
