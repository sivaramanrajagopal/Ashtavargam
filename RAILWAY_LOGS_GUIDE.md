# Railway Logs Guide

## 📊 Where to Find Logs in Railway

### 1. **Deploy Logs** (Build/Startup)
- Railway Dashboard → Your Service → **Deployments** tab
- Click on a deployment → See build and startup logs
- Shows: Docker build, dependencies, startup messages

### 2. **Runtime Logs** (Application Output) ⭐ **THIS IS WHAT YOU NEED**
- Railway Dashboard → Your Service → **Logs** tab
- Shows: All `print()` statements, errors, stdout/stderr
- Real-time streaming logs
- This is where you'll see our debug messages

### 3. **Metrics** (HTTP/Network)
- Railway Dashboard → Your Service → **Metrics** tab
- Shows: HTTP requests, response times, network traffic
- This is what you're currently seeing

---

## 🔍 How to See Debug Logs

### Option 1: Check Runtime Logs Tab
1. Go to Railway Dashboard
2. Select "Agent App" service
3. Click **"Logs"** tab (NOT "Deployments")
4. You should see:
   - `🔑 Supabase key configured: eyJ...`
   - `✅ Supabase connection successful!` or `❌ Supabase connection failed`
   - All the `⏱️` timing logs

### Option 2: Use Railway CLI
```bash
railway logs --service agent-app
```

### Option 3: Check if Logs are Buffered
- Railway might buffer Python `print()` statements
- We've added `sys.stdout.flush()` to ensure immediate output

---

## 📋 What You Should See

After the latest deploy, in **Runtime Logs**, you should see:

**On Startup:**
```
🔑 Supabase key configured: eyJ... (length: XXX)
🔗 Supabase URL: https://...
✅ Supabase connection successful!
```

**On Each Query:**
```
🔍 Calling BAV/SAV API with: ...
⏱️ BAV/SAV API call took 0.21s
✅ BAV/SAV data retrieved: ...
⏱️ retrieve_knowledge took X.XXs
⏱️ LLM call took X.XXs
```

---

## ⚠️ If You Don't See Logs

1. **Check Logs Tab** (not Deployments)
2. **Refresh** the logs view
3. **Make a query** to trigger log output
4. **Check if service is running** (should show "Running" status)

---

## 🧪 Test Query

Send a query through the app, then check **Logs** tab - you should see all the timing logs appear in real-time.

