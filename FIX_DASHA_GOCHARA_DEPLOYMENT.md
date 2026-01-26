# Fix Dasha/Gochara API Deployment Issue

## Problem
Dasha/Gochara API service is not picking up the latest code deployment, while other services (BAV/SAV API and Agent App) have updated successfully.

## Solution Steps

### Step 1: Check Current Service Configuration

1. Go to Railway Dashboard
2. Select **"Dasha Gochara API"** service (or similar name)
3. Go to **"Settings"** tab
4. Check the following:

#### Build & Deploy Settings:
- **Root Directory**: Should be `.` (root of repo)
- **Build Command**: Should be `pip install -r requirements_agent.txt` (or empty if using Dockerfile)
- **Start Command**: Should be `python3 -m uvicorn dasha_gochara_api:app --host 0.0.0.0 --port $PORT`
- **Dockerfile Path**: Should be empty (unless you have a specific Dockerfile for this service)

### Step 2: Force Redeploy

#### Option A: Manual Redeploy (Recommended)

1. Go to Railway Dashboard
2. Select **"Dasha Gochara API"** service
3. Go to **"Deployments"** tab
4. Click **"Redeploy"** button on the latest deployment
5. Wait for deployment to complete
6. Check logs to verify it's using latest code

#### Option B: Trigger via Code Change

If manual redeploy doesn't work, trigger a new deployment:

```bash
# Make a small change to dasha_gochara_api.py
echo "# Deployment trigger - $(date)" >> dasha_gochara_api.py
git add dasha_gochara_api.py
git commit -m "Trigger Dasha/Gochara API redeploy"
git push
```

### Step 3: Verify Service Configuration

Check that the service is configured correctly:

1. **Service Name**: Should be "Dasha Gochara API" or similar
2. **GitHub Connection**: Should be connected to the same repo
3. **Branch**: Should be `main` (or your default branch)
4. **Auto-Deploy**: Should be enabled

### Step 4: Check Deployment Logs

After redeploying, check the logs:

1. Go to **"Logs"** tab
2. Look for:
   ```
   INFO:     Application startup complete.
   INFO:     Uvicorn running on http://0.0.0.0:8080
   ```
3. Check for any errors during startup
4. Verify the commit hash matches latest code

### Step 5: Verify CORS Configuration

After redeployment, verify CORS is working:

1. Open browser console (F12)
2. Test the API:
   ```javascript
   fetch('https://dasha-gochara-api-production.up.railway.app/health')
     .then(r => r.json())
     .then(data => console.log('✅ API Working:', data))
     .catch(e => console.error('❌ Error:', e));
   ```

3. Check Network tab for CORS headers:
   - Should see `Access-Control-Allow-Origin: *`

### Step 6: Test Auspicious Dates Endpoint

After redeployment, test the endpoint:

1. Go to: `https://dasha-gochara-api-production.up.railway.app/docs`
2. Look for `/api/v1/gochara/auspicious-dates` endpoint
3. If visible, the service has latest code
4. If not visible, service still has old code

## Common Issues

### Issue 1: Service Using Wrong Dockerfile

**Symptom**: Service keeps using old code even after redeploy

**Fix**:
1. Go to Settings → Dockerfile Path
2. Set to empty (or correct Dockerfile if needed)
3. Redeploy

### Issue 2: Service Using Cached Build

**Symptom**: Build completes but uses old code

**Fix**:
1. Go to Settings → Build Command
2. Add cache-busting: `pip install --no-cache-dir -r requirements_agent.txt`
3. Redeploy

### Issue 3: Service Not Connected to GitHub

**Symptom**: No new deployments when code is pushed

**Fix**:
1. Go to Settings → Source
2. Verify GitHub connection
3. Verify branch is `main`
4. Enable auto-deploy

### Issue 4: Wrong Start Command

**Symptom**: Service starts but doesn't load latest code

**Fix**:
1. Go to Settings → Start Command
2. Verify it's: `python3 -m uvicorn dasha_gochara_api:app --host 0.0.0.0 --port $PORT`
3. Or: `uvicorn dasha_gochara_api:app --host 0.0.0.0 --port $PORT`
4. Redeploy

## Verification Checklist

After following the steps above:

- [ ] Service shows latest deployment with recent timestamp
- [ ] Logs show "Application startup complete" with no errors
- [ ] `/health` endpoint returns 200 OK
- [ ] `/docs` shows `/api/v1/gochara/auspicious-dates` endpoint
- [ ] CORS headers are present in responses
- [ ] Auspicious Dates modal works in Agent App

## Quick Fix Command

If you have Railway CLI installed:

```bash
railway redeploy --service "Dasha Gochara API"
```

## Still Not Working?

If the service still doesn't pick up latest code:

1. **Delete and Recreate Service** (Last Resort):
   - Create new service in Railway
   - Connect to same GitHub repo
   - Configure with correct settings
   - Deploy

2. **Check for Service-Specific Configuration**:
   - Look for `railway.toml` or service-specific config files
   - Verify they're not overriding deployment settings

3. **Contact Railway Support**:
   - If issue persists, may be a Railway platform issue
   - Check Railway status page

---

**Expected Result**: After redeployment, Dasha/Gochara API should have:
- Latest CORS configuration
- `/api/v1/gochara/auspicious-dates` endpoint working
- No 404 errors
- CORS headers in responses

