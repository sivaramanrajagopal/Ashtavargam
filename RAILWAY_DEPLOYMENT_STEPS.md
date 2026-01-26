# Railway Deployment: Step-by-Step Action Guide

## 🎯 What You Need to Do

Follow these steps in order to deploy your Agent App and API services on Railway.

---

## 📋 Step 1: Deploy Agent App (Main Service)

### 1.1 Go to Railway Dashboard
1. Open https://railway.app
2. Login to your account
3. You should see your project (or create a new one)

### 1.2 Create Agent App Service
1. Click **"New Service"** (or **"Add Service"**)
2. Select **"GitHub Repo"**
3. Choose your repository: **`Ashtavargam`**
4. Click **"Deploy Now"**

### 1.3 Configure Service Name
1. Click on the newly created service
2. Click **"Settings"** tab (top right)
3. Find **"Service Name"** field
4. Change it to: **`Agent App`**
5. Click **"Save"** (if there's a save button)

### 1.4 Verify Build Configuration
1. Still in **Settings** tab
2. Scroll to **"Build"** section
3. Check **"Dockerfile Path"** - should show: **`Dockerfile.agent`**
   - If it doesn't, manually set it to: `Dockerfile.agent`
4. **Build Command** can be empty (or: `pip install -r requirements_agent.txt`)

### 1.5 Verify Deploy Configuration
1. Scroll to **"Deploy"** section
2. Check **"Custom Start Command"** - should show:
   ```
   uvicorn agent_app.main:app --host 0.0.0.0 --port $PORT
   ```
   - If it shows `python app_complete.py`, click on it and change it
   - The value comes from `railway.toml` (which we just updated)

### 1.6 Generate Public Domain
1. Scroll to **"Networking"** section
2. Click **"Generate Domain"** button
3. Railway will create a URL like: `agent-app-production-xxxxx.up.railway.app`
4. **Copy this URL** - you'll need it later!
5. This is your **Agent App URL**

### 1.7 Set Environment Variables (Part 1)
1. Click **"Variables"** tab (top menu)
2. Click **"New Variable"** or **"Raw Editor"**
3. Add these variables (you'll complete API URLs later):

```bash
SUPABASE_URL=https://sfoobtzxdajwlbbuvttx.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InNmb29idHp4ZGFqd2lbYnV2dHR4Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2OTI0NDUwNSwiZXhwIjoyMDg0ODIwNTA1fQ.hv6N7IAAmM3FvFF_B94oMHjKDG6wXrIQ87-UTXs
OPENAI_API_KEY=sk-proj-RdMZMpyHGCOliIYvvzjLpnVVzSFrSvP3_m1dbb77zfuZsRsqlhuLlTUKg7hY71CmlsC8LF_-0TBlbkFJOnOAEBKfeisSatHmMRRejXJu426fIoT9AwKQf0-kbCrGLEx5EJz9b18A
BAV_SAV_API_URL=https://placeholder-update-after-step-2
DASHA_GOCHARA_API_URL=https://placeholder-update-after-step-3
MAX_MESSAGES=50
MAX_TOKENS=8000
RECENT_MESSAGES_COUNT=10
```

4. Click **"Save"** or **"Update"**

### 1.8 Wait for Deployment
1. Go to **"Deployments"** tab
2. Watch the build logs
3. Wait for deployment to complete (green checkmark ✅)
4. Should take 2-5 minutes

### 1.9 Test Agent App
1. Copy your Agent App URL (from Step 1.6)
2. Open in browser: `https://your-agent-app-url.up.railway.app/health`
3. Should return: `{"status": "healthy", "version": "1.0.0"}`
4. If you see Flask HTML → something is wrong, check Step 1.5

✅ **Step 1 Complete!** Agent App is deployed.

---

## 📋 Step 2: Deploy BAV/SAV API Service

### 2.1 Create New Service
1. In the **same Railway project**
2. Click **"New Service"** (or **"Add Service"**)
3. Select **"GitHub Repo"**
4. Choose the **same repository**: **`Ashtavargam`**
5. Click **"Deploy Now"**

### 2.2 Configure Service Name
1. Click on the new service
2. **Settings** → Change name to: **`BAV SAV API`**

### 2.3 Configure Build Settings
1. **Settings** → **Build** section
2. **Dockerfile Path**: Leave empty OR set to `Dockerfile` (the original one)
3. **Build Command**: `pip install -r requirements.txt`

### 2.4 Configure Deploy Settings
1. **Settings** → **Deploy** section
2. **Custom Start Command**: 
   ```
   python3 -m uvicorn api_server:app --host 0.0.0.0 --port $PORT
   ```
   - Click on the field and enter this command

### 2.5 Generate Public Domain
1. **Settings** → **Networking** section
2. Click **"Generate Domain"**
3. Railway creates URL like: `bav-sav-api-production-xxxxx.up.railway.app`
4. **Copy this URL** - you'll need it in Step 4!

### 2.6 Wait for Deployment
1. **Deployments** tab
2. Wait for deployment to complete ✅

### 2.7 Test BAV/SAV API
1. Test: `https://your-bav-sav-api-url.up.railway.app/health`
2. Should return: `{"status": "healthy"}`
3. Test docs: `https://your-bav-sav-api-url.up.railway.app/docs`
4. Should show FastAPI documentation page

✅ **Step 2 Complete!** BAV/SAV API is deployed.

---

## 📋 Step 3: Deploy Dasha/Gochara API Service

### 3.1 Create New Service
1. In the **same Railway project**
2. Click **"New Service"**
3. Select **"GitHub Repo"**
4. Choose **`Ashtavargam`**
5. Click **"Deploy Now"**

### 3.2 Configure Service Name
1. Click on the new service
2. **Settings** → Change name to: **`Dasha Gochara API`**

### 3.3 Configure Build Settings
1. **Settings** → **Build** section
2. **Dockerfile Path**: Leave empty
3. **Build Command**: `pip install -r requirements_agent.txt`

### 3.4 Configure Deploy Settings
1. **Settings** → **Deploy** section
2. **Custom Start Command**: 
   ```
   python3 -m uvicorn dasha_gochara_api:app --host 0.0.0.0 --port $PORT
   ```

### 3.5 Generate Public Domain
1. **Settings** → **Networking** section
2. Click **"Generate Domain"**
3. Railway creates URL like: `dasha-gochara-api-production-xxxxx.up.railway.app`
4. **Copy this URL** - you'll need it in Step 4!

### 3.6 Wait for Deployment
1. **Deployments** tab
2. Wait for deployment to complete ✅

### 3.7 Test Dasha/Gochara API
1. Test: `https://your-dasha-gochara-api-url.up.railway.app/health`
2. Should return: `{"status": "healthy"}`
3. Test docs: `https://your-dasha-gochara-api-url.up.railway.app/docs`

✅ **Step 3 Complete!** Dasha/Gochara API is deployed.

---

## 📋 Step 4: Update Agent App Environment Variables

### 4.1 Go to Agent App Service
1. Click on **"Agent App"** service (from Step 1)
2. Go to **"Variables"** tab

### 4.2 Update API URLs
1. Find `BAV_SAV_API_URL`
2. Replace `https://placeholder-update-after-step-2` with your actual BAV/SAV API URL (from Step 2.5)
3. Find `DASHA_GOCHARA_API_URL`
4. Replace `https://placeholder-update-after-step-3` with your actual Dasha/Gochara API URL (from Step 3.5)

**Example:**
```bash
BAV_SAV_API_URL=https://bav-sav-api-production-xxxxx.up.railway.app
DASHA_GOCHARA_API_URL=https://dasha-gochara-api-production-xxxxx.up.railway.app
```

### 4.3 Save Variables
1. Click **"Save"** or **"Update"**
2. Railway will automatically redeploy the Agent App

### 4.4 Wait for Redeployment
1. Go to **"Deployments"** tab
2. Wait for new deployment to complete ✅

✅ **Step 4 Complete!** Environment variables updated.

---

## 📋 Step 5: Final Verification

### 5.1 Test All Services

#### Agent App:
```bash
# Open in browser or use curl
https://your-agent-app-url.up.railway.app/health
```
Expected: `{"status": "healthy", "version": "1.0.0"}`

#### BAV/SAV API:
```bash
https://your-bav-sav-api-url.up.railway.app/health
```
Expected: `{"status": "healthy"}`

#### Dasha/Gochara API:
```bash
https://your-dasha-gochara-api-url.up.railway.app/health
```
Expected: `{"status": "healthy"}`

### 5.2 Test Agent App Web Interface
1. Open browser: `https://your-agent-app-url.up.railway.app`
2. Should see: **"🕉️ Vedic Astrology AI Agent"** page
3. Click **"Go to Chat"** or **"Go to Dashboard"**
4. Should load the interface

### 5.3 Test Agent Query (Optional)
1. In the chat interface, enter birth details:
   - DOB: `1978-09-18`
   - TOB: `17:05`
   - Place: `Chennai`
   - Latitude: `13.0827`
   - Longitude: `80.2707`
   - Timezone: `5.5`
2. Ask: **"What's my 7th house like?"**
3. Should get a response with actual SAV/BAV data

✅ **All Services Deployed and Working!**

---

## 📊 Summary: What You Should Have

After completing all steps, you should have **3 services** in Railway:

| Service | URL | Status |
|---------|-----|--------|
| **Agent App** | `agent-app-production-xxxxx.up.railway.app` | ✅ Running |
| **BAV/SAV API** | `bav-sav-api-production-xxxxx.up.railway.app` | ✅ Running |
| **Dasha/Gochara API** | `dasha-gochara-api-production-xxxxx.up.railway.app` | ✅ Running |

---

## 🔍 Troubleshooting

### Issue: Agent App shows old Flask app
**Solution**: 
- Check **Settings** → **Deploy** → **Custom Start Command**
- Should be: `uvicorn agent_app.main:app --host 0.0.0.0 --port $PORT`
- If wrong, update it and redeploy

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

### Issue: Services can't communicate
**Solution**:
- Use full Railway domain URLs (not localhost)
- Ensure all services are in the same Railway project
- Check environment variables are set correctly

---

## ✅ Quick Checklist

- [ ] Step 1: Agent App service created and deployed
- [ ] Step 1: Environment variables added (with placeholders)
- [ ] Step 2: BAV/SAV API service created and deployed
- [ ] Step 2: BAV/SAV API URL copied
- [ ] Step 3: Dasha/Gochara API service created and deployed
- [ ] Step 3: Dasha/Gochara API URL copied
- [ ] Step 4: Agent App environment variables updated with real API URLs
- [ ] Step 4: Agent App redeployed
- [ ] Step 5: All services tested and working
- [ ] Step 5: Web interface accessible
- [ ] Step 5: Agent queries working

---

## 🎉 Success!

Once all steps are complete, your Vedic Astrology AI Agent app is fully deployed and ready to use!

