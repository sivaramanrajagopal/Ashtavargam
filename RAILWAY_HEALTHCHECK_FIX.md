# Railway Healthcheck Failure - Troubleshooting Guide

## 🔴 Issue: Healthcheck Failed

**Error:**
```
1/1 replicas never became healthy!
Healthcheck failed!
Attempt #1-7 failed with service unavailable
```

## ✅ Fixed: Syntax Error

**Problem:**
- Syntax error in `agent_app/rag/supabase_rag.py`
- `len(self.supabase_key, flush=True)` - invalid syntax
- Service couldn't start, causing healthcheck to fail

**Fixed:**
- Corrected to: `len(self.supabase_key) > 10`
- `flush=True` moved to `print()` function
- Code pushed to main branch

---

## 🔍 Other Possible Causes

### 1. **Missing Environment Variables**
If service starts but healthcheck fails, check:
- `SUPABASE_URL` - Must be set
- `SUPABASE_KEY` - Must be set (service_role key)
- `OPENAI_API_KEY` - Must be set
- `BAV_SAV_API_URL` - Should be set
- `DASHA_GOCHARA_API_URL` - Should be set

### 2. **Port Binding Issues**
- Service must bind to `0.0.0.0:PORT`
- Railway sets `PORT` environment variable
- Check if service is listening on correct port

### 3. **Healthcheck Endpoint**
- Must respond to `GET /health`
- Should return 200 OK
- Should respond quickly (< 5s)

### 4. **Import Errors**
- Check if all dependencies are installed
- Check if Python version is compatible
- Check for missing modules

---

## 🧪 Verification Steps

### Step 1: Check Deployment Logs
1. Railway Dashboard → Agent App → Deployments
2. Click latest deployment
3. Check for:
   - ✅ "Build successful"
   - ✅ "Starting container"
   - ❌ Any Python errors
   - ❌ Import errors
   - ❌ Syntax errors

### Step 2: Check Runtime Logs
1. Railway Dashboard → Agent App → Logs
2. Look for:
   - `INFO: Application startup complete`
   - `INFO: Uvicorn running on http://0.0.0.0:8080`
   - `🔑 Supabase key configured: ...`
   - Any error messages

### Step 3: Test Healthcheck Manually
```bash
curl https://your-agent-app.railway.app/health
```

Should return:
```json
{"status": "healthy", "service": "agent"}
```

---

## 🔧 Quick Fixes

### If Healthcheck Still Fails:

1. **Check Environment Variables:**
   - Railway → Agent App → Variables
   - Verify all required vars are set
   - No typos in variable names

2. **Check Start Command:**
   - Railway → Agent App → Settings
   - Start Command should be:
     ```
     python -m uvicorn agent_app.main:app --host 0.0.0.0 --port 8080
     ```

3. **Check Dockerfile:**
   - Should use `Dockerfile.agent`
   - Should install all dependencies
   - Should expose port 8080

4. **Manual Redeploy:**
   - Railway → Agent App → Deployments
   - Click "Redeploy"

---

## 📋 Expected Startup Sequence

**Successful startup should show:**
```
INFO:     Started server process [1]
INFO:     Waiting for application startup.
🔑 Supabase key configured: eyJ... (length: XXX)
🔗 Supabase URL: https://...
✅ Supabase connection successful!
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8080
```

**If you see errors instead:**
- Check the error message
- Fix the underlying issue
- Redeploy

---

## 🚨 Common Errors

### Error: "ModuleNotFoundError"
**Fix:** Check `requirements_agent.txt` includes all dependencies

### Error: "Invalid API key"
**Fix:** Check environment variables in Railway

### Error: "Address already in use"
**Fix:** Check port configuration

### Error: "Connection refused"
**Fix:** Check healthcheck endpoint is accessible

