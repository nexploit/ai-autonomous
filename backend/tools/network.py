import subprocess
import socket

def get_network_info() -> dict:
    """Get local network configuration (IP, hostname, interfaces)"""
    try:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        
        return {
            "hostname": hostname,
            "local_ip": local_ip,
            "status": "success"
        }
    except Exception as e:
        return {
            "error": str(e),
            "status": "error"
        }

def dns_lookup(domain: str) -> dict:
    """Resolve domain name to IP address"""
    try:
        ip = socket.gethostbyname(domain)
        return {
            "domain": domain,
            "ip": ip,
            "status": "resolved"
        }
    except socket.gaierror as e:
        return {
            "domain": domain,
            "error": str(e),
            "status": "not_resolved"
        }
    except Exception as e:
        return {
            "domain": domain,
            "error": str(e),
            "status": "error"
        }

def traceroute_host(host: str, max_hops: int = 30) -> dict:
    """Trace route to a host"""
    try:
        result = subprocess.run(
            ["traceroute", "-m", str(max_hops), host],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        return {
            "host": host,
            "output": result.stdout if result.returncode == 0 else result.stderr,
            "status": "success" if result.returncode == 0 else "failed"
        }
    except FileNotFoundError:
        return {
            "host": host,
            "error": "traceroute command not found",
            "status": "error"
        }
    except Exception as e:
        return {
            "host": host,
            "error": str(e),
            "status": "error"
        }

def check_port(host: str, port: int, timeout: int = 5) -> dict:
    """Check if a port is open on a host"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        sock.close()
        
        is_open = result == 0
        return {
            "host": host,
            "port": port,
            "open": is_open,
            "status": "open" if is_open else "closed"
        }
    except Exception as e:
        return {
            "host": host,
            "port": port,
            "error": str(e),
            "status": "error"
        }

def get_active_connections() -> dict:
    """Get active network connections"""
    try:
        result = subprocess.run(
            ["netstat", "-tuln"],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        return {
            "output": result.stdout if result.returncode == 0 else result.stderr,
            "status": "success" if result.returncode == 0 else "failed"
        }
    except FileNotFoundError:
        return {
            "error": "netstat command not found",
            "status": "error"
        }
    except Exception as e:
        return {
            "error": str(e),
            "status": "error"
        }
