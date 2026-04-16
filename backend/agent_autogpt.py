import requests
import json
import re
import asyncio
import sys
from tools.registry import execute_tool

OLLAMA_URL = "http://ollama:11434/api/chat"
REQUEST_TIMEOUT = 45  # 45 second timeout for individual Ollama requests

SYSTEM_PROMPT = """Du bist ein hilfsbereiter AI-Agent mit Zugriff auf Netzwerk-Tools.

Verfügbare Tools:
- ping: Ping einen Host (z.B. {"tool": "ping", "args": {"host": "localhost", "count": 4}})
- dns_lookup: DNS-Auflösung (z.B. {"tool": "dns_lookup", "args": {"domain": "google.com"}})
- network_info: Lokale Netzwerk-Infos abrufen (z.B. {"tool": "network_info", "args": {}})
- check_port: Port auf Host prüfen (z.B. {"tool": "check_port", "args": {"host": "localhost", "port": 8000}})
- traceroute: Route zu Host tracen (z.B. {"tool": "traceroute", "args": {"host": "google.com"}})
- active_connections: Aktive Verbindungen auflisten (z.B. {"tool": "active_connections", "args": {}})
- scan_host: Host auf offene Ports scannen (z.B. {"tool": "scan_host", "args": {"host": "localhost"}})
- shell: Shell-Befehle ausführen (z.B. {"tool": "shell", "args": {"cmd": "whoami"}})

Du MUSST IMMER in REINEM JSON antworten. Keine anderen Worte!

Wenn du ein Tool brauchst, nutze genau die Struktur oben.
Wenn du eine finale Antwort hast:
{"final": "DEINE ANTWORT HIER"}

NIE Text außerhalb von JSON! Immer valides JSON!"""

def extract_json(text):
    # Versuche valides JSON zu finden
    try:
        # Erste: Suche nach ganzen JSON-Objekten
        match = re.search(r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', text, re.DOTALL)
        if match:
            candidate = match.group(0)
            json.loads(candidate)  # Validiere
            return candidate
    except:
        pass
    
    # Fallback: Probiere einfach den ganzen Text
    try:
        json.loads(text)
        return text
    except:
        pass
    
    return None


class AutoGPT:

    def call_llm(self, prompt):
        try:
            r = requests.post(
                OLLAMA_URL,
                json={
                    "model": "llama3",
                    "messages": [
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": prompt}
                    ],
                    "stream": False
                },
                timeout=REQUEST_TIMEOUT
            )
            data = r.json()
            return data.get("message", {}).get("content", str(data))
        except requests.exceptions.Timeout:
            return "REQUEST ERROR: Ollama timeout (>30s). Servidor puede estar sobrecargado."
        except requests.exceptions.ConnectionError:
            return "REQUEST ERROR: No se pudo conectar a Ollama. Verifica que el servicio esté corriendo."
        except Exception as e:
            return f"REQUEST ERROR: {e}"

    def run(self, goal, max_steps=3):
        history = f"ZIEL: {goal}\n"
        sys.stdout.write(f"[AGENT] Starting with goal: {goal}\n")
        sys.stdout.flush()
        last_tool_result = None

        for step in range(max_steps):
            sys.stdout.write(f"[AGENT] Step {step+1}/{max_steps}\n")
            sys.stdout.flush()
            output = self.call_llm(history)
            msg = f"[AGENT] LLM output: {output[:300]}..." if len(output) > 300 else f"[AGENT] LLM output: {output}"
            sys.stdout.write(msg + "\n")
            sys.stdout.flush()

            json_part = extract_json(output)
            sys.stdout.write(f"[AGENT] Extracted JSON: {json_part}\n")
            sys.stdout.flush()

            if json_part:
                try:
                    parsed = json.loads(json_part)
                    sys.stdout.write(f"[AGENT] Parsed: {parsed}\n")
                    sys.stdout.flush()

                    if "final" in parsed:
                        result = parsed["final"]
                        sys.stdout.write(f"[AGENT] Final answer: {result}\n")
                        sys.stdout.flush()
                        return result

                    if "tool" in parsed:
                        tool_name = parsed["tool"]
                        tool_args = parsed.get("args", {})
                        sys.stdout.write(f"[AGENT] Executing tool: {tool_name} with args: {tool_args}\n")
                        sys.stdout.flush()
                        result = execute_tool(tool_name, tool_args)
                        sys.stdout.write(f"[AGENT] Tool result: {result}\n")
                        sys.stdout.flush()
                        last_tool_result = result
                        history += f"\nTool '{tool_name}' Result:\n{result}\n"
                        continue

                except Exception as e:
                    sys.stdout.write(f"[AGENT] JSON parsing error: {e}\n")
                    sys.stdout.flush()
                    history += f"\nJSON ERROR: {e}\n"

            history += f"\n{output}\n"
            
        # Fallback: Wenn nach max_steps kein valides JSON kam, gib das letzte Tool-Ergebnis zurück
        sys.stdout.write(f"[AGENT] Max steps reached\n")
        sys.stdout.flush()
        if last_tool_result:
            return f"Tool-Ergebnis: {last_tool_result}"
        return "Keine finale Antwort nach " + str(max_steps) + " Schritten"
