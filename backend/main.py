from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import sys

from agent_autogpt import AutoGPT

app = FastAPI()

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
    return {"status": "ok", "msg": "AutoGPT mit RAG läuft"}


@app.get("/health")
def health():
    if agent.rag:
        stats = agent.rag.get_stats()
        return {"status": "healthy", "agent": "ready", "rag": stats}
    return {"status": "healthy", "agent": "ready", "rag": "disabled"}


@app.get("/rag/stats")
def rag_stats():
    if not agent.rag:
        return JSONResponse(status_code=503, content={"error": "RAG not initialized"})
    return agent.rag.get_stats()


@app.post("/rag/reload")
def rag_reload():
    if not agent.rag:
        return JSONResponse(status_code=503, content={"error": "RAG not initialized"})
    try:
        count = agent.rag.ingest_documents()
        return {"status": "success", "documents_loaded": count, "stats": agent.rag.get_stats()}
    except Exception as e:
        return JSONResponse(status_code=400, content={"error": str(e)})


@app.get("/ui")
def ui():
    return JSONResponse(
        status_code=410,
        content={
            "error": "UI is served by the frontend container via nginx",
            "frontend_path": "/"
        }
    )


@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    sys.stdout.write("[WS] Client connected\n")
    sys.stdout.flush()

    try:
        await ws.send_text("✅ Verbunden mit AutoGPT+RAG")

        while True:
            try:
                data = await ws.receive_text()
                sys.stdout.write(f"[WS] Received: {data}\n")
                sys.stdout.flush()

                loop = asyncio.get_event_loop()

                def run_agent():
                    try:
                        sys.stdout.write(f"[EXECUTOR] Running agent\n")
                        sys.stdout.flush()
                        result = agent.run(data)
                        sys.stdout.write(f"[EXECUTOR] Result: {str(result)[:100]}\n")
                        sys.stdout.flush()
                        return result
                    except Exception as e:
                        sys.stdout.write(f"[EXECUTOR] Error: {e}\n")
                        sys.stdout.flush()
                        return f"AGENT ERROR: {e}"

                try:
                    result = await asyncio.wait_for(
                        loop.run_in_executor(None, run_agent),
                        timeout=300
                    )
                    sys.stdout.write(f"[WS] Got result, sending...\n")
                    sys.stdout.flush()
                except asyncio.TimeoutError:
                    result = "TIMEOUT: Agent took too long"
                    sys.stdout.write(f"[WS] Timeout\n")
                    sys.stdout.flush()
                except Exception as e:
                    result = f"ERROR: {str(e)}"
                    sys.stdout.write(f"[WS] Executor error: {e}\n")
                    sys.stdout.flush()

                # 🔥 SENDE ANTWORT
                try:
                    await ws.send_text(str(result))
                    sys.stdout.write(f"[WS] Sent to client\n")
                    sys.stdout.flush()
                except Exception as send_error:
                    sys.stdout.write(f"[WS] Failed to send: {send_error}\n")
                    sys.stdout.flush()
                    break

            except WebSocketDisconnect:
                sys.stdout.write("[WS] Client disconnected\n")
                sys.stdout.flush()
                break
            except Exception as loop_error:
                sys.stdout.write(f"[WS] Loop error: {loop_error}\n")
                sys.stdout.flush()
                break

    except Exception as e:
        sys.stdout.write(f"[WS] Handler error: {e}\n")
        sys.stdout.flush()
