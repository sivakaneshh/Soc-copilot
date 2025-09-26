import React from 'react';

interface QueryPreviewProps {
  currentQuery?: any;
}

export default function QueryPreview({ currentQuery }: QueryPreviewProps) {
  return (
    <div style={{ 
      background: 'white', 
      borderRadius: '8px', 
      padding: '20px', 
      boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
      height: '400px'
    }}>
      <h3>🔍 Elasticsearch DSL Query</h3>
      {currentQuery ? (
        <div>
          <div style={{ marginBottom: '15px', padding: '10px', backgroundColor: '#e3f2fd', borderRadius: '4px' }}>
            <strong>Original Query:</strong> "{currentQuery.query_id ? 'Previous query' : 'Current query'}"
            <br />
            <strong>Intent:</strong> {currentQuery.intent || 'Unknown'}
            <br />
            <strong>Query Time:</strong> {currentQuery.result?.took || 0}ms
          </div>
          <div style={{ height: '250px', overflow: 'auto' }}>
            <pre style={{ 
              background: '#f8f9fa', 
              padding: '15px', 
              borderRadius: '4px',
              fontSize: '12px',
              lineHeight: '1.4',
              margin: 0,
              border: '1px solid #e9ecef'
            }}>
              {JSON.stringify(currentQuery.dsl, null, 2)}
            </pre>
          </div>
          <div style={{ marginTop: '10px', fontSize: '12px', color: '#666' }}>
            💡 This DSL query was automatically generated from your natural language input
          </div>
        </div>
      ) : (
        <div style={{ 
          display: 'flex', 
          flexDirection: 'column',
          alignItems: 'center', 
          justifyContent: 'center',
          height: '300px',
          color: '#666',
          textAlign: 'center'
        }}>
          <div style={{ fontSize: '48px', marginBottom: '16px' }}>🔍</div>
          <p style={{ fontStyle: 'italic', marginBottom: '8px' }}>
            Your generated Elasticsearch query will appear here
          </p>
          <p style={{ fontSize: '14px', color: '#999' }}>
            Ask a question in the chat to see the DSL translation
          </p>
        </div>
      )}
    </div>
  );
}