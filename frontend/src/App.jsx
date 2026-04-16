import { useState, useEffect, useRef } from "react";
import "./App.css";

export default function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [isConnected, setIsConnected] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const wsRef = useRef(null);
  const chatEndRef = useRef(null);

  // WebSocket Connection
  useEffect(() => {
    const wsProtocol = window.location.protocol === "https:" ? "wss:" : "ws:";
    const wsUrl = `${wsProtocol}//${window.location.host}/ws`;

    const connect = () => {
      try {
        console.log("Connecting to WebSocket:", wsUrl);
        wsRef.current = new WebSocket(wsUrl);

        wsRef.current.onopen = () => {
          console.log("✓ WebSocket verbunden");
          setIsConnected(true);
          addMessage("system", "✓ Mit Backend verbunden");
        };

        wsRef.current.onmessage = (event) => {
          console.log("Message received:", event.data);
          addMessage("ai", event.data);
          setIsLoading(false);
        };

        wsRef.current.onerror = (error) => {
          console.error("WebSocket Error:", error);
          addMessage("error", "⚠️ Verbindungsfehler");
          setIsLoading(false);
        };

        wsRef.current.onclose = () => {
          console.log("WebSocket geschlossen");
          setIsConnected(false);
          // Versuche zu reconnecten
          setTimeout(connect, 3000);
        };
      } catch (error) {
        console.error("WebSocket Connection Error:", error);
        setTimeout(connect, 3000);
      }
    };

    connect();

    return () => {
      if (wsRef.current) {
        wsRef.current.close();
      }
    };
  }, []);

  // Auto-scroll to bottom
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const addMessage = (type, text) => {
    setMessages((prev) => [...prev, { type, text, id: Date.now() }]);
  };

  const handleSend = () => {
    const trimmedInput = input.trim();

    if (!trimmedInput) return;

    if (!isConnected || !wsRef.current) {
      addMessage("error", "⚠️ Nicht mit Backend verbunden");
      return;
    }

    addMessage("user", trimmedInput);
    setIsLoading(true);
    wsRef.current.send(trimmedInput);
    setInput("");
  };

  const handleKeyPress = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="app-container">
      <div className="header">
        <div className="header-content">
          <h1>🤖 AI Autonomus Agent</h1>
          <div className={`status ${isConnected ? "connected" : "disconnected"}`}>
            <span className="status-dot"></span>
            {isConnected ? "Online" : "Offline"}
          </div>
        </div>
      </div>

      <div className="chat-container">
        <div className="messages">
          {messages.length === 0 && (
            <div className="welcome-message">
              <h2>Willkommen! 👋</h2>
              <p>Geben Sie ein Ziel ein und starten Sie den autonomen Agenten.</p>
            </div>
          )}

          {messages.map((msg) => (
            <div key={msg.id} className={`message message-${msg.type}`}>
              <div className="message-content">
                <div className="message-text">{msg.text}</div>
              </div>
            </div>
          ))}

          {isLoading && (
            <div className="message message-loading">
              <div className="message-content">
                <div className="loading-spinner"></div>
                <span>Agent arbeitet...</span>
              </div>
            </div>
          )}

          <div ref={chatEndRef} />
        </div>
      </div>

      <div className="input-area">
        <div className="input-wrapper">
          <textarea
            id="msg"
            placeholder="Ziel eingeben... (Enter zum Senden, Shift+Enter für Zeilenumbruch)"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={handleKeyPress}
            className="message-input"
            disabled={isLoading || !isConnected}
          />
          <button
            onClick={handleSend}
            disabled={isLoading || !input.trim() || !isConnected}
            className="send-button"
          >
            {isLoading ? "⏳ Lädt..." : "→ Start"}
          </button>
        </div>
      </div>
    </div>
  );
}
