# Railway Logs Not Showing - Troubleshooting Guide

## 🔍 Where to Find Logs in Railway

### **Option 1: Runtime Logs Tab** ⭐ **PRIMARY LOCATION**

1. Railway Dashboard → Your Project
2. Click on **"Agent App"** service
3. Click **"Logs"** tab (NOT "Deployments")
4. This shows real-time application logs (stdout/stderr)

**What you'll see:**
- All `print()` statements
- Application errors
- Startup messages
- Runtime activity

---

### **Option 2: Deployments Tab** (Build/Startup Only)

1. Railway Dashboard → Agent App service
2. Click **"Deployments"** tab
3. Click on a specific deployment
4. Shows: Build logs, container startup, initial messages

**What you'll see:**
- Docker build output
- Dependency installation
- Container startup
- First few seconds of runtime

**Limitation:** Only shows logs during deployment, not ongoing runtime

---

## ❓ Why You Might Not See Logs

### **1. Looking at Wrong Tab**
- **Deployments tab:** Only shows build/startup (first few seconds)
- **Logs tab:** Shows ongoing runtime logs (what you need)

### **2. No Activity Yet**
- Logs only appear when something happens
- Make a request to the service to generate logs
- Or wait for healthcheck requests

### **3. Logs Are Buffered**
- Python `print()` might be buffered
- We've added `flush=True` to fix this
- May need to trigger activity to see logs

### **4. Service Not Running**
- Check if service status is "Running"
- If "Failed" or "Stopped", check Deployments tab for errors

### **5. UI Needs Refresh**
- Try refreshing the page
- Clear browser cache
- Try different browser

---

## 🧪 How to Generate Logs

### **Method 1: Make a Request**
1. Open your app in browser
2. Send a query
3. Check Logs tab - should see timing logs appear

### **Method 2: Healthcheck**
- Railway automatically pings `/health` endpoint
- Should see: `INFO: ... "GET /health HTTP/1.1" 200 OK`

### **Method 3: Manual Test**
```bash
curl https://your-agent-app.railway.app/health
```
Then check Logs tab

---

## 📋 What You Should See

### **On Startup (in Deployments tab):**
```
Starting Container
🔑 Supabase key configured: eyJ... (length: 215)
🔗 Supabase URL: https://...
✅ Supabase connection successful!
INFO: Started server process [1]
INFO: Application startup complete.
INFO: Uvicorn running on http://0.0.0.0:8080
```

### **On Each Request (in Logs tab):**
```
INFO: ... "GET /health HTTP/1.1" 200 OK
🔍 Calling BAV/SAV API with: ...
⏱️ BAV/SAV API call took 0.21s
✅ BAV/SAV data retrieved: ...
⏱️ retrieve_knowledge took 1.93s
⏱️ LLM call took 5.15s
```

---

## 🔧 Troubleshooting Steps

### **Step 1: Verify Service is Running**
- Railway Dashboard → Agent App
- Status should be "Running" (green)
- If not, check Deployments tab for errors

### **Step 2: Check Logs Tab**
- Click "Logs" tab (not Deployments)
- Should see real-time log stream
- If empty, make a request to generate logs

### **Step 3: Trigger Activity**
- Open app in browser
- Send a query
- Check Logs tab immediately after

### **Step 4: Check Deployments Tab**
- Click latest deployment
- Check for startup errors
- Look for Python errors, import errors

### **Step 5: Use Railway CLI** (Alternative)
```bash
railway logs --service agent-app
```

---

## ⚠️ Common Issues

### **Issue: "No logs available"**
**Solution:** 
- Make a request to generate logs
- Check if service is actually running
- Try refreshing the page

### **Issue: "Only see startup logs"**
**Solution:**
- You're in Deployments tab
- Switch to Logs tab for runtime logs

### **Issue: "Logs stop after startup"**
**Solution:**
- Service might have crashed
- Check Deployments tab for errors
- Check service status

### **Issue: "Can't find Logs tab"**
**Solution:**
- Make sure you're in the service view (not project view)
- Click on "Agent App" service first
- Then look for "Logs" tab

---

## 🎯 Quick Test

1. Go to Railway → Agent App → Logs tab
2. Open your app in browser: `https://your-agent-app.railway.app/chat`
3. Send a test query
4. Immediately check Logs tab
5. You should see timing logs appear in real-time

