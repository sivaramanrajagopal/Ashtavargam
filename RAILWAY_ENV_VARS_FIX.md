# Railway Environment Variables Fix

## Error
```
ValidationError: 1 validation error for ChatOpenAI
Did not find openai_api_key, please add an environment variable `OPENAI_API_KEY`
```

## Problem
The Agent App service is missing environment variables, specifically `OPENAI_API_KEY`.

## Solution: Add Environment Variables to Agent App Service

### Step 1: Go to Agent App Service
1. Railway Dashboard
2. Click on **"Agent App"** service (the one that's failing)
3. Go to **"Variables"** tab

### Step 2: Add All Required Variables
Click **"New Variable"** or **"Raw Editor"** and add these:

```bash
SUPABASE_URL=https://sfoobtzxdajwlbbuvttx.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InNmb29idHp4ZGFqd2lbYnV2dHR4Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2OTI0NDUwNSwiZXhwIjoyMDg0ODIwNTA1fQ.hv6N7IAAmM3FvFF_B94oMHjKDG6wXrIQ87-UTXs
OPENAI_API_KEY=sk-proj-RdMZMpyHGCOliIYvvzjLpnVVzSFrSvP3_m1dbb77zfuZsRsqlhuLlTUKg7hY71CmlsC8LF_-0TBlbkFJOnOAEBKfeisSatHmMRRejXJu426fIoT9AwKQf0-kbCrGLEx5EJz9b18A
BAV_SAV_API_URL=https://placeholder-update-after-bav-api-deployed
DASHA_GOCHARA_API_URL=https://placeholder-update-after-dasha-api-deployed
MAX_MESSAGES=50
MAX_TOKENS=8000
RECENT_MESSAGES_COUNT=10
```

### Step 3: Save Variables
1. Click **"Save"** or **"Update"**
2. Railway will automatically redeploy the service

### Step 4: Wait for Redeployment
1. Go to **"Deployments"** tab
2. Watch for new deployment
3. Should complete successfully now ✅

## Critical Variables

The Agent App **requires** these variables to start:

1. **OPENAI_API_KEY** ⚠️ **CRITICAL** - Without this, the app cannot start
2. **SUPABASE_URL** - For RAG system
3. **SUPABASE_KEY** - For RAG system
4. **BAV_SAV_API_URL** - Can use placeholder for now
5. **DASHA_GOCHARA_API_URL** - Can use placeholder for now

## Quick Fix Checklist

- [ ] Go to Agent App service
- [ ] Click "Variables" tab
- [ ] Add `OPENAI_API_KEY` (most critical!)
- [ ] Add `SUPABASE_URL`
- [ ] Add `SUPABASE_KEY`
- [ ] Add `BAV_SAV_API_URL` (placeholder OK for now)
- [ ] Add `DASHA_GOCHARA_API_URL` (placeholder OK for now)
- [ ] Save variables
- [ ] Wait for auto-redeploy
- [ ] Check deployment logs - should start successfully

## After Adding Variables

The Agent App should:
1. ✅ Start without errors
2. ✅ Initialize ChatOpenAI with API key
3. ✅ Connect to Supabase
4. ✅ Be ready to receive requests

## Note

You can update `BAV_SAV_API_URL` and `DASHA_GOCHARA_API_URL` later after you deploy those services. For now, placeholders are fine - the app will start but those features won't work until the APIs are deployed.

