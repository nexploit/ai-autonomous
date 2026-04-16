from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import os
import sys

from agent_autogpt import AutoGPT

app = FastAPI()

# CORS Configuration für Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

agent = AutoGPT()


@app.get("/")
def root():
    return {"status": "ok", "msg": "AutoGPT läuft"}


@app.get("/ui")
def ui():
    # absoluter sicherer Pfad
    path = "/app/frontend/index.html"

    print("DEBUG CHECK PATH:", path)
    print("EXISTS:", os.path.exists(path))

    if os.path.exists(path):
        return FileResponse(path)

    return {"error": f"NOT FOUND: {path}"}

@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()

    try:
        # 🔥 Verbindung bestätigen (wichtig)
        await ws.send_text("✅ Verbunden mit AutoGPT")

        while True:
            data = await ws.receive_text()
            sys.stdout.write(f"[WS] Received message: {data}\n")
            sys.stdout.flush()

            loop = asyncio.get_event_loop()

            def run_agent():
                try:
                    sys.stdout.write(f"[EXECUTOR] Starting agent.run() with: {data}\n")
                    sys.stdout.flush()
                    result = agent.run(data)
                    sys.stdout.write(f"[EXECUTOR] agent.run() returned: {result}\n")
                    sys.stdout.flush()
                    return result
                except Exception as e:
                    sys.stdout.write(f"[EXECUTOR] Exception: {e}\n")
                    sys.stdout.flush()
                    return f"AGENT ERROR: {e}"

            try:
                result = await asyncio.wait_for(
                    loop.run_in_executor(None, run_agent),
                    timeout=120  # 120 second timeout for agent execution
                )
            except asyncio.TimeoutError:
                result = "TIMEOUT ERROR: Agent execution exceeded 60 seconds. Request aborted."
            except Exception as e:
                sys.stdout.write(f"[WS] Exception during execution: {e}\n")
                sys.stdout.flush()
                result = f"ERROR: {e}"

            sys.stdout.write(f"[WS] Sending result: {result}\n")
            sys.stdout.flush()
            await ws.send_text(str(result))

    except WebSocketDisconnect:
        pass
    except Exception as e:
        sys.stdout.write(f"WS ERROR: {e}\n")
        sys.stdout.flush()
