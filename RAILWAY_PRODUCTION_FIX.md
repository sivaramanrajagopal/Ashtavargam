# Railway Production Issues - Fix Guide

## 🔴 Issue 1: Supabase API Key Error

**Error:**
```
Invalid API key
Double check your Supabase `anon` or `service_role` API key.
```

**Root Cause:**
- `SUPABASE_KEY` environment variable is missing or incorrect in Railway
- Must use `service_role` key (not `anon` key) for server-side operations

**Fix Steps:**

1. **Get Supabase Service Role Key:**
   - Go to Supabase Dashboard → Settings → API
   - Copy the `service_role` key (NOT the `anon` key)
   - ⚠️ Keep this secret! It has full database access

2. **Add to Railway Environment Variables:**
   - Go to Railway → Agent App service → Variables tab
   - Add/Update:
     ```
     SUPABASE_URL=https://your-project.supabase.co
     SUPABASE_KEY=your-service-role-key-here
     ```
   - Click "Save"

3. **Redeploy:**
   - Railway will auto-redeploy when you save variables
   - Or manually trigger redeploy

---

## 🔴 Issue 2: LLM Timeout

**Error:**
```
openai.APITimeoutError: Request timed out.
LLM call took 29.88s (exceeds 15s timeout)
```

**Root Cause:**
- Network latency in production
- LLM calls taking longer than 15s timeout
- Timeout might not be enforced properly

**Fix Steps:**

1. **Increase LLM Timeout:**
   - Current: 15s
   - Recommended: 30s for production (network can be slower)

2. **Add Better Error Handling:**
   - Graceful fallback if timeout occurs
   - Retry logic for transient failures

---

## ✅ Quick Fix Commands

### For Supabase Key:
1. Check Railway Variables:
   - Railway Dashboard → Agent App → Variables
   - Verify `SUPABASE_URL` and `SUPABASE_KEY` are set

2. Verify Key Format:
   - Should start with `eyJ...` (JWT token)
   - Should be `service_role` key (not `anon`)

### For LLM Timeout:
- Increase timeout from 15s to 30s
- Add retry logic
- Better error messages

---

## 🧪 Verification

After fixes, check logs for:
- ✅ No more "Invalid API key" errors
- ✅ RAG retrieval working (should see context retrieved)
- ✅ LLM calls completing within timeout
- ✅ Total query time: ~10-15s (not 30s+)

