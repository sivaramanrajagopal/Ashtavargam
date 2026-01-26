# Railway CORS Fix - Deployment Instructions

## Issue
CORS errors are blocking API requests from the Agent App to BAV/SAV API and Dasha/Gochara API.

## Root Cause
The CORS configuration was updated in the code, but **Railway services need to be manually redeployed** for the changes to take effect.

## Solution Applied

### Code Changes
1. **api_server.py** (BAV/SAV API):
   - Updated CORS middleware configuration
   - Set `allow_credentials=False` to allow wildcard origins
   - Added `max_age=3600` for preflight caching
   - Set `allow_methods=["*"]` to allow all HTTP methods

2. **dasha_gochara_api.py** (Dasha/Gochara API):
   - Same CORS configuration updates

## Deployment Steps

### Step 1: Verify Code is Pushed
```bash
git log --oneline -5
# Should see: "Fix CORS issues for Railway deployment"
```

### Step 2: Redeploy BAV/SAV API Service

1. Go to Railway Dashboard
2. Select **"BAV SAV API"** service (or similar name)
3. Go to **"Deployments"** tab
4. Click **"Redeploy"** button (or trigger a new deployment)
5. Wait for deployment to complete (check logs)

### Step 3: Redeploy Dasha/Gochara API Service

1. Go to Railway Dashboard
2. Select **"Dasha Gochara API"** service (or similar name)
3. Go to **"Deployments"** tab
4. Click **"Redeploy"** button (or trigger a new deployment)
5. Wait for deployment to complete (check logs)

### Step 4: Verify Deployment

After both services are redeployed:

1. **Test BAV/SAV API**:
   - Open Agent App
   - Click "Ashtakavarga" button
   - Should load without CORS errors

2. **Test Dasha/Gochara API**:
   - Open Agent App
   - Click "Auspicious Dates" button
   - Should load without CORS errors

3. **Check Browser Console**:
   - Open Developer Tools (F12)
   - Check Console tab
   - Should see successful API calls
   - No CORS errors

## Alternative: Force Redeploy via Git

If Railway auto-deployment is enabled:

1. Make a small change to trigger redeploy:
   ```bash
   # Add a comment to api_server.py
   echo "# CORS fix deployed" >> api_server.py
   git add api_server.py
   git commit -m "Trigger redeploy for CORS fix"
   git push
   ```

2. Railway will automatically redeploy all services

## Troubleshooting

### Still Getting CORS Errors?

1. **Check Railway Logs**:
   - Go to each service's "Logs" tab
   - Look for startup messages
   - Verify service is running

2. **Verify CORS Configuration**:
   - Check that `allow_origins=["*"]` is set
   - Check that `allow_credentials=False`
   - Check that `allow_methods=["*"]`

3. **Test API Directly**:
   - Open `https://bav-sav-api-production.up.railway.app/docs`
   - Try the endpoint from Swagger UI
   - Check if CORS headers are present in response

4. **Clear Browser Cache**:
   - Hard refresh (Ctrl+Shift+R or Cmd+Shift+R)
   - Or clear browser cache completely

### 404 Error for Auspicious Dates?

The endpoint `/api/v1/gochara/auspicious-dates` exists in the code. If you get 404:

1. **Verify Service is Deployed**:
   - Check Railway logs for Dasha/Gochara API
   - Ensure service started successfully

2. **Check Endpoint Registration**:
   - Open `https://dasha-gochara-api-production.up.railway.app/docs`
   - Look for `/api/v1/gochara/auspicious-dates` endpoint
   - If not visible, service needs redeployment

3. **Verify Route**:
   - The endpoint should be at: `POST /api/v1/gochara/auspicious-dates`
   - Not at: `/api/v1/auspicious-dates` or `/auspicious-dates`

## Expected Behavior After Fix

✅ **Before Fix**:
```
Access to fetch at 'https://bav-sav-api-production.up.railway.app/api/v1/calculate/full' 
from origin 'https://agent-app-production.up.railway.app' has been blocked by CORS policy
```

✅ **After Fix**:
- API calls succeed
- No CORS errors in console
- Data loads correctly in modals

## Verification Checklist

- [ ] Code changes committed and pushed
- [ ] BAV/SAV API service redeployed
- [ ] Dasha/Gochara API service redeployed
- [ ] Both services show successful deployment in logs
- [ ] Ashtakavarga modal loads without errors
- [ ] Auspicious Dates modal loads without errors
- [ ] No CORS errors in browser console

---

**Note**: Railway auto-deployment should pick up the changes, but if CORS errors persist, manually trigger a redeploy as described above.

