# Railway.toml Fix - Agent App Configuration

## Problem
Railway was reading the start command from `railway.toml` which had:
```toml
startCommand = "python app_complete.py"  # Old Flask app ❌
```

This prevented editing the start command in the Railway UI.

## Solution
Updated `railway.toml` to use the Agent App:

```toml
[build]
builder = "dockerfile"
dockerfilePath = "Dockerfile.agent"  # ✅ Uses agent Dockerfile

[deploy]
startCommand = "uvicorn agent_app.main:app --host 0.0.0.0 --port $PORT"  # ✅ Agent app
healthcheckPath = "/health"
healthcheckTimeout = 100
restartPolicyType = "on_failure"
restartPolicyMaxRetries = 10
```

## Changes Made
1. ✅ Added `dockerfilePath = "Dockerfile.agent"` - ensures correct Dockerfile
2. ✅ Changed `startCommand` to use `uvicorn agent_app.main:app`
3. ✅ Changed `healthcheckPath` to `/health` (FastAPI endpoint)

## Next Steps
1. **Commit and push** the updated `railway.toml`:
   ```bash
   git add railway.toml
   git commit -m "Update railway.toml for agent app deployment"
   git push
   ```

2. **Railway will auto-detect** the changes and redeploy

3. **Verify** in Railway Dashboard:
   - Settings → Deploy should now show the new command
   - Build should use `Dockerfile.agent`
   - Service should deploy the agent app (not Flask app)

## Alternative: Service-Specific Configuration

If you want to keep `railway.toml` for the old Flask app and use different config for Agent App:

### Option 1: Delete railway.toml
- Delete `railway.toml` from repo
- Configure everything in Railway UI (Settings → Build/Deploy)

### Option 2: Use Railway UI Override
- Keep `railway.toml` as is
- In Railway UI: Settings → Deploy → Custom Start Command
- Railway UI settings override `railway.toml` if set

### Option 3: Service-Specific Files (Advanced)
- Create `railway.agent.toml` for agent service
- Railway doesn't auto-detect this, so use UI settings instead

## Recommended Approach
✅ **Use the updated `railway.toml`** - This is the simplest and ensures consistency.

## Verification
After deployment, check:
```bash
curl https://your-agent-app-url.up.railway.app/health
```
Should return: `{"status": "healthy", "version": "1.0.0"}`

If you see Flask HTML → still using old config ❌
If you see FastAPI JSON → agent app is running ✅

