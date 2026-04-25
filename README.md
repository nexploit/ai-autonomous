# ai-autonomous

Eine Docker-basierte Anwendung mit autonomem AI-Agent fuer Netzwerk-Operationen.

## Projektuebersicht

Dieses Repository enthaelt folgende Komponenten:

### AI und Inference Model

* **Ollama** - Lokales LLM-Runtime-System
* **Llama3 8B** - Open-Source Sprachmodell lokal gehostet
* Keine Cloud-Abhaengigkeiten - vollstaendig auf lokaler Hardware
* Inference laeuft containerisiert in Docker
* CPU-optimiert fuer lokale Ausfuehrung

### Backend

* Python-Backend auf Basis von FastAPI
* Integrierter autonomer Agent mit Ollama / Llama3
* WebSocket-basierte Kommunikation
* Tool-Registry fuer spezialisierte Netzwerkfunktionen

### Frontend

* Node.js-Server fuer die React-Oberflaeche
* WebSocket-basierte Benutzeroberflaeche
* Vite-basierte Build-Pipeline
* Neues Frontend-Design im Stil von `MU/TH/UR` / `Nostromo Industrial`
* `http://localhost` wird ueber Nginx mit der statischen Konsole aus `backend/frontend/index.html` ausgeliefert

### Infrastruktur

* Docker-Compose-Setup mit folgenden Diensten:
* **Ollama** - LLM-Runtime mit Llama3 Modell
* **Backend** - FastAPI mit autonomem Agent
* **Frontend** - Node.js UI Server
* **Nginx** - Reverse Proxy und Auslieferung der Hauptoberflaeche

### Netzwerk-Tools

Der Agent hat Zugriff auf folgende spezialisierte Tools:

* **Ping** - Erreichbarkeit von Hosts pruefen
* **DNS-Lookup** - Domain zu IP aufloesen
* **Traceroute** - Route zu Host tracen
* **Port-Check** - Ports auf Hosts pruefen
* **Aktive Verbindungen** - Netzwerk-Verbindungen auflisten
* **Network Info** - Lokale Netzwerk-Konfiguration
* **Scan Host** - Ports scannen

### Dokumentation

Weitere Projekt-Dokumentation liegt unter `docs/`.
Dort befinden sich unter anderem Setup-, RAG- und Security-Dokumente.

---

## Installation und Verwendung

### Voraussetzungen

* Docker und Docker Compose installiert
* Mindestens 8 GB RAM fuer das Llama3 Modell

### Starten der Anwendung

```bash
docker-compose up -d
```

Die Anwendung ist dann verfuegbar unter:

* **Frontend**: http://localhost
* **Backend API**: http://localhost:8000
* **Ollama API**: http://localhost:11435

### UI-Design

Das Frontend wurde visuell auf einen industriellen `Alien`-inspirierten Bordcomputer-Look umgestellt:

* Bernsteinfarbene `MU/TH/UR`-Konsole mit technischem Panel-Layout
* Statusanzeigen, Command-Feed und Terminal-Optik im `Nostromo`-Stil
* Neue statische Hauptoberflaeche unter `backend/frontend/index.html`
* Zusaetzlich modernisierte React-Oberflaeche unter `frontend/src/`

### Stoppen

```bash
docker-compose down
```

---

## Inference Model Details

### Ollama

**Ollama** ist ein leichtgewichtiges lokales LLM-Runtime-System mit folgenden Vorteilen:

* Vollstaendig lokal
* Open Source
* Datenschutzfreundlich
* Keine API-Gebuehren
* Gute lokale Performance

### Llama3 8B Modell

* **Parameter:** 8 Milliarden
* **Trainiert von:** Meta
* **Lizenz:** Open Source
* **Speicher:** ca. 16 GB RAM/VRAM empfohlen
* **Inferenz-Latenz:** ca. 2 bis 5 Sekunden pro Anfrage auf CPU

### Integration im Agent

Der autonome Agent nutzt Llama3 fuer:

1. Prompt-Parsing
2. Tool-Selection
3. Response-Generation
4. JSON-Output

Alle Verarbeitung erfolgt lokal ohne externe API-Calls.

---

## Architektur

```text
                Nginx (Port 80)
                      |
          +-----------+-----------+
          |                       |
   Nostromo UI              Backend (8000)
 backend/frontend           FastAPI + WS
      index.html                  |
                                  |
                            Ollama (11434)
                              Llama3 lokal
```

Die React-Oberflaeche im Ordner `frontend/` bleibt weiterhin Teil des Projekts, waehrend Nginx fuer `http://localhost` aktuell die neue statische Nostromo-Konsole ausliefert.

---

## Backend-Tools erweitern

Um neue Tools hinzuzufuegen:

1. Tool-Datei erstellen, zum Beispiel `backend/tools/my_tool.py`
2. Tool in `backend/tools/registry.py` registrieren
3. Agent-Prompt in `backend/agent_autogpt.py` erweitern
4. Backend neu bauen:

```bash
docker-compose up -d --build backend
```

---

## Environment und Konfiguration

### Docker Compose Services

| Service | Port | Image | Zweck |
|---------|------|-------|-------|
| ollama | 11434 | ollama/ollama | LLM Runtime lokal |
| backend | 8000 | python:3.11-slim | FastAPI Agent |
| frontend | 3000 | node:22 | React UI Server |
| nginx | 80 | nginx:alpine | Reverse Proxy und Nostromo-UI |

### Volumes

* `ai-autonomus_ollama` - Persistente Speicherung des Llama3 Modells

---

## Datenschutz und Sicherheit

Diese Anwendung laeuft vollstaendig lokal:

* Keine Cloud-Abhaengigkeiten fuer Inference
* Keine Weitergabe von Benutzeranfragen an externe APIs
* Offline-faehig nach initialem Model-Download
* Volle Kontrolle ueber Daten und Infrastruktur

---

## Troubleshooting

### Agent antwortet nicht

1. Backend-Logs pruefen:

```bash
docker logs ai-autonomus-backend-1 --tail 100
```

2. Ollama-Status pruefen:

```bash
docker logs ai-autonomus-ollama-1 --tail 50
```

3. Container-Status pruefen:

```bash
docker ps -a
```

### Technischer Hinweis

Die aktive Backend-Anwendung startet ueber `backend/main.py`.
Frueherer Altbestand wurde nach `backend/legacy/` verschoben und ist derzeit nicht Teil des produktiven Startpfads.

### Modell laedt zu lange

Das Llama3-8B-Modell benoetigt beim ersten Start einige Sekunden zum Laden. Das ist normal.

### Port-Konflikte

Falls Ports bereits belegt sind, in `docker-compose.yaml` anpassen:

```yaml
nginx:
  ports:
    - "8080:80"
```

---

## Lizenz

Dieses Projekt steht unter der MIT Lizenz.

---

## Autor und Erstellung

Die Docker-Anwendung wurde von **Peter Niemietz** in Zusammenarbeit mit **Docker AI Gordon** erstellt.
