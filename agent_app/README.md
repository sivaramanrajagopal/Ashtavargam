# Vedic Astrology AI Agent

A production-ready LangGraph-powered AI agent system for comprehensive Vedic astrology analysis.

## Features

- **Intelligent Routing**: Agent automatically decides which APIs to call based on user queries
- **RAG-Powered**: Uses Supabase PG Vector for context-aware interpretations
- **Multi-Source Analysis**: Combines BAV/SAV, Dasha, and Gochara data
- **Interactive Dashboard**: House-by-house analysis with tabbed interface
- **Production-Ready**: FastAPI backend with Railway deployment support

## Architecture

```
User Query
    ↓
Router Node (Analyzes Intent)
    ↓
Calculator Node (Calls APIs: BAV/SAV, Dasha, Gochara)
    ↓
RAG Retrieval Node (Queries Supabase Vector Store)
    ↓
Analysis Node (Generates Interpretation with OpenAI)
    ↓
Response Node (Formats Output)
```

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements_agent.txt
```

### 2. Configure Environment Variables

Create a `.env` file or set environment variables:

```bash
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-service-role-key
OPENAI_API_KEY=your-openai-api-key
BAV_SAV_API_URL=http://localhost:8000
DASHA_GOCHARA_API_URL=http://localhost:8001
PORT=8080
```

### 3. Set Up Supabase

Follow instructions in `setup_supabase.md` to:
- Create Supabase project
- Enable pgvector extension
- Create `vedic_knowledge` table

### 4. Populate Knowledge Base

```bash
python agent_app/knowledge/populate_knowledge_base.py
```

### 5. Run the Server

```bash
uvicorn agent_app.main:app --host 0.0.0.0 --port 8080
```

Or use the Procfile:

```bash
# Using Procfile.agent
foreman start -f Procfile.agent
```

## API Endpoints

### Health Check
```
GET /health
```

### Query Agent
```
POST /api/agent/query
Body: {
    "query": "What will happen in my 7th house?",
    "birth_data": {
        "dob": "1990-01-01",
        "tob": "10:30",
        "lat": 13.0827,
        "lon": 80.2707,
        "tz_offset": 5.5
    }
}
```

### Get Full Dashboard
```
POST /api/agent/dashboard
Body: {
    "birth_data": {
        "dob": "1990-01-01",
        "tob": "10:30",
        "lat": 13.0827,
        "lon": 80.2707,
        "tz_offset": 5.5
    }
}
```

## Agent Decision Logic

The agent intelligently routes queries:

1. **House Analysis**: Detects house-specific queries (e.g., "7th house", "marriage")
   - Calls: BAV/SAV API, Dasha API, Gochara API
   - Retrieves: House-specific knowledge

2. **Dasha Analysis**: Detects Dasha queries
   - Calls: Dasha API
   - Retrieves: Dasha interpretations

3. **Gochara Analysis**: Detects transit queries
   - Calls: Gochara API
   - Retrieves: Transit knowledge

4. **Full Dashboard**: Detects comprehensive analysis requests
   - Calls: All APIs
   - Retrieves: Comprehensive knowledge
   - Generates: All 12 houses analysis

## File Structure

```
agent_app/
├── main.py                    # FastAPI server
├── graphs/
│   └── astrology_agent_graph.py  # LangGraph agent
├── tools/
│   └── astrology_tools.py     # LangChain tools
├── rag/
│   └── supabase_rag.py        # RAG system
├── knowledge/
│   └── populate_knowledge_base.py  # Knowledge base population
└── templates/
    └── dashboard.html         # Frontend interface
```

## Deployment

See `RAILWAY_DEPLOYMENT.md` for Railway deployment instructions.

## Testing

Test the agent locally:

```bash
# Start the server
uvicorn agent_app.main:app --reload

# Test query endpoint
curl -X POST http://localhost:8080/api/agent/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What will happen in my 7th house?",
    "birth_data": {
      "dob": "1990-01-01",
      "tob": "10:30",
      "lat": 13.0827,
      "lon": 80.2707,
      "tz_offset": 5.5
    }
  }'
```

## Dependencies

- **LangChain**: Tool integration and LLM orchestration
- **LangGraph**: Agent state management and routing
- **FastAPI**: Production-ready web framework
- **Supabase**: Vector database for RAG
- **OpenAI**: LLM for interpretations

## License

Same as parent project.

