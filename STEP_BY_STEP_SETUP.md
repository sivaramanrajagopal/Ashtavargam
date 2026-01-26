# Step-by-Step Setup Guide for Vedic Astrology AI Agent

Follow these steps in order to get your agentic system up and running.

## Prerequisites Checklist

Before starting, ensure you have:
- [ ] Python 3.9+ installed
- [ ] Supabase account (free tier works)
- [ ] OpenAI API key
- [ ] BAV/SAV API running (port 8000) or Railway URL
- [ ] Dasha/Gochara API running (port 8001) or Railway URL

---

## Step 1: Set Up Supabase (15-20 minutes)

### 1.1 Create Supabase Project

1. Go to https://supabase.com
2. Sign up or log in
3. Click "New Project"
4. Fill in:
   - **Name**: `vedic-astrology-rag` (or any name)
   - **Database Password**: Create a strong password (save it!)
   - **Region**: Choose closest to you
   - **Pricing Plan**: Free tier is fine
5. Click "Create new project"
6. Wait 2-3 minutes for project to initialize

### 1.2 Enable pgvector Extension

1. In your Supabase project, go to **SQL Editor** (left sidebar)
2. Click "New query"
3. Paste this SQL:

```sql
-- Enable pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;
```

4. Click "Run" (or press Ctrl+Enter)
5. You should see "Success. No rows returned"

### 1.3 Create Knowledge Base Table

1. Still in SQL Editor, create a new query
2. Paste this SQL:

```sql
-- Create vedic_knowledge table
CREATE TABLE vedic_knowledge (
    id BIGSERIAL PRIMARY KEY,
    content TEXT NOT NULL,
    embedding vector(1536),  -- OpenAI text-embedding-3-small dimension
    metadata JSONB,
    category VARCHAR(50),  -- 'dasha', 'gochara', 'bav_sav', 'house', 'remedy', 'general'
    house_number INTEGER,  -- 1-12 if house-specific (NULL if not)
    planet VARCHAR(20),   -- If planet-specific (NULL if not)
    created_at TIMESTAMP DEFAULT NOW()
);

-- Create index for vector similarity search
CREATE INDEX vedic_knowledge_embedding_idx 
ON vedic_knowledge 
USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);

-- Create indexes for filtering
CREATE INDEX vedic_knowledge_category_idx ON vedic_knowledge(category);
CREATE INDEX vedic_knowledge_house_idx ON vedic_knowledge(house_number);
CREATE INDEX vedic_knowledge_planet_idx ON vedic_knowledge(planet);
```

3. Click "Run"
4. You should see "Success. No rows returned"

### 1.4 Get Supabase Credentials

1. Go to **Settings** (gear icon, left sidebar)
2. Click **API**
3. Copy these values (you'll need them in Step 2):
   - **Project URL**: `https://xxxxx.supabase.co`
   - **service_role key**: (the secret key, not the anon key)

**⚠️ Important**: Keep the service_role key secret! Don't commit it to Git.

---

## Step 2: Install Dependencies (5 minutes)

### 2.1 Install Python Packages

Open terminal in your project directory and run:

```bash
cd /Users/sivaramanrajagopal/Ashtavargam
pip install -r requirements_agent.txt
```

If you get permission errors, use:
```bash
pip install --user -r requirements_agent.txt
```

Or use a virtual environment (recommended):
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements_agent.txt
```

### 2.2 Verify Installation

```bash
python3 -c "import langchain, langgraph, fastapi, supabase, openai; print('✅ All packages installed')"
```

---

## Step 3: Configure Environment Variables (5 minutes)

### 3.1 Create .env File

Create a file named `.env` in the project root:

```bash
cd /Users/sivaramanrajagopal/Ashtavargam
touch .env
```

### 3.2 Add Environment Variables

Open `.env` and add:

```bash
# Supabase Configuration
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_KEY=your-service-role-key-here

# OpenAI Configuration
OPENAI_API_KEY=sk-your-openai-key-here

# API URLs (use localhost for local testing, Railway URLs for production)
BAV_SAV_API_URL=http://localhost:8000
DASHA_GOCHARA_API_URL=http://localhost:8001

# Server Configuration
PORT=8080
```

**Replace:**
- `your-project-id.supabase.co` with your actual Supabase URL
- `your-service-role-key-here` with your actual Supabase service_role key
- `sk-your-openai-key-here` with your actual OpenAI API key

### 3.3 Get OpenAI API Key

1. Go to https://platform.openai.com
2. Sign up or log in
3. Go to **API Keys** (left sidebar)
4. Click "Create new secret key"
5. Copy the key (starts with `sk-`)
6. Paste it in your `.env` file

**⚠️ Important**: Add `.env` to `.gitignore` to keep secrets safe!

---

## Step 4: Populate Knowledge Base (10-15 minutes)

### 4.1 Run Population Script

```bash
cd /Users/sivaramanrajagopal/Ashtavargam
python3 agent_app/knowledge/populate_knowledge_base.py
```

You should see output like:
```
Initializing RAG system...
Populating House Significations...
  ✓ Stored House 1 (Lagna / Ascendant)
  ✓ Stored House 2 (Dhana / Wealth)
  ...
Populating Dasha Interpretations...
  ✓ Stored Sun Dasha
  ...
Populating Advanced Ashtakavarga Rules...
  ✓ Stored Advanced Rule (House 1)
  ...
✅ Knowledge base population completed!
```

### 4.2 Verify in Supabase

1. Go to Supabase dashboard
2. Click **Table Editor** (left sidebar)
3. Select `vedic_knowledge` table
4. You should see rows with content, category, etc.

**Expected**: ~100+ rows (12 houses + 9 dashas + 4 gochara + 5 bav_sav + 5 remedies + 59 advanced rules)

---

## Step 5: Start the APIs (If Not Running)

### 5.1 Start BAV/SAV API (Terminal 1)

```bash
cd /Users/sivaramanrajagopal/Ashtavargam
# In a new terminal window
uvicorn api_server:app --host 0.0.0.0 --port 8000
```

### 5.2 Start Dasha/Gochara API (Terminal 2)

```bash
cd /Users/sivaramanrajagopal/Ashtavargam
# In another new terminal window
uvicorn dasha_gochara_api:app --host 0.0.0.0 --port 8001
```

**Note**: If these are already running on Railway, skip this step and use Railway URLs in `.env`.

---

## Step 6: Start the Agent Server (5 minutes)

### 6.1 Start FastAPI Server

```bash
cd /Users/sivaramanrajagopal/Ashtavargam
uvicorn agent_app.main:app --host 0.0.0.0 --port 8080 --reload
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8080
INFO:     Application startup complete.
```

### 6.2 Verify Server is Running

Open browser and go to:
- http://localhost:8080 (should show dashboard)
- http://localhost:8080/health (should show `{"status":"healthy",...}`)
- http://localhost:8080/docs (FastAPI Swagger UI)

---

## Step 7: Test the Agent (10 minutes)

### 7.1 Test via Browser

1. Open http://localhost:8080
2. Fill in birth details:
   - DOB: `1990-01-01`
   - TOB: `10:30`
   - Place: `Chennai`
   - Lat: `13.0827`
   - Lon: `80.2707`
   - Timezone: `5.5`
3. Enter query: `"What will happen in my 7th house?"`
4. Click "Ask Agent"
5. Wait for response (may take 10-30 seconds)

### 7.2 Test via API (Optional)

```bash
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

### 7.3 Test Full Dashboard

1. In browser, click "Get Full Dashboard"
2. Wait for analysis (may take 30-60 seconds)
3. You should see tabbed interface with all 12 houses

---

## Step 8: Deploy to Railway (Optional, 20-30 minutes)

### 8.1 Prepare for Deployment

1. Ensure `.env` is in `.gitignore`:
   ```bash
   echo ".env" >> .gitignore
   ```

2. Commit your code:
   ```bash
   git add .
   git commit -m "Add LangGraph agentic system"
   git push
   ```

### 8.2 Create Railway Project

1. Go to https://railway.app
2. Sign up or log in
3. Click "New Project"
4. Select "Deploy from GitHub repo"
5. Select your `Ashtavargam` repository
6. Railway will detect the project

### 8.3 Configure Railway

1. In Railway project, go to **Settings**
2. Set **Root Directory**: `/` (or leave default)
3. Set **Build Command**: `pip install -r requirements_agent.txt`
4. Set **Start Command**: `uvicorn agent_app.main:app --host 0.0.0.0 --port $PORT`

### 8.4 Add Environment Variables

In Railway project, go to **Variables** tab and add:

```
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_KEY=your-service-role-key
OPENAI_API_KEY=sk-your-openai-key
BAV_SAV_API_URL=https://your-bav-sav-api.railway.app
DASHA_GOCHARA_API_URL=https://your-dasha-gochara-api.railway.app
PORT=8080
```

### 8.5 Deploy

1. Railway will automatically deploy on push
2. Or click "Deploy" button
3. Wait for build to complete (2-5 minutes)
4. Get your Railway URL (e.g., `https://your-app.railway.app`)

### 8.6 Populate Knowledge Base on Railway

You have two options:

**Option A: Run locally pointing to production Supabase**
```bash
# Use production Supabase credentials in .env
python3 agent_app/knowledge/populate_knowledge_base.py
```

**Option B: SSH into Railway and run**
```bash
# In Railway, go to your service → Connect → SSH
# Then run the population script
```

---

## Troubleshooting

### Issue: "Supabase connection failed"
- ✅ Check SUPABASE_URL and SUPABASE_KEY in `.env`
- ✅ Verify Supabase project is active
- ✅ Check if table `vedic_knowledge` exists

### Issue: "OpenAI API error"
- ✅ Check OPENAI_API_KEY is correct
- ✅ Verify you have API credits
- ✅ Check rate limits

### Issue: "API connection failed"
- ✅ Verify BAV/SAV API is running on port 8000
- ✅ Verify Dasha/Gochara API is running on port 8001
- ✅ Check API URLs in `.env`

### Issue: "No knowledge retrieved"
- ✅ Run `populate_knowledge_base.py` again
- ✅ Check Supabase table has rows
- ✅ Verify embeddings were generated

### Issue: "Import errors"
- ✅ Run `pip install -r requirements_agent.txt` again
- ✅ Check Python version (3.9+)
- ✅ Use virtual environment

---

## Next Steps After Setup

1. **Test with Real Data**: Use actual birth charts
2. **Monitor Performance**: Check response times
3. **Add More Knowledge**: Expand knowledge base as needed
4. **Optimize Queries**: Fine-tune RAG retrieval
5. **Scale**: Upgrade Supabase/OpenAI if needed

---

## Quick Reference Commands

```bash
# Start all services locally
# Terminal 1: BAV/SAV API
uvicorn api_server:app --port 8000

# Terminal 2: Dasha/Gochara API  
uvicorn dasha_gochara_api:app --port 8001

# Terminal 3: Agent Server
uvicorn agent_app.main:app --port 8080 --reload

# Populate knowledge base
python3 agent_app/knowledge/populate_knowledge_base.py

# Test health
curl http://localhost:8080/health
```

---

## Support

If you encounter issues:
1. Check logs in terminal
2. Verify environment variables
3. Test each component individually
4. Check Supabase dashboard for data
5. Review Railway logs if deployed

Good luck! 🚀

