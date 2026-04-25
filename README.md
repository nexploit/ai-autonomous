# ai-autonomous

Eine vollständige Docker-basierte Anwendung mit autonomem AI-Agent für Netzwerk-Operationen.

## Projektübersicht

Dieses Repository enthält folgende Komponenten:

### AI & Inference Model

* **Ollama** - Lokales LLM-Runtime-System
* **Llama3 8B** - Open-Source Sprachmodell lokal gehostet
* Keine Cloud-Abhängigkeiten - vollständig auf lokaler Hardware
* Inference läuft containerisiert in Docker
* CPU-optimiert für schnelle Inferenz

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

### Dokumentation

Weitere Projekt-Dokumentation liegt unter `docs/`.
Dort befinden sich unter anderem Setup-, RAG- und Security-Dokumente.

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

## Inference Model Details

### Ollama - Lokales LLM Runtime

**Ollama** ist ein leichtgewichtiges, lokales LLM-Runtime-System das folgende Vorteile bietet:

* **Vollständig lokal** - Keine Daten an Cloud-Provider
* **Open Source** - Transparent und erweiterbar
* **Datenschutz** - Alle Inferenzen laufen auf deinem System
* **Kostenlos** - Keine API-Gebühren
* **Schnell** - CPU-optimierte Inferenz

### Llama3 8B Modell

* **Parameter:** 8 Milliarden
* **Trainiert von:** Meta
* **Lizenz:** Open Source (Llama 2 Community License)
* **Speicher:** ~16GB RAM/VRAM empfohlen
* **Inferenz-Latenz:** 2-5 Sekunden pro Anfrage (CPU)

### Integration im Agent

Der autonome Agent nutzt Llama3 für:

1. **Prompt-Parsing** - Versteht Benutzeranfragen
2. **Tool-Selection** - Wählt passendes Netzwerk-Tool
3. **Response-Generation** - Generiert Antworten basierend auf Tool-Ergebnissen
4. **JSON-Output** - Strukturierte Kommunikation mit Backend

Alle Verarbeitung erfolgt lokal ohne externe API-Calls.

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
                            │  (Lokal gehostet)
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
| ollama | 11434 | ollama/ollama | LLM Runtime (lokal gehostet) |
| backend | 8000 | python:3.11-slim | FastAPI Agent |
| frontend | 3000 | node:22 | UI Server |
| nginx | 80 | nginx:alpine | Reverse Proxy |

### Volumes

* `ai-autonomus_ollama` - Persistente Speicherung des Llama3 Modells (lokal)

---

## Datenschutz & Sicherheit

### Lokale Ausführung

Diese Anwendung läuft vollständig lokal:

* **Keine Cloud-Abhängigkeiten** - Ollama und Llama3 laufen in deinem Docker Container
* **Datenschutz** - Keine Benutzeranfragen oder Daten werden an externe Server gesendet
* **Offline-fähig** - Funktioniert auch ohne Internetverbindung (nach initialem Download)
* **Volle Kontrolle** - Du hast vollständige Kontrolle über deine Daten

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

### Technischer Hinweis

Die aktive Backend-Anwendung startet über `backend/main.py`.
Früherer Altbestand wurde nach `backend/legacy/` verschoben und ist derzeit nicht Teil des produktiven Startpfads.

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
