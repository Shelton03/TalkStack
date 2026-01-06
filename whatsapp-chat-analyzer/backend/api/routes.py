from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import Optional, Literal
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from ..utils.file_utils import extract_zip, find_chat_file, find_media_files
from ..parser.whatsapp_parser import parse_chat_file
from ..media.audio_transcription import transcribe_audio_files, merge_transcriptions_into_chat
from ..analytics.basic_stats import calculate_basic_stats
from ..analytics.temporal import calculate_temporal_stats
from ..analytics.linguistic import calculate_linguistic_stats
from ..insights.insight_engine import get_insights
from ..llm.llm_client import get_llm_client
from .schemas import AnalysisResult

router = APIRouter()

@router.post("/upload", response_model=AnalysisResult)
async def upload_chat_and_analyze(
    file: UploadFile = File(...),
    enable_transcription: bool = Form(False),
    enable_ai_insights: bool = Form(False),
    llm_provider: Optional[Literal["gemini", "openai", "ollama"]] = Form(None),
    llm_api_key_or_url: Optional[str] = Form(None),
):
    logger.info("\n" + "=" * 70)
    logger.info("🚀 NEW ANALYSIS REQUEST RECEIVED")
    logger.info("=" * 70)
    logger.info(f"📁 File: {file.filename}")
    logger.info(f"🎙️  Transcription enabled: {enable_transcription}")
    logger.info(f"✨ AI insights enabled: {enable_ai_insights}")
    if enable_ai_insights:
        logger.info(f"🤖 LLM Provider: {llm_provider}")
    
    if not file.filename.endswith(".zip"):
        logger.error(f"❌ Invalid file type: {file.filename}")
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload a ZIP file.")

    zip_content = await file.read()
    logger.info(f"📦 ZIP file size: {len(zip_content)} bytes")
    
    try:
        logger.info("📂 Extracting ZIP archive...")
        temp_dir = extract_zip(zip_content)
        logger.info(f"✅ Extracted to: {temp_dir.name}")
        
        logger.info("🔍 Looking for chat file...")
        chat_file_path = find_chat_file(temp_dir.name)
        logger.info(f"✅ Found chat file: {chat_file_path}")
        
        # 1. Parse chat file to get initial DataFrame
        logger.info("📖 Parsing chat file...")
        df = parse_chat_file(chat_file_path)
        if df.empty:
            logger.error("❌ Chat DataFrame is empty after parsing")
            raise HTTPException(status_code=400, detail="Could not parse chat file or file is empty.")
        logger.info(f"✅ Parsed {len(df)} messages")

        transcription_results = None
        # 2. (Optional) Transcribe audio and merge results
        if enable_transcription:
            logger.info("\n" + "🎙️" * 30)
            logger.info("🎙️  TRANSCRIPTION REQUESTED - Starting audio processing...")
            logger.info("🎙️" * 30)
            media_files = list(find_media_files(temp_dir.name))
            logger.info(f"📁 Found {len(media_files)} total media files")
            transcriptions = transcribe_audio_files(media_files, df)
            df = merge_transcriptions_into_chat(df, transcriptions)
            # Make transcriptions JSON serializable
            transcription_results = [
                {**t, "timestamp": t["timestamp"].isoformat()} for t in transcriptions
            ]
            logger.info(f"✅ Transcription complete. Generated {len(transcription_results)} results")
        else:
            logger.info("⏭️  Transcription skipped (not enabled)")

        # 3. Calculate all analytics on the final DataFrame
        logger.info("\n📊 Calculating analytics...")
        basic_stats = calculate_basic_stats(df)
        temporal_stats = calculate_temporal_stats(df)
        linguistic_stats = calculate_linguistic_stats(df)
        logger.info("✅ Analytics calculated successfully")

        analytics_data = {
            "basic_stats": basic_stats,
            "temporal_stats": temporal_stats,
            "linguistic_stats": linguistic_stats,
        }

        # 4. (Optional) Generate insights
        insights_result = None
        if enable_ai_insights:
            logger.info("\n✨ Generating AI insights...")
            try:
                # Use strict=True to ensure errors are raised if config is missing
                llm_client = get_llm_client(llm_provider, llm_api_key_or_url, strict=True)
                insights_result = get_insights(analytics_data, llm_client)
                logger.info("✅ AI insights generated successfully")
            except Exception as e:
                logger.error(f"❌ Error generating AI insights: {e}")
                insights_result = f"AI insights were enabled, but an error occurred:\n\n{e}"
        else:
            logger.info("📝 Generating mock insights (AI disabled)...")
            insights_result = get_insights(analytics_data, None) # Get mock summary
            logger.info("✅ Mock insights generated")

        # 5. Clean up temporary directory
        temp_dir.cleanup()
        logger.info("🧹 Cleaned up temporary files")

        logger.info("\n" + "=" * 70)
        logger.info("✅ ANALYSIS COMPLETE - Sending response to client")
        logger.info("=" * 70 + "\n")

        # 6. Format and return response
        return AnalysisResult(
            basic_stats=basic_stats,
            temporal_stats=temporal_stats,
            linguistic_stats=linguistic_stats,
            transcriptions=transcription_results,
            insights=insights_result,
        )

    except FileNotFoundError as e:
        logger.error(f"❌ File not found: {e}")
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        # Generic error for any other unhandled exception
        logger.error(f"❌ Unexpected error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")
