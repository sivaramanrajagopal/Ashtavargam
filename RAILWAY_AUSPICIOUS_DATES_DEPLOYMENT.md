# Railway Deployment: Auspicious Dates Feature

## ✅ Answer: NO New Service Needed!

The **Auspicious Dates** endpoint is part of the **existing Dasha/Gochara API service**.

---

## 📍 Where the Endpoint Lives

- **File**: `dasha_gochara_api.py`
- **Endpoint**: `POST /api/v1/gochara/auspicious-dates`
- **Service**: Dasha/Gochara API (port 8001)
- **Status**: Already part of existing service ✅

---

## 🔍 Check Your Current Railway Services

### Step 1: Verify You Have Dasha/Gochara API Service

1. Go to **Railway Dashboard**
2. Check your project
3. Look for a service named:
   - **"Dasha Gochara API"** OR
   - **"Dasha/Gochara API"** OR
   - **"Dasha-Gochara-API"**

### Step 2: If Service Exists ✅

**You're all set!** Just need to redeploy:

1. **Option A: Automatic Redeploy** (Recommended)
   - Railway will auto-deploy when you push to GitHub
   - Since you just pushed, it should redeploy automatically
   - Check **Deployments** tab to see if it's deploying

2. **Option B: Manual Redeploy**
   - Go to **Deployments** tab
   - Click **"Redeploy"** on latest deployment
   - Or click **"Deploy"** button

### Step 3: If Service Doesn't Exist ❌

You need to create the Dasha/Gochara API service:

---

## 🚀 How to Deploy Dasha/Gochara API Service (If Needed)

### Step 1: Create New Service

1. Go to **Railway Dashboard**
2. In your **same project** (where Agent App is deployed)
3. Click **"New Service"** (or **"Add Service"**)
4. Select **"GitHub Repo"**
5. Choose your repository: **`Ashtavargam`**
6. Click **"Deploy Now"**

### Step 2: Configure Service Name

1. Click on the newly created service
2. Click **"Settings"** tab
3. Find **"Service Name"** field
4. Change it to: **`Dasha Gochara API`**
5. Click **"Save"**

### Step 3: Configure Build Settings

1. Still in **Settings** tab
2. Scroll to **"Build"** section
3. **Root Directory**: `.` (default)
4. **Build Command**: `pip install -r requirements.txt`
   - (This installs all dependencies including `pyswisseph`)

### Step 4: Configure Deploy Settings

1. Scroll to **"Deploy"** section
2. **Custom Start Command**: 
   ```
   python3 -m uvicorn dasha_gochara_api:app --host 0.0.0.0 --port $PORT
   ```
   - Click on the field and enter this command
   - Railway will automatically set `$PORT`

### Step 5: Generate Public Domain

1. Scroll to **"Networking"** section
2. Click **"Generate Domain"** button
3. Railway will create a URL like: `dasha-gochara-api-production-xxxxx.up.railway.app`
4. **Copy this URL** - you'll need it for Agent App environment variables!
5. This is your **DASHA_GOCHARA_API_URL**

### Step 6: Environment Variables

**Good News**: Dasha/Gochara API service needs **NO environment variables** ✅

- It's a standalone calculation service
- Uses only Swiss Ephemeris (pyswisseph)
- No external API calls
- No OpenAI or Supabase needed

### Step 7: Wait for Deployment

1. Go to **"Deployments"** tab
2. Watch the build logs
3. Wait for deployment to complete (green checkmark ✅)
4. Should take 2-5 minutes

### Step 8: Test the Service

1. Test health endpoint:
   ```bash
   curl https://your-dasha-gochara-api-url.up.railway.app/health
   ```
   Should return: `{"status": "healthy", "version": "1.0.0"}`

2. Test API docs:
   - Open in browser: `https://your-dasha-gochara-api-url.up.railway.app/docs`
   - You should see all endpoints including:
     - `/api/v1/dasha/current`
     - `/api/v1/dasha/bhukti`
     - `/api/v1/gochara/current`
     - `/api/v1/gochara/calculate`
     - **`/api/v1/gochara/auspicious-dates`** ← New endpoint! ✅

### Step 9: Update Agent App Environment Variables

1. Go to your **Agent App** service in Railway
2. Click **"Variables"** tab
3. Find **`DASHA_GOCHARA_API_URL`** variable
4. Update it to your new service URL:
   ```
   DASHA_GOCHARA_API_URL=https://dasha-gochara-api-production-xxxxx.up.railway.app
   ```
5. Click **"Save"**

### Step 10: Redeploy Agent App (If Needed)

1. Go to **Agent App** service
2. **Deployments** tab
3. Click **"Redeploy"** to pick up the new environment variable

---

## 📋 Summary: What You Need

### Current Railway Services Structure:

```
Your Railway Project
├── Agent App Service
│   ├── URL: https://agent-app-production-xxxxx.up.railway.app
│   ├── Port: 8080
│   └── Env Vars: OPENAI_API_KEY, SUPABASE_URL, SUPABASE_KEY, 
│                 BAV_SAV_API_URL, DASHA_GOCHARA_API_URL
│
├── BAV/SAV API Service (if deployed)
│   ├── URL: https://bav-sav-api-production-xxxxx.up.railway.app
│   ├── Port: 8000
│   └── Env Vars: NONE
│
└── Dasha/Gochara API Service (if deployed)
    ├── URL: https://dasha-gochara-api-production-xxxxx.up.railway.app
    ├── Port: 8001
    ├── Env Vars: NONE
    └── Endpoints:
        ├── /api/v1/dasha/current
        ├── /api/v1/dasha/bhukti
        ├── /api/v1/gochara/current
        ├── /api/v1/gochara/calculate
        └── /api/v1/gochara/auspicious-dates ← NEW! ✅
```

---

## ✅ Quick Checklist

- [ ] Check if "Dasha Gochara API" service exists in Railway
- [ ] If exists: Redeploy to get latest code (auto or manual)
- [ ] If not exists: Create new service following steps above
- [ ] Generate public domain for Dasha/Gochara API
- [ ] Update `DASHA_GOCHARA_API_URL` in Agent App environment variables
- [ ] Test `/api/v1/gochara/auspicious-dates` endpoint
- [ ] Verify it works from Agent App frontend

---

## 🎯 Key Points

1. **NO new service needed** - Auspicious Dates is part of Dasha/Gochara API
2. **Just redeploy** existing Dasha/Gochara API service (if it exists)
3. **Or create it** if you don't have it yet
4. **No environment variables** needed for Dasha/Gochara API service
5. **Update Agent App** environment variable to point to Dasha/Gochara API URL

---

## 🧪 Testing the Auspicious Dates Endpoint

Once deployed, test it:

```bash
curl -X POST "https://your-dasha-gochara-api-url.up.railway.app/api/v1/gochara/auspicious-dates" \
  -H "Content-Type: application/json" \
  -d '{
    "dob": "1978-09-18",
    "tob": "17:05",
    "lat": 13.0827,
    "lon": 80.2707,
    "tz_offset": 5.5,
    "month": "2024-01",
    "top_n": 10
  }'
```

Should return JSON with `top_5`, `top_10`, and `all_dates` arrays.

---

**That's it! No new service needed - just ensure Dasha/Gochara API is deployed and up-to-date.** ✅

