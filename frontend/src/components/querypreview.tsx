import React, { useState } from 'react';

export default function QueryPreview() {
  const [dslQuery, setDslQuery] = useState<any>(null);

  return (
    <div style={{ border: '1px solid #ccc', padding: '15px', borderRadius: '5px', height: '300px' }}>
      <h3>Elasticsearch DSL Query Preview</h3>
      {dslQuery ? (
        <pre style={{ background: '#f5f5f5', padding: '10px', overflow: 'auto', fontSize: '12px' }}>
          {JSON.stringify(dslQuery, null, 2)}
        </pre>
      ) : (
        <p style={{ color: '#666', fontStyle: 'italic' }}>
          Your generated Elasticsearch query will appear here
        </p>
      )}
    </div>
  );
}