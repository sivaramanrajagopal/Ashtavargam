# OpenAI API Key Error Fix

## Error
```
401 - Incorrect API key provided: sk-proj-...
```

## Problem
The `OPENAI_API_KEY` in Railway environment variables is either:
1. Incorrect/expired
2. Has extra spaces or characters
3. Truncated or corrupted
4. Not properly saved

## Solution: Fix OpenAI API Key in Railway

### Step 1: Get a Valid OpenAI API Key
1. Go to https://platform.openai.com/api-keys
2. Login to your OpenAI account
3. Click **"Create new secret key"**
4. Copy the **full key** (starts with `sk-proj-...` or `sk-...`)
5. **Save it immediately** - you won't see it again!

### Step 2: Update in Railway
1. Railway Dashboard → **Agent App** service
2. Go to **"Variables"** tab
3. Find `OPENAI_API_KEY`
4. Click to edit
5. **Delete the old value completely**
6. Paste the **new key** (no spaces, no quotes)
7. Click **"Save"** or **"Update"**

### Step 3: Verify Key Format
- ✅ Should start with `sk-proj-` or `sk-`
- ✅ No spaces before or after
- ✅ No quotes around it
- ✅ Full key (usually 50+ characters)
- ✅ Exact format: `OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxx`

### Step 4: Redeploy
1. Go to **"Deployments"** tab
2. Click **"Redeploy"** (or wait for auto-redeploy)
3. Wait for deployment to complete

### Step 5: Test Again
1. Try your query again
2. Should work now ✅

## Common Issues

### Issue 1: Key Has Spaces
**Wrong:**
```
OPENAI_API_KEY= sk-proj-...  ❌ (space after =)
OPENAI_API_KEY =sk-proj-...  ❌ (space before =)
```

**Correct:**
```
OPENAI_API_KEY=sk-proj-...  ✅ (no spaces)
```

### Issue 2: Key Has Quotes
**Wrong:**
```
OPENAI_API_KEY="sk-proj-..."  ❌
OPENAI_API_KEY='sk-proj-...'  ❌
```

**Correct:**
```
OPENAI_API_KEY=sk-proj-...  ✅ (no quotes)
```

### Issue 3: Key Truncated
- Make sure you copied the **full key**
- OpenAI keys are usually 50+ characters
- Check if it ends properly

### Issue 4: Key Expired/Revoked
- If key was revoked, create a new one
- Old keys won't work

## Quick Fix Checklist

- [ ] Get new OpenAI API key from platform.openai.com
- [ ] Go to Agent App → Variables tab
- [ ] Update `OPENAI_API_KEY` with new key
- [ ] Verify no spaces or quotes
- [ ] Save variables
- [ ] Redeploy Agent App
- [ ] Test query again

## Other Errors (Non-Critical)

### `/favicon.ico` 404 Error
- **Not critical** - just missing favicon file
- Can be ignored
- Doesn't affect functionality

### Grammarly Error
- **Browser extension error** - can be ignored
- Not related to your app
- Doesn't affect functionality

## After Fix

Once the API key is correct:
- ✅ Agent App will connect to OpenAI
- ✅ Queries will work
- ✅ LLM responses will be generated
- ✅ No more 401 errors

