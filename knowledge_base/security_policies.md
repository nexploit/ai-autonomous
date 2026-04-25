# Security & Access Control Policies

## Network Access Rules

### External Access (Outbound)
- **Port 80 (HTTP)**: Allowed to Internet
- **Port 443 (HTTPS)**: Allowed to Internet
- **Port 53 (DNS)**: Allowed to 8.8.8.8, 1.1.1.1
- **Port 123 (NTP)**: Allowed for time sync
- **All other ports**: Blocked by default

### Internal Access (192.168.1.0/24)
- **Port 22 (SSH)**: Allowed within subnet
- **Port 3306 (MySQL)**: Allowed only from specific hosts
- **Port 5432 (PostgreSQL)**: Allowed only from specific hosts
- **Port 27017 (MongoDB)**: Allowed only from specific hosts
- **ICMP (Ping)**: Allowed (diagnostic)

### Administrative Access
- **Port 3389 (RDP)**: Only from admin subnet (192.168.1.100-110)
- **Port 8000-9000 (App Ports)**: Restricted to internal network
- **Port 22 (SSH)**: SSH Keys required, no password auth

## Data Sensitivity Levels

### Level 1: Public Data
- DNS Resolutions
- Ping/ICMP responses
- Public HTTP/HTTPS traffic
- No encryption required for logging

### Level 2: Internal Data
- Network topology information
- Port scan results
- Active connection states
- IP addresses and hostnames
- Should be logged securely

### Level 3: Sensitive Data
- Credentials (SSH keys, passwords)
- PII (Personal Identifiable Information)
- Financial data
- Medical records
- **NEVER** log or transmit unencrypted

## Audit & Logging

### What to Log
- Tool execution (name, args, timestamp)
- Query results (redacted of sensitive data)
- Errors and exceptions
- Authentication attempts
- Access to knowledge base

### What NOT to Log
- Plaintext passwords or tokens
- SSH private keys
- Personal data (SSN, credit cards, etc.)
- Internal IP ranges (in public logs)

### Log Retention
- Daily logs: 30 days
- Monthly archives: 1 year
- Security incidents: 7 years

## Tool-Specific Security

### ping Tool
- **Risk**: Can be used for network reconnaissance
- **Mitigation**: Log all ping requests
- **Safe Usage**: Only to known hosts

### traceroute Tool
- **Risk**: Reveals network topology
- **Mitigation**: Restrict to internal networks
- **Safe Usage**: Only for troubleshooting

### port_scan/scan_host Tool
- **Risk**: Can be used for attacking
- **Mitigation**: Rate limiting, restrict to specific ports
- **Safe Usage**: Only on authorized hosts

### shell Tool
- **Risk**: Arbitrary code execution
- **Mitigation**: Restrict to trusted users, whitelist commands
- **Allowed Commands**: Common diagnostic tools only

## Compliance Requirements

### GDPR (if in EU)
- No personal data in network logs
- Right to be forgotten
- Data portability

### PCI DSS (if handling payment data)
- Encrypt all network traffic
- Strong access control
- Regular security testing

### HIPAA (if in healthcare)
- Encrypt health information
- Audit logs for all access
- 2-factor authentication

## Best Practices

### Principle of Least Privilege
- Only allow necessary ports/tools
- Restrict by source IP when possible
- Use firewall rules for enforcement

### Defense in Depth
- Multiple layers of security
- Firewall + WAF + IDS/IPS
- Network segmentation

### Regular Audits
- Review access logs weekly
- Security scans monthly
- Penetration testing annually

### Incident Response
- Document all security incidents
- Notify stakeholders within 24 hours
- Post-incident review (lessons learned)
