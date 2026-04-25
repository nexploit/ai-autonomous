from agents.planner import plan
from agents.executor import execute
from agents.critic import critic
from db import save

def run(goal):
    steps = plan(goal)
    results = []

    for s in steps:
        r = execute(s)
        c = critic(s, r)

        results.append({"step": s, "result": r, "review": c})

    save("goal", goal)
    save("result", str(results))

    return results