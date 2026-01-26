# Railway Healthcheck Failure Fix

## Problem
Healthcheck is failing: `/health` endpoint not responding

## Possible Causes

### 1. Service Not Starting Properly
- Check deployment logs for errors
- Service might be crashing on startup

### 2. Port Mismatch
- Start command uses fixed port `8080`
- Railway might assign different port
- Solution: Use `$PORT` or let Railway handle it

### 3. Healthcheck Path Not Configured
- Railway needs to know the healthcheck path
- Should be `/health` for BAV/SAV API

### 4. Service Taking Too Long to Start
- Healthcheck timeout might be too short
- Service needs more time to initialize

---

## Solutions

### Solution 1: Check Deployment Logs
1. Go to Railway Dashboard
2. Click on **BAV/SAV API** service
3. Go to **"Deployments"** tab
4. Click on the latest deployment
5. Check **"Build Logs"** and **"Deploy Logs"**
6. Look for errors or crashes

### Solution 2: Fix Port in Start Command
**Current:**
```
python3 -m uvicorn api_server:app --host 0.0.0.0 --port 8080
```

**Better (use Railway's PORT):**
```
python3 -m uvicorn api_server:app --host 0.0.0.0 --port ${PORT:-8080}
```

**Or let Railway handle it:**
- Railway automatically sets `PORT` environment variable
- The code in `api_server.py` already reads it: `port = int(os.environ.get("PORT", 8000))`
- So we can use: `python3 -m uvicorn api_server:app --host 0.0.0.0 --port $PORT`

### Solution 3: Configure Healthcheck in Railway
1. Go to **Settings** → **Deploy** section
2. Find **"Healthcheck Path"** (if available)
3. Set it to: `/health`
4. Set **"Healthcheck Timeout"** to: `100` (seconds)

### Solution 4: Use Railway's Default Healthcheck
Railway automatically checks the root path `/` if no healthcheck is configured. But our API has `/health`, so we need to either:
- Configure healthcheck path in Railway settings, OR
- Add a root endpoint that redirects to `/health`

---

## Quick Fix Steps

### Step 1: Update Start Command
1. Go to **BAV/SAV API** service → **Settings** → **Deploy**
2. Update **Start Command** to:
   ```
   python3 -m uvicorn api_server:app --host 0.0.0.0 --port ${PORT:-8080}
   ```
   OR simply:
   ```
   python3 -m uvicorn api_server:app --host 0.0.0.0 --port 8080
   ```
   (Railway will route traffic correctly)

### Step 2: Check Build/Deploy Logs
1. Go to **Deployments** tab
2. Check for any errors in logs
3. Common issues:
   - Missing dependencies
   - Import errors
   - Port conflicts

### Step 3: Verify Health Endpoint Exists
The `/health` endpoint exists in `api_server.py`:
```python
@app.get("/health", response_model=HealthResponse)
async def health_check():
    return {"status": "healthy"}
```

### Step 4: Test Manually (After Deployment)
Once deployed, test:
```bash
curl https://your-bav-api-url.up.railway.app/health
```

---

## Alternative: Add Root Endpoint

If Railway is checking `/` instead of `/health`, we can add a root endpoint:

```python
@app.get("/")
async def root():
    return {"status": "healthy", "service": "BAV/SAV API"}
```

But this requires code changes. Better to configure healthcheck in Railway.

---

## Most Likely Issue

**The service is probably crashing on startup.** Check the deployment logs to see the actual error.

**Common startup errors:**
- Missing Python dependencies
- Import errors (e.g., `ashtakavarga_calculator_final` not found)
- System library issues (pyswisseph dependencies)

---

## Action Items

1. ✅ Check deployment logs for errors
2. ✅ Verify start command is correct
3. ✅ Check if service is actually running
4. ✅ Test `/health` endpoint manually after deployment
5. ✅ Configure healthcheck path in Railway if needed

---

## Debugging Steps

1. **Check Logs:**
   - Railway Dashboard → Service → Deployments → Latest → View Logs

2. **Check Service Status:**
   - Is the service actually running?
   - Are there any crash loops?

3. **Test Health Endpoint:**
   - After deployment, manually test: `curl https://your-url/health`

4. **Check Port:**
   - Railway sets PORT automatically
   - Our code reads it: `os.environ.get("PORT", 8000)`
   - Start command should use the same port

---

## Recommended Fix

**Update Start Command in Railway:**
```
python3 -m uvicorn api_server:app --host 0.0.0.0 --port 8080
```

**Then check deployment logs** to see what's actually failing.

