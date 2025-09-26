import axios from "axios";

const API_BASE = "http://localhost:8000";

export async function postNLQuery(data: {user_id: string, query: string}) {
    const resp = await axios.post(`${API_BASE}/converse/`, data);
    return resp.data;
}
