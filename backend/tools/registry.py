from tools.pentest import scan_host, list_ports
from tools.ping import ping_host
from tools.network import (
    get_network_info,
    dns_lookup,
    traceroute_host,
    check_port,
    get_active_connections
)
import subprocess

def run_shell(cmd):
    return subprocess.getoutput(cmd)

TOOLS = {
    "scan_host": scan_host,
    "list_ports": list_ports,
    "shell": run_shell,
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
    return "Unknown tool"
