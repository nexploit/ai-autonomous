import requests

def critic(step, result):
    r = requests.post("http://ollama:11434/api/generate", json={
        "model": "llama3",
        "prompt": f"Bewerte:\n{step}\n{result}"
    }).json()

    return r["response"]