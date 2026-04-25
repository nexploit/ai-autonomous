from tools.pentest import scan_host, list_ports
from tools.ping import ping_host
from tools.network import (
    get_network_info,
    dns_lookup,
    traceroute_host,
    check_port,
    get_active_connections
)

TOOLS = {
    "scan_host": scan_host,
    "list_ports": list_ports,
    "ping": ping_host,
    "network_info": get_network_info,
    "dns_lookup": dns_lookup,
    "traceroute": traceroute_host,
    "check_port": check_port,
    "active_connections": get_active_connections,
}

def execute_tool(name, args):
    if name in TOOLS:
        return TOOLS[name](**args) if isinstance(args, dict) else TOOLS[name](args)
    return {
        "status": "error",
        "error": f"Unknown tool: {name}",
        "available_tools": sorted(TOOLS.keys())
    }
