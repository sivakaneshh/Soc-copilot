import React, { useState } from "react";
import { postNLQuery } from "../services/api";

export default function ChatBox() {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState<string[]>([]);

  const handleSend = async () => {
    if (!input) return;
    setMessages([...messages, `You: ${input}`]);
    const response = await postNLQuery({ user_id: "demo", query: input });
    setMessages([...messages, `You: ${input}`, `SOC Copilot: ${response.explanation}`]);
    setInput("");
  };

  return (
    <div>
      <div style={{ height: "300px", overflowY: "scroll", border: "1px solid gray" }}>
        {messages.map((msg, idx) => <div key={idx}>{msg}</div>)}
      </div>
      <input value={input} onChange={e => setInput(e.target.value)} placeholder="Type query..." />
      <button onClick={handleSend}>Send</button>
    </div>
  );
}
