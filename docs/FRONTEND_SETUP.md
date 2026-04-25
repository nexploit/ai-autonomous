# Frontend Setup

## Ueberblick

Das Frontend besteht aus einer React-App mit Vite-Build und einem kleinen Node.js-Server fuer die Auslieferung der Build-Artefakte.
Im Produktivpfad wird das Frontend ueber Nginx ausgeliefert.

## Architektur

```text
Browser -> Nginx (:80) -> Frontend (:3000)
                     -> WebSocket /ws -> Backend (:8000)
```

## Wichtige Dateien

- `frontend/src/App.jsx`
  Chat-Oberflaeche und WebSocket-Client
- `frontend/src/App.css`
  Styling der Chat-Oberflaeche
- `frontend/server.js`
  Liefert das gebaute Frontend aus `dist/` aus
- `frontend/Dockerfile`
  Multi-Stage-Build fuer Build und Laufzeit
- `nginx.conf`
  Reverse Proxy fuer Frontend, API und WebSocket

## Start mit Docker

```bash
docker compose up --build
```

Danach ist die Anwendung unter `http://localhost` erreichbar.

## WebSocket-Verhalten

Das Frontend verbindet sich mit:

- `ws://<host>/ws`
- bzw. `wss://<host>/ws` bei HTTPS

Eigenschaften:

- automatischer Reconnect
- Ladeanzeige waehrend Anfragen
- Anzeige von Backend-Antworten im Chat

## Typische Fehlerquellen

### Nachricht erscheint im Backend-Log, aber nicht im Frontend

Das wurde bereits im aktuellen Stand behoben, indem Nachrichten eindeutige IDs erhalten.

### Frontend verbindet sich nicht

- Nginx-Container pruefen
- Backend-Container pruefen
- Browser-Konsole auf WebSocket-Fehler pruefen

### Build schlaegt fehl

- `frontend/package.json` pruefen
- Frontend-Container neu bauen
- lokale Node-Umgebung nicht mit Docker-Ergebnis verwechseln
