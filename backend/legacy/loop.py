import time
from db import get_tasks, close_task
from orchestrator import run

def loop():
    while True:
        tasks = get_tasks()

        for tid, task in tasks:
            print("Running:", task)
            run(task)
            close_task(tid)

        time.sleep(10)