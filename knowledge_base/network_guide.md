# Network Knowledge Base

## Netzwerk-Topologie

### Lokale Netzwerk-Struktur
- **Gateway**: 192.168.1.1
- **Subnetz**: 192.168.1.0/24
- **Broadcast**: 192.168.1.255
- **DHCP Range**: 192.168.1.100 - 192.168.1.254
- **DNS Server**: 8.8.8.8, 1.1.1.1 (Primary), 8.8.4.4 (Secondary)

### Häufig genutzte Hosts
- localhost: 127.0.0.1 (lokale Maschine)
- google.com: 142.251.41.14 (wichtiger Public DNS)
- cloudflare.com: 104.16.132.229 (CDN/DNS Service)

## Häufige Netzwerk-Probleme & Lösungen

### Problem: Host antwortet nicht auf Ping
**Ursachen:**
1. Host ist offline oder nicht erreichbar
2. Firewall blockiert ICMP-Pakete
3. Host antwortet nicht auf Ping (konfiguriert)
4. Netzwerk-Interface ist down
5. Routing-Problem (falsche Route)

**Diagnose-Schritte:**
1. Führe `ping` mit 4 Paketen durch
2. Überprüfe mit `traceroute` wo die Verbindung abbricht
3. Versuche `check_port` auf häufigen Ports (22, 80, 443, 3389)
4. Nutze `network_info` um lokale Konfiguration zu prüfen

### Problem: DNS-Auflösung fehlgeschlagen
**Ursachen:**
1. DNS-Server nicht erreichbar
2. Domain existiert nicht
3. Typo im Domain-Namen
4. DNS-Cache Problem
5. Netzwerk-Konnektivität unterbrochen

**Lösungen:**
- Nutze `dns_lookup` mit korrektem Domain-Namen
- Versuche alternative DNS-Server (8.8.8.8, 1.1.1.1)
- Überprüfe Netzwerk-Konnektivität mit `ping` zuerst

### Problem: Port ist nicht erreichbar
**Häufige Blockierungen:**
- Port 22 (SSH): Oft nur intern erlaubt
- Port 3389 (RDP): Windows Remote Desktop, meist blockiert
- Port 445 (SMB): Netzwerk-Freigaben, blockiert im Internet
- Port 25 (SMTP): E-Mail, meist blockiert

**Test-Ports (meist offen):**
- Port 80 (HTTP): Web
- Port 443 (HTTPS): Secure Web
- Port 8000-9000: Applikations-Ports

## Best Practices für Netzwerk-Diagnose

### Ping
- Standard: 4 Pakete
- Bei langsamer Verbindung: 2 Sekunden Timeout
- Wartet auf Antwort, sonst Timeout

### Traceroute
- Zeigt Route zu Host
- Stoppt bei blockiertem Host
- Nützlich für Routing-Probleme
- Kann bis zu 30 Hops zeigen

### Port-Checks
- Immer vom Ziel-Host aus prüfen
- Bei Firewall: von aussen und innen testen
- SSH (22), HTTP (80), HTTPS (443), RDP (3389) sind häufig getestet

### Aktive Verbindungen
- Zeigt etablierte TCP-Verbindungen
- Hilft bei Performance-Problemen
- Zeigt offene Ports auf der lokalen Maschine

## Sicherheits-Richtlinien

### Sichere Ports
- Port 22 (SSH): Nur von erlaubten Netzwerken
- Port 443 (HTTPS): Verschlüsselt, sicher
- Port 80 (HTTP): Unverschlüsselt, nur für öffentliche Daten

### Unsichere Ports (blockieren)
- Port 23 (Telnet): Unverschlüsselt, veraltet
- Port 25 (SMTP): Oft Spam-Ziel
- Port 445 (SMB): Interne Netzwerke, nicht extern

## Performance-Tuning

### Schnelle Diagnose
1. Starte mit `ping` (schnell, zeigt Konnektivität)
2. Dann `dns_lookup` (zeigt DNS-Probleme)
3. Dann `traceroute` (zeigt Route-Probleme)
4. Zuletzt `check_port` oder `scan_host` (zeigt Service-Probleme)

### Bei Problemen
- Netzwerk-Info sammeln: `network_info`
- Verbindungen prüfen: `active_connections`
- Ports scannen: `scan_host`
- Shell-Befehle ausführen: `shell`
