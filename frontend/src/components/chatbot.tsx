import React, { useState } from "react";
import { postNLQuery } from "../services/api";

interface ChatBoxProps {
  onQueryResult?: (query: any, result: any) => void;
}

export default function ChatBox({ onQueryResult }: ChatBoxProps) {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState<Array<{type: 'user' | 'bot', content: string, query?: any}>>([]);
  const [loading, setLoading] = useState(false);

  const handleSend = async () => {
    if (!input.trim() || loading) return;
    
    const userMessage = { type: 'user' as const, content: input };
    setMessages(prev => [...prev, userMessage]);
    setLoading(true);

    try {
      const response = await postNLQuery({ user_id: "demo", query: input });
      
      const botMessage = { 
        type: 'bot' as const, 
        content: `Found ${response.result?.hits?.total?.value || 0} results. ${response.explanation}`,
        query: response
      };
      
      setMessages(prev => [...prev, botMessage]);
      
      // Pass results to parent component
      if (onQueryResult) {
        onQueryResult(response, response.result);
      }
      
    } catch (error) {
      const errorMessage = { 
        type: 'bot' as const, 
        content: `Error: ${error instanceof Error ? error.message : 'Something went wrong'}` 
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setLoading(false);
      setInput("");
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const sampleQueries = [
    "Show me failed login attempts in the last 24 hours",
    "Find suspicious network activity",
    "Show authentication logs for user admin",
    "Display system errors from the past week"
  ];

  return (
    <div style={{ background: 'white', borderRadius: '8px', padding: '20px', boxShadow: '0 2px 4px rgba(0,0,0,0.1)' }}>
      <div style={{ 
        height: "300px", 
        overflowY: "auto", 
        border: "1px solid #ddd", 
        borderRadius: '4px',
        padding: '15px',
        marginBottom: '15px',
        backgroundColor: '#f9f9f9'
      }}>
        {messages.length === 0 ? (
          <div style={{ color: '#666', textAlign: 'center', marginTop: '50px' }}>
            <p>👋 Welcome to SOC Copilot!</p>
            <p>Ask me about your security logs in natural language.</p>
          </div>
        ) : (
          messages.map((msg, idx) => (
            <div key={idx} style={{ 
              marginBottom: '10px',
              padding: '10px',
              borderRadius: '8px',
              backgroundColor: msg.type === 'user' ? '#007bff' : '#e9ecef',
              color: msg.type === 'user' ? 'white' : '#333',
              marginLeft: msg.type === 'user' ? '20px' : '0',
              marginRight: msg.type === 'user' ? '0' : '20px'
            }}>
              <strong>{msg.type === 'user' ? 'You' : '🤖 SOC Copilot'}:</strong> {msg.content}
            </div>
          ))
        )}
        {loading && (
          <div style={{ textAlign: 'center', color: '#666' }}>
            <p>🔍 Analyzing your query...</p>
          </div>
        )}
      </div>

      <div style={{ display: 'flex', gap: '10px', marginBottom: '15px' }}>
        <input 
          value={input} 
          onChange={e => setInput(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Ask about your security logs..."
          style={{ 
            flex: 1, 
            padding: '10px', 
            border: '1px solid #ddd', 
            borderRadius: '4px',
            fontSize: '14px'
          }}
          disabled={loading}
        />
        <button 
          onClick={handleSend}
          disabled={loading || !input.trim()}
          style={{ 
            padding: '10px 20px', 
            backgroundColor: loading ? '#ccc' : '#007bff',
            color: 'white', 
            border: 'none', 
            borderRadius: '4px',
            cursor: loading ? 'not-allowed' : 'pointer',
            fontSize: '14px'
          }}
        >
          {loading ? 'Searching...' : 'Send'}
        </button>
      </div>

      <div>
        <p style={{ margin: '0 0 10px 0', fontSize: '14px', color: '#666' }}>Try these sample queries:</p>
        <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px' }}>
          {sampleQueries.map((query, idx) => (
            <button
              key={idx}
              onClick={() => setInput(query)}
              style={{
                padding: '5px 10px',
                backgroundColor: '#f8f9fa',
                border: '1px solid #ddd',
                borderRadius: '12px',
                fontSize: '12px',
                cursor: 'pointer',
                color: '#007bff'
              }}
            >
              {query}
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}
