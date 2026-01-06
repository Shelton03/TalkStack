import pandas as pd
from typing import Dict, Any

def calculate_basic_stats(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Calculates basic chat statistics.

    Args:
        df: The chat DataFrame.

    Returns:
        A dictionary containing basic statistics.
    """
    if df.empty:
        return {
            "total_messages": 0,
            "messages_per_user": {},
            "total_words": 0,
            "words_per_user": {},
            "avg_message_length_per_user": {},
            "chat_duration_days": 0,
            "chat_start_date": None,
            "chat_end_date": None,
        }

    # Filter out system messages for user-specific stats
    user_df = df[df["sender"] != "System"].copy()
    
    total_messages = len(user_df)
    messages_per_user = user_df["sender"].value_counts().to_dict()
    
    user_df["word_count"] = user_df["message"].apply(lambda s: len(s.split()))
    
    total_words = int(user_df["word_count"].sum())
    words_per_user = user_df.groupby("sender")["word_count"].sum().astype(int).to_dict()
    
    avg_message_length_per_user = user_df.groupby("sender")["word_count"].mean().to_dict()
    
    chat_start_date = df["timestamp"].min()
    chat_end_date = df["timestamp"].max()
    chat_duration = chat_end_date - chat_start_date
    
    return {
        "total_messages": total_messages,
        "messages_per_user": {str(k): int(v) for k, v in messages_per_user.items()},
        "total_words": total_words,
        "words_per_user": {str(k): int(v) for k, v in words_per_user.items()},
        "avg_message_length_per_user": {str(k): float(v) for k, v in avg_message_length_per_user.items()},
        "chat_duration_days": chat_duration.days,
        "chat_start_date": chat_start_date.strftime('%Y-%m-%d'),
        "chat_end_date": chat_end_date.strftime('%Y-%m-%d'),
    }
