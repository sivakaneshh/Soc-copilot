import React from 'react';

interface ChartViewProps {
  data?: any[];
  title?: string;
}

export default function ChartView({ data = [], title = "Security Analytics" }: ChartViewProps) {
  return (
    <div style={{ border: '1px solid #ccc', padding: '15px', borderRadius: '5px', height: '300px' }}>
      <h3>{title}</h3>
      {data.length > 0 ? (
        <div style={{ height: '250px', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
          <p>Chart visualization will be implemented here</p>
        </div>
      ) : (
        <div style={{ height: '250px', display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#666' }}>
          <p>No data available for visualization</p>
        </div>
      )}
    </div>
  );
}