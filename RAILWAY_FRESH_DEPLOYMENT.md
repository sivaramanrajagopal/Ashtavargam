# Railway Fresh Deployment: Step-by-Step Guide

## 🎯 Goal
Deploy the **Agent App** and **API services** correctly, ensuring Railway uses the new agent app (not the old Flask app).

---

## 📋 Prerequisites

Before starting, ensure you have:
- ✅ GitHub repo connected to Railway
- ✅ Supabase credentials ready
- ✅ OpenAI API key ready
- ✅ All code committed to GitHub

---

## 🚀 Step 1: Deploy Agent App (Main Service)

### 1.1 Create New Service
1. Go to **Railway Dashboard**
2. Click **"New Project"** (or select existing project)
3. Click **"New Service"**
4. Select **"GitHub Repo"**
5. Choose your repository: `Ashtavargam`
6. Click **"Deploy Now"**

### 1.2 Configure Service Name
1. Click on the service (it will have a random name)
2. Click **"Settings"** tab
3. Change **Service Name** to: `Agent App` or `Vedic Astrology AI Agent`
4. Click **"Save"**

### 1.3 Configure Build Settings
1. Still in **Settings** tab
2. Scroll to **Build** section
3. Set **Dockerfile Path**: `Dockerfile.agent` ⚠️ **CRITICAL - This ensures it uses the agent app**
4. Leave **Build Command** empty (or set: `pip install -r requirements_agent.txt`)
5. **Root Directory**: `.` (default)

### 1.4 Configure Deploy Settings
1. Scroll to **Deploy** section
2. Set **Start Command**: 
   ```
   uvicorn agent_app.main:app --host 0.0.0.0 --port $PORT
   ```
3. **Restart Policy**: `ON_FAILURE` (default)

### 1.5 Generate Public Domain
1. Scroll to **Networking** section
2. Click **"Generate Domain"**
3. Railway will create a URL like: `agent-app-production-xxxxx.up.railway.app`
4. **Copy this URL** - you'll need it later
5. This is your **Agent App URL**

### 1.6 Set Environment Variables (Part 1)
1. Go to **Variables** tab
2. Add these variables (you'll complete them after creating API services):

```bash
# Supabase (you have these)
SUPABASE_URL=https://sfoobtzxdajwlbbuvttx.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InNmb29idHp4ZGFqd2lbYnV2dHR4Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2OTI0NDUwNSwiZXhwIjoyMDg0ODIwNTA1fQ.hv6N7IAAmM3FvFF_B94oMHjKDG6wXrIQ87-UTXs

# OpenAI (you have this)
OPENAI_API_KEY=sk-proj-RdMZMpyHGCOliIYvvzjLpnVVzSFrSvP3_m1dbb77zfuZsRsqlhuLlTUKg7hY71CmlsC8LF_-0TBlbkFJOnOAEBKfeisSatHmMRRejXJu426fIoT9AwKQf0-kbCrGLEx5EJz9b18A

# API URLs (will add after creating services)
BAV_SAV_API_URL=https://placeholder-will-update-later
DASHA_GOCHARA_API_URL=https://placeholder-will-update-later

# Optional: Context Management
MAX_MESSAGES=50
MAX_TOKENS=8000
RECENT_MESSAGES_COUNT=10
```

### 1.7 Deploy Agent App
1. Go to **Deployments** tab
2. Click **"Redeploy"** (or wait for auto-deploy)
3. Watch the build logs
4. Verify it shows: `Using Dockerfile.agent`
5. Wait for deployment to complete (green checkmark)

### 1.8 Verify Agent App
1. Click on the service
2. Copy the **Public Domain** URL
3. Test in browser: `https://your-agent-app-url.up.railway.app/health`
4. Should return: `{"status": "healthy", "version": "1.0.0"}`

✅ **Step 1 Complete**: Agent App is deployed!

---

## 🚀 Step 2: Deploy BAV/SAV API Service

### 2.1 Create New Service
1. In the **same Railway project**
2. Click **"New Service"**
3. Select **"GitHub Repo"**
4. Choose the **same repository**: `Ashtavargam`
5. Click **"Deploy Now"**

### 2.2 Configure Service Name
1. Click on the new service
2. **Settings** → Change name to: `BAV SAV API`

### 2.3 Configure Build Settings
1. **Settings** → **Build** section
2. **Dockerfile Path**: Leave empty or use `Dockerfile` (the original one)
3. **Build Command**: `pip install -r requirements.txt`
4. **Root Directory**: `.`

### 2.4 Configure Deploy Settings
1. **Settings** → **Deploy** section
2. **Start Command**: 
   ```
   python3 -m uvicorn api_server:app --host 0.0.0.0 --port $PORT
   ```

### 2.5 Generate Public Domain
1. **Settings** → **Networking** section
2. Click **"Generate Domain"**
3. Railway creates URL like: `bav-sav-api-production-xxxxx.up.railway.app`
4. **Copy this URL** - you'll need it for Agent App environment variables

### 2.6 Deploy BAV/SAV API
1. **Deployments** tab
2. Click **"Redeploy"** (or wait for auto-deploy)
3. Wait for deployment to complete

### 2.7 Verify BAV/SAV API
1. Test: `https://your-bav-sav-api-url.up.railway.app/health`
2. Should return: `{"status": "healthy"}`
3. Test docs: `https://your-bav-sav-api-url.up.railway.app/docs`
4. Should show FastAPI documentation

✅ **Step 2 Complete**: BAV/SAV API is deployed!

---

## 🚀 Step 3: Deploy Dasha/Gochara API Service

### 3.1 Create New Service
1. In the **same Railway project**
2. Click **"New Service"**
3. Select **"GitHub Repo"**
4. Choose the **same repository**: `Ashtavargam`
5. Click **"Deploy Now"**

### 3.2 Configure Service Name
1. Click on the new service
2. **Settings** → Change name to: `Dasha Gochara API`

### 3.3 Configure Build Settings
1. **Settings** → **Build** section
2. **Dockerfile Path**: Leave empty
3. **Build Command**: `pip install -r requirements_agent.txt`
4. **Root Directory**: `.`

### 3.4 Configure Deploy Settings
1. **Settings** → **Deploy** section
2. **Start Command**: 
   ```
   python3 -m uvicorn dasha_gochara_api:app --host 0.0.0.0 --port $PORT
   ```

### 3.5 Generate Public Domain
1. **Settings** → **Networking** section
2. Click **"Generate Domain"**
3. Railway creates URL like: `dasha-gochara-api-production-xxxxx.up.railway.app`
4. **Copy this URL** - you'll need it for Agent App environment variables

### 3.6 Deploy Dasha/Gochara API
1. **Deployments** tab
2. Click **"Redeploy"** (or wait for auto-deploy)
3. Wait for deployment to complete

### 3.7 Verify Dasha/Gochara API
1. Test: `https://your-dasha-gochara-api-url.up.railway.app/health`
2. Should return: `{"status": "healthy"}`
3. Test docs: `https://your-dasha-gochara-api-url.up.railway.app/docs`
4. Should show FastAPI documentation

✅ **Step 3 Complete**: Dasha/Gochara API is deployed!

---

## 🔗 Step 4: Update Agent App Environment Variables

### 4.1 Go to Agent App Service
1. Click on **Agent App** service
2. Go to **Variables** tab

### 4.2 Update API URLs
1. Find `BAV_SAV_API_URL`
2. Replace `https://placeholder-will-update-later` with your actual BAV/SAV API URL
3. Find `DASHA_GOCHARA_API_URL`
4. Replace `https://placeholder-will-update-later` with your actual Dasha/Gochara API URL

**Example:**
```bash
BAV_SAV_API_URL=https://bav-sav-api-production-xxxxx.up.railway.app
DASHA_GOCHARA_API_URL=https://dasha-gochara-api-production-xxxxx.up.railway.app
```

### 4.3 Verify All Variables
Make sure you have all these variables set:

```bash
SUPABASE_URL=https://sfoobtzxdajwlbbuvttx.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InNmb29idHp4ZGFqd2lbYnV2dHR4Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2OTI0NDUwNSwiZXhwIjoyMDg0ODIwNTA1fQ.hv6N7IAAmM3FvFF_B94oMHjKDG6wXrIQ87-UTXs
OPENAI_API_KEY=sk-proj-RdMZMpyHGCOliIYvvzjLpnVVzSFrSvP3_m1dbb77zfuZsRsqlhuLlTUKg7hY71CmlsC8LF_-0TBlbkFJOnOAEBKfeisSatHmMRRejXJu426fIoT9AwKQf0-kbCrGLEx5EJz9b18A
BAV_SAV_API_URL=https://bav-sav-api-production-xxxxx.up.railway.app
DASHA_GOCHARA_API_URL=https://dasha-gochara-api-production-xxxxx.up.railway.app
MAX_MESSAGES=50
MAX_TOKENS=8000
RECENT_MESSAGES_COUNT=10
```

### 4.4 Redeploy Agent App
1. Go to **Deployments** tab
2. Click **"Redeploy"**
3. Wait for deployment to complete

✅ **Step 4 Complete**: Environment variables updated!

---

## ✅ Step 5: Final Verification

### 5.1 Test All Services

#### Agent App:
```bash
curl https://your-agent-app-url.up.railway.app/health
```
Expected: `{"status": "healthy", "version": "1.0.0"}`

#### BAV/SAV API:
```bash
curl https://your-bav-sav-api-url.up.railway.app/health
```
Expected: `{"status": "healthy"}`

#### Dasha/Gochara API:
```bash
curl https://your-dasha-gochara-api-url.up.railway.app/health
```
Expected: `{"status": "healthy"}`

### 5.2 Test Agent App Web Interface
1. Open browser: `https://your-agent-app-url.up.railway.app`
2. Should see: **"🕉️ Vedic Astrology AI Agent"** page
3. Click **"Go to Chat"** or **"Go to Dashboard"**
4. Should load the chat interface or dashboard

### 5.3 Test Agent Query (Optional)
1. In the chat interface, enter birth details
2. Ask a question: "What's my 7th house like?"
3. Should get a response with actual SAV/BAV data

✅ **All Services Deployed and Working!**

---

## 📊 Service Summary

After completion, you should have **3 services** in Railway:

| Service | URL | Purpose |
|---------|-----|---------|
| **Agent App** | `agent-app-production-xxxxx.up.railway.app` | Main web app with chat/dashboard |
| **BAV/SAV API** | `bav-sav-api-production-xxxxx.up.railway.app` | Ashtakavarga calculations |
| **Dasha/Gochara API** | `dasha-gochara-api-production-xxxxx.up.railway.app` | Dasha, Bhukti, Gochara calculations |

---

## 🔍 Troubleshooting

### Issue: Agent App shows old Flask app
**Solution**: 
- Check **Settings** → **Build** → **Dockerfile Path** is set to `Dockerfile.agent`
- Check **Settings** → **Deploy** → **Start Command** is `uvicorn agent_app.main:app --host 0.0.0.0 --port $PORT`
- Redeploy

### Issue: API URLs not working
**Solution**:
- Verify API services are deployed and running
- Check API service URLs in browser (`/health` endpoint)
- Ensure URLs use `https://` (not `http://`)
- Check environment variables are set correctly in Agent App

### Issue: Build fails
**Solution**:
- Check build logs for errors
- Verify `requirements_agent.txt` exists
- Check Dockerfile paths are correct
- Ensure all dependencies are in requirements files

### Issue: Services can't communicate
**Solution**:
- Use full Railway domain URLs (not localhost)
- Ensure all services are in the same Railway project
- Check CORS is enabled in API services
- Verify environment variables are set correctly

---

## 📝 Quick Reference

### Agent App Configuration:
- **Dockerfile**: `Dockerfile.agent`
- **Start Command**: `uvicorn agent_app.main:app --host 0.0.0.0 --port $PORT`
- **Requirements**: `requirements_agent.txt`

### BAV/SAV API Configuration:
- **Dockerfile**: `Dockerfile` (or empty)
- **Start Command**: `python3 -m uvicorn api_server:app --host 0.0.0.0 --port $PORT`
- **Requirements**: `requirements.txt`

### Dasha/Gochara API Configuration:
- **Dockerfile**: (empty)
- **Start Command**: `python3 -m uvicorn dasha_gochara_api:app --host 0.0.0.0 --port $PORT`
- **Requirements**: `requirements_agent.txt`

---

## ✅ Deployment Checklist

- [ ] Step 1: Agent App service created
- [ ] Step 1: Dockerfile.agent configured
- [ ] Step 1: Start command set correctly
- [ ] Step 1: Public domain generated
- [ ] Step 1: Environment variables added (with placeholders)
- [ ] Step 1: Agent App deployed and verified
- [ ] Step 2: BAV/SAV API service created
- [ ] Step 2: Start command set correctly
- [ ] Step 2: Public domain generated
- [ ] Step 2: BAV/SAV API deployed and verified
- [ ] Step 3: Dasha/Gochara API service created
- [ ] Step 3: Start command set correctly
- [ ] Step 3: Public domain generated
- [ ] Step 3: Dasha/Gochara API deployed and verified
- [ ] Step 4: Agent App environment variables updated with real API URLs
- [ ] Step 4: Agent App redeployed
- [ ] Step 5: All services tested and working
- [ ] Step 5: Web interface accessible
- [ ] Step 5: Agent queries working

---

## 🎉 Success!

Once all steps are complete, your Vedic Astrology AI Agent app is fully deployed on Railway with:
- ✅ Agent App (main web interface)
- ✅ BAV/SAV API (calculations)
- ✅ Dasha/Gochara API (timing analysis)
- ✅ All services communicating correctly
- ✅ No old Flask app interference

