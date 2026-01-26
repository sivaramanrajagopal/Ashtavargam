# Redeploy BAV/SAV API to Fix CORS

## Current Status
- ✅ **Dasha/Gochara API**: Working correctly (no CORS errors)
- ❌ **BAV/SAV API**: Still has CORS errors - needs redeployment

## Problem
The BAV/SAV API service is still running old code without the updated CORS configuration. The code has been fixed and pushed, but Railway hasn't redeployed the service yet.

## Solution: Manual Redeploy

### Step 1: Go to Railway Dashboard
1. Open https://railway.app
2. Select your project
3. Find **"BAV SAV API"** service (or similar name)

### Step 2: Check Deployment Status
1. Click on **"BAV SAV API"** service
2. Go to **"Deployments"** tab
3. Check the latest deployment:
   - **Status**: Should be "Active" (green)
   - **Commit**: Should show commit `2fbbbf3` or later (with CORS fix)
   - **Time**: Check if it's recent

### Step 3: Redeploy Service
1. In **"Deployments"** tab
2. Find the latest deployment
3. Click **"Redeploy"** button (three dots menu → Redeploy)
4. Wait for deployment to complete (2-5 minutes)
5. Watch the logs to ensure it starts successfully

### Step 4: Verify CORS Configuration
After redeployment, verify CORS is working:

1. **Test Health Endpoint**:
   ```bash
   curl -I https://bav-sav-api-production.up.railway.app/health
   ```
   Should see CORS headers in response

2. **Test from Browser Console**:
   Open Agent App, then in Browser Console (F12):
   ```javascript
   fetch('https://bav-sav-api-production.up.railway.app/health')
     .then(r => {
       console.log('✅ CORS Headers:', r.headers.get('access-control-allow-origin'));
       return r.json();
     })
     .then(data => console.log('✅ Response:', data))
     .catch(e => console.error('❌ Error:', e));
   ```
   Should see: `✅ CORS Headers: *`

3. **Test Ashtakavarga Modal**:
   - Open Agent App
   - Click "Ashtakavarga" button
   - Should load without CORS errors

## Alternative: Force Redeploy via Code

If manual redeploy doesn't work, trigger via code change:

```bash
# Add a comment to trigger redeploy
echo "# Trigger BAV/SAV API redeploy - $(date)" >> api_server.py
git add api_server.py
git commit -m "Trigger BAV/SAV API redeploy for CORS fix"
git push
```

Railway should automatically redeploy the service.

## Expected CORS Headers

After redeployment, API responses should include:

```
Access-Control-Allow-Origin: *
Access-Control-Allow-Methods: *
Access-Control-Allow-Headers: *
Access-Control-Expose-Headers: *
Access-Control-Max-Age: 3600
```

## Verification Checklist

After redeployment:

- [ ] Service shows latest deployment with recent timestamp
- [ ] Logs show "Application startup complete" with no errors
- [ ] `/health` endpoint returns 200 OK with CORS headers
- [ ] `/docs` page loads correctly
- [ ] Ashtakavarga modal works without CORS errors
- [ ] No CORS errors in browser console

## Troubleshooting

### Still Getting CORS Errors?

1. **Clear Browser Cache**:
   - Hard refresh: `Ctrl+Shift+R` (Windows) or `Cmd+Shift+R` (Mac)
   - Or clear browser cache completely

2. **Check Service Logs**:
   - Go to Railway → BAV/SAV API → Logs
   - Look for startup errors
   - Verify service is running

3. **Verify CORS Configuration**:
   - Check that `api_server.py` has the updated CORS middleware
   - Should have `allow_origins=["*"]` and `allow_credentials=False`

4. **Test API Directly**:
   - Open `https://bav-sav-api-production.up.railway.app/docs`
   - Try making a request from Swagger UI
   - Check Network tab for CORS headers

### Service Not Starting?

1. **Check Start Command**:
   - Settings → Deploy → Start Command
   - Should be: `python3 -m uvicorn api_server:app --host 0.0.0.0 --port 8080`
   - NOT: `--port $PORT` (this causes errors)

2. **Check Build Command**:
   - Settings → Build → Build Command
   - Should be: `pip install -r requirements.txt`

3. **Check Logs for Errors**:
   - Look for import errors, missing dependencies, etc.

---

**After redeployment, the BAV/SAV API should work correctly with CORS enabled!**

