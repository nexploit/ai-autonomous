import requests

def improve(code):
    r = requests.post("http://ollama:11434/api/generate", json={
        "model": "llama3",
        "prompt": f"Verbessere diesen Python Code:\n{code}"
    }).json()

    return r["response"]