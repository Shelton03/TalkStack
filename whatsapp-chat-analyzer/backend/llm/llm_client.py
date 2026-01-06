from typing import Optional, Literal
import os

# Mock LLM libraries
try:
    import google.generativeai as genai
    GOOGLE_AVAILABLE = True
except ImportError:
    GOOGLE_AVAILABLE = False

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

try:
    import ollama
    OLLAMA_AVAILABLE = True
except ImportError:
    OLLAMA_AVAILABLE = False

LLMProvider = Literal["gemini", "openai", "ollama"]

class LLMClient:
    def __init__(self, provider: LLMProvider, api_key_or_url: Optional[str] = None):
        self.provider = provider
        self.api_key_or_url = api_key_or_url
        self._client = self._initialize_client()

    def _initialize_client(self):
        if self.provider == "gemini":
            if not GOOGLE_AVAILABLE:
                raise ImportError("Google Generative AI SDK not found. Please `pip install google-generativeai`")
            if not self.api_key_or_url:
                raise ValueError("API key is required for Gemini.")
            genai.configure(api_key=self.api_key_or_url)
            return genai.GenerativeModel('gemini-pro')
        
        elif self.provider == "openai":
            if not OPENAI_AVAILABLE:
                raise ImportError("OpenAI SDK not found. Please `pip install openai`")
            if not self.api_key_or_url:
                raise ValueError("API key is required for OpenAI.")
            return OpenAI(api_key=self.api_key_or_url)

        elif self.provider == "ollama":
            if not OLLAMA_AVAILABLE:
                raise ImportError("Ollama SDK not found. Please `pip install ollama`")
            # For Ollama, api_key_or_url can be the base URL, e.g., "http://localhost:11434"
            return ollama.Client(host=self.api_key_or_url)

        else:
            raise ValueError(f"Unsupported LLM provider: {self.provider}")

    def generate_insight(self, prompt: str) -> str:
        """
        Generates text using the configured LLM provider.
        """
        try:
            if self.provider == "gemini":
                response = self._client.generate_content(prompt)
                return response.text

            elif self.provider == "openai":
                chat_completion = self._client.chat.completions.create(
                    messages=[{"role": "user", "content": prompt}],
                    model="gpt-3.5-turbo",
                )
                return chat_completion.choices[0].message.content

            elif self.provider == "ollama":
                # Ensure the model is specified. Defaulting to 'llama2' if not part of the client setup.
                # A more robust solution might pass the model name during generation.
                response = self._client.generate(model='llama2', prompt=prompt)
                return response['response']

        except Exception as e:
            raise RuntimeError(f"Failed to generate insight from {self.provider}: {e}") from e

def get_llm_client(
    provider: LLMProvider, 
    api_key_or_url: Optional[str] = None,
    strict: bool = False
) -> Optional[LLMClient]:
    """Factory function to get an LLM client."""
    if not provider:
        if strict:
            raise ValueError("LLM Provider was not specified.")
        return None
    try:
        return LLMClient(provider, api_key_or_url)
    except (ImportError, ValueError) as e:
        if strict:
            raise e
        print(f"Error initializing LLM client: {e}")
        return None
