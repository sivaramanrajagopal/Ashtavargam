# Agent App Running Flask Instead of FastAPI - Fix

## Problem
Agent App service is running Flask app (`app_complete.py`) instead of FastAPI agent app (`agent_app.main:app`).

**Logs show:**
```
Serving Flask app 'app_complete'
Complete Ashtakavarga Calculator - Flask Web Application
GET /health HTTP/1.1" 404
```

## Root Cause
The Agent App service is using the wrong Dockerfile or start command.

## Solution: Fix Agent App Service Configuration

### Step 1: Go to Agent App Service
1. Railway Dashboard
2. Click on **"Agent App"** service
3. Go to **"Settings"** tab

### Step 2: Verify Build Settings
1. **Build** section
2. **Dockerfile Path**: Should be `Dockerfile.agent` ✅
   - If it's `Dockerfile`, change it to `Dockerfile.agent`

### Step 3: Verify Deploy Settings (CRITICAL)
1. **Deploy** section
2. **Custom Start Command**: Should be:
   ```
   python -m uvicorn agent_app.main:app --host 0.0.0.0 --port 8080
   ```
   
   **NOT:**
   ```
   python app_complete.py  ❌ WRONG!
   ```

### Step 4: Check if Dockerfile.agent CMD is Overriding
The `Dockerfile.agent` has a CMD, but Railway's start command should override it. If it's not working:
1. Make sure start command is explicitly set in Railway UI
2. The start command in UI overrides Dockerfile CMD

## Correct Configuration for Agent App

| Setting | Should Be |
|---------|-----------|
| **Dockerfile Path** | `Dockerfile.agent` |
| **Start Command** | `python -m uvicorn agent_app.main:app --host 0.0.0.0 --port 8080` |
| **NOT** | `python app_complete.py` ❌ |

## Why This Happened

Possible reasons:
1. Start command not set in Railway UI (using Dockerfile CMD instead)
2. Dockerfile path wrong (using `Dockerfile` instead of `Dockerfile.agent`)
3. Railway cached old configuration

## Quick Fix Steps

1. ✅ Go to **Agent App** service → **Settings**
2. ✅ **Build** → Dockerfile Path: `Dockerfile.agent`
3. ✅ **Deploy** → Start Command: `python -m uvicorn agent_app.main:app --host 0.0.0.0 --port 8080`
4. ✅ **Save** settings
5. ✅ **Deployments** → **Redeploy**

## After Fix

The Agent App should:
- ✅ Start `agent_app.main:app` (FastAPI)
- ✅ Have `/health` endpoint working
- ✅ Show FastAPI startup logs, not Flask logs
- ✅ Healthcheck should pass

## Verification

After redeploy, logs should show:
```
INFO:     Started server process
INFO:     Uvicorn running on http://0.0.0.0:8080
INFO:     Application startup complete.
```

**NOT:**
```
Serving Flask app 'app_complete'  ❌
```

