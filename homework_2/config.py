import json, os
from pathlib import Path

# Local credentials live outside the repo by default:
# ~/Documents/credentials.json
#
# Example:
# {
#   "provider_order": ["groq", "gemini", "openrouter"],
#   "groq": {"api_key": "...", "model": "llama-3.3-70b-versatile"},
#   "gemini": {"api_key": "...", "model": "gemini-2.5-flash"},
#   "openrouter": {"api_key": "...", "model": "google/gemini-2.5-flash"}
# }

CREDENTIALS_PATH = Path(os.environ.get("CMF_AI_CREDENTIALS", Path.home() / "Documents" / "credentials.json"))
PROVIDER_ORDER = ["groq", "gemini", "openrouter"]

DEFAULT_MODELS = {
    "groq": "llama-3.3-70b-versatile",
    "gemini": "gemini-2.5-flash",
    "openrouter": "google/gemini-2.5-flash",
}

DEFAULT_BASE_URLS = {
    "groq": "https://api.groq.com/openai/v1/chat/completions",
    "gemini": "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent",
    "openrouter": "https://openrouter.ai/api/v1/chat/completions",
}

EXAMPLE_CREDENTIALS = {
    "provider_order": ["groq", "gemini", "openrouter"],
    "groq": {"api_key": "your_groq_key", "model": DEFAULT_MODELS["groq"]},
    "gemini": {"api_key": "your_gemini_key", "model": DEFAULT_MODELS["gemini"]},
    "openrouter": {"api_key": "your_openrouter_key", "model": DEFAULT_MODELS["openrouter"]},
}


def load_credentials(path=CREDENTIALS_PATH):
    if not path.exists():
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def provider_settings(name, credentials):
    raw = credentials.get(name, {})
    if isinstance(raw, str):
        raw = {"api_key": raw}

    env_prefix = name.upper()
    api_key = raw.get("api_key") or raw.get("key") or credentials.get(f"{name}_api_key") or credentials.get(f"{name}_api") or os.environ.get(f"{env_prefix}_API_KEY")
    model = raw.get("model") or os.environ.get(f"{env_prefix}_MODEL") or DEFAULT_MODELS.get(name)
    base_url = raw.get("base_url") or DEFAULT_BASE_URLS.get(name)

    if not api_key:
        return None
    api_key = str(api_key).strip()
    return {
        "name": name,
        "api_key": api_key,
        "model": model,
        "base_url": base_url,
        "site_url": raw.get("site_url", "http://localhost"),
        "app_name": raw.get("app_name", "cmf-ai-homework-2"),
    }


def get_llm_providers():
    credentials = load_credentials()
    order = credentials.get("provider_order", PROVIDER_ORDER)
    providers = []

    for name in order:
        settings = provider_settings(name, credentials)
        if settings:
            providers.append(settings)

    if providers:
        return providers

    path = str(CREDENTIALS_PATH)
    raise RuntimeError(
        "No LLM API keys found. Create local credentials at "
        f"{path} or set GROQ_API_KEY, GEMINI_API_KEY, or OPENROUTER_API_KEY."
    )
