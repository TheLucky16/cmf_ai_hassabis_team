import config, json
from huggingface_hub import InferenceClient
from openai import OpenAI

with open("data/raw_webpage.txt") as f:
    website_text = f.read()
prompt = config.stage_2_prompt
combined_prompt = prompt + "\n\nWebsite content:\n" + website_text
with open(config.or_token_path) as f:
    token = f.read().strip()



def ask_llm(prompt):
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key='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',
    )
    response = client.chat.completions.create(
        model=config.model,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content

output = ask_llm(combined_prompt)


output = output.replace("```json", "")
output = output.replace("```", "")
output = output.strip()
data = json.loads(output)
with open("data/curriculum.json", "w") as f:
    json.dump(data, f, indent=4)