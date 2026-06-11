# SOC Copilot

> AI-powered Security Operations Center assistant (vibecoded prototype).

This repository contains a prototype SOC assistant with a FastAPI backend and a React frontend. It includes local development and Docker-based configurations to run the full stack (Elasticsearch + Redis + Kibana) and now uses Elasticsearch retrieval plus a Hugging Face text-generation model for RAG answers.

## Contents

- `backend/` — FastAPI app, Python dependencies in `backend/requirements.txt`.
- `frontend/` — React app, Node dependencies in `frontend/package.json`.
- `docker-compose.yml` — Development/devstack with `backend`, `frontend`, `redis`, `elasticsearch`, and `kibana` services.
- `demo/` — sample logs for experimenting.

## Quick start (recommended)

Run the full stack (backend, frontend, and required services) with Docker Compose:

```bash
docker-compose up --build
```

Open the frontend at: http://localhost:3000
The backend API is available at: http://localhost:8000 (health: `/health`).

## Local development

### Backend (Python / FastAPI)

Prereqs: Python 3.11+, pip

From the project root:

```bash
cd backend
python -m venv .venv
source .venv/Scripts/activate    # Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The backend exposes routers under `/converse`, `/reports`, and `/logs` and a health endpoint at `/health`.

### Frontend (React)

Prereqs: Node.js (16+) and npm or yarn

From the project root:

```bash
cd frontend
npm install
npm start
```

This launches the React dev server on http://localhost:3000 and proxies calls to the backend configured in the frontend code.

## Docker (service notes)

- The `backend` service is defined in `backend/Dockerfile` and runs `uvicorn app.main:app --reload --host 0.0.0.0 --port 8000`.
- `docker-compose.yml` wires `redis` and `elasticsearch` and exposes Kibana on port 5601.
- Persistent uploads are mounted from `./uploads` into the backend container.

## Configuration

- Environment variables used by Docker Compose: `ELASTICSEARCH_URL`, `REDIS_URL` (set in `docker-compose.yml`).
- RAG / Hugging Face variables: `HF_TOKEN`, `HF_MODEL_ID`, and `HF_FALLBACK_MODEL_ID`. Set `HF_TOKEN` to a valid Hugging Face access token and override `HF_MODEL_ID` only with a model that is available through an enabled Hugging Face provider. If your chosen model is not supported, the backend falls back to `HF_FALLBACK_MODEL_ID`.
- For local development, create a `.env` file in `backend/` if you need to store secrets or service URLs and load them with `python-dotenv`. Docker Compose also reads `backend/.env` for the backend service.

## How the RAG flow works

1. The chat endpoint converts the user question into Elasticsearch DSL.
2. Elasticsearch returns the most relevant log hits.
3. The backend formats those hits into a compact evidence block.
4. That evidence block is sent to the Hugging Face inference API together with the user question.
5. The model returns a grounded answer that the UI shows alongside the raw query results.

## Contributing

1. Create a branch for your work.
2. Run the stack locally (see Quick start or Local development).
3. Keep commits small and focused; update this README with any stack changes.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
