import React, { useState } from 'react';

export default function ReportDownload() {
  const [isGenerating, setIsGenerating] = useState(false);
  const [downloadLink, setDownloadLink] = useState<string | null>(null);

  const handleGenerateReport = async () => {
    setIsGenerating(true);
    try {
      const response = await fetch('http://localhost:8000/reports/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ user_id: 'demo', query_ids: [] }),
      });
      const data = await response.json();
      setDownloadLink(data.download_link);
    } catch (error) {
      console.error('Error generating report:', error);
    } finally {
      setIsGenerating(false);
    }
  };

  return (
    <div style={{ border: '1px solid #ccc', padding: '15px', borderRadius: '5px' }}>
      <h3>Security Report Generator</h3>
      <p>Generate comprehensive security reports based on your queries.</p>
      
      <button 
        onClick={handleGenerateReport}
        disabled={isGenerating}
        style={{
          padding: '10px 20px',
          backgroundColor: isGenerating ? '#ccc' : '#007bff',
          color: 'white',
          border: 'none',
          borderRadius: '5px',
          cursor: isGenerating ? 'not-allowed' : 'pointer'
        }}
      >
        {isGenerating ? 'Generating...' : 'Generate Report'}
      </button>
      
      {downloadLink && (
        <div style={{ marginTop: '10px' }}>
          <a 
            href={downloadLink} 
            download
            style={{ color: '#007bff', textDecoration: 'underline' }}
          >
            Download Report
          </a>
        </div>
      )}
    </div>
  );
}