from typing import Dict, Any, Optional
import json
import pandas as pd
from ..llm.llm_client import LLMClient

def generate_prompt(analytics_data: Dict[str, Any]) -> str:
    """Formats analytics data into a structured prompt for an LLM."""
    
    # Extract key metrics to help guide the LLM
    basic_stats = analytics_data.get("basic_stats", {})
    linguistic_stats = analytics_data.get("linguistic_stats", {})
    total_messages = basic_stats.get("total_messages", 0)
    
    # Get top words for topic analysis
    most_common_words = linguistic_stats.get("most_common_words", [])
    top_words_list = [w['word'] for w in most_common_words[:10]] if most_common_words else []
    
    prompt = """
    You are an insightful relationship and communication analyst examining a WhatsApp chat conversation.
    Based on the following data, provide meaningful, engaging insights about the relationship dynamics, 
    communication styles, and individual characteristics of the participants.
    
    Here is the data:
    """
    
    # Pretty-print JSON to make it readable for the LLM
    prompt += json.dumps(analytics_data, indent=2)
    
    prompt += f"""
    
    Please provide a comprehensive analysis with the following sections:
    
    **🌟 Relationship Dynamics**
    - Analyze the quality and nature of this relationship (e.g., close friendship, romantic, family, professional)
    - Only infer relationship characteristics if there are at least {min(100, total_messages)} messages to base your analysis on. With fewer messages, focus on observable patterns rather than relationship quality.
    - Assess the balance of communication (is it mutual, one-sided, or dynamic?)
    - Identify the emotional tone if clear from the data
    
    **👥 Individual Characteristics**
    For each person, describe what you can observe:
    - Their communication approach (how they express themselves)
    - Be flexible in describing their style - go beyond simple verbose/concise labels and describe actual patterns
    - Observable personality traits from their messaging patterns
    - Their role or behavior in the conversation
    - Linguistic tendencies or communication habits
    
    **💬 Most Discussed Topics**
    Based on the most common words ({', '.join(top_words_list[:5])}), identify:
    - Main themes or subjects they discuss frequently
    - What these topics reveal about their interests or relationship
    - Any notable focus areas in their conversations
    - Connect these words to meaningful topics rather than just listing them
    
    **📊 Communication Patterns**
    - Timing patterns and what they suggest about schedules/habits
    - Activity peaks and their potential significance
    - Any distinctive behaviors or patterns in the data
    
    **💡 Key Insights**
    - 2-3 interesting or noteworthy observations about this conversation
    - What makes this communication dynamic unique or notable
    - Only make confident inferences when supported by sufficient data
    
    IMPORTANT GUIDELINES:
    - Be data-driven: only make claims you can support with the actual statistics provided
    - With limited data ({total_messages} messages), focus on observable patterns rather than deep psychological analysis
    - Be flexible and natural in your descriptions - avoid overly rigid categorizations
    - Make your analysis warm and engaging, but honest about what can and cannot be inferred
    - Use emojis sparingly to enhance readability
    - Aim for 300-500 words, adjusting based on the richness of the data
    """
    return prompt

def get_insights(
    analytics_data: Dict[str, Any],
    llm_client: Optional[LLMClient] = None
) -> str:
    """
    Generates insights from analytics data, either using an LLM or a mock summary.

    Args:
        analytics_data: A dictionary of computed analytics.
        llm_client: An optional initialized LLM client.

    Returns:
        A string containing the generated or mock insights.
    """
    if llm_client:
        try:
            prompt = generate_prompt(analytics_data)
            insight = llm_client.generate_insight(prompt)
            return insight
        except Exception as e:
            return f"An error occurred while generating AI insights: {e}"
    else:
        return generate_mock_summary(analytics_data)

def generate_mock_summary(analytics_data: Dict[str, Any]) -> str:
    """
    Generates an insightful summary based on the analytics data.
    This is used when AI insights are disabled.
    """
    summary = "💬 **Chat Analysis Summary**\n\n"
    
    try:
        basic_stats = analytics_data.get("basic_stats", {})
        temporal_stats = analytics_data.get("temporal_stats", {})
        linguistic_stats = analytics_data.get("linguistic_stats", {})
        
        # Total messages and engagement
        total_messages = basic_stats.get("total_messages", 0)
        duration_days = basic_stats.get("chat_duration_days", 0)
        avg_msgs_per_day = round(total_messages / max(duration_days, 1), 1)
        
        summary += f"**📊 Overall Activity**\n"
        summary += f"- {total_messages} messages exchanged over {duration_days} days\n"
        summary += f"- Average of {avg_msgs_per_day} messages per day\n\n"
        
        # Analyze user dynamics
        messages_per_user = basic_stats.get("messages_per_user", {})
        words_per_user = basic_stats.get("words_per_user", {})
        avg_length_per_user = basic_stats.get("avg_message_length_per_user", {})
        
        # Check if we have enough data for relationship insights
        has_sufficient_data = total_messages >= 50
        
        if messages_per_user:
            users = list(messages_per_user.keys())
            most_active_user = max(messages_per_user, key=messages_per_user.get)
            
            summary += f"**👥 Communication Dynamics**\n"
            
            # Balance analysis - only if sufficient data
            if len(users) == 2 and has_sufficient_data:
                user1, user2 = users
                ratio = messages_per_user[user1] / max(messages_per_user[user2], 1)
                if 0.8 <= ratio <= 1.2:
                    summary += f"- Beautifully balanced conversation - both participants contribute equally! 🤝\n"
                elif ratio > 1.5 or ratio < 0.67:
                    summary += f"- {most_active_user} is the conversation driver, sending {messages_per_user[most_active_user]} messages 💬\n"
                else:
                    summary += f"- {most_active_user} leads the conversation with {messages_per_user[most_active_user]} messages\n"
            elif len(users) == 2:
                # With limited data, just state facts
                user1, user2 = users
                summary += f"- {user1}: {messages_per_user[user1]} messages | {user2}: {messages_per_user[user2]} messages\n"
            
            # Individual styles - be more flexible
            summary += f"\n**🎭 Communication Approaches**\n"
            for user in users:
                msg_count = messages_per_user.get(user, 0)
                avg_words = avg_length_per_user.get(user, 0)
                
                # More flexible descriptions
                if avg_words < 3:
                    style = "very brief responses"
                elif avg_words < 8:
                    style = "quick, snappy messages"
                elif avg_words < 15:
                    style = "conversational style"
                elif avg_words < 25:
                    style = "thoughtful, detailed messages"
                else:
                    style = "elaborate, expressive communication"
                    
                summary += f"- **{user}**: {style} (avg {avg_words:.1f} words/message)\n"
            
        # Temporal patterns
        summary += f"\n**⏰ Activity Patterns**\n"
        most_active_hour = temporal_stats.get("most_active_hour")
        if most_active_hour is not None:
            time_desc = ""
            if 5 <= most_active_hour < 12:
                time_desc = "morning people ☀️"
            elif 12 <= most_active_hour < 17:
                time_desc = "afternoon chatters 🌤️"
            elif 17 <= most_active_hour < 22:
                time_desc = "evening conversationalists 🌆"
            else:
                time_desc = "night owls 🌙"
            summary += f"- Peak activity at {most_active_hour}:00 - you're {time_desc}\n"
        
        most_active_day = temporal_stats.get("most_active_day_name")
        if most_active_day:
            summary += f"- Most active on {most_active_day}s\n"
            
        # Word insights with topic inference
        common_words = linguistic_stats.get("most_common_words", [])
        if common_words:
            summary += f"\n**💬 Most Discussed Topics**\n"
            
            # Get top 10 words for topic analysis
            top_words = [w['word'] for w in common_words[:10]]
            
            # Try to infer topics from word clusters
            topics = []
            work_words = {'work', 'job', 'meeting', 'office', 'project', 'boss', 'email', 'deadline', 'team'}
            food_words = {'food', 'dinner', 'lunch', 'breakfast', 'eating', 'restaurant', 'cooking', 'pizza', 'coffee'}
            family_words = {'mom', 'dad', 'family', 'parents', 'brother', 'sister', 'home', 'house', 'kids'}
            social_words = {'party', 'friends', 'movie', 'game', 'weekend', 'tonight', 'tomorrow', 'plans'}
            emotion_words = {'love', 'happy', 'sad', 'sorry', 'thanks', 'miss', 'feel', 'hope', 'wish'}
            
            top_words_set = set(top_words)
            if top_words_set & work_words:
                topics.append("work and career")
            if top_words_set & food_words:
                topics.append("food and dining")
            if top_words_set & family_words:
                topics.append("family matters")
            if top_words_set & social_words:
                topics.append("social activities")
            if top_words_set & emotion_words:
                topics.append("feelings and emotions")
            
            if topics:
                summary += f"- Common themes: {', '.join(topics)}\n"
            
            # Show top words
            top_5_words = ', '.join([f"'{w}'" for w in top_words[:5]])
            summary += f"- Most frequent words: {top_5_words}\n"
            
            # Add context if sufficient data
            if has_sufficient_data and len(common_words) >= 3:
                summary += f"- These words suggest the conversation revolves around shared interests and daily life\n"
        
    except Exception as e:
        summary += f"\n⚠️ Could not generate full analysis: {e}"

    return summary
