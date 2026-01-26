# BAV/SAV API Service - Railway Configuration

## Service Settings for Railway Dashboard

### Service Name
```
BAV SAV API
```
(or any name you prefer, e.g., "Ashtakavarga API")

---

## Build Configuration

### Root Directory
```
.
```
(Leave as default - root of repository)

### Dockerfile Path
```
(Leave empty)
```
OR if you have a Dockerfile:
```
Dockerfile
```

### Build Command
```
pip install -r requirements.txt
```

**Alternative (if you want to avoid cache issues):**
```
pip install --no-cache-dir -r requirements.txt
```

---

## Deploy Configuration

### Start Command
```
python3 -m uvicorn api_server:app --host 0.0.0.0 --port 8080
```

**Important Notes:**
- Use `8080` (fixed port), NOT `$PORT` (Railway doesn't expand it)
- Use `python3` (not `python`) to ensure Python 3.x
- `--host 0.0.0.0` allows external connections
- `api_server:app` refers to the `app` object in `api_server.py`

---

## Complete Configuration Summary

### In Railway Dashboard → Settings:

| Setting | Value |
|---------|-------|
| **Service Name** | `BAV SAV API` |
| **Root Directory** | `.` |
| **Dockerfile Path** | (empty) |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `python3 -m uvicorn api_server:app --host 0.0.0.0 --port 8080` |

---

## Step-by-Step Setup

### 1. Go to Railway Dashboard
- Open https://railway.app
- Select your project
- Find or create "BAV SAV API" service

### 2. Configure Build Settings
1. Click on "BAV SAV API" service
2. Go to **Settings** tab
3. Scroll to **"Build"** section
4. Set:
   - **Root Directory**: `.` (default)
   - **Dockerfile Path**: (leave empty)
   - **Build Command**: `pip install -r requirements.txt`

### 3. Configure Deploy Settings
1. Still in **Settings** tab
2. Scroll to **"Deploy"** section
3. Find **"Start Command"** field
4. Enter:
   ```
   python3 -m uvicorn api_server:app --host 0.0.0.0 --port 8080
   ```
5. Click **Save** (if there's a save button)

### 4. Generate Public Domain
1. Scroll to **"Networking"** section
2. Click **"Generate Domain"** button
3. Railway creates URL like: `bav-sav-api-production-xxxxx.up.railway.app`
4. **Copy this URL** - you'll need it for Agent App environment variables

### 5. Deploy
1. Go to **"Deployments"** tab
2. Click **"Redeploy"** (or wait for auto-deploy)
3. Wait for deployment to complete (2-5 minutes)
4. Check logs to verify it started successfully

---

## Verification

### Check Service is Running
1. Go to **"Logs"** tab
2. Should see:
   ```
   INFO:     Application startup complete.
   INFO:     Uvicorn running on http://0.0.0.0:8080
   ```

### Test Health Endpoint
```bash
curl https://your-bav-sav-api-url.up.railway.app/health
```
Should return: `{"status": "healthy"}`

### Test API Documentation
Open in browser:
```
https://your-bav-sav-api-url.up.railway.app/docs
```
Should show FastAPI Swagger UI documentation

### Test CORS Headers
In browser console (F12):
```javascript
fetch('https://your-bav-sav-api-url.up.railway.app/health')
  .then(r => {
    console.log('CORS Header:', r.headers.get('access-control-allow-origin'));
    return r.json();
  })
  .then(data => console.log('Response:', data));
```
Should see: `CORS Header: *`

---

## Common Issues

### Issue 1: Port Error
**Error**: `Invalid value for '--port': '$PORT' is not a valid integer`

**Fix**: Use fixed port `8080` instead of `$PORT`:
```
python3 -m uvicorn api_server:app --host 0.0.0.0 --port 8080
```

### Issue 2: Module Not Found
**Error**: `ModuleNotFoundError: No module named 'api_server'`

**Fix**: 
- Verify **Root Directory** is set to `.` (root)
- Verify `api_server.py` exists in root directory
- Check build logs for installation errors

### Issue 3: CORS Errors
**Error**: CORS policy blocking requests

**Fix**:
- Verify service has been redeployed with latest code
- Check that `api_server.py` has CORS middleware configured
- Verify CORS headers in response (see verification above)

### Issue 4: Build Fails
**Error**: Build command fails

**Fix**:
- Check `requirements.txt` exists
- Verify all dependencies are listed
- Check build logs for specific error messages

---

## Environment Variables (Optional)

The BAV/SAV API doesn't require any environment variables, but you can add:

| Variable | Value | Purpose |
|----------|-------|---------|
| `PORT` | `8080` | (Railway sets this automatically) |
| `LOG_LEVEL` | `INFO` | For logging (optional) |

---

## Quick Reference

**Copy-paste these commands:**

**Build Command:**
```bash
pip install -r requirements.txt
```

**Start Command:**
```bash
python3 -m uvicorn api_server:app --host 0.0.0.0 --port 8080
```

---

**After configuration, the service should deploy and work correctly!** ✅

