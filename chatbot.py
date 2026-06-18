"""Shared LLM connector for the cmf_ai_hw_1 pipeline.

`get_answer(prompt)` sends a prompt to Google Gemini (free tier) and returns the
model's text answer. Agents 1, 2 and 3 all call this single function.

Setup:
    1. Get a free API key: https://aistudio.google.com/apikey
    2. export GEMINI_API_KEY="your-key"
    3. pip install -r requirements.txt   (installs google-genai)

The google-genai import is done lazily inside get_answer() so the rest of the
pipeline can be imported and unit-tested without the dependency installed.
"""

import os
import time

# Free-tier model: 1M-token context, no credit card required.
DEFAULT_MODEL = "gemini-2.5-flash"


def get_answer(prompt, *, model=DEFAULT_MODEL, temperature=0.4, max_retries=4):
    """Send `prompt` to Gemini and return the text response.

    Retries with exponential backoff on rate-limit (429) and transient server
    (5xx) errors, which matters on the free tier (~10 requests/minute).

    Raises RuntimeError if GEMINI_API_KEY is not set.
    """
    # Load GEMINI_API_KEY from a local .env file, if python-dotenv is installed.
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass

    from google import genai
    from google.genai import errors, types

    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY is not set. Get a free key at "
            "https://aistudio.google.com/apikey and run: export GEMINI_API_KEY=..."
        )

    client = genai.Client(api_key=api_key)
    config = types.GenerateContentConfig(temperature=temperature)

    last_err = None
    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model=model,
                contents=prompt,
                config=config,
            )
            return (response.text or "").strip()
        except errors.APIError as exc:
            last_err = exc
            code = getattr(exc, "code", None)
            retryable = code == 429 or (isinstance(code, int) and code >= 500)
            if retryable and attempt < max_retries - 1:
                # Back off: 5s, 10s, 20s, ... (free tier resets per minute).
                time.sleep(5 * (2 ** attempt))
                continue
            raise

    raise last_err
