# Railway Deployment Fix: Deploy Agent App Instead of Old Flask App

## Problem
Railway is deploying the **old Flask app** (`app_complete.py`) instead of the **new RAG Agent app** (`agent_app/main.py`).

## Root Cause
Railway detects deployment files in this order:
1. `Procfile` (exists - points to old Flask app)
2. `Dockerfile` (exists - builds old Flask app)
3. `railway.json` (may exist)

Railway is using `Procfile` which runs: `python app_complete.py` (old app)

---

## Solution: Configure Railway to Use Agent App

### Option 1: Use Railway Service Settings (Recommended)

1. Go to Railway Dashboard
2. Select your **Agent App** service (or create new service)
3. Go to **Settings** tab
4. Configure:

#### Build Settings:
- **Root Directory**: `.` (root)
- **Build Command**: `pip install -r requirements_agent.txt`
- **Dockerfile Path**: `Dockerfile.agent` ⚠️ **IMPORTANT**

#### Deploy Settings:
- **Start Command**: `uvicorn agent_app.main:app --host 0.0.0.0 --port $PORT`

OR use the `railway.agent.json` configuration file.

---

### Option 2: Rename Files (Not Recommended - breaks old app)

**Don't do this** - it will break the old Flask app deployment.

---

### Option 3: Create Separate Railway Service (Best Practice)

Deploy the agent app as a **separate service** in Railway:

1. **Create New Service** in Railway
2. **Name it**: "Agent App" or "Vedic Astrology AI Agent"
3. **Connect to same GitHub repo**
4. **Configure**:
   - Root Directory: `.`
   - Dockerfile: `Dockerfile.agent`
   - Start Command: `uvicorn agent_app.main:app --host 0.0.0.0 --port $PORT`

---

## Required Environment Variables

### For Agent App Service:

```bash
# Supabase (Required)
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-service-role-key

# OpenAI (Required)
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxx

# API Endpoints (Required)
BAV_SAV_API_URL=https://your-bav-sav-api.railway.app
DASHA_GOCHARA_API_URL=https://your-dasha-gochara-api.railway.app

# Server (Railway sets automatically, but can override)
PORT=8080

# Optional: Context Management
MAX_MESSAGES=50
MAX_TOKENS=8000
RECENT_MESSAGES_COUNT=10
```

---

## API Endpoint Names Reference

### Environment Variable Names:
- `BAV_SAV_API_URL` - Base URL for BAV/SAV API
- `DASHA_GOCHARA_API_URL` - Base URL for Dasha/Gochara API
- `SUPABASE_URL` - Supabase project URL
- `SUPABASE_KEY` - Supabase service role key
- `OPENAI_API_KEY` - OpenAI API key

### BAV/SAV API Endpoints (used by agent):
- `POST {BAV_SAV_API_URL}/api/v1/calculate/full` - Full calculation
- `POST {BAV_SAV_API_URL}/api/v1/calculate/bav` - BAV only
- `POST {BAV_SAV_API_URL}/api/v1/calculate/sav` - SAV only
- `GET {BAV_SAV_API_URL}/health` - Health check

### Dasha/Gochara API Endpoints (used by agent):
- `POST {DASHA_GOCHARA_API_URL}/api/v1/dasha/current` - Current Dasha
- `POST {DASHA_GOCHARA_API_URL}/api/v1/dasha/bhukti` - Dasha-Bhukti table
- `POST {DASHA_GOCHARA_API_URL}/api/v1/dasha/calculate` - Full Dasha
- `POST {DASHA_GOCHARA_API_URL}/api/v1/gochara/current` - Current transits
- `POST {DASHA_GOCHARA_API_URL}/api/v1/gochara/calculate` - Transits for date
- `GET {DASHA_GOCHARA_API_URL}/health` - Health check

---

## Step-by-Step Fix

### Step 1: Check Current Deployment
1. Go to Railway Dashboard
2. Check which service is active
3. Look at **Settings** → **Deploy** → **Start Command**
4. If it shows `python app_complete.py`, it's deploying the old app

### Step 2: Update Service Configuration
1. Go to **Settings** → **Build**
2. Set **Dockerfile Path**: `Dockerfile.agent`
3. Go to **Settings** → **Deploy**
4. Set **Start Command**: `uvicorn agent_app.main:app --host 0.0.0.0 --port $PORT`

### Step 3: Set Environment Variables
Go to **Variables** tab and add all required variables (see above).

### Step 4: Redeploy
1. Go to **Deployments** tab
2. Click **"Redeploy"** or push a new commit
3. Watch build logs to verify it's using `Dockerfile.agent`

### Step 5: Verify
1. Visit your Railway URL
2. Should see: "🕉️ Vedic Astrology AI Agent" (not the old Flask app)
3. Visit `/chat` endpoint - should show chat interface
4. Visit `/health` - should return FastAPI health check

---

## Verification Queries

### Check if Agent App is Running:
```bash
# Should return FastAPI docs
curl https://your-app.railway.app/docs

# Should return health check
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

**If you see**: Flask app HTML (old app) ❌
**If you see**: FastAPI root page or chat interface ✅

---

## Railway Configuration File

The `railway.agent.json` file should help Railway detect the agent app:

```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS",
    "buildCommand": "pip install -r requirements_agent.txt"
  },
  "deploy": {
    "startCommand": "uvicorn agent_app.main:app --host 0.0.0.0 --port $PORT",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

**Note**: Railway may not auto-detect this. You need to manually configure in Settings.

---

## Quick Fix Checklist

- [ ] Create separate Railway service for Agent App
- [ ] Set Dockerfile Path to `Dockerfile.agent`
- [ ] Set Start Command to `uvicorn agent_app.main:app --host 0.0.0.0 --port $PORT`
- [ ] Set all environment variables
- [ ] Redeploy service
- [ ] Verify `/health` endpoint returns FastAPI response
- [ ] Verify `/chat` endpoint shows chat interface
- [ ] Test agent query endpoint

---

## Why This Happens

Railway's detection priority:
1. `Procfile` (exists - old Flask app) ← **Currently using this**
2. `Dockerfile` (exists - old Flask app)
3. `railway.json` or `railway.agent.json`
4. Auto-detection

Since `Procfile` exists and points to `app_complete.py`, Railway uses it.

**Solution**: Override in Railway Settings to use `Dockerfile.agent` and custom start command.

---

## Alternative: Use Railway CLI

```bash
# Install Railway CLI
npm i -g @railway/cli

# Login
railway login

# Link to your project
railway link

# Set service variables
railway variables set SUPABASE_URL=https://...
railway variables set SUPABASE_KEY=...
railway variables set OPENAI_API_KEY=...
railway variables set BAV_SAV_API_URL=https://...
railway variables set DASHA_GOCHARA_API_URL=https://...

# Deploy with specific Dockerfile
railway up --dockerfile Dockerfile.agent
```

