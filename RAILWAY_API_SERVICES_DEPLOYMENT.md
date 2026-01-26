# Railway API Services Deployment Guide

## 🎯 Goal
Deploy two separate API services:
1. **BAV/SAV API** - For Ashtakavarga calculations
2. **Dasha/Gochara API** - For Dasha, Bhukti, and Gochara calculations

---

## 📋 Step 1: Deploy BAV/SAV API Service

### 1.1 Create New Service
1. Go to **Railway Dashboard**
2. In your **same project** (where Agent App is deployed)
3. Click **"New Service"** (or **"Add Service"**)
4. Select **"GitHub Repo"**
5. Choose your repository: **`Ashtavargam`**
6. Click **"Deploy Now"**

### 1.2 Configure Service Name
1. Click on the newly created service
2. Click **"Settings"** tab
3. Find **"Service Name"** field
4. Change it to: **`BAV SAV API`**
5. Click **"Save"** (if there's a save button)

### 1.3 Configure Build Settings
1. Still in **Settings** tab
2. Scroll to **"Build"** section
3. **Dockerfile Path**: Leave empty OR set to `Dockerfile` (the original one)
4. **Build Command**: `pip install -r requirements.txt`
5. **Root Directory**: `.` (default)

### 1.4 Configure Deploy Settings
1. Scroll to **"Deploy"** section
2. **Custom Start Command**: 
   ```
   python3 -m uvicorn api_server:app --host 0.0.0.0 --port 8080
   ```
   - Click on the field and enter this command
   - This overrides any `railway.toml` settings

### 1.5 Generate Public Domain
1. Scroll to **"Networking"** section
2. Click **"Generate Domain"** button
3. Railway will create a URL like: `bav-sav-api-production-xxxxx.up.railway.app`
4. **Copy this URL** - you'll need it for Agent App environment variables!
5. This is your **BAV/SAV API URL**

### 1.6 Wait for Deployment
1. Go to **"Deployments"** tab
2. Watch the build logs
3. Wait for deployment to complete (green checkmark ✅)
4. Should take 2-5 minutes

### 1.7 Test BAV/SAV API
1. Test health endpoint:
   ```bash
   curl https://your-bav-sav-api-url.up.railway.app/health
   ```
   Should return: `{"status": "healthy"}`

2. Test API docs:
   - Open in browser: `https://your-bav-sav-api-url.up.railway.app/docs`
   - Should show FastAPI documentation page

✅ **Step 1 Complete!** BAV/SAV API is deployed.

---

## 📋 Step 2: Deploy Dasha/Gochara API Service

### 2.1 Create New Service
1. In the **same Railway project**
2. Click **"New Service"**
3. Select **"GitHub Repo"**
4. Choose the **same repository**: **`Ashtavargam`**
5. Click **"Deploy Now"**

### 2.2 Configure Service Name
1. Click on the new service
2. **Settings** → Change name to: **`Dasha Gochara API`**

### 2.3 Configure Build Settings
1. **Settings** → **Build** section
2. **Dockerfile Path**: Leave empty
3. **Build Command**: `pip install -r requirements_agent.txt`
4. **Root Directory**: `.`

### 2.4 Configure Deploy Settings
1. **Settings** → **Deploy** section
2. **Custom Start Command**: 
   ```
   python3 -m uvicorn dasha_gochara_api:app --host 0.0.0.0 --port 8080
   ```
   - Click on the field and enter this command

### 2.5 Generate Public Domain
1. **Settings** → **Networking** section
2. Click **"Generate Domain"**
3. Railway creates URL like: `dasha-gochara-api-production-xxxxx.up.railway.app`
4. **Copy this URL** - you'll need it for Agent App environment variables!
5. This is your **Dasha/Gochara API URL**

### 2.6 Wait for Deployment
1. **Deployments** tab
2. Wait for deployment to complete ✅

### 2.7 Test Dasha/Gochara API
1. Test health endpoint:
   ```bash
   curl https://your-dasha-gochara-api-url.up.railway.app/health
   ```
   Should return: `{"status": "healthy"}`

2. Test API docs:
   - Open in browser: `https://your-dasha-gochara-api-url.up.railway.app/docs`
   - Should show FastAPI documentation page

✅ **Step 2 Complete!** Dasha/Gochara API is deployed.

---

## 📋 Step 3: Update Agent App Environment Variables

### 3.1 Go to Agent App Service
1. Click on **"Agent App"** service (the first one you deployed)
2. Go to **"Variables"** tab

### 3.2 Update API URLs
1. Find `BAV_SAV_API_URL`
2. Replace the placeholder with your actual BAV/SAV API URL (from Step 1.5)
   - Example: `https://bav-sav-api-production-xxxxx.up.railway.app`

3. Find `DASHA_GOCHARA_API_URL`
4. Replace the placeholder with your actual Dasha/Gochara API URL (from Step 2.5)
   - Example: `https://dasha-gochara-api-production-xxxxx.up.railway.app`

### 3.3 Verify All Variables
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

### 3.4 Save and Redeploy
1. Click **"Save"** or **"Update"**
2. Railway will automatically redeploy the Agent App
3. Go to **"Deployments"** tab
4. Wait for new deployment to complete ✅

✅ **Step 3 Complete!** Environment variables updated.

---

## ✅ Step 4: Final Verification

### 4.1 Test All Services

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

### 4.2 Test Agent App Web Interface
1. Open browser: `https://your-agent-app-url.up.railway.app`
2. Should see: **"🕉️ Vedic Astrology AI Agent"** page
3. Click **"Go to Chat"** or **"Go to Dashboard"**
4. Should load the interface

### 4.3 Test Agent Query (Full Integration Test)
1. In the chat interface, enter birth details:
   - DOB: `1978-09-18`
   - TOB: `17:05`
   - Place: `Chennai`
   - Latitude: `13.0827`
   - Longitude: `80.2707`
   - Timezone: `5.5`
2. Ask: **"What's my 7th house like?"**
3. Should get a response with:
   - Actual SAV/BAV data
   - Dasha information
   - Gochara (transit) data
   - AI-generated interpretation

✅ **All Services Deployed and Working!**

---

## 📊 Summary: What You Should Have

After completing all steps, you should have **3 services** in Railway:

| Service | URL | Purpose | Status |
|---------|-----|---------|--------|
| **Agent App** | `agent-app-production-xxxxx.up.railway.app` | Main web app with chat/dashboard | ✅ Running |
| **BAV/SAV API** | `bav-sav-api-production-xxxxx.up.railway.app` | Ashtakavarga calculations | ✅ Running |
| **Dasha/Gochara API** | `dasha-gochara-api-production-xxxxx.up.railway.app` | Dasha, Bhukti, Gochara calculations | ✅ Running |

---

## 🔍 Troubleshooting

### Issue: BAV/SAV API build fails
**Solution**:
- Check build logs for errors
- Verify `requirements.txt` exists
- Check that `api_server.py` exists in root directory
- Ensure Dockerfile path is correct (or empty)

### Issue: Dasha/Gochara API build fails
**Solution**:
- Check build logs for errors
- Verify `requirements_agent.txt` exists
- Check that `dasha_gochara_api.py` exists in root directory
- Verify `calculators/` directory is included

### Issue: API URLs not working in Agent App
**Solution**:
- Verify API services are deployed and running
- Check API service URLs in browser (`/health` endpoint)
- Ensure URLs use `https://` (not `http://`)
- Check environment variables are set correctly in Agent App
- Verify no typos in URLs

### Issue: Agent App can't reach APIs
**Solution**:
- Use full Railway domain URLs (not localhost)
- Ensure all services are in the same Railway project
- Check CORS is enabled in API services (should be automatic)
- Verify environment variables are saved correctly

---

## 📝 Quick Reference

### BAV/SAV API Configuration:
- **Service Name**: `BAV SAV API`
- **Dockerfile**: `Dockerfile` (or empty)
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `python3 -m uvicorn api_server:app --host 0.0.0.0 --port 8080`
- **Requirements**: `requirements.txt`

### Dasha/Gochara API Configuration:
- **Service Name**: `Dasha Gochara API`
- **Dockerfile**: (empty)
- **Build Command**: `pip install -r requirements_agent.txt`
- **Start Command**: `python3 -m uvicorn dasha_gochara_api:app --host 0.0.0.0 --port 8080`
- **Requirements**: `requirements_agent.txt`

### Agent App Configuration:
- **Service Name**: `Agent App`
- **Dockerfile**: `Dockerfile.agent`
- **Start Command**: `python -m uvicorn agent_app.main:app --host 0.0.0.0 --port 8080`
- **Requirements**: `requirements_agent.txt`
- **Environment Variables**: Must include `BAV_SAV_API_URL` and `DASHA_GOCHARA_API_URL`

---

## ✅ Deployment Checklist

- [ ] Step 1: BAV/SAV API service created
- [ ] Step 1: BAV/SAV API configured (build and deploy settings)
- [ ] Step 1: BAV/SAV API public domain generated
- [ ] Step 1: BAV/SAV API deployed and tested
- [ ] Step 2: Dasha/Gochara API service created
- [ ] Step 2: Dasha/Gochara API configured (build and deploy settings)
- [ ] Step 2: Dasha/Gochara API public domain generated
- [ ] Step 2: Dasha/Gochara API deployed and tested
- [ ] Step 3: Agent App environment variables updated with API URLs
- [ ] Step 3: Agent App redeployed
- [ ] Step 4: All services tested and working
- [ ] Step 4: Web interface accessible
- [ ] Step 4: Agent queries working with real API data

---

## 🎉 Success!

Once all steps are complete, your complete Vedic Astrology AI Agent system is fully deployed on Railway with:
- ✅ Agent App (main web interface)
- ✅ BAV/SAV API (calculations)
- ✅ Dasha/Gochara API (timing analysis)
- ✅ All services communicating correctly
- ✅ Full end-to-end functionality

