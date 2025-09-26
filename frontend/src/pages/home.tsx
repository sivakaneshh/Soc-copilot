import React, { useState } from 'react';
import ChatBox from '../components/chatbot';
import QueryPreview from '../components/querypreview';
import ReportDownload from '../components/reportdownload';
import ChartView from '../components/chartview';
import LogUpload from '../components/logupload';

export default function Home() {
  const [currentQuery, setCurrentQuery] = useState<any>(null);
  const [queryResult, setQueryResult] = useState<any>(null);

  const handleQueryResult = (query: any, result: any) => {
    setCurrentQuery(query);
    setQueryResult(result);
  };

  return (
    <div style={{ padding: '20px', maxWidth: '1400px', margin: '0 auto' }}>
      {/* Log Upload Section */}
      <div style={{ marginBottom: '30px' }}>
        <LogUpload onUploadSuccess={(indexName) => console.log('Logs uploaded to:', indexName)} />
      </div>

      {/* Main Dashboard */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px', marginBottom: '20px' }}>
        <div>
          <h2>🤖 Ask SOC Copilot</h2>
          <ChatBox onQueryResult={handleQueryResult} />
        </div>
        <div>
          <h2>🔍 Query Preview</h2>
          <QueryPreview currentQuery={currentQuery} />
        </div>
      </div>

      {/* Analytics Section */}
      <div style={{ marginBottom: '20px' }}>
        <ChartView queryResult={queryResult} />
      </div>

      {/* Reports Section */}
      <div>
        <h2>📄 Generate Reports</h2>
        <ReportDownload currentQuery={currentQuery} />
      </div>
    </div>
  );
}