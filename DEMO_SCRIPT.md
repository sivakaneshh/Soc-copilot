# 🔒 SOC Copilot - Demo Script for Presentation

## Project Overview
SOC Copilot is an AI-powered Security Operations Center assistant that allows security analysts to query security logs using natural language, which gets automatically translated to Elasticsearch queries.

## Demo Flow - "How to Use SOC Copilot"

### 1. 📁 **Log Upload - Where You Upload Your Logs**

**Location**: Top section of the main dashboard

**Steps for Demo**:
1. **Option A - Upload Real Logs**: 
   - Click the upload area or drag & drop a JSON/CSV file
   - Supported formats: JSON arrays, JSONL (one JSON per line), CSV
   - Example files you can create:
     ```json
     [
       {
         "@timestamp": "2024-01-15T10:30:00Z",
         "log_type": "authentication",
         "user": "admin",
         "source_ip": "192.168.1.100",
         "status": "failed",
         "message": "Login attempt failed"
       }
     ]
     ```

2. **Option B - Generate Sample Data** (Recommended for Demo):
   - Click "📊 Create Sample Security Logs" button
   - This generates 100 realistic logs with:
     - Authentication events (login attempts, failures)
     - Network activities (connections, traffic)
     - System events (processes, file changes)
   - Logs are automatically indexed in Elasticsearch

**What Happens**: 
- Logs are parsed and stored in Elasticsearch with proper field mappings
- You'll see the new index appear in the "Available Log Indices" section
- Ready for querying within seconds

### 2. 🤖 **Natural Language Querying - How You Search**

**Location**: Left side of main dashboard - "Ask SOC Copilot"

**Demo Queries to Try**:
```
1. "Show me failed login attempts in the last 24 hours"
2. "Find suspicious network activity" 
3. "Display authentication logs for user admin"
4. "Show system errors from the past week"
5. "List all failed login attempts from IP 192.168.1.100"
```

**What to Show**:
- Type natural language query in the chat interface
- SOC Copilot processes and responds with findings
- Shows result count and explanation
- Sample queries provided for easy demo

**Key Features to Highlight**:
- No need to know Elasticsearch syntax
- Understands security terminology
- Extracts entities (IPs, usernames, time ranges)
- Provides contextual responses

### 3. 🔍 **Query Translation - See the Magic**

**Location**: Right side of main dashboard - "Query Preview"

**What Happens**:
- Shows the generated Elasticsearch DSL query
- Displays query metadata (intent, entities, timing)
- Demonstrates AI translation capabilities

**Demo Points**:
- "This complex Elasticsearch query was generated automatically"
- "Notice how it understood the time range, log types, and conditions"
- "No technical Elasticsearch knowledge required"

### 4. 📊 **Data Visualization - Where Your Graphs Are**

**Location**: Middle section below the chat - "Data Visualization"

**What You'll See**:
- **Summary Statistics**: Total results, query time, log types
- **Log Type Distribution**: Bar chart showing breakdown by category
- **Real-time Analytics**: Updates with each query

**Demo Points**:
- Visual representation of query results
- Immediate insights into log patterns
- Security analytics at a glance

### 5. 📄 **Report Generation - Export Your Findings**

**Location**: Bottom section - "Generate Reports"

**How It Works**:
1. Run some queries to gather data
2. Click "📄 Generate PDF Report" 
3. Professional PDF report downloads automatically

**Report Contains**:
- Executive summary
- Key security findings
- Metrics and statistics
- Recommendations
- Query details

## 🎯 **Demo Script for Presentation**

### Opening (2 minutes)
"Today I'll show you SOC Copilot - an AI assistant that revolutionizes how security teams analyze logs. Instead of writing complex database queries, you simply ask questions in plain English."

### Demo Flow (8-10 minutes)

**Step 1: Data Setup** (1 minute)
1. Open http://localhost:3000
2. Click "📊 Create Sample Security Logs"
3. Show the indexed logs appearing

**Step 2: Natural Language Queries** (4 minutes)
1. Type: "Show me failed login attempts"
   - Show the results and response
   - Highlight the natural language understanding

2. Type: "Find suspicious network activity" 
   - Show different results
   - Point out the AI interpretation

3. Type: "Display authentication logs for user admin"
   - Show user-specific filtering
   - Demonstrate entity extraction

**Step 3: Technical Translation** (2 minutes)
1. Point to Query Preview panel
2. Explain: "This complex Elasticsearch query was generated automatically"
3. Show the DSL structure and complexity

**Step 4: Visual Analytics** (2 minutes)
1. Point to the charts and statistics
2. Explain: "Immediate visual insights from your queries"
3. Show log type distribution

**Step 5: Professional Reporting** (1 minute)
1. Click "Generate PDF Report"
2. Show the professional report that downloads
3. Explain: "Ready for management or compliance"

### Closing (1 minute)
"SOC Copilot transforms security operations by making log analysis accessible to everyone on your team, not just database experts."

## 🔧 **Technical Architecture Highlights**

### Frontend (React + TypeScript)
- **Log Upload**: Drag & drop interface with real-time feedback
- **Chat Interface**: Natural language input with sample queries
- **Query Preview**: Real-time DSL generation display
- **Data Visualization**: Interactive charts and statistics
- **Report Generation**: One-click PDF creation

### Backend (Python + FastAPI)
- **NLP Translation**: Advanced natural language to DSL conversion
- **Elasticsearch Integration**: Full-text search and analytics
- **Redis Caching**: Fast query result storage
- **PDF Generation**: Professional security reports
- **REST API**: Clean, documented endpoints

### Data Processing
- **Log Parsing**: Supports JSON, JSONL, CSV formats
- **Field Mapping**: Intelligent field detection and typing
- **Sample Data**: Realistic security logs for demonstration
- **Real-time Indexing**: Immediate search availability

## 🚀 **URLs for Demo**

- **Main Application**: http://localhost:3000
- **API Documentation**: http://localhost:8000/docs
- **Elasticsearch**: http://localhost:9200
- **Kibana (Advanced)**: http://localhost:5601

## 💡 **Key Selling Points**

1. **No Technical Expertise Required**: Anyone can query security logs
2. **Instant Results**: Real-time translation and search
3. **Professional Reports**: Management-ready documentation  
4. **Scalable Architecture**: Docker-based, production-ready
5. **Open Integration**: Works with existing log sources

## 🎯 **Questions You Might Get**

**Q**: "What log formats does it support?"
**A**: JSON, JSONL, CSV - most common security log formats

**Q**: "How accurate is the natural language processing?"
**A**: Handles common security queries with high accuracy, continuously learning

**Q**: "Can it scale for enterprise use?"
**A**: Yes, built on Elasticsearch which scales horizontally

**Q**: "How do we integrate with our existing SIEM?"
**A**: Can ingest from any log source, APIs available for integration

## 🔍 **Troubleshooting During Demo**

If services aren't running:
```bash
cd c:\Users\sksiv\OneDrive\Documents\GitHub\Soc-copilot
docker-compose down
docker-compose up -d
```

If frontend won't load:
- Check http://localhost:3000
- Verify all containers are running: `docker-compose ps`

If queries fail:
- Use sample data generation first
- Check Elasticsearch is healthy: http://localhost:9200/_cluster/health

---

**Good luck with your presentation! 🚀**