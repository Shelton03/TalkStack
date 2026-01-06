from typing import List, Dict, Any, Tuple
import pandas as pd
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Mock whisper for now to avoid heavy dependency
try:
    import whisper
    WHISPER_AVAILABLE = True
    logger.info("✅ Whisper module successfully imported and available")
except ImportError:
    WHISPER_AVAILABLE = False
    whisper = None
    logger.warning("⚠️ Whisper module not available - transcription will be skipped")

def transcribe_audio_files(
    media_files: List[Tuple[str, str]], 
    df: pd.DataFrame
) -> List[Dict[str, Any]]:
    """
    Transcribes audio files and aligns them with the chat data.

    Args:
        media_files: A list of tuples containing (full_path, file_name).
        df: The main chat DataFrame to find sender and timestamp context.

    Returns:
        A list of dictionaries, where each dictionary represents a transcribed message.
    """
    logger.info("=" * 60)
    logger.info("🎙️  TRANSCRIPTION FUNCTION CALLED")
    logger.info("=" * 60)
    logger.info(f"Total media files received: {len(media_files)}")
    
    if not WHISPER_AVAILABLE:
        logger.warning("❌ Whisper not installed. Skipping transcription.")
        logger.info("💡 To enable transcription, install: pip install openai-whisper")
        # Return a mock transcription so the frontend can display a message
        return [{
            "timestamp": pd.Timestamp.now(),
            "sender": "System",
            "message": "Voice note transcription was enabled, but the 'openai-whisper' package is not installed. Please install it to use this feature.",
            "message_type": "system",
            "media_filename": None
        }]

    logger.info("🔧 Loading Whisper model (base)...")
    model = whisper.load_model("base")
    logger.info("✅ Whisper model loaded successfully")
    transcriptions = []

    audio_files = [
        (path, name) for path, name in media_files 
        if name.endswith(('.opus', '.ogg', '.mp3', '.m4a'))
    ]
    
    logger.info(f"🎵 Found {len(audio_files)} audio files to transcribe")
    logger.info(f"Audio file types: {set([name.split('.')[-1] for _, name in audio_files])}")

    for idx, (audio_path, audio_filename) in enumerate(audio_files, 1):
        logger.info(f"\n📝 Processing audio {idx}/{len(audio_files)}: {audio_filename}")
        # Find the corresponding message in the DataFrame
        voice_note_reference = df[df["media_filename"] == audio_filename]
        
        if not voice_note_reference.empty:
            timestamp = voice_note_reference.iloc[0]["timestamp"]
            sender = voice_note_reference.iloc[0]["sender"]
            logger.info(f"   👤 Sender: {sender}")
            logger.info(f"   📅 Timestamp: {timestamp}")
            
            try:
                # Transcribe audio
                logger.info(f"   🎤 Starting transcription of: {audio_filename}")
                result = model.transcribe(audio_path, fp16=False)
                transcribed_text = result["text"]
                logger.info(f"   ✅ Successfully transcribed!")
                logger.info(f"   💬 Text: {transcribed_text[:100]}{'...' if len(transcribed_text) > 100 else ''}")

                transcriptions.append({
                    "timestamp": timestamp,
                    "sender": sender,
                    "message": f"[Transcribed Voice Note]: {transcribed_text}",
                    "message_type": "text", # Treat it as a text message after transcription
                    "media_filename": None
                })
            except Exception as e:
                logger.error(f"   ❌ Error transcribing {audio_filename}: {e}")
                transcriptions.append({
                    "timestamp": timestamp,
                    "sender": sender,
                    "message": f"[Error transcribing voice note: {audio_filename}]",
                    "message_type": "system",
                    "media_filename": audio_filename
                })
        else:
            logger.warning(f"   ⚠️ No matching message found in DataFrame for: {audio_filename}")
    
    logger.info(f"\n{'=' * 60}")
    logger.info(f"✅ TRANSCRIPTION COMPLETE: {len(transcriptions)} audio files transcribed")
    logger.info(f"{'=' * 60}\n")
    return transcriptions

def merge_transcriptions_into_chat(
    df: pd.DataFrame, 
    transcriptions: List[Dict[str, Any]]
) -> pd.DataFrame:
    """
    Merges transcriptions back into the main DataFrame and sorts by time.
    """
    logger.info("🔄 Merging transcriptions into chat DataFrame...")
    
    if not transcriptions:
        logger.info("   ℹ️  No transcriptions to merge")
        return df

    trans_df = pd.DataFrame(transcriptions)
    logger.info(f"   📊 Created transcription DataFrame with {len(trans_df)} rows")
    
    # Remove original voice note references
    original_count = len(df)
    df_no_voice_notes = df[df["message_type"] != "voice_note"].copy()
    voice_notes_removed = original_count - len(df_no_voice_notes)
    logger.info(f"   🗑️  Removed {voice_notes_removed} original voice note placeholders")
    
    # Combine and sort
    combined_df = pd.concat([df_no_voice_notes, trans_df], ignore_index=True)
    combined_df = combined_df.sort_values(by="timestamp").reset_index(drop=True)
    logger.info(f"   ✅ Merged and sorted. Final DataFrame has {len(combined_df)} rows")
    
    return combined_df
