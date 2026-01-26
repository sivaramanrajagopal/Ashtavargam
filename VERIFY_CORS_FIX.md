# How to Verify CORS Fix is Deployed

## Quick Test

### Test 1: Check BAV/SAV API CORS Headers

Open your browser and go to:
```
https://bav-sav-api-production.up.railway.app/docs
```

Then open Browser Developer Tools (F12) → Network tab, and try making a request from Swagger UI.

**Expected**: Response headers should include:
```
Access-Control-Allow-Origin: *
Access-Control-Allow-Methods: *
Access-Control-Allow-Headers: *
```

### Test 2: Check Dasha/Gochara API CORS Headers

Open:
```
https://dasha-gochara-api-production.up.railway.app/docs
```

Try making a request and check Network tab for CORS headers.

### Test 3: Direct API Test (from Browser Console)

Open Agent App, then in Browser Console (F12), run:

```javascript
// Test BAV/SAV API CORS
fetch('https://bav-sav-api-production.up.railway.app/health', {
  method: 'GET',
  headers: {'Content-Type': 'application/json'}
})
.then(r => {
  console.log('✅ CORS Headers:', r.headers.get('access-control-allow-origin'));
  return r.json();
})
.then(data => console.log('✅ Response:', data))
.catch(e => console.error('❌ CORS Error:', e));
```

**Expected**: Should see `✅ CORS Headers: *` and successful response.

## Check Railway Deployment Status

### Method 1: Railway Dashboard

1. Go to https://railway.app
2. Select your project
3. For each service (BAV/SAV API, Dasha/Gochara API):
   - Click on the service
   - Go to "Deployments" tab
   - Check the latest deployment:
     - **Status**: Should be "Active" (green)
     - **Commit**: Should show commit `2fbbbf3` or later
     - **Time**: Should be recent (after you pushed the code)

### Method 2: Check Service Logs

1. Go to Railway Dashboard
2. Select "BAV SAV API" service
3. Go to "Logs" tab
4. Look for startup messages:
   ```
   INFO:     Application startup complete.
   INFO:     Uvicorn running on http://0.0.0.0:8080
   ```
5. Check the timestamp - if it's old, service hasn't redeployed

### Method 3: Check API Health Endpoint

```bash
# Test BAV/SAV API
curl -I https://bav-sav-api-production.up.railway.app/health

# Should see CORS headers in response
```

## If Services Haven't Redeployed

### Option 1: Manual Redeploy (Recommended)

1. **BAV/SAV API Service**:
   - Railway Dashboard → "BAV SAV API" service
   - "Deployments" tab → Click "Redeploy" button
   - Wait for deployment to complete (check logs)

2. **Dasha/Gochara API Service**:
   - Railway Dashboard → "Dasha Gochara API" service
   - "Deployments" tab → Click "Redeploy" button
   - Wait for deployment to complete (check logs)

### Option 2: Trigger Auto-Deploy

If auto-deploy is enabled, make a small change to trigger it:

```bash
# Add a comment to trigger redeploy
echo "# Trigger redeploy" >> api_server.py
git add api_server.py
git commit -m "Trigger redeploy"
git push
```

Railway should automatically redeploy all services.

## After Redeployment

1. **Wait 1-2 minutes** for services to fully start
2. **Test Ashtakavarga modal** - should work without CORS errors
3. **Test Auspicious Dates** - should work (404 should be resolved)
4. **Check browser console** - no CORS errors

## Troubleshooting

### Still Getting CORS Errors After Redeploy?

1. **Clear Browser Cache**:
   - Hard refresh: `Ctrl+Shift+R` (Windows) or `Cmd+Shift+R` (Mac)
   - Or clear browser cache completely

2. **Check CORS Configuration in Code**:
   ```python
   # Should be in api_server.py and dasha_gochara_api.py
   app.add_middleware(
       CORSMiddleware,
       allow_origins=["*"],
       allow_credentials=False,
       allow_methods=["*"],
       allow_headers=["*"],
       expose_headers=["*"],
       max_age=3600,
   )
   ```

3. **Verify Service is Running**:
   - Check Railway logs for errors
   - Verify service shows "Active" status
   - Check health endpoint returns 200 OK

4. **Check Network Tab**:
   - Open Developer Tools (F12) → Network tab
   - Make a request
   - Look at the OPTIONS (preflight) request
   - Check if it returns 200 OK with CORS headers

### 404 Error for Auspicious Dates?

The endpoint `/api/v1/gochara/auspicious-dates` exists in the code. If you get 404:

1. **Verify Service Deployed Latest Code**:
   - Check Railway deployment shows latest commit
   - Check service logs for startup errors

2. **Test Endpoint Directly**:
   ```
   https://dasha-gochara-api-production.up.railway.app/docs
   ```
   - Look for `/api/v1/gochara/auspicious-dates` endpoint
   - If not visible, service needs redeployment

3. **Check Route Registration**:
   - The endpoint should be registered at startup
   - Check service logs for route registration messages

## Success Indicators

✅ **CORS Fixed When**:
- No CORS errors in browser console
- API calls succeed
- Ashtakavarga modal loads data
- Auspicious Dates modal loads data
- Network tab shows successful requests with CORS headers

---

**Current Status**: Code is fixed and pushed. Services need redeployment on Railway.

