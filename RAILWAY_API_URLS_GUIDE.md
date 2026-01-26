# How to Get API URLs from Railway

## Your Current Service
- **Agent App URL**: `web-production-6dac6.up.railway.app`

---

## Option 1: APIs Deployed as Separate Services (Recommended)

If you have **separate Railway services** for BAV/SAV API and Dasha/Gochara API:

### Step 1: Get Service URLs
1. Go to Railway Dashboard
2. You should see **multiple services** in your project:
   - **Agent App** (your current service)
   - **BAV/SAV API** (separate service)
   - **Dasha/Gochara API** (separate service)

3. For each service:
   - Click on the service
   - Go to **Settings** → **Networking**
   - Click **"Generate Domain"** (if not already generated)
   - Copy the URL (e.g., `bav-sav-api-production-xxxxx.up.railway.app`)

### Step 2: Use These URLs in Environment Variables

In your **Agent App** service, set:

```bash
BAV_SAV_API_URL=https://bav-sav-api-production-xxxxx.up.railway.app
DASHA_GOCHARA_API_URL=https://dasha-gochara-api-production-xxxxx.up.railway.app
```

---

## Option 2: APIs Not Yet Deployed (Need to Deploy)

If you don't have separate services yet, you need to deploy them:

### Deploy BAV/SAV API Service

1. **Create New Service** in Railway
2. **Name it**: "BAV SAV API" or "Ashtakavarga API"
3. **Connect to same GitHub repo**
4. **Configure**:
   - **Root Directory**: `.`
   - **Dockerfile Path**: (use existing `Dockerfile` or create one)
   - **Start Command**: `python3 -m uvicorn api_server:app --host 0.0.0.0 --port $PORT`
   - **Port**: Railway will set automatically
5. **Get URL**: Settings → Networking → Generate Domain
6. **Note the URL**: `https://bav-sav-api-production-xxxxx.up.railway.app`

### Deploy Dasha/Gochara API Service

1. **Create New Service** in Railway
2. **Name it**: "Dasha Gochara API"
3. **Connect to same GitHub repo**
4. **Configure**:
   - **Root Directory**: `.`
   - **Build Command**: `pip install -r requirements_agent.txt`
   - **Start Command**: `python3 -m uvicorn dasha_gochara_api:app --host 0.0.0.0 --port $PORT`
5. **Get URL**: Settings → Networking → Generate Domain
6. **Note the URL**: `https://dasha-gochara-api-production-xxxxx.up.railway.app`

### Update Agent App Environment Variables

In your **Agent App** service (web-production-6dac6), set:

```bash
BAV_SAV_API_URL=https://bav-sav-api-production-xxxxx.up.railway.app
DASHA_GOCHARA_API_URL=https://dasha-gochara-api-production-xxxxx.up.railway.app
```

---

## Option 3: Use Same Service with Different Routes (Not Recommended)

If all APIs are in the same service, you can use the same URL:

```bash
BAV_SAV_API_URL=https://web-production-6dac6.up.railway.app
DASHA_GOCHARA_API_URL=https://web-production-6dac6.up.railway.app
```

**But this won't work** because:
- Your agent app runs on port 8080
- BAV/SAV API needs port 8000
- Dasha/Gochara API needs port 8001

**You need separate services** for each API.

---

## Quick Check: What Services Do You Have?

1. Go to Railway Dashboard
2. Look at your project
3. Count the services:

**If you see 1 service:**
- You only have the Agent App
- You need to deploy BAV/SAV API and Dasha/Gochara API as separate services

**If you see 3 services:**
- Agent App ✅
- BAV/SAV API ✅
- Dasha/Gochara API ✅
- Just copy their URLs

---

## How to Find Service URLs in Railway

### Method 1: From Dashboard
1. Railway Dashboard → Your Project
2. Click on each service
3. Look at the **top bar** - URL is shown there
4. Or go to **Settings** → **Networking** → **Domains**

### Method 2: From Settings
1. Click on service
2. **Settings** tab
3. **Networking** section
4. **Public Domain** shows the URL
5. If not set, click **"Generate Domain"**

### Method 3: From Deployments
1. Click on service
2. **Deployments** tab
3. Latest deployment shows the URL in logs

---

## Example Railway Project Structure

```
Your Railway Project
├── Service 1: Agent App
│   └── URL: web-production-6dac6.up.railway.app
│   └── Port: 8080
│   └── Uses: Dockerfile.agent
│
├── Service 2: BAV/SAV API
│   └── URL: bav-sav-api-production-xxxxx.up.railway.app
│   └── Port: 8000 (or Railway assigned)
│   └── Uses: api_server.py
│
└── Service 3: Dasha/Gochara API
    └── URL: dasha-gochara-api-production-xxxxx.up.railway.app
    └── Port: 8001 (or Railway assigned)
    └── Uses: dasha_gochara_api.py
```

---

## Environment Variables for Agent App

Once you have all URLs, set in **Agent App** service:

```bash
# Your existing service
# No variable needed - this is the agent app itself

# Other services (set these in Agent App)
BAV_SAV_API_URL=https://bav-sav-api-production-xxxxx.up.railway.app
DASHA_GOCHARA_API_URL=https://dasha-gochara-api-production-xxxxx.up.railway.app

# Supabase and OpenAI
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-service-role-key
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxx
```

---

## Testing API URLs

After setting URLs, test them:

```bash
# Test BAV/SAV API
curl https://bav-sav-api-production-xxxxx.up.railway.app/health

# Test Dasha/Gochara API
curl https://dasha-gochara-api-production-xxxxx.up.railway.app/health

# Test Agent App
curl https://web-production-6dac6.up.railway.app/health
```

All should return JSON responses.

---

## Troubleshooting

### Issue: Can't find other services
**Solution**: You need to create them. Follow "Option 2" above.

### Issue: Services exist but no URLs
**Solution**: Go to Settings → Networking → Generate Domain

### Issue: URLs not working
**Solution**: 
- Check services are deployed and running
- Check Railway logs for errors
- Verify CORS is enabled on API services

### Issue: Agent app can't reach APIs
**Solution**:
- Use HTTPS URLs (not HTTP)
- Use full Railway domain URLs
- Check environment variables are set correctly
- Verify APIs are accessible (test with curl)

---

## Summary

1. **Your Agent App**: `web-production-6dac6.up.railway.app` ✅
2. **BAV/SAV API**: Create separate service → Get URL → Set as `BAV_SAV_API_URL`
3. **Dasha/Gochara API**: Create separate service → Get URL → Set as `DASHA_GOCHARA_API_URL`
4. **Set all environment variables** in Agent App service
5. **Redeploy** Agent App

