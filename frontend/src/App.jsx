import { useState, useEffect, useRef } from "react";
import "./App.css";

export default function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [isConnected, setIsConnected] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const wsRef = useRef(null);
  const chatEndRef = useRef(null);
  const reconnectTimeoutRef = useRef(null);
  const messageIdRef = useRef(0);

  const formatMessageText = (value) => {
    if (typeof value !== "string") {
      try {
        return JSON.stringify(value, null, 2);
      } catch {
        return String(value);
      }
    }

    const trimmed = value.trim();
    if (!trimmed) return "";

    try {
      const parsed = JSON.parse(trimmed);
      if (typeof parsed === "string") {
        return parsed;
      }
      return JSON.stringify(parsed, null, 2);
    } catch {
      return value;
    }
  };

  useEffect(() => {
    const wsProtocol = window.location.protocol === "https:" ? "wss:" : "ws:";
    const wsUrl = `${wsProtocol}//${window.location.host}/ws`;

    const connect = () => {
      try {
        console.log("Connecting to WebSocket:", wsUrl);
        wsRef.current = new WebSocket(wsUrl);

        wsRef.current.onopen = () => {
          console.log("WebSocket connected");
          setIsConnected(true);
          addMessage("system", "Link to backend established.");
        };

        wsRef.current.onmessage = (event) => {
          console.log("Message received:", event.data);
          addMessage("ai", event.data);
          setIsLoading(false);
        };

        wsRef.current.onerror = (error) => {
          console.error("WebSocket error:", error);
          addMessage("error", "Connection fault detected.");
          setIsLoading(false);
        };

        wsRef.current.onclose = () => {
          console.log("WebSocket closed");
          setIsConnected(false);
          setIsLoading(false);
          reconnectTimeoutRef.current = setTimeout(connect, 3000);
        };
      } catch (error) {
        console.error("WebSocket connection error:", error);
        reconnectTimeoutRef.current = setTimeout(connect, 3000);
      }
    };

    connect();

    return () => {
      if (wsRef.current) {
        wsRef.current.close();
      }
      if (reconnectTimeoutRef.current) {
        clearTimeout(reconnectTimeoutRef.current);
      }
    };
  }, []);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const addMessage = (type, text) => {
    messageIdRef.current += 1;
    setMessages((prev) => [
      ...prev,
      {
        type,
        text: formatMessageText(text),
        id: `msg-${Date.now()}-${messageIdRef.current}`,
      },
    ]);
  };

  const handleSend = () => {
    const trimmedInput = input.trim();

    if (!trimmedInput) return;

    if (!isConnected || !wsRef.current) {
      addMessage("error", "No active backend link.");
      return;
    }

    addMessage("user", trimmedInput);
    setIsLoading(true);

    try {
      wsRef.current.send(trimmedInput);
      setInput("");
      console.log("Message sent to backend");
    } catch (error) {
      console.error("Failed to send message:", error);
      setIsLoading(false);
      addMessage("error", "Transmission failed.");
    }
  };

  const handleKeyPress = (event) => {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      handleSend();
    }
  };

  const statusLabel = isConnected ? "LINK STABLE" : "LINK LOST";
  const messageCount = messages.length.toString().padStart(2, "0");

  return (
    <div className="app-container">
      <div className="screen-effects" aria-hidden="true" />

      <header className="header">
        <div className="header-content">
          <div className="title-block">
            <p className="eyebrow">SEEGSON COMMUNICATION GRID</p>
            <h1>MU/TH/UR // AUTONOMOUS AGENT</h1>
            <p className="subline">NOSTROMO INTERFACE EMULATION</p>
          </div>

          <div className="header-panels">
            <div className="metric-panel">
              <span className="metric-label">UPLINK</span>
              <strong className="metric-value">{statusLabel}</strong>
            </div>
            <div
              className={`status ${isConnected ? "connected" : "disconnected"}`}
            >
              <span className="status-dot"></span>
              {isConnected ? "ONLINE" : "OFFLINE"}
            </div>
          </div>
        </div>
      </header>

      <main className="chat-shell">
        <aside className="system-column">
          <section className="panel panel-primary">
            <span className="panel-label">SYSTEM PROFILE</span>
            <div className="panel-grid">
              <div>
                <span className="grid-label">UNIT</span>
                <strong>MU/TH/UR</strong>
              </div>
              <div>
                <span className="grid-label">SESSION</span>
                <strong>{messageCount}</strong>
              </div>
              <div>
                <span className="grid-label">MODE</span>
                <strong>AUTONOMOUS</strong>
              </div>
              <div>
                <span className="grid-label">CHANNEL</span>
                <strong>{isConnected ? "SYNCHRONIZED" : "STANDBY"}</strong>
              </div>
            </div>
          </section>

          <section className="panel">
            <span className="panel-label">DIRECTIVES</span>
            <ul className="directive-list">
              <li>Transmit objective to initiate the agent cycle.</li>
              <li>Use Shift plus Enter for multiline command blocks.</li>
              <li>Responses return through the live command channel.</li>
            </ul>
          </section>
        </aside>

        <section className="chat-container">
          <div className="messages">
            {messages.length === 0 && (
              <div className="welcome-message panel">
                <span className="panel-label">BOOT SEQUENCE</span>
                <h2>INTERFACE READY</h2>
                <p>
                  Define a mission parameter and the system will begin autonomous
                  execution.
                </p>
              </div>
            )}

            {messages.map((msg) => (
              <div key={msg.id} className={`message message-${msg.type}`}>
                <div className="message-content">
                  <div className="message-tag">{msg.type}</div>
                  <div className="message-text">{msg.text}</div>
                </div>
              </div>
            ))}

            {isLoading && (
              <div className="message message-loading">
                <div className="message-content">
                  <div className="loading-spinner"></div>
                  <span>EXECUTING TASK ROUTINE // STANDBY</span>
                </div>
              </div>
            )}

            <div ref={chatEndRef} />
          </div>
        </section>
      </main>

      <div className="input-area">
        <div className="input-wrapper">
          <div className="input-panel">
            <label className="input-label" htmlFor="msg">
              COMMAND LINE
            </label>
            <textarea
              id="msg"
              placeholder="Enter mission objective... [Enter = send / Shift+Enter = newline]"
              value={input}
              onChange={(event) => setInput(event.target.value)}
              onKeyPress={handleKeyPress}
              className="message-input"
              disabled={isLoading || !isConnected}
            />
          </div>
          <button
            onClick={handleSend}
            disabled={isLoading || !input.trim() || !isConnected}
            className="send-button"
          >
            {isLoading ? "PROCESSING" : "EXECUTE"}
          </button>
        </div>
      </div>
    </div>
  );
}
