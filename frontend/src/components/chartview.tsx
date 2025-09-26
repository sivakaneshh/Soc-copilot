import React, { useEffect, useState } from 'react';

interface ChartData {
    name: string;
    value: number;
    color: string;
}

interface ChartViewProps {
    queryResult?: any;
}

const ChartView: React.FC<ChartViewProps> = ({ queryResult }) => {
    const [chartData, setChartData] = useState<ChartData[]>([]);
    const [totalLogs, setTotalLogs] = useState(0);

    useEffect(() => {
        if (queryResult && queryResult.hits) {
            processQueryResults(queryResult);
        }
    }, [queryResult]);

    const processQueryResults = (result: any) => {
        const hits = result.hits.hits || [];
        setTotalLogs(result.hits.total?.value || hits.length);

        // Analyze log types
        const logTypeCounts: { [key: string]: number } = {};

        hits.forEach((hit: any) => {
            const source = hit._source;
            
            // Count by log type
            const logType = source.log_type || 'unknown';
            logTypeCounts[logType] = (logTypeCounts[logType] || 0) + 1;
        });

        // Prepare chart data
        const logTypeData = Object.entries(logTypeCounts).map(([name, value]) => ({
            name,
            value,
            color: getColorForLogType(name)
        }));

        setChartData(logTypeData);
    };

    const getColorForLogType = (logType: string): string => {
        const colors: { [key: string]: string } = {
            'authentication': '#ff6b6b',
            'network': '#4ecdc4',
            'system': '#45b7d1',
            'security': '#f9ca24',
            'error': '#ff4757',
            'unknown': '#747d8c'
        };
        return colors[logType] || '#95a5a6';
    };

    const renderBarChart = (data: ChartData[]) => {
        if (!data.length) return null;

        const maxValue = Math.max(...data.map(d => d.value));
        
        return (
            <div style={{ background: '#f8f9fa', padding: '20px', borderRadius: '8px' }}>
                <h4>📊 Log Types Distribution</h4>
                <div style={{ marginTop: '16px' }}>
                    {data.map((item, index) => (
                        <div key={index} style={{ display: 'flex', alignItems: 'center', marginBottom: '12px' }}>
                            <div style={{ width: '120px', fontSize: '14px', textTransform: 'capitalize' }}>{item.name}</div>
                            <div style={{ flex: 1, background: '#e9ecef', borderRadius: '4px', height: '24px', position: 'relative' }}>
                                <div 
                                    style={{
                                        width: `${(item.value / maxValue) * 100}%`,
                                        backgroundColor: item.color,
                                        height: '100%',
                                        borderRadius: '4px',
                                        display: 'flex',
                                        alignItems: 'center',
                                        justifyContent: 'flex-end',
                                        paddingRight: '8px',
                                        minWidth: '30px'
                                    }}
                                >
                                    <span style={{ color: 'white', fontSize: '12px', fontWeight: 'bold', textShadow: '1px 1px 1px rgba(0,0,0,0.5)' }}>{item.value}</span>
                                </div>
                            </div>
                        </div>
                    ))}
                </div>
            </div>
        );
    };

    const renderSummaryStats = () => {
        if (!queryResult) return null;

        const hits = queryResult.hits?.hits || [];
        const queryTime = queryResult.took || 0;

        return (
            <div style={{ background: '#f8f9fa', padding: '20px', borderRadius: '8px' }}>
                <h4>📈 Query Summary</h4>
                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(150px, 1fr))', gap: '20px', marginTop: '16px' }}>
                    <div style={{ textAlign: 'center', background: 'white', padding: '20px', borderRadius: '8px', boxShadow: '0 1px 3px rgba(0,0,0,0.1)' }}>
                        <div style={{ fontSize: '24px', fontWeight: 'bold', color: '#007bff', marginBottom: '8px' }}>{totalLogs.toLocaleString()}</div>
                        <div style={{ color: '#666', fontSize: '14px' }}>Total Results</div>
                    </div>
                    <div style={{ textAlign: 'center', background: 'white', padding: '20px', borderRadius: '8px', boxShadow: '0 1px 3px rgba(0,0,0,0.1)' }}>
                        <div style={{ fontSize: '24px', fontWeight: 'bold', color: '#007bff', marginBottom: '8px' }}>{queryTime}ms</div>
                        <div style={{ color: '#666', fontSize: '14px' }}>Query Time</div>
                    </div>
                    <div style={{ textAlign: 'center', background: 'white', padding: '20px', borderRadius: '8px', boxShadow: '0 1px 3px rgba(0,0,0,0.1)' }}>
                        <div style={{ fontSize: '24px', fontWeight: 'bold', color: '#007bff', marginBottom: '8px' }}>{hits.length}</div>
                        <div style={{ color: '#666', fontSize: '14px' }}>Displayed</div>
                    </div>
                    <div style={{ textAlign: 'center', background: 'white', padding: '20px', borderRadius: '8px', boxShadow: '0 1px 3px rgba(0,0,0,0.1)' }}>
                        <div style={{ fontSize: '24px', fontWeight: 'bold', color: '#007bff', marginBottom: '8px' }}>{chartData.length}</div>
                        <div style={{ color: '#666', fontSize: '14px' }}>Log Types</div>
                    </div>
                </div>
            </div>
        );
    };

    return (
        <div style={{ background: 'white', borderRadius: '8px', padding: '20px', boxShadow: '0 2px 4px rgba(0,0,0,0.1)' }}>
            <h3>📊 Data Visualization</h3>
            {!queryResult ? (
                <div style={{ textAlign: 'center', padding: '40px', color: '#666' }}>
                    <p>🔍 Run a query to see visualizations and analytics</p>
                    <p style={{ fontSize: '14px', color: '#999' }}>Charts will show log distribution, trends, and summary statistics</p>
                </div>
            ) : (
                <div style={{ display: 'flex', flexDirection: 'column', gap: '30px' }}>
                    {renderSummaryStats()}
                    {renderBarChart(chartData)}
                </div>
            )}


        </div>
    );
};

export default ChartView;