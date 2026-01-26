# Railway Deployment: Fix Old App vs Agent App Issue

## 🔴 Problem
Railway is deploying the **old Flask app** (`app_complete.py`) instead of the **new RAG Agent app** (`agent_app/main.py`).

**Why?** Railway detects `Procfile` first, which runs: `python app_complete.py`

---

## ✅ Solution: Configure Railway Settings

### Step 1: Go to Railway Dashboard
1. Open your Railway project
2. Select the service that should run the Agent App
3. Go to **Settings** tab

### Step 2: Configure Build Settings
1. Scroll to **Build** section
2. Set **Dockerfile Path**: `Dockerfile.agent` ⚠️ **CRITICAL**
3. Leave **Build Command** empty (or set: `pip install -r requirements_agent.txt`)

### Step 3: Configure Deploy Settings
1. Scroll to **Deploy** section
2. Set **Start Command**: 
   ```
   uvicorn agent_app.main:app --host 0.0.0.0 --port $PORT
   ```

### Step 4: Set Environment Variables
Go to **Variables** tab and add:

```bash
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-service-role-key
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxx
BAV_SAV_API_URL=https://your-bav-sav-api.railway.app
DASHA_GOCHARA_API_URL=https://your-dasha-gochara-api.railway.app
```

### Step 5: Redeploy
1. Go to **Deployments** tab
2. Click **"Redeploy"** or push a new commit
3. Verify build logs show: `Using Dockerfile.agent`

---

## 📋 Environment Variables List

### Required Variables:

| Variable Name | Description | Example |
|--------------|-------------|---------|
| `SUPABASE_URL` | Supabase project URL | `https://xxxxx.supabase.co` |
| `SUPABASE_KEY` | Supabase service role key | `eyJhbGciOiJIUzI1NiIs...` |
| `OPENAI_API_KEY` | OpenAI API key | `sk-proj-xxxxxxxxxxxxx` |
| `BAV_SAV_API_URL` | BAV/SAV API base URL | `https://bav-sav-api.railway.app` |
| `DASHA_GOCHARA_API_URL` | Dasha/Gochara API base URL | `https://dasha-gochara-api.railway.app` |
| `PORT` | Server port (Railway sets automatically) | `8080` |

### Optional Variables:

| Variable Name | Default | Description |
|--------------|---------|-------------|
| `MAX_MESSAGES` | `50` | Max messages in conversation |
| `MAX_TOKENS` | `8000` | Max tokens in context |
| `RECENT_MESSAGES_COUNT` | `10` | Recent messages to preserve |

---

## 🔗 API Endpoint Names Used in Code

The agent app uses these environment variables to construct API endpoints:

### BAV/SAV API (from `BAV_SAV_API_URL`):
- `{BAV_SAV_API_URL}/api/v1/calculate/full`
- `{BAV_SAV_API_URL}/api/v1/calculate/bav`
- `{BAV_SAV_API_URL}/api/v1/calculate/sav`
- `{BAV_SAV_API_URL}/health`

### Dasha/Gochara API (from `DASHA_GOCHARA_API_URL`):
- `{DASHA_GOCHARA_API_URL}/api/v1/dasha/current`
- `{DASHA_GOCHARA_API_URL}/api/v1/dasha/bhukti`
- `{DASHA_GOCHARA_API_URL}/api/v1/dasha/calculate`
- `{DASHA_GOCHARA_API_URL}/api/v1/gochara/current`
- `{DASHA_GOCHARA_API_URL}/api/v1/gochara/calculate`
- `{DASHA_GOCHARA_API_URL}/health`

---

## 🔍 How to Verify

### Check if Agent App is Running:
```bash
# Should show FastAPI docs
curl https://your-app.railway.app/docs

# Should return JSON health check
curl https://your-app.railway.app/health
```

**Expected Response**:
```json
{"status": "healthy", "version": "1.0.0"}
```

### Check if Old App is Running (Wrong):
```bash
curl https://your-app.railway.app/
```

**If you see**: Flask HTML page → ❌ Wrong app
**If you see**: FastAPI root or chat interface → ✅ Correct app

---

## 📁 File Comparison

| File | Old Flask App | Agent App |
|-----|--------------|-----------|
| **Procfile** | `web: python app_complete.py` | `web: uvicorn agent_app.main:app --host 0.0.0.0 --port $PORT` |
| **Dockerfile** | `Dockerfile` | `Dockerfile.agent` |
| **Entry Point** | `app_complete.py` | `agent_app/main.py` |
| **Requirements** | `requirements.txt` | `requirements_agent.txt` |
| **Port** | `5004` | `8080` |

---

## 🚀 Quick Fix Summary

1. **Railway Settings** → **Build** → Set Dockerfile: `Dockerfile.agent`
2. **Railway Settings** → **Deploy** → Set Start Command: `uvicorn agent_app.main:app --host 0.0.0.0 --port $PORT`
3. **Railway Settings** → **Variables** → Add all environment variables
4. **Redeploy** the service
5. **Verify** `/health` endpoint returns FastAPI response

---

## ⚠️ Important Notes

- Railway detects `Procfile` first, so it uses the old app
- You must **manually override** in Railway Settings
- Use `Dockerfile.agent` (not `Dockerfile`)
- Use `requirements_agent.txt` (not `requirements.txt`)
- The `railway.agent.json` file exists but Railway may not auto-detect it

---

## 📝 Complete Environment Variables Template

Copy this into Railway → Variables:

```bash
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-service-role-key-here
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxx
BAV_SAV_API_URL=https://your-bav-sav-api.railway.app
DASHA_GOCHARA_API_URL=https://your-dasha-gochara-api.railway.app
PORT=8080
MAX_MESSAGES=50
MAX_TOKENS=8000
RECENT_MESSAGES_COUNT=10
```

