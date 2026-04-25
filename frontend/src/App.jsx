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

  // WebSocket Connection mit Keep-Alive
  useEffect(() => {
    const wsProtocol = window.location.protocol === "https:" ? "wss:" : "ws:";
    const wsUrl = `${wsProtocol}//${window.location.host}/ws`;

    const connect = () => {
      try {
        console.log("Connecting to WebSocket:", wsUrl);
        wsRef.current = new WebSocket(wsUrl);

        // 🔥 NO TIMEOUT - Browser kümmert sich selbst darum
        wsRef.current.onopen = () => {
          console.log("✓ WebSocket verbunden");
          setIsConnected(true);
          addMessage("system", "✓ Mit Backend verbunden");
        };

        wsRef.current.onmessage = (event) => {
          console.log("Message received:", event.data);
          addMessage("ai", event.data);
          setIsLoading(false);  // Stop loading spinner
        };

        wsRef.current.onerror = (error) => {
          console.error("WebSocket Error:", error);
          addMessage("error", "⚠️ Verbindungsfehler");
          setIsLoading(false);
        };

        wsRef.current.onclose = () => {
          console.log("WebSocket geschlossen");
          setIsConnected(false);
          setIsLoading(false);
          // Reconnect nach 3s
          reconnectTimeoutRef.current = setTimeout(connect, 3000);
        };
      } catch (error) {
        console.error("WebSocket Connection Error:", error);
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

  // Auto-scroll to bottom
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
      addMessage("error", "⚠️ Nicht mit Backend verbunden");
      return;
    }

    // Send user message
    addMessage("user", trimmedInput);
    setIsLoading(true);
    
    // Send to backend - NO TIMEOUT HERE
    try {
      wsRef.current.send(trimmedInput);
      setInput("");
      console.log("Message sent to backend");
    } catch (error) {
      console.error("Failed to send message:", error);
      setIsLoading(false);
      addMessage("error", "⚠️ Nachricht konnte nicht gesendet werden");
    }
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
                <span>Agent arbeitet... (kann 10-30 Sekunden dauern)</span>
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
