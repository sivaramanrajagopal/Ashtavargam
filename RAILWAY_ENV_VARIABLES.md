# Railway Environment Variables for Agent App

## Required Environment Variables

### 1. Supabase Configuration
```bash
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-service-role-key-here
```

**Where to get:**
- Go to Supabase Dashboard → Settings → API
- Copy **Project URL** → `SUPABASE_URL`
- Copy **service_role key** (secret) → `SUPABASE_KEY`

---

### 2. OpenAI Configuration
```bash
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxx
```

**Where to get:**
- Go to https://platform.openai.com/api-keys
- Create new API key
- Copy the key → `OPENAI_API_KEY`

---

### 3. API Endpoints (BAV/SAV and Dasha/Gochara)

#### Option A: If APIs are deployed separately on Railway
```bash
BAV_SAV_API_URL=https://your-bav-sav-api.railway.app
DASHA_GOCHARA_API_URL=https://your-dasha-gochara-api.railway.app
```

#### Option B: If APIs are on same Railway service (different ports)
```bash
BAV_SAV_API_URL=http://localhost:8000
DASHA_GOCHARA_API_URL=http://localhost:8001
```

#### Option C: If using external/public APIs
```bash
BAV_SAV_API_URL=https://your-domain.com/api/bav-sav
DASHA_GOCHARA_API_URL=https://your-domain.com/api/dasha-gochara
```

**Note:** For Railway services, use the generated Railway domain URLs.

---

### 4. Server Configuration
```bash
PORT=8080
```

**Note:** Railway automatically sets `PORT` environment variable. Your app should use `$PORT` or default to 8080.

---

### 5. Optional: Context Window Management
```bash
MAX_MESSAGES=50
MAX_TOKENS=8000
RECENT_MESSAGES_COUNT=10
```

---

## Complete Environment Variables List

Copy this into Railway → Variables:

```bash
# Supabase
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-service-role-key

# OpenAI
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxx

# API Endpoints
BAV_SAV_API_URL=https://your-bav-sav-api.railway.app
DASHA_GOCHARA_API_URL=https://your-dasha-gochara-api.railway.app

# Server (Railway sets this automatically)
PORT=8080

# Optional: Context Management
MAX_MESSAGES=50
MAX_TOKENS=8000
RECENT_MESSAGES_COUNT=10
```

---

## API Endpoint Names Reference

### BAV/SAV API Endpoints
- Base URL: `BAV_SAV_API_URL` (default: `http://localhost:8000`)
- Endpoints:
  - `POST /api/v1/calculate/full` - Full BAV/SAV calculation
  - `POST /api/v1/calculate/bav` - Individual BAV calculation
  - `POST /api/v1/calculate/sav` - SAV calculation
  - `GET /health` - Health check

### Dasha/Gochara API Endpoints
- Base URL: `DASHA_GOCHARA_API_URL` (default: `http://localhost:8001`)
- Endpoints:
  - `POST /api/v1/dasha/current` - Current Dasha period
  - `POST /api/v1/dasha/bhukti` - Dasha-Bhukti table
  - `POST /api/v1/dasha/calculate` - Full Dasha calculation
  - `POST /api/v1/gochara/current` - Current transits
  - `POST /api/v1/gochara/calculate` - Transits for specific date
  - `GET /health` - Health check

---

## How to Set in Railway

1. Go to Railway Dashboard
2. Select your project
3. Click on the **Agent App** service
4. Go to **Variables** tab
5. Click **+ New Variable**
6. Add each variable one by one:
   - Name: `SUPABASE_URL`
   - Value: `https://your-project.supabase.co`
   - Click **Add**
7. Repeat for all variables

---

## Verification

After setting variables, check logs to verify:

```bash
# In Railway logs, you should see:
✅ Supabase connected
✅ OpenAI API key configured
✅ BAV/SAV API URL: https://...
✅ Dasha/Gochara API URL: https://...
```

---

## Troubleshooting

### Issue: App not using environment variables
- **Check:** Variables are set in Railway (not just `.env` file)
- **Check:** Variable names match exactly (case-sensitive)
- **Check:** No extra spaces in variable values

### Issue: Cannot connect to APIs
- **Check:** API URLs are correct (use Railway service URLs)
- **Check:** APIs are deployed and running
- **Check:** CORS is enabled on API services

### Issue: Supabase connection fails
- **Check:** `SUPABASE_URL` is correct (no trailing slash)
- **Check:** `SUPABASE_KEY` is service_role key (not anon key)
- **Check:** Supabase project is active

### Issue: OpenAI errors
- **Check:** `OPENAI_API_KEY` is valid and has credits
- **Check:** API key has proper permissions
- **Check:** No extra spaces or quotes in key

