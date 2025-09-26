import axios from "axios";

const API_BASE = "http://localhost:8000";

export async function postNLQuery(data: {user_id: string, query: string}) {
    const resp = await axios.post(`${API_BASE}/converse/`, data);
    return resp.data;
}

export async function uploadLogs(file: File) {
    const formData = new FormData();
    formData.append('file', file);
    
    const resp = await axios.post(`${API_BASE}/logs/upload`, formData, {
        headers: {
            'Content-Type': 'multipart/form-data',
        },
    });
    return resp.data;
}

export async function getLogIndices() {
    const resp = await axios.get(`${API_BASE}/logs/indices`);
    return resp.data;
}

export async function createSampleData() {
    const resp = await axios.post(`${API_BASE}/logs/sample-data`);
    return resp.data;
}

export async function generateReport(data: {query_ids: string[], report_type: string}) {
    const resp = await axios.post(`${API_BASE}/reports/generate`, data, {
        responseType: 'blob'
    });
    return resp.data;
}
