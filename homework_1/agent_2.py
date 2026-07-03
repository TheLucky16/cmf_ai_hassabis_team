import json
import os
from chatbot import get_answer


def parse_llm_response(response: str):
    # Expecting LLM to return valid JSON
    try:
        return json.loads(response)
    except json.JSONDecodeError:
        # If the response contains extra text, try to extract JSON
        import re
        match = re.search(r'\[.*\]', response, re.DOTALL)
        if match:
            return json.loads(match.group(0))
        else:
            raise ValueError("Failed to parse JSON from LLM response")

def create_semantic_blocks(cleaned_markdown: str, prompt_path: str = 'inputs/agent_2_prompt.txt') -> list:
    # Load the prompt
    with open(prompt_path, 'r', encoding='utf-8') as f:
        prompt_template = f.read()
    prompt = prompt_template.replace('[PASTE RAW TEXT HERE]', cleaned_markdown)
    
    # Call LLM
    raw_answer = get_answer(prompt)  
    
    # Parse the response into a list of blocks
    blocks = parse_llm_response(raw_answer)
    return blocks


input_file = 'outputs/agent_1_output.md'
output_file = 'outputs/agent_2_output.json'

if not os.path.exists(input_file):
    print(f"File {input_file} not found. Please run agent 1 first.")
    exit(1)

with open(input_file, 'r', encoding='utf-8') as f:
    cleaned_text = f.read()

semantic_blocks = create_semantic_blocks(cleaned_text)

os.makedirs(os.path.dirname(output_file) or '.', exist_ok=True)
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(semantic_blocks, f, ensure_ascii=False)

print(f"Created {len(semantic_blocks)} micro-lessons. Result saved to {output_file}")