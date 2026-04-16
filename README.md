# ai-autonomous

Eine vollständige Docker-basierte Anwendung mit autonomem AI-Agent für Netzwerk-Operationen.

## Projektübersicht

Dieses Repository enthält folgende Komponenten:

### Backend

* Python-Backend auf Basis von FastAPI
* Integrierter autonomer Agent (Ollama / Llama3)
* WebSocket-basierte Kommunikation
* Tool-Registry für spezialisierte Funktionen

### Frontend

* Node.js-Server
* Benutzeroberfläche für WebSocket-basierten Chat
* Vite-basierte Build-Pipeline

### Infrastruktur

* Docker-Compose-Setup mit folgenden Diensten:

  * **Ollama** - LLM-Runtime mit Llama3 Modell
  * **Backend** - FastAPI mit autonomem Agent
  * **Frontend** - Node.js UI Server
  * **Nginx** - Reverse Proxy

### Netzwerk-Tools

Der Agent hat Zugriff auf folgende spezialisierte Tools:

* **Ping** - Erreichbarkeit von Hosts prüfen
* **DNS-Lookup** - Domain zu IP auflösen
* **Traceroute** - Route zu Host tracen
* **Port-Check** - Ports auf Hosts prüfen
* **Aktive Verbindungen** - Netzwerk-Verbindungen auflisten
* **Network Info** - Lokale Netzwerk-Konfiguration
* **Scan Host** - Ports scannen

### Sonstiges

* `.gitignore` enthält Ausschlüsse für:

  * Python (`__pycache__`, `*.pyc`, `venv/`)
  * Node.js (`node_modules/`)
  * Docker (`.docker/`)
  * IDE-Dateien (`.vscode/`, `.idea/`)
  * Umgebungsdateien (`.env`)

---

## Installation & Verwendung

### Voraussetzungen

* Docker & Docker Compose installiert
* Mindestens 8GB RAM (für Llama3 Modell)

### Starten der Anwendung

```bash
docker-compose up -d
```

Die Anwendung ist dann verfügbar unter:
- **Frontend**: http://localhost
- **Backend API**: http://localhost:8000
- **Ollama API**: http://localhost:11435

### Stoppen

```bash
docker-compose down
```

---

## Architektur

```
┌─────────────────────────────────────────────────────────┐
│                      Nginx (Port 80)                    │
└──────────────────────┬──────────────────────────────────┘
                       │
        ┌──────────────┴──────────────┐
        │                             │
┌───────▼────────┐          ┌────────▼────────┐
│   Frontend     │          │    Backend      │
│  (Port 3000)   │          │  (Port 8000)    │
│   Node.js UI   │          │  FastAPI        │
└────────────────┘          └────────┬────────┘
                                     │
                            ┌────────▼────────┐
                            │     Ollama      │
                            │  (Port 11434)   │
                            │  Llama3 Model   │
                            └─────────────────┘
```

---

## Backend-Tools erweitern

Um neue Tools hinzuzufügen:

1. **Tool-Datei erstellen** (z.B. `backend/tools/my_tool.py`):

```python
def my_tool(param: str) -> dict:
    """Beschreibung des Tools"""
    try:
        result = do_something(param)
        return {"status": "success", "data": result}
    except Exception as e:
        return {"status": "error", "error": str(e)}
```

2. **In Registry registrieren** (`backend/tools/registry.py`):

```python
from tools.my_tool import my_tool

TOOLS = {
    ...
    "my_tool": my_tool,
}
```

3. **Agent-Prompt updaten** (`backend/agent_autogpt.py`):

Zeile im `SYSTEM_PROMPT` hinzufügen mit Tool-Beschreibung.

4. **Backend neu bauen**:

```bash
docker-compose up -d --build backend
```

---

## Environment & Konfiguration

### Docker Compose Services

| Service | Port | Image | Zweck |
|---------|------|-------|-------|
| ollama | 11434 | ollama/ollama | LLM Runtime |
| backend | 8000 | python:3.11-slim | FastAPI Agent |
| frontend | 3000 | node:22 | UI Server |
| nginx | 80 | nginx:alpine | Reverse Proxy |

### Volumes

* `ai-autonomus_ollama` - Persistente Speicherung des Llama3 Modells

---

## Troubleshooting

### Agent antwortet nicht

1. Logs prüfen:
```bash
docker logs ai-autonomus-backend-1 --tail 100
```

2. Ollama-Status:
```bash
docker logs ai-autonomus-ollama-1 --tail 50
```

3. WebSocket-Verbindung überprüfen:
```bash
docker ps -a | grep ai-autonomus
```

### Modell lädt zu lange

Das Llama3 8B Modell benötigt beim ersten Start 10-15 Sekunden zum Laden. Dies ist normal.

### Port-Konflikte

Falls Ports bereits belegt sind, in `docker-compose.yaml` anpassen:

```yaml
nginx:
  ports:
    - "8080:80"  # Statt 80:80
```

---

## Lizenz

Dieses Projekt steht unter der MIT Lizenz.

---

## Autor & Erstellung

Die Docker-Anwendung wurde von **Peter Niemietz** ([peter.niemietz@nexploit.de](mailto:peter.niemietz@nexploit.de)) in Zusammenarbeit mit **Docker AI Gordon** erstellt.

**Datum:** 16.04.2026
