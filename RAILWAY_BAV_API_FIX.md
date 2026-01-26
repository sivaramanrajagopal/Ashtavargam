# BAV/SAV API Service Configuration Fix

## Problem
BAV/SAV API service is trying to run Agent App code instead of API code.

**Error shows:**
```
File "/app/agent_app/main.py", line 15, in <module>
```

This means it's trying to start `agent_app.main:app` instead of `api_server:app`.

## Root Cause
The BAV/SAV API service is using the wrong start command or Dockerfile.

## Solution: Fix BAV/SAV API Service Configuration

### Step 1: Go to BAV/SAV API Service
1. Railway Dashboard
2. Click on **"BAV SAV API"** service (NOT Agent App)
3. Go to **"Settings"** tab

### Step 2: Check Build Settings
1. **Build** section
2. **Dockerfile Path**: Should be `Dockerfile` (NOT `Dockerfile.agent`)
   - If it shows `Dockerfile.agent`, change it to `Dockerfile`
   - OR leave it empty (Railway will auto-detect `Dockerfile`)

### Step 3: Check Deploy Settings (CRITICAL)
1. **Deploy** section
2. **Custom Start Command**: Should be:
   ```
   python3 -m uvicorn api_server:app --host 0.0.0.0 --port 8080
   ```
   
   **NOT:**
   ```
   python -m uvicorn agent_app.main:app --host 0.0.0.0 --port 8080  ❌ WRONG!
   ```

### Step 4: Verify Configuration
**BAV/SAV API should have:**
- **Dockerfile Path**: `Dockerfile` (or empty)
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `python3 -m uvicorn api_server:app --host 0.0.0.0 --port 8080`

**NOT:**
- ❌ `Dockerfile.agent`
- ❌ `agent_app.main:app`
- ❌ `requirements_agent.txt`

### Step 5: Save and Redeploy
1. After fixing the settings
2. Click **"Save"** (if there's a save button)
3. Go to **"Deployments"** tab
4. Click **"Redeploy"**
5. Should now start `api_server:app` correctly

## Correct Configuration Summary

| Setting | BAV/SAV API | Agent App |
|---------|-------------|-----------|
| **Dockerfile** | `Dockerfile` | `Dockerfile.agent` |
| **Build Command** | `pip install -r requirements.txt` | (auto) |
| **Start Command** | `python3 -m uvicorn api_server:app --host 0.0.0.0 --port 8080` | `python -m uvicorn agent_app.main:app --host 0.0.0.0 --port 8080` |
| **Requirements** | `requirements.txt` | `requirements_agent.txt` |
| **Main File** | `api_server.py` | `agent_app/main.py` |

## Why This Happened

Railway might have:
1. Picked up `railway.toml` which is configured for Agent App
2. Used wrong Dockerfile
3. Used wrong start command from a previous deployment

## Quick Fix Checklist

- [ ] Go to **"BAV SAV API"** service
- [ ] Settings → Build → Dockerfile Path: `Dockerfile` (or empty)
- [ ] Settings → Deploy → Start Command: `python3 -m uvicorn api_server:app --host 0.0.0.0 --port 8080`
- [ ] Save settings
- [ ] Deployments → Redeploy
- [ ] Check logs - should show `api_server:app` starting, not `agent_app.main:app`

## After Fix

The BAV/SAV API should:
1. ✅ Start `api_server:app` (not `agent_app.main:app`)
2. ✅ Not need environment variables (no OpenAI, no Supabase)
3. ✅ Have `/health` endpoint working
4. ✅ Healthcheck should pass

## Verification

After redeploy, check logs should show:
```
INFO:     Started server process
INFO:     Uvicorn running on http://0.0.0.0:8080
INFO:     Application startup complete.
```

And the health endpoint should work:
```bash
curl https://your-bav-api-url.up.railway.app/health
```
Should return: `{"status": "healthy"}`

