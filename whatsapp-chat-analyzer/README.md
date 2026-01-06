# WhatsApp Chat Analyzer

This project is a local-first MVP designed to analyze WhatsApp chat exports. It provides key metrics, temporal and linguistic analytics, optional voice note transcription, and optional AI-powered insights.

The application consists of a FastAPI backend for processing and a React frontend for visualization.

## Features

-   **Chat Parsing**: Parses exported `.txt` chat files to extract messages, senders, and timestamps.
-   **Basic Analytics**: Calculates metrics like message counts, word counts, and average message length per user.
-   **Temporal Analysis**: Visualizes chat activity over time, by hour, and by day of the week.
-   **Linguistic Analysis**: Identifies the most frequently used words.
-   **Optional Voice Note Transcription**: If enabled, uses OpenAI's Whisper to transcribe `.opus` voice notes.
-   **Optional AI Insights**: If enabled, sends a summary of analytics to an LLM (Gemini, OpenAI, or a local Ollama instance) to generate a qualitative summary of the chat.

## Privacy Considerations

This is a **local-first** application. Your chat data is processed on your machine.

-   The chat ZIP file is sent from the frontend to a locally running backend server.
-   **No data is stored permanently**. All processing is done in-memory or in a temporary directory that is deleted after each analysis.
-   **External network calls are opt-in only**:
    -   If "Enable voice note transcription" is checked, audio files are processed by the locally running Whisper model. Depending on your Whisper setup, this should not require an internet connection.
    -   If "Enable AI-generated insights" is checked, a **non-identifiable, aggregated JSON summary** of the analytics is sent to the selected LLM provider (Google, OpenAI, or Ollama). The raw chat text is **never** sent.

## Project Structure

```
whatsapp-chat-analyzer/
├── backend/       # FastAPI application
└── frontend/      # React/Vite application
```

## How to Run

### Prerequisites

-   Python 3.11+
-   Node.js 18+ and npm
-   An exported WhatsApp chat `.zip` file.

### 1. Backend Setup

```bash
# Navigate to the backend directory
cd whatsapp-chat-analyzer/backend

# Create a virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# (Optional) For voice transcription, install Whisper
pip install openai-whisper

# (Optional) For AI insights, install the required SDKs
# pip install google-generativeai openai ollama

# Run the FastAPI server
uvicorn main:app --reload
```

The backend will be running at `http://localhost:8000`.

### 2. Frontend Setup

```bash
# Open a new terminal and navigate to the frontend directory
cd whatsapp-chat-analyzer/frontend

# Install dependencies
npm install

# Run the Vite development server
npm run dev
```

The frontend will be running at `http://localhost:5173` (or another port if 5173 is in use). Open this URL in your browser to use the application.

## How to Use

1.  Open the frontend URL in your browser.
2.  Click the "Choose File" button and select your WhatsApp chat `.zip` file.
3.  (Optional) Check the box to enable voice note transcription.
4.  (Optional) Check the box to enable AI-generated insights and configure the provider and API key/URL.
5.  Click the "Analyze" button.
6.  View the dashboard with your chat analytics.

## Limitations of the MVP

-   **1-on-1 Chats Only**: The parser is optimized for two-person chats. Group chats may produce unexpected results.
-   **Limited Parser Robustness**: The regex-based parser might fail on unconventional message formats or different languages.
-   **Basic Stopword List**: The common word analysis uses a simple, built-in list of English stopwords.
-   **No Image/Video Analysis**: All media except for voice notes is ignored.
-   **Whisper Model**: The transcription feature uses the base Whisper model by default, which is fast but not the most accurate.
-   **Simple Error Handling**: While the app tries to fail gracefully, complex errors might require checking the console logs of the backend or frontend.
