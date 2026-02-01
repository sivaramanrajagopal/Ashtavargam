# Railway CLI - View Logs Guide

## ✅ Service Status
Your service is **WORKING** - health endpoint responds correctly!

## 📋 Steps to View Logs with Railway CLI

### Step 1: Link Project
```bash
railway link
```

**What happens:**
- Railway CLI will show list of your projects
- Select the project that contains "Agent App" service
- This links your local directory to the Railway project

### Step 2: View Logs
```bash
# View all logs for linked project
railway logs

# Or view logs for specific service
railway logs --service agent-app
```

**What you'll see:**
- Real-time log stream
- All print() statements
- HTTP requests
- Errors and warnings

---

## 🔍 Alternative: Railway Web UI

If CLI doesn't work, try web UI:

1. **Go to Railway Dashboard**
2. **Select your project**
3. **Click "Agent App" service**
4. **Look for:**
   - "Logs" tab
   - "View Logs" button
   - "Metrics" tab (might show some logs)

---

## 🧪 Quick Test

Since service is working:

1. **Open app:** https://agent-app-production.up.railway.app/chat
2. **Send a query:** "What's my 7th house like?"
3. **Check logs immediately after** (CLI or UI)
4. **Should see timing logs appear**

---

## 📊 Expected Log Output

After making a request, you should see:
```
INFO: ... "POST /api/chat/message HTTP/1.1" 200 OK
🔍 Calling BAV/SAV API with: ...
⏱️ BAV/SAV API call took 0.21s
✅ BAV/SAV data retrieved: ...
⏱️ retrieve_knowledge took 1.93s
⏱️ LLM call took 5.15s
⏱️ Total agent_graph.invoke took 7.54s
```

---

## ⚠️ If Logs Still Don't Show

1. **Service is working** (health check passes)
2. **Logs might be buffered** (wait a few seconds)
3. **Try making a request** to generate logs
4. **Check Railway UI** (different location)
5. **Use Railway CLI** (most reliable)

