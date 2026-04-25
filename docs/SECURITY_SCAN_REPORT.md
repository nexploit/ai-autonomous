# Docker Security Scan Report

Datum: 16.04.2026  
Scan-Tool: Docker Scout v1.20.3

---

## Zusammenfassung

Ein Sicherheitsscan mit Docker Scout wurde durchgeführt für alle Production Images der ai-autonomus Anwendung. Insgesamt wurden **74 Vulnerabilities** gefunden, davon:

- **0 CRITICAL** 
- **19 HIGH**
- **25 MEDIUM**
- **29 LOW**
- **4 UNSPECIFIED**

---

## Details pro Image

### 1. ai-autonomus-backend:latest

**Basis:** `python:3.11-slim`  
**Größe:** 64 MB  
**Packages:** 187  

**Vulnerabilities:**
- **0 CRITICAL** | **4 HIGH** | **2 MEDIUM** | **26 LOW** | **2 UNSPECIFIED**
- **Total: 34 Vulnerabilities**

**Kritische Findings:**

| Paket | CVE | Severity | Fix |
|-------|-----|----------|-----|
| openssl | CVE-2026-28390 | HIGH | Upgrade zu 3.5.5-1~deb13u2 |
| openssl | CVE-2026-28389 | HIGH | Upgrade zu 3.5.5-1~deb13u2 |
| openssl | CVE-2026-28388 | HIGH | Upgrade zu 3.5.5-1~deb13u2 |
| wheel | CVE-2026-24049 | HIGH | Upgrade zu 0.46.2 (Path Traversal) |
| pip | CVE-2025-8869 | MEDIUM | Upgrade zu 25.3 (Link Following) |
| tar | CVE-2025-45582 | MEDIUM | No fix available yet |

**Empfehlung:** OpenSSL und wheel sollten aktualisiert werden. Die Debian-basierten LOW-CVEs sind meist deprecated und erfordern mehrheitlich kein Handeln.

---

### 2. ai-autonomus-frontend:latest

**Basis:** `node:22-alpine`  
**Größe:** 60 MB  
**Packages:** 283  

**Vulnerabilities:**
- **0 CRITICAL** | **7 HIGH** | **5 MEDIUM** | **1 LOW** | **2 UNSPECIFIED**
- **Total: 15 Vulnerabilities**

**Kritische Findings:**

| Paket | CVE | Severity | Fix |
|-------|-----|----------|-----|
| openssl | CVE-2026-31790 | HIGH | Upgrade zu 3.5.6-r0 |
| openssl | CVE-2026-28390 | HIGH | Upgrade zu 3.5.6-r0 |
| openssl | CVE-2026-28389 | HIGH | Upgrade zu 3.5.6-r0 |
| openssl | CVE-2026-28388 | HIGH | Upgrade zu 3.5.6-r0 |
| openssl | CVE-2026-2673 | HIGH | Upgrade zu 3.5.6-r0 |
| picomatch | CVE-2026-33671 | HIGH | Upgrade zu 4.0.4 (ReDoS) |
| musl | CVE-2026-40200 | HIGH | Upgrade zu 1.2.5-r23 |
| brace-expansion | CVE-2026-33750 | MEDIUM | Upgrade zu 5.0.5 (Resource Exhaustion) |
| zlib | CVE-2026-22184 | MEDIUM | Upgrade zu 1.3.2-r0 |
| busybox | CVE-2025-60876 | MEDIUM | No fix available |

**Empfehlung:** Alpine 3.23 und Node 22 sollten aktualisiert werden. OpenSSL CVEs sollten priorisiert werden.

---

### 3. nginx:alpine (Reverse Proxy)

**Basis:** `nginx:alpine`  
**Größe:** 26 MB  
**Packages:** 88  

**Vulnerabilities:**
- **0 CRITICAL** | **8 HIGH** | **13 MEDIUM** | **2 LOW** | **2 UNSPECIFIED**
- **Total: 25 Vulnerabilities**

**Kritische Findings:**

| Paket | CVE | Severity | Fix |
|-------|-----|----------|-----|
| openssl | CVE-2026-31790 | HIGH | Upgrade zu 3.5.6-r0 |
| openssl | CVE-2026-28390 | HIGH | Upgrade zu 3.5.6-r0 |
| openssl | CVE-2026-28389 | HIGH | Upgrade zu 3.5.6-r0 |
| openssl | CVE-2026-28388 | HIGH | Upgrade zu 3.5.6-r0 |
| openssl | CVE-2026-2673 | HIGH | Upgrade zu 3.5.6-r0 |
| musl | CVE-2026-40200 | HIGH | Upgrade zu 1.2.5-r23 |
| nghttp2 | CVE-2026-27135 | HIGH | No fix available |
| curl | CVE-2026-3805 | HIGH | No fix available |
| curl | Multiple CVEs | MEDIUM | Multiple issues in curl 8.17.0 |

**Empfehlung:** OpenSSL und musl sollten aktualisiert werden. curl und nghttp2 haben derzeit keine Fixes.

---

## Aktionsplan

### Kurzfristig (Diese Woche)

1. **Backend Dockerfile aktualisieren**
   - OpenSSL Update in Debian
   - wheel Paket updaten
   - pip neu bauen

2. **Frontend Dockerfile aktualisieren**
   - Alpine 3.23 → Neuere Version
   - Node.js 22 auf LTS oder neuere Version
   - picomatch updaten

3. **Nginx neu bauen**
   - Alpine 3.23 → Neuere Alpine Version
   - OpenSSL updaten

### Mittelfristig (Diese Woche - nächste Woche)

4. **Docker Image Scanning automatisieren**
   - GitHub Actions Workflow erstellen
   - Docker Scout bei jedem Build laufen lassen
   - CVEs blockieren bei HIGH+ Severity

5. **Dependency Updates etablieren**
   - Regelmäßige Updates mit Renovate/Dependabot
   - Automated PR für Updates
   - CI/CD Pipeline zur Validierung

### Langfristig

6. **Zu Docker Hardened Images (DHI) migrieren**
   - Chainguard Images verwenden (zero-CVEs)
   - Beispiel: `cgr.dev/chainguard/node:22-dev`
   - Deutlich kleinere Attack Surface

---

## Empfohlene Fixes

### Backend: Dockerfile

```dockerfile
FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    iputils-ping \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
# Upgrade kritische Pakete
RUN pip install --upgrade pip wheel && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Frontend: Dockerfile

```dockerfile
FROM node:22-alpine AS builder
# Aktualisiere picomatch und Dependencies
RUN npm install -g npm@latest

WORKDIR /app
COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

FROM node:22-alpine
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY server.js .
EXPOSE 3000
CMD ["node", "server.js"]
```

### Nginx: docker-compose.yaml

```yaml
nginx:
  image: nginx:alpine  # Überprüfe auf neuere Version
  # Alternativ: nginx:latest-alpine
```

---

## Scanner-Ergebnis Referenzen

- Backend: `docker scout cves ai-autonomus-backend:latest`
- Frontend: `docker scout cves ai-autonomus-frontend:latest`
- Nginx: `docker scout cves nginx:alpine`

---

## Sicherheits-Best-Practices für Zukunft

1. **Image Scanning in CI/CD**
   - Jeden Build scannen
   - CVE-Schwellwert setzen (z.B. HIGH+ blockt Build)

2. **Regelmäßige Updates**
   - Wöchentliche oder tägliche Updates prüfen
   - Automatische PRs für Updates

3. **Minimal Images nutzen**
   - Alpine statt Debian (wo möglich)
   - Scratch/Distroless für Production
   - Docker Hardened Images (DHI) von Chainguard

4. **Non-Root User**
   - Container als Non-Root laufen lassen
   - Limitierte Capabilities

5. **Vulnerability Monitoring**
   - Docker Scout einplanen
   - Regelmäßige Audits
   - Alerts für neue CVEs

---

## Fazit

Die Anwendung hat keine CRITICAL Vulnerabilities. Die HIGH- und MEDIUM-CVEs sollten in den nächsten 1-2 Wochen behoben werden durch:

1. Base Image Updates
2. Dependency Updates
3. Regelmäßiges Scanning etablieren

Mittelfristig sollte zu Docker Hardened Images (DHI) migriert werden für maximale Sicherheit und Zero-CVEs.
