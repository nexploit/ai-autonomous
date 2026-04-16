import requests

def plan(goal):
    prompt = f"Zerlege in konkrete Pentest/IT Schritte:\n{goal}"

    r = requests.post("http://ollama:11434/api/generate", json={
        "model": "llama3",
        "prompt": prompt
    }).json()

    return [s for s in r["response"].split("\n") if s.strip()]