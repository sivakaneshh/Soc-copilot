import React, { useState } from 'react';
import { generateReport } from '../services/api';

interface ReportDownloadProps {
  currentQuery?: any;
}

export default function ReportDownload({ currentQuery }: ReportDownloadProps) {
  const [isGenerating, setIsGenerating] = useState(false);
  const [reportGenerated, setReportGenerated] = useState(false);

  const handleGenerateReport = async () => {
    if (!currentQuery) {
      alert('Please run a query first to generate a report');
      return;
    }

    setIsGenerating(true);
    setReportGenerated(false);
    
    try {
      const reportData = await generateReport({
        query_ids: [currentQuery.query_id || 'current'],
        report_type: 'security_summary'
      });
      
      // Create blob and download
      const blob = new Blob([reportData], { type: 'application/pdf' });
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `soc-report-${Date.now()}.pdf`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);
      
      setReportGenerated(true);
    } catch (error) {
      console.error('Error generating report:', error);
      alert('Error generating report. Please try again.');
    } finally {
      setIsGenerating(false);
    }
  };

  const reportTypes = [
    { id: 'security_summary', name: 'Security Summary', description: 'Overview of security events and trends' },
    { id: 'incident_report', name: 'Incident Report', description: 'Detailed analysis of security incidents' },
    { id: 'compliance_report', name: 'Compliance Report', description: 'Compliance status and audit trail' }
  ];

  return (
    <div style={{ 
      background: 'white', 
      borderRadius: '8px', 
      padding: '20px', 
      boxShadow: '0 2px 4px rgba(0,0,0,0.1)' 
    }}>
      <h3>📄 Security Report Generator</h3>
      <p style={{ color: '#666', marginBottom: '20px' }}>
        Generate comprehensive security reports based on your query results.
      </p>
      
      {!currentQuery ? (
        <div style={{ 
          background: '#fff3cd', 
          border: '1px solid #ffeaa7', 
          borderRadius: '4px', 
          padding: '15px',
          marginBottom: '20px'
        }}>
          <strong>⚠️ No query data available</strong>
          <p style={{ margin: '5px 0 0 0', fontSize: '14px' }}>
            Run a search query first to generate reports with actual data.
          </p>
        </div>
      ) : (
        <div style={{ 
          background: '#d1ecf1', 
          border: '1px solid #bee5eb', 
          borderRadius: '4px', 
          padding: '15px',
          marginBottom: '20px'
        }}>
          <strong>✅ Ready to generate report</strong>
          <p style={{ margin: '5px 0 0 0', fontSize: '14px' }}>
            Found {currentQuery.result?.hits?.total?.value || 0} records for your query.
          </p>
        </div>
      )}

      <div style={{ marginBottom: '20px' }}>
        <h4 style={{ marginBottom: '15px' }}>📊 Available Report Types</h4>
        <div style={{ display: 'grid', gap: '10px' }}>
          {reportTypes.map((type) => (
            <div key={type.id} style={{
              background: '#f8f9fa',
              padding: '12px',
              borderRadius: '4px',
              border: '1px solid #e9ecef'
            }}>
              <div style={{ fontWeight: 'bold', marginBottom: '4px' }}>{type.name}</div>
              <div style={{ fontSize: '14px', color: '#666' }}>{type.description}</div>
            </div>
          ))}
        </div>
      </div>
      
      <button 
        onClick={handleGenerateReport}
        disabled={isGenerating || !currentQuery}
        style={{
          padding: '12px 24px',
          backgroundColor: isGenerating ? '#6c757d' : (!currentQuery ? '#e9ecef' : '#28a745'),
          color: !currentQuery ? '#6c757d' : 'white',
          border: 'none',
          borderRadius: '4px',
          cursor: isGenerating || !currentQuery ? 'not-allowed' : 'pointer',
          fontSize: '16px',
          fontWeight: 'bold'
        }}
      >
        {isGenerating ? '📝 Generating Report...' : '📄 Generate PDF Report'}
      </button>
      
      {reportGenerated && (
        <div style={{ 
          marginTop: '15px', 
          padding: '10px',
          background: '#d4edda',
          border: '1px solid #c3e6cb',
          borderRadius: '4px',
          color: '#155724'
        }}>
          <strong>✅ Report generated successfully!</strong>
          <p style={{ margin: '5px 0 0 0', fontSize: '14px' }}>
            Your security report has been downloaded.
          </p>
        </div>
      )}
    </div>
  );
}