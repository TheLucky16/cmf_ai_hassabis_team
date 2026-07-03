import os, json, config
from openai import OpenAI


def load_text(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


users_text = load_text('data/users.md')
curriculum_text = ''
if os.path.exists('data/curriculum.json'):
    curriculum_text = load_text('data/curriculum.json')
else:
    curriculum_text = '[]'

prompt_template = load_text('data/agent_3_prompt.txt')
prompt_filled = prompt_template.replace('{{USERS}}', users_text).replace('{{CURRICULUM}}', curriculum_text)

with open(config.or_token_path) as f:
    token = f.read().strip()

client = OpenAI(base_url='https://openrouter.ai/api/v1', api_key=token)


def ask_llm(prompt: str) -> str:
    response = client.chat.completions.create(
        model=config.model,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content


if __name__ == '__main__':
    out = ask_llm(prompt_filled)
    # strip fences if present
    s = out.strip()
    if s.startswith('```'):
        # find end fence
        end = s.find('```', 3)
        if end != -1:
            # skip first line (```json or ```)
            nl = s.find('\n')
            if nl != -1:
                s = s[nl+1:end].strip()
            else:
                s = s[3:end].strip()

    # try parse as JSON, fallback to extracting first {...}
    os.makedirs('data', exist_ok=True)
    out_path = os.path.join('data', 'recommendations.json')
    try:
        parsed = json.loads(s)
        with open(out_path, 'w', encoding='utf-8') as f:
            json.dump(parsed, f, ensure_ascii=False, indent=2)
    except Exception:
        start = s.find('{')
        end = s.rfind('}')
        if start != -1 and end != -1 and end > start:
            candidate = s[start:end+1]
            try:
                parsed = json.loads(candidate)
                with open(out_path, 'w', encoding='utf-8') as f:
                    json.dump(parsed, f, ensure_ascii=False, indent=2)
            except Exception:
                with open(out_path, 'w', encoding='utf-8') as f:
                    f.write(candidate)
        else:
            with open(out_path, 'w', encoding='utf-8') as f:
                f.write(s)
