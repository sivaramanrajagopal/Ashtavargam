# Railway Environment Variables Verification

## Error
The Agent App is still showing:
```
ValidationError: Did not find openai_api_key, please add an environment variable `OPENAI_API_KEY`
```

## Problem
Even though you added environment variables, the service is still not finding them.

## Solution: Verify Environment Variables Are Set Correctly

### Step 1: Double-Check You're in the Right Service
1. Railway Dashboard
2. Make sure you're in **"Agent App"** service (NOT BAV/SAV API)
3. The service name should be **"Agent App"**

### Step 2: Verify Variables Tab
1. Click on **"Agent App"** service
2. Go to **"Variables"** tab
3. Check that these variables exist:

```bash
OPENAI_API_KEY=sk-proj-RdMZMpyHGCOliIYvvzjLpnVVzSFrSvP3_m1dbb77zfuZsRsqlhuLlTUKg7hY71CmlsC8LF_-0TBlbkFJOnOAEBKfeisSatHmMRRejXJu426fIoT9AwKQf0-kbCrGLEx5EJz9b18A
SUPABASE_URL=https://sfoobtzxdajwlbbuvttx.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InNmb29idHp4ZGFqd2lbYnV2dHR4Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2OTI0NDUwNSwiZXhwIjoyMDg0ODIwNTA1fQ.hv6N7IAAmM3FvFF_B94oMHjKDG6wXrIQ87-UTXs
```

### Step 3: Check Variable Format
- **Variable Name**: `OPENAI_API_KEY` (exact, case-sensitive)
- **Variable Value**: Should start with `sk-proj-...`
- **No spaces** around the `=` sign
- **No quotes** around the value

### Step 4: Save Variables
1. After adding/verifying variables
2. Click **"Save"** or **"Update"** button
3. Railway should show a confirmation

### Step 5: Force Redeploy
1. Go to **"Deployments"** tab
2. Click **"Redeploy"** button (or wait for auto-redeploy)
3. This ensures the new environment variables are loaded

## Common Issues

### Issue 1: Variables Added to Wrong Service
**Problem**: Added variables to BAV/SAV API instead of Agent App
**Solution**: Make sure you're in **"Agent App"** service

### Issue 2: Variables Not Saved
**Problem**: Added variables but didn't click "Save"
**Solution**: Click "Save" button after adding variables

### Issue 3: Typo in Variable Name
**Problem**: `OPENAI_API_KEY` vs `OPENAI_APIKEY` vs `OPENAI_KEY`
**Solution**: Must be exactly `OPENAI_API_KEY` (case-sensitive)

### Issue 4: Service Not Redeployed
**Problem**: Variables added but service not redeployed
**Solution**: Go to Deployments → Click "Redeploy"

## Step-by-Step Verification

1. ✅ Go to Railway Dashboard
2. ✅ Click on **"Agent App"** service (verify service name)
3. ✅ Go to **"Variables"** tab
4. ✅ Check `OPENAI_API_KEY` exists
5. ✅ Verify value starts with `sk-proj-...`
6. ✅ Check `SUPABASE_URL` exists
7. ✅ Check `SUPABASE_KEY` exists
8. ✅ Click **"Save"** if you made changes
9. ✅ Go to **"Deployments"** tab
10. ✅ Click **"Redeploy"** to force reload

## Alternative: Use Raw Editor

If the UI is confusing, use **"Raw Editor"**:

1. Variables tab → Click **"Raw Editor"**
2. Paste this format:
```
OPENAI_API_KEY=sk-proj-RdMZMpyHGCOliIYvvzjLpnVVzSFrSvP3_m1dbb77zfuZsRsqlhuLlTUKg7hY71CmlsC8LF_-0TBlbkFJOnOAEBKfeisSatHmMRRejXJu426fIoT9AwKQf0-kbCrGLEx5EJz9b18A
SUPABASE_URL=https://sfoobtzxdajwlbbuvttx.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InNmb29idHp4ZGFqd2lbYnV2dHR4Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2OTI0NDUwNSwiZXhwIjoyMDg0ODIwNTA1fQ.hv6N7IAAmM3FvFF_B94oMHjKDG6wXrIQ87-UTXs
BAV_SAV_API_URL=https://placeholder
DASHA_GOCHARA_API_URL=https://placeholder
```

3. Click **"Save"**
4. Redeploy

## After Fixing

Once variables are correctly set and service is redeployed:
1. Check deployment logs
2. Should see service starting successfully
3. No more `OPENAI_API_KEY` errors
4. Healthcheck should pass

## Quick Checklist

- [ ] In **"Agent App"** service (not BAV API)
- [ ] `OPENAI_API_KEY` variable exists
- [ ] Value is correct (starts with `sk-proj-...`)
- [ ] `SUPABASE_URL` variable exists
- [ ] `SUPABASE_KEY` variable exists
- [ ] Clicked **"Save"** button
- [ ] Service redeployed after saving
- [ ] Check deployment logs for success

