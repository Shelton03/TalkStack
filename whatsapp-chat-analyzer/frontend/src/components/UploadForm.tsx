import React, { useState } from 'react';
import { LLMProvider } from '../types';

interface UploadFormProps {
  onAnalyze: (
    file: File,
    enableTranscription: boolean,
    enableAiInsights: boolean,
    llmProvider?: LLMProvider,
    llmApiKeyOrUrl?: string
  ) => void;
  isLoading: boolean;
}

export const UploadForm: React.FC<UploadFormProps> = ({ onAnalyze, isLoading }) => {
  const [file, setFile] = useState<File | null>(null);
  const [enableTranscription, setEnableTranscription] = useState(false);
  const [enableAiInsights, setEnableAiInsights] = useState(false);
  const [llmProvider, setLlmProvider] = useState<LLMProvider>('gemini');
  const [llmApiKeyOrUrl, setLlmApiKeyOrUrl] = useState('');

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files) {
      setFile(event.target.files[0]);
    }
  };

  const handleSubmit = (event: React.FormEvent) => {
    event.preventDefault();
    if (file) {
      onAnalyze(file, enableTranscription, enableAiInsights, llmProvider, llmApiKeyOrUrl);
    }
  };

  return (
    <div className="w-full max-w-lg p-8 space-y-6 bg-gradient-to-br from-white to-gray-50 rounded-xl shadow-xl dark:from-gray-800 dark:to-gray-900 border border-gray-200 dark:border-gray-700">
      <div className="text-center">
        <span className="text-5xl mb-3 inline-block">💬</span>
        <h2 className="text-3xl font-bold bg-gradient-to-r from-purple-600 to-blue-600 bg-clip-text text-transparent dark:from-purple-400 dark:to-blue-400">
          Analyze Your Chat
        </h2>
        <p className="mt-2 text-sm text-gray-600 dark:text-gray-400">
          Upload your WhatsApp chat export and discover insights
        </p>
      </div>
      
      <form onSubmit={handleSubmit} className="space-y-6">
        <div>
          <label htmlFor="file-upload" className="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2">
            📁 WhatsApp Chat ZIP File
          </label>
          <div className="relative">
            <input
              id="file-upload"
              type="file"
              accept=".zip"
              onChange={handleFileChange}
              required
              className="block w-full text-sm text-gray-500 file:mr-4 file:py-3 file:px-6 file:rounded-lg file:border-0 file:text-sm file:font-semibold file:bg-gradient-to-r file:from-purple-500 file:to-blue-500 file:text-white hover:file:from-purple-600 hover:file:to-blue-600 file:cursor-pointer file:transition-all file:duration-200 cursor-pointer border-2 border-dashed border-gray-300 dark:border-gray-600 rounded-lg p-4 hover:border-purple-400 dark:hover:border-purple-500 transition-colors"
            />
          </div>
          {file && (
            <p className="mt-2 text-xs text-green-600 dark:text-green-400 flex items-center gap-1">
              ✓ <span>{file.name} selected</span>
            </p>
          )}
        </div>
        
        <div className="space-y-4 bg-gray-50 dark:bg-gray-800/50 p-4 rounded-lg">
          <div className="flex items-start">
            <div className="flex items-center h-5">
              <input 
                id="transcription" 
                type="checkbox" 
                checked={enableTranscription} 
                onChange={(e) => setEnableTranscription(e.target.checked)} 
                className="w-5 h-5 text-purple-600 border-gray-300 rounded focus:ring-purple-500 cursor-pointer" 
              />
            </div>
            <div className="ml-3">
              <label htmlFor="transcription" className="font-semibold text-gray-700 dark:text-gray-300 cursor-pointer flex items-center gap-2">
                🎙️ Enable Voice Note Transcription
              </label>
              <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">Transcribe audio messages using Whisper AI</p>
            </div>
          </div>

          <div className="flex items-start">
            <div className="flex items-center h-5">
              <input 
                id="ai-insights" 
                type="checkbox" 
                checked={enableAiInsights} 
                onChange={(e) => setEnableAiInsights(e.target.checked)} 
                className="w-5 h-5 text-purple-600 border-gray-300 rounded focus:ring-purple-500 cursor-pointer" 
              />
            </div>
            <div className="ml-3">
              <label htmlFor="ai-insights" className="font-semibold text-gray-700 dark:text-gray-300 cursor-pointer flex items-center gap-2">
                ✨ Enable AI-Generated Insights
              </label>
              <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">Get deeper relationship and personality insights</p>
            </div>
          </div>
        </div>

        {enableAiInsights && (
          <div className="p-5 border-2 border-purple-200 rounded-lg dark:border-purple-800 bg-purple-50/50 dark:bg-purple-900/20 space-y-4 animate-fadeIn">
            <div>
              <label htmlFor="llm-provider" className="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2">
                🤖 LLM Provider
              </label>
              <select 
                id="llm-provider" 
                value={llmProvider} 
                onChange={(e) => setLlmProvider(e.target.value as LLMProvider)} 
                className="block w-full px-4 py-3 bg-white border-2 border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-purple-500 sm:text-sm dark:bg-gray-700 dark:border-gray-600 dark:text-white cursor-pointer transition-all"
              >
                <option value="gemini">✨ Gemini</option>
                <option value="openai">🧠 OpenAI</option>
                <option value="ollama">🏠 Ollama (local)</option>
              </select>
            </div>
            <div>
              <label htmlFor="llm-key" className="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2">
                {llmProvider === 'ollama' ? '🔗 Ollama Base URL' : '🔑 API Key'}
              </label>
              <input 
                id="llm-key" 
                type="text" 
                value={llmApiKeyOrUrl} 
                onChange={(e) => setLlmApiKeyOrUrl(e.target.value)} 
                placeholder={llmProvider === 'ollama' ? 'e.g., http://localhost:11434' : 'Enter your API key'}
                className="block w-full px-4 py-3 bg-white border-2 border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-purple-500 sm:text-sm dark:bg-gray-700 dark:border-gray-600 dark:text-white transition-all"
              />
            </div>
          </div>
        )}
        
        <button 
          type="submit" 
          disabled={!file || isLoading} 
          className="w-full px-6 py-4 text-base font-bold text-white bg-gradient-to-r from-purple-600 to-blue-600 border border-transparent rounded-lg shadow-lg hover:from-purple-700 hover:to-blue-700 focus:outline-none focus:ring-4 focus:ring-purple-500/50 disabled:from-gray-400 disabled:to-gray-500 disabled:cursor-not-allowed transform hover:scale-[1.02] transition-all duration-200 flex items-center justify-center gap-2"
        >
          {isLoading ? (
            <>
              <svg className="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Analyzing Your Chat...
            </>
          ) : (
            <>
              🚀 Start Analysis
            </>
          )}
        </button>
      </form>
    </div>
  );
};
