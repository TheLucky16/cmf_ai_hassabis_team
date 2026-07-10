import json, re, time, urllib.error, urllib.parse, urllib.request
from pathlib import Path
from config import get_llm_providers

PROVIDER_INDEX = 0


def read_text(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def write_text(path, text):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


def read_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def write_json(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def split_lessons(lessons_text):
    chunks = re.split(r"(?m)^## Lesson\s+", lessons_text)
    lessons = []

    for chunk in chunks[1:]:
        title, body = chunk.split("\n", 1)
        number = int(title.split(":", 1)[0].strip())
        lessons.append({"number": number, "title": "Lesson " + title.strip(), "body": body.strip()})

    return lessons


def format_history(history, max_turns=6):
    recent = history[-max_turns:]
    return "\n\n".join(f"{m['speaker']}: {m['text']}" for m in recent)


def add_message(history, speaker, text):
    history.append({"speaker": speaker, "text": text})
    return history


def save_dialogue(history, path):
    lines = ["# Mentor-Student Dialogue", ""]
    for msg in history:
        lines.append(f"## Turn {msg['turn']}: {msg['speaker']} ({msg['action']})")
        lines.append("")
        lines.append(msg["text"].strip())
        lines.append("")
    write_text(path, "\n".join(lines))


def save_state(state, path):
    write_json(path, state)


def choose_label(raw, allowed, default):
    raw = raw.strip().lower()
    normalized = re.sub(r"[\s-]+", "_", raw)
    for label in allowed:
        if re.search(rf"\b{re.escape(label)}\b", raw) or re.search(rf"\b{re.escape(label)}\b", normalized):
            return label
    return default


def get_status(text):
    match = re.search(r"STATUS:\s*(.+)", text)
    return match.group(1).strip().lower() if match else ""


def retry_wait_seconds(error_text, attempt):
    match = re.search(r"try again in ([0-9.]+)s", error_text, re.I)
    if match:
        return float(match.group(1)) + 1
    return 2 * (attempt + 1)


def _provider_order(provider=None):
    global PROVIDER_INDEX
    providers = get_llm_providers()

    if provider:
        chosen = [p for p in providers if p["name"] == provider]
        if not chosen:
            raise RuntimeError(f"Provider '{provider}' is not configured.")
        return chosen

    start = PROVIDER_INDEX % len(providers)
    PROVIDER_INDEX += 1
    return providers[start:] + providers[:start]


def _post_json(url, headers, payload, timeout=90):
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")

    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        body = re.sub(r"\s+", " ", body).strip()[:300]
        raise RuntimeError(f"HTTP {exc.code}: {body}") from None
    except urllib.error.URLError as exc:
        raise RuntimeError(str(exc.reason)) from None


def _chat_completion(provider, prompt, system=None, temperature=0.4, max_tokens=1200):
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})

    headers = {
        "Authorization": f"Bearer {provider['api_key']}",
        "Content-Type": "application/json",
        "Accept": "application/json",
        "User-Agent": "cmf-ai-homework-2/1.0",
    }
    if provider["name"] == "openrouter":
        headers["HTTP-Referer"] = provider["site_url"]
        headers["X-Title"] = provider["app_name"]

    payload = {
        "model": provider["model"],
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
    }
    data = _post_json(provider["base_url"], headers, payload)
    return data["choices"][0]["message"]["content"].strip()


def _gemini(provider, prompt, system=None, temperature=0.4, max_tokens=1200):
    text = f"{system}\n\n{prompt}" if system else prompt
    url = provider["base_url"].format(model=urllib.parse.quote(provider["model"], safe=""))
    url = f"{url}?key={urllib.parse.quote(provider['api_key'], safe='')}"
    payload = {
        "contents": [{"role": "user", "parts": [{"text": text}]}],
        "generationConfig": {"temperature": temperature, "maxOutputTokens": max_tokens},
    }
    data = _post_json(url, {"Content-Type": "application/json"}, payload)
    candidates = data.get("candidates", [])
    if not candidates:
        raise RuntimeError("Gemini returned no candidates")

    candidate = candidates[0]
    content = candidate.get("content", {})
    parts = content.get("parts", [])
    text = "".join(part.get("text", "") for part in parts).strip()
    if text:
        return text

    reason = candidate.get("finishReason", "unknown finish reason")
    raise RuntimeError(f"Gemini returned no text ({reason})")


def get_answer(prompt, system=None, provider=None, temperature=0.4, max_tokens=1200, max_retries=2):
    errors = []

    for settings in _provider_order(provider):
        for attempt in range(max_retries):
            try:
                if settings["name"] == "gemini":
                    return _gemini(settings, prompt, system, temperature, max_tokens)
                return _chat_completion(settings, prompt, system, temperature, max_tokens)
            except Exception as exc:
                errors.append(f"{settings['name']}: {exc}")
                if attempt < max_retries - 1:
                    time.sleep(retry_wait_seconds(str(exc), attempt))

    raise RuntimeError("All LLM providers failed: " + "; ".join(errors))
