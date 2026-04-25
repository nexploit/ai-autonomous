# Incident Response & History

## Häufige Netzwerk-Incidents

### Incident 1: Host-Cluster nicht erreichbar
**Szenario**: Mehrere Hosts im Subnetz 192.168.1.50-60 sind nicht erreichbar

**Ursachen gefunden**:
- Switch war down (Hardware-Fehler)
- Netzwerk-Kabel beschädigt
- VLAN-Konfiguration falsch

**Diagnose**:
1. Ping zu 192.168.1.1 (Gateway) → erfolgreich
2. Ping zu 192.168.1.100 (Working Host) → erfolgreich
3. Ping zu 192.168.1.55 (Problem-Host) → Timeout
4. Traceroute zu 192.168.1.55 → stoppt bei Gateway

**Lösung**: Switch neukonfigurieren, Kabel prüfen

---

### Incident 2: DNS-Auflösung instabil
**Szenario**: Intermittierende DNS-Fehler bei domain.local Auflösung

**Root Cause**: DNS-Cache-Poisoning

**Symptome**:
- `dns_lookup domain.local` funktioniert manchmal
- Alternative DNS (8.8.8.8) funktioniert zuverlässig
- Lokaler DNS-Service hat Memory-Leak

**Lösung**:
- Cache leeren
- DNS-Service neu starten
- Auf stabilen DNS (1.1.1.1) wechseln

---

### Incident 3: Port 443 blockiert
**Szenario**: HTTPS zu external-api.com funktioniert nicht

**Ursachen**:
- Firewall-Regel zu restriktiv
- Proxy erzwingt MITM (Man-in-the-Middle)
- Certificate-Pinning Problem

**Diagnose**:
1. `check_port external-api.com 443` → Connection timeout
2. `traceroute external-api.com` → Sichtbar bis Firewall, dann blockiert
3. `shell curl -v https://external-api.com` → TLS-Fehler

**Lösung**: Firewall-Regel anpassen, Proxy-Zertifikat installieren

---

## Learning Patterns

### Pattern 1: "Host nicht erreichbar"
Folge dieser Diagnose-Kette:
1. `ping` Host (ICMP Check)
2. `dns_lookup` hostname (DNS Check)
3. `traceroute` Host (Route Check)
4. `check_port` Host 22 (SSH Check)
5. `network_info` (lokale Prüfung)

### Pattern 2: "Service nicht verfügbar"
Prüfe in dieser Reihenfolge:
1. `network_info` (lokale Netzwerk OK?)
2. `check_port` IP Port (Port offen?)
3. `ping` Ziel (Host erreichbar?)
4. `shell netstat -an` (lokale Verbindungen?)

### Pattern 3: "Routing-Problem"
Nutze diese Tools:
1. `traceroute` Ziel (Route sichtbar?)
2. `check_port` Gateway 80 (Gateway erreichbar?)
3. `network_info` (Lokale Routen OK?)
4. `shell route print` (Routing-Tabelle)

---

## Performance-Baselines

### Typische Ping-Zeiten
- Localhost (127.0.0.1): < 1ms
- Lokales Netzwerk (192.168.x.x): 1-5ms
- ISP Gateway: 5-20ms
- Google (8.8.8.8): 10-50ms
- Internationale Server: 50-200ms

### Typische Port-Response-Zeiten
- SSH (Port 22): < 100ms
- HTTP (Port 80): 50-200ms
- HTTPS (Port 443): 50-300ms
- Custom Apps: variable, prüfen

---

## Sicherheits-Zwischenfälle

### Unnormal Hohe Verbindungszahl
`active_connections` zeigt > 1000 Verbindungen → Möglicher DDoS-Angriff
Lösung: Traffic-Filterung, Rate-Limiting

### Unerwartete offene Ports
`scan_host localhost` zeigt unbekannte Ports
Lösung: Prozesse prüfen (`shell lsof -i`), Firewall-Regel prüfen

### DNS Hijacking
`dns_lookup domain.com` gibt falsche IP zurück
Lösung: Auf vertrauenswürdigen DNS wechseln (8.8.8.8, 1.1.1.1)
