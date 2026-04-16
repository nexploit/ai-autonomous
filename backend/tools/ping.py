import subprocess
import json

def ping_host(host: str, count: int = 4) -> dict:
    """
    Ping a host and return the result as JSON
    """
    try:
        result = subprocess.run(
            ["ping", "-c", str(count), host],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        output = result.stdout if result.returncode == 0 else result.stderr
        
        return {
            "success": result.returncode == 0,
            "host": host,
            "count": count,
            "output": output,
            "status": "reachable" if result.returncode == 0 else "unreachable"
        }
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "host": host,
            "error": "Ping timeout",
            "status": "timeout"
        }
    except Exception as e:
        return {
            "success": False,
            "host": host,
            "error": str(e),
            "status": "error"
        }
