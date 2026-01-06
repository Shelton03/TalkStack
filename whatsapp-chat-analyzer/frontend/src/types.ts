export interface BasicStats {
  total_messages: number;
  messages_per_user: Record<string, number>;
  total_words: number;
  words_per_user: Record<string, number>;
  avg_message_length_per_user: Record<string, number>;
  chat_duration_days: number;
  chat_start_date?: string;
  chat_end_date?: string;
}

export interface TemporalStats {
  most_active_day?: string;
  most_active_hour?: number;
  message_volume_over_time: { date: string; message_count: number }[];
  activity_by_hour: { hour: number; message_count: number }[];
  activity_by_day_of_week: { day: string; message_count: number }[];
}

export interface LinguisticStats {
  most_common_words: { word: string; count: number }[];
  most_common_words_per_user: Record<string, { word: string; count: number }[]>;
}

export interface Transcription {
  timestamp: string;
  sender: string;
  message: string;
}

export interface AnalysisResult {
  basic_stats: BasicStats;
  temporal_stats: TemporalStats;
  linguistic_stats: LinguisticStats;
  transcriptions?: Transcription[];
  insights?: string;
}

export type LLMProvider = "gemini" | "openai" | "ollama";
