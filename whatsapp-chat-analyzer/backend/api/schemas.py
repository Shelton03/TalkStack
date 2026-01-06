from pydantic import BaseModel
from typing import Dict, List, Any, Optional

class BasicStats(BaseModel):
    total_messages: int
    messages_per_user: Dict[str, int]
    total_words: int
    words_per_user: Dict[str, int]
    avg_message_length_per_user: Dict[str, float]
    chat_duration_days: int
    chat_start_date: Optional[str] = None
    chat_end_date: Optional[str] = None

class TemporalStats(BaseModel):
    most_active_day: Optional[str] = None
    most_active_hour: Optional[int] = None
    message_volume_over_time: List[Dict[str, Any]]
    activity_by_hour: List[Dict[str, Any]]
    activity_by_day_of_week: List[Dict[str, Any]]

class LinguisticStats(BaseModel):
    most_common_words: List[Dict[str, Any]]
    most_common_words_per_user: Dict[str, List[Dict[str, Any]]]

class TranscriptionResult(BaseModel):
    timestamp: str
    sender: str
    message: str

class AnalysisResult(BaseModel):
    basic_stats: BasicStats
    temporal_stats: TemporalStats
    linguistic_stats: LinguisticStats
    transcriptions: Optional[List[Dict[str, Any]]] = None
    insights: Optional[str] = None
