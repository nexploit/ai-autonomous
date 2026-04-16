from tools.pentest import scan_host, list_ports

def execute(step):
    step = step.lower()

    if "scan" in step:
        return scan_host("localhost")

    if "ports" in step:
        return list_ports()

    return "kein tool matched"