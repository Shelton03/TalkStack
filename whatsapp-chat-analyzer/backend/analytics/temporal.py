import pandas as pd
from typing import Dict, Any, List

def calculate_temporal_stats(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Calculates temporal chat statistics (activity over time).

    Args:
        df: The chat DataFrame.

    Returns:
        A dictionary containing temporal statistics.
    """
    if df.empty:
        return {
            "most_active_day": None,
            "most_active_hour": None,
            "message_volume_over_time": [],
            "activity_by_hour": [],
            "activity_by_day_of_week": [],
        }

    user_df = df[df["sender"] != "System"].copy()
    
    # Most active day and hour
    most_active_day = user_df["timestamp"].dt.date.value_counts().idxmax()
    most_active_hour = user_df["timestamp"].dt.hour.value_counts().idxmax()
    
    # Get most active day of week name
    most_active_day_of_week_idx = user_df["timestamp"].dt.dayofweek.value_counts().idxmax()
    day_name_map = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday', 5: 'Saturday', 6: 'Sunday'}
    most_active_day_name = day_name_map[most_active_day_of_week_idx]

    # Message volume over time (e.g., daily)
    user_df['date'] = user_df['timestamp'].dt.date
    daily_volume = user_df.groupby('date').size().reset_index(name='message_count')
    message_volume_over_time = [
        {"date": str(row.date), "message_count": row.message_count}
        for row in daily_volume.itertuples()
    ]
    
    # Activity by hour of the day
    hourly_activity = user_df["timestamp"].dt.hour.value_counts().sort_index()
    activity_by_hour = [
        {"hour": int(hour), "message_count": int(count)}
        for hour, count in hourly_activity.items()
    ]

    # Activity by day of the week
    day_map = {0: 'Mon', 1: 'Tue', 2: 'Wed', 3: 'Thu', 4: 'Fri', 5: 'Sat', 6: 'Sun'}
    day_of_week_activity = user_df["timestamp"].dt.dayofweek.value_counts().sort_index()
    activity_by_day_of_week = [
        {"day": day_map[day_idx], "message_count": int(count)}
        for day_idx, count in day_of_week_activity.items()
    ]
    
    return {
        "most_active_day": str(most_active_day),
        "most_active_day_name": most_active_day_name,
        "most_active_hour": int(most_active_hour),
        "message_volume_over_time": message_volume_over_time,
        "activity_by_hour": activity_by_hour,
        "activity_by_day_of_week": activity_by_day_of_week,
    }
