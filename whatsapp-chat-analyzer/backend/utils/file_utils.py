import zipfile
import tempfile
import os
import logging
from pathlib import Path
from typing import Generator, Tuple, List

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def extract_zip(zip_file: bytes) -> tempfile.TemporaryDirectory:
    """
    Extracts a zip file into a temporary directory.

    Args:
        zip_file: The content of the zip file in bytes.

    Returns:
        A TemporaryDirectory object containing the extracted files.
    """
    temp_dir = tempfile.TemporaryDirectory()
    zip_path = Path(temp_dir.name) / "chat.zip"

    with open(zip_path, "wb") as f:
        f.write(zip_file)

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(temp_dir.name)
    
    os.remove(zip_path) # Clean up the zip file after extraction
    
    return temp_dir

def find_chat_file(temp_dir_path: str) -> str:
    """
    Finds the primary chat file - looks for any .txt file with 'chat' anywhere in the filename.
    For example: "chat.txt", "WhatsApp Chat.txt", "my_chat_export.txt", "chat_with_john.txt" all work.

    Args:
        temp_dir_path: The path to the temporary directory.

    Returns:
        The full path to the chat file.

    Raises:
        FileNotFoundError: If no suitable chat file is found.
    """
    logger.info(f"🔍 Searching for chat file in: {temp_dir_path}")
    
    txt_files: List[str] = []
    chat_txt_files: List[str] = []

    for root, _, files in os.walk(temp_dir_path):
        for file in files:
            if file.lower().endswith(".txt"):
                full_path = os.path.join(root, file)
                txt_files.append(full_path)
                logger.debug(f"   Found .txt file: {file}")
                
                # Check if 'chat' appears anywhere in the filename (case-insensitive)
                if "chat" in file.lower():
                    chat_txt_files.append(full_path)
                    logger.info(f"   ✅ Found chat file: {file}")
    
    logger.info(f"📊 Found {len(txt_files)} total .txt files, {len(chat_txt_files)} with 'chat' in name")
    
    if chat_txt_files:
        # Prioritize files with "chat" in their name
        selected_file = chat_txt_files[0]
        logger.info(f"✅ Selected chat file: {os.path.basename(selected_file)}")
        return selected_file
    elif txt_files:
        # If no "chat" files, but other .txt files exist, pick the first one
        selected_file = txt_files[0]
        logger.warning(f"⚠️  No 'chat' file found, using first .txt file: {os.path.basename(selected_file)}")
        return selected_file
    else:
        logger.error("❌ No .txt files found in the ZIP archive")
        raise FileNotFoundError("Could not find any '.txt' chat file in the provided ZIP file.")

def find_media_files(temp_dir_path: str) -> Generator[Tuple[str, str], None, None]:
    """
    Finds all media files (non-txt) in the extracted directory.

    Args:
        temp_dir_path: The path to the temporary directory.

    Yields:
        Tuples of (file_path, file_name).
    """
    for root, _, files in os.walk(temp_dir_path):
        for file in files:
            if not file.lower().endswith(".txt"):
                file_path = os.path.join(root, file)
                yield file_path, file
