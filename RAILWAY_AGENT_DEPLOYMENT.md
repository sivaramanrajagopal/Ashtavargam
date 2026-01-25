# Railway Deployment Guide for Agentic AI App

## Overview
This guide will help you deploy the Vedic Astrology AI Agent app to Railway, including all dependencies (Supabase, OpenAI, FastAPI services).

## Prerequisites

1. **Railway Account**: Sign up at https://railway.app
2. **GitHub Repository**: Your code should be in GitHub (already done ✅)
3. **Supabase Project**: Set up Supabase for RAG (see `setup_supabase.md`)
4. **OpenAI API Key**: Get from https://platform.openai.com/api-keys
5. **BAV/SAV API**: Either deploy separately or use existing service
6. **Dasha/Gochara API**: Either deploy separately or use existing service

---

## Step 1: Set Up Supabase (If Not Done)

### 1.1 Create Supabase Project
1. Go to https://supabase.com
2. Create a new project
3. Note your:
   - **Project URL**: `https://xxxxx.supabase.co`
   - **Service Role Key**: (Settings → API → service_role key)

### 1.2 Enable pgvector Extension
1. Go to SQL Editor in Supabase
2. Run:
   ```sql
   CREATE EXTENSION IF NOT EXISTS vector;
   ```

### 1.3 Create Knowledge Base Table
Run the SQL from `agent_app/rag/supabase_rpc_setup.sql` in Supabase SQL Editor.

### 1.4 Populate Knowledge Base
```bash
# Locally, run:
cd agent_app/knowledge
python populate_knowledge_base.py
```

---

## Step 2: Deploy BAV/SAV API (If Not Already Deployed)

### Option A: Deploy as Separate Service
1. In Railway, create new service
2. Connect to your GitHub repo
3. Set root directory to: `/` (root)
4. Use `Dockerfile` (for Flask app) or create FastAPI service
5. Set environment variables:
   - `PORT=8000`
6. Deploy and note the URL: `https://bav-sav-api.railway.app`

### Option B: Use Existing Service
If you already have BAV/SAV API running, use that URL.

---

## Step 3: Deploy Dasha/Gochara API (If Not Already Deployed)

### Option A: Deploy as Separate Service
1. In Railway, create new service
2. Connect to your GitHub repo
3. Set root directory to: `/` (root)
4. Create new service with:
   - Build command: `pip install -r requirements_agent.txt`
   - Start command: `python3 -m uvicorn dasha_gochara_api:app --host 0.0.0.0 --port $PORT`
5. Set environment variables:
   - `PORT=8001`
6. Deploy and note the URL: `https://dasha-gochara-api.railway.app`

### Option B: Use Existing Service
If you already have Dasha/Gochara API running, use that URL.

---

## Step 4: Deploy Agent App to Railway

### 4.1 Create New Railway Service
1. Go to Railway dashboard: https://railway.app
2. Click **"New Project"**
3. Select **"Deploy from GitHub repo"**
4. Choose your repository: `sivaramanrajagopal/Ashtavargam`
5. Click **"Deploy Now"**

### 4.2 Configure Service Settings
1. Click on the service name
2. Go to **Settings** tab
3. Set **Root Directory**: `./` (root)
4. Set **Build Command**: (leave empty, Railway auto-detects)
5. Set **Start Command**: (leave empty, uses Procfile.agent)

### 4.3 Configure Environment Variables
Go to **Variables** tab and add:

#### Required Variables:
```bash
# Supabase Configuration
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-service-role-key-here

# OpenAI Configuration
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxx

# API URLs (use Railway service URLs or localhost for testing)
BAV_SAV_API_URL=https://your-bav-sav-api.railway.app
DASHA_GOCHARA_API_URL=https://your-dasha-gochara-api.railway.app

# Server Configuration
PORT=8080
```

#### Optional Variables:
```bash
# For debugging
LOG_LEVEL=INFO

# If using custom domains
DOMAIN=your-domain.com
```

### 4.4 Configure Build Settings
1. Railway will auto-detect `Dockerfile.agent`
2. If not detected, go to **Settings** → **Build**:
   - **Dockerfile Path**: `Dockerfile.agent`
   - **Docker Build Context**: `.`

### 4.5 Deploy
1. Railway will automatically build and deploy
2. Watch the **Deployments** tab for build logs
3. Wait for deployment to complete (usually 3-5 minutes)

---

## Step 5: Get Service URL

1. After deployment, go to **Settings** → **Networking**
2. Click **"Generate Domain"** to get a public URL
3. Your app will be available at: `https://your-app-name.railway.app`

---

## Step 6: Verify Deployment

### 6.1 Check Health
Visit: `https://your-app-name.railway.app/health`

Should return:
```json
{"status": "healthy", "version": "1.0.0"}
```

### 6.2 Test Chat Interface
1. Visit: `https://your-app-name.railway.app/chat`
2. Enter birth details
3. Start a chat session
4. Verify it connects to APIs

### 6.3 Check Logs
1. Go to **Deployments** tab
2. Click on latest deployment
3. Check **Logs** for any errors

---

## Step 7: Set Up Custom Domain (Optional)

1. Go to **Settings** → **Networking**
2. Click **"Custom Domain"**
3. Add your domain
4. Follow DNS configuration instructions
5. Wait for SSL certificate (automatic)

---

## Troubleshooting

### Issue: Build Fails
- **Check**: Dockerfile.agent exists and is correct
- **Check**: All dependencies in requirements_agent.txt
- **Solution**: Check build logs in Railway

### Issue: App Crashes on Start
- **Check**: All environment variables are set
- **Check**: API URLs are correct and accessible
- **Solution**: Check logs for specific error messages

### Issue: Cannot Connect to Supabase
- **Check**: SUPABASE_URL and SUPABASE_KEY are correct
- **Check**: Supabase project is active
- **Solution**: Verify credentials in Supabase dashboard

### Issue: OpenAI API Errors
- **Check**: OPENAI_API_KEY is valid and has credits
- **Check**: API key has proper permissions
- **Solution**: Test API key at https://platform.openai.com

### Issue: Cannot Reach BAV/SAV or Dasha/Gochara APIs
- **Check**: API URLs are correct (use Railway service URLs)
- **Check**: APIs are deployed and running
- **Check**: CORS settings allow requests from agent app
- **Solution**: Test API endpoints directly

---

## Architecture Overview

```
┌─────────────────────────────────────────┐
│     Railway Agent App (Port 8080)      │
│  - Chat Interface                       │
│  - LangGraph Agent                     │
│  - RAG System                          │
└──────────────┬──────────────────────────┘
               │
       ┌───────┴────────┐
       │             │
       ▼             ▼
┌─────────────┐  ┌──────────────┐
│  Supabase   │  │   OpenAI     │
│  (RAG DB)   │  │   (LLM)      │
└─────────────┘  └──────────────┘
       │
       │
       ▼
┌─────────────────────────────────────┐
│  External APIs (Railway Services)   │
│  - BAV/SAV API (Port 8000)          │
│  - Dasha/Gochara API (Port 8001)    │
└─────────────────────────────────────┘
```

---

## Cost Estimation

### Railway:
- **Free Tier**: $5 credit/month
- **Hobby Plan**: $20/month (if needed)
- **Agent App**: ~$5-10/month (depending on usage)

### Supabase:
- **Free Tier**: 500MB database, 2GB bandwidth
- **Pro Plan**: $25/month (if needed)

### OpenAI:
- **Pay-as-you-go**: ~$0.01-0.10 per chat session
- **Depends on**: Message length, model used

---

## Next Steps

1. ✅ Deploy all services
2. ✅ Test chat interface
3. ✅ Monitor logs for errors
4. ✅ Set up monitoring/alerts (optional)
5. ✅ Configure backups (optional)

---

## Support

- Railway Docs: https://docs.railway.app
- Supabase Docs: https://supabase.com/docs
- OpenAI Docs: https://platform.openai.com/docs

