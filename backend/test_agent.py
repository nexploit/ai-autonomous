import requests
import json
import re

OLLAMA_URL = "http://ollama:11434/api/chat"
SYSTEM_PROMPT = """
Du bist ein autonomer AI-Agent.
Antworte IMMER im JSON Format.

{"tool": "name", "args": {...}}
oder
{"final": "Antwort"}
"""

def extract_json(text):
    match = re.search(r'\{.*\}', text, re.DOTALL)
    return match.group(0) if match else None

r = requests.post(OLLAMA_URL, json={
    "model": "llama3",
    "messages": [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": "What is 2+2?"}
    ]
})

output = r.json().get("message", {}).get("content", str(r.json()))
print("LLM OUTPUT:")
print(output)
print("\n" + "="*50)
print("EXTRACTED JSON:")
json_part = extract_json(output)
print(json_part)

if json_part:
    try:
        parsed = json.loads(json_part)
        print("PARSED:", parsed)
    except Exception as e:
        print("PARSE ERROR:", e)
