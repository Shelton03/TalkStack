import re
import pandas as pd
import logging
from typing import List, Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Regex to parse a WhatsApp chat line
# Handles both 12-hour and 24-hour time formats, with or without seconds.
# Example: [31/12/2023, 10:00:05 PM] John Doe: Message
# Example: [1/1/24, 10:00] Jane Doe: Message
# Example: 31/12/2023, 10:00 - John Doe: Message (older format)
WHATSAPP_CHAT_REGEX = re.compile(
    r"\[(\d{1,2}/\d{1,2}/\d{2,4},\s*\d{1,2}:\d{2}(?::\d{2})?\s*(?:[AP]M)?)\]\s([^:]+):\s?(.*)",
    re.IGNORECASE
)

# Alternative regex for older format with hyphen instead of brackets
WHATSAPP_LEGACY_REGEX = re.compile(
    r"(\d{1,2}/\d{1,2}/\d{2,4},\s*\d{1,2}:\d{2}(?::\d{2})?\s*(?:[AP]M)?)\s-\s([^:]+):\s?(.*)",
    re.IGNORECASE
)

# Regex for system messages like "Messages are end-to-end encrypted"
SYSTEM_MESSAGE_REGEX = re.compile(
    r"\[(\d{1,2}/\d{1,2}/\d{2,4},\s*\d{1,2}:\d{2}(?::\d{2})?\s*(?:[AP]M)?)\]\s([^:]+):\s?(.+)"
)

MEDIA_OMITTED_MSG = "<Media omitted>"

def parse_chat_file(file_path: str) -> pd.DataFrame:
    """
    Parses a WhatsApp chat export file (.txt).

    Args:
        file_path: The path to the chat file.

    Returns:
        A pandas DataFrame with columns: timestamp, sender, message, message_type, media_filename.
    """
    logger.info(f"📖 Starting to parse chat file: {file_path}")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        logger.info(f"✅ Successfully read {len(lines)} lines from file")
    except Exception as e:
        logger.error(f"❌ Error reading file: {e}")
        return pd.DataFrame()
    
    # Log first few lines to help debug format issues
    if lines:
        logger.info("📝 First 5 lines of the chat file:")
        for i, line in enumerate(lines[:5], 1):
            logger.info(f"   Line {i}: {line.strip()[:100]}")

    chat_data: List[Dict[str, Any]] = []
    current_message_lines: List[str] = []
    matched_count = 0
    unmatched_count = 0
    unmatched_samples = []  # Store first 3 unmatched lines for debugging
    
    # Debug: Test regex on first line
    if lines:
        test_line = lines[0].replace('\u202f', ' ').replace('\u200e', '').replace('\u2028', ' ')
        logger.info(f"🧪 Testing regex on first line:")
        logger.info(f"   Line: {test_line.strip()[:100]}")
        test_match = WHATSAPP_CHAT_REGEX.match(test_line)
        if test_match:
            logger.info(f"   ✅ WHATSAPP_CHAT_REGEX matched!")
            logger.info(f"   Groups: {test_match.groups()}")
        else:
            logger.warning(f"   ❌ WHATSAPP_CHAT_REGEX did not match")
            logger.warning(f"   Regex pattern: {WHATSAPP_CHAT_REGEX.pattern}")
    
    for line in lines:
        # Normalize invisible Unicode spacing characters that appear in some exports
        normalized_line = (
            line
            .replace('\u202f', ' ')   # narrow no-break space
            .replace('\u200e', '')    # left-to-right mark
            .replace('\u2028', ' ')   # line separator
        )
        # Try matching the modern bracket format first: [DD/MM/YY, HH:MM:SS AM/PM] Name: Message
        match = WHATSAPP_CHAT_REGEX.match(normalized_line)
        
        if not match:
            # Try the legacy format with hyphen: DD/MM/YY, HH:MM AM/PM - Name: Message
            match = WHATSAPP_LEGACY_REGEX.match(normalized_line)
        
        # Check for system messages (special invisible character after colon)
        system_match = SYSTEM_MESSAGE_REGEX.match(normalized_line) if not match else None

        if match:
            matched_count += 1
            # If we have a pending multi-line message, save it first
            if current_message_lines:
                chat_data[-1]['message'] += ' '.join(current_message_lines)
                current_message_lines = []

            # Extract data from the matched line
            # Groups (with current regex):
            #   1 -> timestamp string
            #   2 -> sender name
            #   3 -> message text
            timestamp_str = match.group(1)
            sender = match.group(2)
            message_text = match.group(3).strip()

            message_type = "text"
            media_filename = None

            if MEDIA_OMITTED_MSG in message_text:
                message_type = "media"
                message_text = ""
            elif "(file attached)" in message_text:
                parts = message_text.split("(file attached)")
                media_filename = parts[0].strip()
                message_text = ""
                message_type = "voice_note" if ".opus" in media_filename else "media"
            
            chat_data.append({
                "timestamp_str": timestamp_str,
                "sender": sender,
                "message": message_text,
                "message_type": message_type,
                "media_filename": media_filename,
            })
        elif system_match:
            matched_count += 1
            if current_message_lines:
                chat_data[-1]['message'] += ' '.join(current_message_lines)
                current_message_lines = []
            # This is a system message (e.g., "Messages are end-to-end encrypted")
            timestamp_str = system_match.group(1)
            sender = system_match.group(2)
            message_text = system_match.group(3).strip()
            
            chat_data.append({
                "timestamp_str": timestamp_str,
                "sender": "System",
                "message": message_text,
                "message_type": "system",
                "media_filename": None,
            })

        elif chat_data:
            # This is a continuation of the previous message (multi-line)
            current_message_lines.append(normalized_line.strip())
        else:
            unmatched_count += 1
            # Store first 3 unmatched lines for debugging
            if len(unmatched_samples) < 3:
                unmatched_samples.append(normalized_line.strip())

    # Add the last multi-line message if it exists
    if current_message_lines and chat_data:
        chat_data[-1]['message'] += ' '.join(current_message_lines)

    logger.info(f"📊 Parsing complete:")
    logger.info(f"   ✅ Matched lines: {matched_count}")
    logger.info(f"   ⚠️  Unmatched lines: {unmatched_count}")
    logger.info(f"   📝 Total messages parsed: {len(chat_data)}")
    
    # Log unmatched samples for debugging
    if unmatched_samples:
        logger.warning(f"\n🔍 First {len(unmatched_samples)} unmatched lines (for debugging):")
        for i, sample in enumerate(unmatched_samples, 1):
            logger.warning(f"   {i}. {sample[:100]}")
            
            # Analyze why it didn't match
            reasons = []
            if not sample.strip():
                reasons.append("Empty line")
            elif not sample.startswith('['):
                reasons.append("Doesn't start with '['")
            elif '] ' not in sample and ']: ' not in sample:
                reasons.append("Missing '] ' or ']: ' separator")
            elif ':' not in sample:
                reasons.append("No colon ':' found (needed for sender:message format)")
            else:
                # Check timestamp format
                if not re.search(r'\d{1,2}/\d{1,2}/\d{2,4}', sample):
                    reasons.append("No date pattern found (expected MM/DD/YY or similar)")
                if not re.search(r'\d{1,2}:\d{2}', sample):
                    reasons.append("No time pattern found (expected HH:MM)")
                if reasons == []:
                    reasons.append("Unknown - pattern should match but didn't")
            
            logger.warning(f"      Reason: {', '.join(reasons)}")
    
    if not chat_data:
        logger.error("❌ No messages were parsed! The file format may not be recognized.")
        logger.error("💡 Expected format examples:")
        logger.error("   [31/12/2023, 10:00:05 PM] John Doe: Message")
        logger.error("   31/12/2023, 10:00 - John Doe: Message")
        return pd.DataFrame()

    df = pd.DataFrame(chat_data)
    logger.info(f"✅ Created DataFrame with {len(df)} rows")
    
    # Convert timestamp string to datetime object
    # The format can vary, so we let pandas infer it, but provide hints
    try:
        df['timestamp'] = pd.to_datetime(df['timestamp_str'], errors='coerce')
    except Exception as e:
        logger.warning(f"⚠️  Using fallback timestamp parsing: {e}")
        df['timestamp'] = pd.to_datetime(df['timestamp_str'], errors='coerce', format='mixed')

    # Count how many timestamps failed to parse
    null_timestamps = df['timestamp'].isna().sum()
    if null_timestamps > 0:
        logger.warning(f"⚠️  {null_timestamps} timestamps could not be parsed and will be dropped")

    df = df.dropna(subset=['timestamp']) # Drop rows where timestamp could not be parsed
    logger.info(f"✅ After timestamp parsing: {len(df)} rows remain")
    
    df = df.sort_values(by="timestamp").reset_index(drop=True)
    df = df.drop(columns=['timestamp_str'])

    logger.info(f"🎉 Parsing successful! Returning DataFrame with {len(df)} messages")
    return df[["timestamp", "sender", "message", "message_type", "media_filename"]]
