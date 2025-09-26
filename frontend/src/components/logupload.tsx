import React, { useState, useCallback } from 'react';
import { uploadLogs, getLogIndices, createSampleData } from '../services/api';
import './logupload.css';

interface LogIndex {
    index_name: string;
    doc_count: number;
    size_bytes: number;
}

interface LogUploadProps {
    onUploadSuccess?: (indexName: string) => void;
}

const LogUpload: React.FC<LogUploadProps> = ({ onUploadSuccess }) => {
    const [uploading, setUploading] = useState(false);
    const [indices, setIndices] = useState<LogIndex[]>([]);
    const [uploadResult, setUploadResult] = useState<string>('');
    const [dragActive, setDragActive] = useState(false);

    const handleDrag = useCallback((e: React.DragEvent) => {
        e.preventDefault();
        e.stopPropagation();
        if (e.type === "dragenter" || e.type === "dragover") {
            setDragActive(true);
        } else if (e.type === "dragleave") {
            setDragActive(false);
        }
    }, []);

    const handleDrop = useCallback((e: React.DragEvent) => {
        e.preventDefault();
        e.stopPropagation();
        setDragActive(false);
        
        if (e.dataTransfer.files && e.dataTransfer.files[0]) {
            handleFile(e.dataTransfer.files[0]);
        }
    }, []);

    const handleFileInput = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files && e.target.files[0]) {
            handleFile(e.target.files[0]);
        }
    };

    const handleFile = async (file: File) => {
        if (!file.name.endsWith('.json') && !file.name.endsWith('.csv')) {
            setUploadResult('Error: Only JSON and CSV files are supported');
            return;
        }

        setUploading(true);
        setUploadResult('');

        try {
            const result = await uploadLogs(file);
            setUploadResult(`Success: ${result.message}`);
            if (onUploadSuccess) {
                onUploadSuccess(result.index_name);
            }
            await loadIndices();
        } catch (error: any) {
            setUploadResult(`Error: ${error.response?.data?.detail || error.message}`);
        } finally {
            setUploading(false);
        }
    };

    const loadIndices = async () => {
        try {
            const data = await getLogIndices();
            setIndices(data);
        } catch (error) {
            console.error('Error loading indices:', error);
        }
    };

    const handleCreateSampleData = async () => {
        setUploading(true);
        try {
            const result = await createSampleData();
            setUploadResult(`Success: ${result.message}`);
            if (onUploadSuccess) {
                onUploadSuccess(result.index_name);
            }
            await loadIndices();
        } catch (error: any) {
            setUploadResult(`Error: ${error.response?.data?.detail || error.message}`);
        } finally {
            setUploading(false);
        }
    };

    React.useEffect(() => {
        loadIndices();
    }, []);

    const formatBytes = (bytes: number): string => {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    };

    return (
        <div className="log-upload">
            <h3>📁 Log Management</h3>
            
            <div className="upload-section">
                <div
                    className={`upload-area ${dragActive ? 'drag-active' : ''}`}
                    onDragEnter={handleDrag}
                    onDragLeave={handleDrag}
                    onDragOver={handleDrag}
                    onDrop={handleDrop}
                >
                    <div className="upload-content">
                        <div className="upload-icon">📄</div>
                        <p>Drag & drop your security logs here</p>
                        <p className="upload-subtitle">Supports JSON and CSV files</p>
                        <input
                            type="file"
                            accept=".json,.csv"
                            onChange={handleFileInput}
                            style={{ display: 'none' }}
                            id="file-input"
                        />
                        <label htmlFor="file-input" className="upload-button">
                            Choose File
                        </label>
                    </div>
                </div>

                <div className="sample-data-section">
                    <button 
                        onClick={handleCreateSampleData}
                        disabled={uploading}
                        className="sample-button"
                    >
                        📊 Create Sample Security Logs
                    </button>
                    <p className="sample-description">
                        Generate realistic sample logs for demonstration
                    </p>
                </div>

                {uploading && (
                    <div className="uploading">
                        ⏳ Processing logs...
                    </div>
                )}

                {uploadResult && (
                    <div className={`upload-result ${uploadResult.startsWith('Success') ? 'success' : 'error'}`}>
                        {uploadResult}
                    </div>
                )}
            </div>

            <div className="indices-section">
                <h4>📊 Available Log Indices</h4>
                {indices.length === 0 ? (
                    <p className="no-indices">No log indices found. Upload some logs to get started!</p>
                ) : (
                    <div className="indices-list">
                        {indices.map((index) => (
                            <div key={index.index_name} className="index-item">
                                <div className="index-name">{index.index_name}</div>
                                <div className="index-stats">
                                    📋 {index.doc_count.toLocaleString()} docs • 💾 {formatBytes(index.size_bytes)}
                                </div>
                            </div>
                        ))}
                    </div>
                )}
            </div>


        </div>
    );
};

export default LogUpload;