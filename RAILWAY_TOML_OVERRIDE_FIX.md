# Railway.toml Override Fix

## Problem
Railway keeps defaulting to `Dockerfile.agent` for all services because `railway.toml` has:
```toml
dockerfilePath = "Dockerfile.agent"
```

This applies to ALL services in the project, not just Agent App.

## Solution
Removed `dockerfilePath` and `startCommand` from `railway.toml` so each service can be configured individually in Railway UI.

## What Changed

### Before:
```toml
[build]
dockerfilePath = "Dockerfile.agent"  # Applied to ALL services ❌

[deploy]
startCommand = "python -m uvicorn agent_app.main:app..."  # Applied to ALL services ❌
```

### After:
```toml
[build]
# dockerfilePath removed - configure per service ✅

[deploy]
# startCommand removed - configure per service ✅
```

## Now Configure Each Service in Railway UI

### Agent App Service:
1. Settings → Build → Dockerfile Path: `Dockerfile.agent`
2. Settings → Deploy → Start Command: `python -m uvicorn agent_app.main:app --host 0.0.0.0 --port 8080`

### BAV/SAV API Service:
1. Settings → Build → Dockerfile Path: `Dockerfile` (or empty)
2. Settings → Deploy → Start Command: `python3 -m uvicorn api_server:app --host 0.0.0.0 --port 8080`

### Dasha/Gochara API Service:
1. Settings → Build → Dockerfile Path: (empty)
2. Settings → Deploy → Start Command: `python3 -m uvicorn dasha_gochara_api:app --host 0.0.0.0 --port 8080`

## After Pushing Changes

1. Railway will detect the updated `railway.toml`
2. Services will no longer be forced to use `Dockerfile.agent`
3. You can now set Dockerfile path individually in Railway UI
4. Settings should stick and not revert

## Next Steps

1. ✅ Changes committed and pushed
2. ⏳ Wait for Railway to detect changes (or manually redeploy)
3. ⏳ Go to BAV/SAV API service → Settings
4. ⏳ Set Dockerfile Path to `Dockerfile` (should work now!)
5. ⏳ Set Start Command to `python3 -m uvicorn api_server:app --host 0.0.0.0 --port 8080`
6. ⏳ Save and redeploy

## Why This Works

Railway UI settings **override** `railway.toml` when explicitly set. But if `railway.toml` has a value, Railway uses it as default. By removing it, we let each service have its own configuration.

