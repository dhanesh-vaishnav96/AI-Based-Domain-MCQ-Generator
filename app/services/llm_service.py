from groq import Groq
import json
import re
import time
import logging
from app.core.config import settings

# Initialize client
client = Groq(api_key=settings.GROQ_API_KEY)
logger = logging.getLogger(__name__)

MAX_RETRIES = 3

# Model priority list (config + fallback)
MODELS = [
    settings.GROQ_MODEL,   # from .env
    "llama-3.1-8b-instant"
]

def call_llm(prompt: str, model_name: str):
    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": "You are a strict JSON generator."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )

    return response.choices[0].message.content

def extract_json(response_text: str):
    cleaned = re.sub(r"```json|```", "", response_text).strip()

    match = re.search(r"\[.*?\]", cleaned, re.DOTALL)
    if not match:
        raise ValueError("No valid JSON array found")

    return json.loads(match.group(0))


def generate_with_retry(prompt: str):
    last_error = None

    for model_name in MODELS:
        for attempt in range(MAX_RETRIES):
            try:
                logger.info(f"Using model: {model_name} (attempt {attempt+1})")

                raw_response = call_llm(prompt, model_name)

                return extract_json(raw_response)

            except Exception as e:
                last_error = e
                error_str = str(e)

                logger.warning(f"{model_name} attempt {attempt+1} failed: {error_str}")

                if "JSON" in error_str or "Extra data" in error_str:
                    prompt += "\n\nIMPORTANT: Return ONLY JSON array. No explanation."

                # Handle rate limit
                if "429" in error_str or "rate_limit" in error_str:
                    time.sleep(5)
                else:
                    time.sleep(2 ** attempt)

    raise Exception(f"All models failed: {str(last_error)}")