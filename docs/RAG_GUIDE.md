# RAG Guide

## Ueberblick

Das Projekt verwendet aktuell eine einfache dateibasierte RAG-Variante ohne externe Vektor-Datenbank.
Die Wissensbasis liegt in `knowledge_base/` und wird beim Start des Backends geladen.

## Aktueller Aufbau

- `backend/rag_engine.py`
  Laedt Markdown-Dateien aus der Wissensbasis und fuehrt eine einfache Keyword-Suche aus.
- `knowledge_base/*.md`
  Enthalten die lokalen Wissensdokumente.
- `backend/agent_autogpt.py`
  Holt bei einer Anfrage relevanten Kontext aus der RAG-Engine und uebergibt ihn an das LLM.
- `docker-compose.yaml`
  Mountet `./knowledge_base` nach `/app/knowledge_base` in den Backend-Container.

## Verhalten

Beim Backend-Start:

1. Die RAG-Engine initialisiert `./knowledge_base`.
2. Alle `.md`-Dateien werden eingelesen.
3. Bei jeder Nutzeranfrage sucht die Engine passende Dokumente per Keyword-Matching.
4. Treffer werden als Zusatzkontext an das Modell weitergegeben.

## Verfuegbare Endpunkte

### `GET /health`

Liefert den allgemeinen Systemstatus. Wenn RAG aktiv ist, werden auch RAG-Statistiken ausgegeben.

### `GET /rag/stats`

Liefert Informationen ueber:

- Modus
- Anzahl geladener Dokumente
- Speicherpfad
- Dokumentenliste

### `POST /rag/reload`

Laedt die Dokumente aus `knowledge_base/` erneut.

## Wissensbasis erweitern

Lege einfach weitere Markdown-Dateien in `knowledge_base/` an, zum Beispiel:

```md
# Firewall Hinweise

- Port 443 muss offen sein
- Interne Services nur im Docker-Netz erreichbar machen
```

Danach entweder:

- Backend neu starten
- oder `POST /rag/reload` aufrufen

## Bekannte Grenzen

- Keine semantischen Embeddings
- Keine Vektor-Datenbank
- Relevanz basiert nur auf einfachen Stichworttreffern
- Sehr grosse Dokumentenmengen sind fuer diesen Ansatz ungeeignet

## Troubleshooting

### Es werden keine Dokumente gefunden

- Pruefen, ob Dateien in `knowledge_base/` liegen
- Pruefen, ob `docker-compose.yaml` das Volume korrekt mountet
- `GET /rag/stats` aufrufen und Dokumentenanzahl kontrollieren

### Neue Dokumente tauchen nicht auf

- `POST /rag/reload` ausfuehren
- Dateiendung `.md` verwenden
- Gueltige UTF-8-kodierte Textdateien verwenden
