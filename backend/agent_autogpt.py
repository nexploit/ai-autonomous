import requests
import json
import re
import sys
import os
from tools.registry import execute_tool
from rag_engine import RAGEngine

OLLAMA_URL = "http://ollama:11434/api/chat"
REQUEST_TIMEOUT = 180
DEFAULT_MODEL = os.getenv("OLLAMA_MODEL", "llama3")
MEDICAL_MODEL = os.getenv("OLLAMA_MEDICAL_MODEL", "medgemma:4b")

MEDICAL_KEYWORDS = {
    "arzt", "atemnot", "behandlung", "blutdruck", "cholesterin", "diagnose",
    "durchfall", "erbrechen", "fieber", "gesundheit", "hdl", "herz", "husten",
    "infekt", "insulin", "krank", "krankheit", "medizin", "medikament",
    "medizinisch", "medikamente", "notaufnahme", "patient", "praxis",
    "schmerzen", "symptom", "symptome", "therapie", "vorsorge", "wunde"
}

SYSTEM_PROMPT = """Du bist ein hilfsbereiter AI-Agent mit Zugriff auf Netzwerk-Tools.

ANTWORTE IMMER IN JSON FORMAT. Beispiele:

Wenn du ein Tool nutzen willst:
{"tool": "ping", "args": {"host": "localhost"}}

Wenn du die finale Antwort hast:
{"final": "Deine Antwort hier"}

NUR JSON. KEINE ANDEREN WORTE!"""

MEDICAL_SYSTEM_PROMPT = """Du bist ein medizinischer Berater fuer allgemeine Gesundheitsfragen.

ANTWORTE IMMER IN JSON FORMAT.

Nutze ausschliesslich dieses Format:
{"final": "Deine Antwort hier"}

Gib keine Tools aus. Formuliere klar, vorsichtig und mit Hinweis auf aerztliche Hilfe bei akuten Warnzeichen.
NUR JSON. KEINE ANDEREN WORTE!"""

def extract_json(text):
    """Extract JSON from text - sehr tolerant"""
    # Versuche verschiedene Methoden
    
    # 1. Suche nach {"..."}
    try:
        match = re.search(r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', text, re.DOTALL)
        if match:
            candidate = match.group(0)
            parsed = json.loads(candidate)
            return candidate
    except:
        pass
    
    # 2. Versuche ganzen Text
    try:
        parsed = json.loads(text.strip())
        return text.strip()
    except:
        pass
    
    # 3. Suche nach JSON-ähnlichem Pattern
    try:
        # Entferne Markdown-Code-Blöcke
        clean = re.sub(r'```json\n?', '', text)
        clean = re.sub(r'```\n?', '', clean)
        clean = clean.strip()
        
        match = re.search(r'\{.*\}', clean, re.DOTALL)
        if match:
            candidate = match.group(0)
            parsed = json.loads(candidate)
            return candidate
    except:
        pass
    
    return None


class AutoGPT:
    def __init__(self):
        sys.stdout.write(
            f"[AUTOGPT] Initializing with default model: {DEFAULT_MODEL} and medical model: {MEDICAL_MODEL}\n"
        )
        sys.stdout.flush()
        
        try:
            self.rag = RAGEngine(persist_dir="./knowledge_base")
            stats = self.rag.get_stats()
            sys.stdout.write(f"[AUTOGPT] RAG ready: {len(stats.get('documents_list', []))} docs\n")
            sys.stdout.flush()
        except Exception as e:
            sys.stdout.write(f"[AUTOGPT] RAG error: {e}\n")
            sys.stdout.flush()
            self.rag = None

    def is_medical_query(self, text):
        lowered = text.lower()
        return any(keyword in lowered for keyword in MEDICAL_KEYWORDS)

    def call_llm(self, prompt, model_name, system_prompt):
        try:
            r = requests.post(
                OLLAMA_URL,
                json={
                    "model": model_name,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": prompt}
                    ],
                    "stream": False,
                    "keep_alive": "5m"
                },
                timeout=REQUEST_TIMEOUT
            )
            data = r.json()
            response = data.get("message", {}).get("content", str(data))
            return response
        except requests.exceptions.Timeout:
            return '{"error": "Ollama timeout"}'
        except requests.exceptions.ConnectionError:
            return '{"error": "Cannot connect to Ollama"}'
        except Exception as e:
            return f'{{"error": "{str(e)}"}}'

    def run(self, goal, max_steps=3):
        sys.stdout.write(f"[AGENT] Goal: {goal}\n")
        sys.stdout.flush()

        is_medical = self.is_medical_query(goal)
        selected_model = MEDICAL_MODEL if is_medical else DEFAULT_MODEL
        selected_prompt = MEDICAL_SYSTEM_PROMPT if is_medical else SYSTEM_PROMPT
        sys.stdout.write(f"[AGENT] Using model: {selected_model}\n")
        sys.stdout.flush()
        
        # RAG Context
        rag_context = ""
        if self.rag and not is_medical:
            try:
                retrieved = self.rag.retrieve_context(goal, top_k=2)
                if retrieved:
                    rag_context = "\n📚 KNOWLEDGE:\n" + "\n".join(retrieved)
            except Exception as e:
                sys.stdout.write(f"[AGENT] RAG error: {e}\n")
                sys.stdout.flush()
        
        history = f"ZIEL: {goal}\n{rag_context}\n"
        
        for step in range(max_steps):
            sys.stdout.write(f"[AGENT] Step {step+1}/{max_steps}\n")
            sys.stdout.flush()
            
            output = self.call_llm(history, selected_model, selected_prompt)
            sys.stdout.write(f"[AGENT] LLM: {output[:200]}\n")
            sys.stdout.flush()

            json_str = extract_json(output)
            
            if not json_str:
                # Kein JSON erkannt - einfach als Antwort nehmen
                sys.stdout.write(f"[AGENT] No JSON - using as answer\n")
                sys.stdout.flush()
                return output[:500]
            
            try:
                parsed = json.loads(json_str)
                sys.stdout.write(f"[AGENT] Parsed: {str(parsed)[:100]}\n")
                sys.stdout.flush()

                # Check for final answer
                if "final" in parsed:
                    result = parsed["final"]
                    sys.stdout.write(f"[AGENT] Final: {result[:100]}\n")
                    sys.stdout.flush()
                    return result

                # Check for tool
                if "tool" in parsed:
                    tool_name = parsed["tool"]
                    tool_args = parsed.get("args", {})
                    sys.stdout.write(f"[AGENT] Tool: {tool_name}\n")
                    sys.stdout.flush()
                    
                    try:
                        result = execute_tool(tool_name, tool_args)
                        sys.stdout.write(f"[AGENT] Tool result: {str(result)[:100]}\n")
                        sys.stdout.flush()
                        history += f"\nTool '{tool_name}' returned:\n{result}\n"
                        continue
                    except Exception as e:
                        sys.stdout.write(f"[AGENT] Tool error: {e}\n")
                        sys.stdout.flush()
                        history += f"\nTool error: {e}\n"
                        continue

                # Unbekanntes JSON - weiter zur nächsten Iteration
                history += f"\n{output}\n"
                
            except json.JSONDecodeError as e:
                sys.stdout.write(f"[AGENT] JSON parse error: {e}\n")
                sys.stdout.flush()
                history += f"\n{output}\n"
        
        # Fallback nach max_steps
        sys.stdout.write(f"[AGENT] Max steps reached\n")
        sys.stdout.flush()
        return f"Agent hat nach {max_steps} Schritten keine finale Antwort gefunden. Letzter Output: {output[:200]}"
