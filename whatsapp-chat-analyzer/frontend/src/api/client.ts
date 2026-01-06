import axios from 'axios';
import { AnalysisResult, LLMProvider } from '../types';

const apiClient = axios.create({
  baseURL: 'http://localhost:8000/api', // Adjust if your backend runs on a different port
  headers: {
    'Content-Type': 'multipart/form-data',
  },
});

export const uploadAndAnalyzeChat = async (
  file: File,
  enableTranscription: boolean,
  enableAiInsights: boolean,
  llmProvider?: LLMProvider,
  llmApiKeyOrUrl?: string
): Promise<AnalysisResult> => {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('enable_transcription', String(enableTranscription));
  formData.append('enable_ai_insights', String(enableAiInsights));
  if (llmProvider) {
    formData.append('llm_provider', llmProvider);
  }
  if (llmApiKeyOrUrl) {
    formData.append('llm_api_key_or_url', llmApiKeyOrUrl);
  }

  try {
    const response = await apiClient.post<AnalysisResult>('/upload', formData);
    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error) && error.response) {
      // Throw the error message from the backend
      throw new Error(error.response.data.detail || 'An unknown error occurred');
    }
    throw new Error('An unexpected error occurred during analysis.');
  }
};
