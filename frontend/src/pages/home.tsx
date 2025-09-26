import React from 'react';
import ChatBox from '../components/chatbot';
import QueryPreview from '../components/querypreview';
import ReportDownload from '../components/reportdownload';

export default function Home() {
  return (
    <div style={{ padding: '20px', maxWidth: '1200px', margin: '0 auto' }}>
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px', marginBottom: '20px' }}>
        <div>
          <h2>Ask SOC Copilot</h2>
          <ChatBox />
        </div>
        <div>
          <h2>Query Preview</h2>
          <QueryPreview />
        </div>
      </div>
      <div>
        <h2>Generate Reports</h2>
        <ReportDownload />
      </div>
    </div>
  );
}