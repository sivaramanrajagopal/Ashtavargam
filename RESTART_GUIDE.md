# Server Restart Guide for Phase 1 Optimizations

## 🔄 What Needs Restarting?

### **Agent App Server (Port 8080) - REQUIRED**
**Why:** We changed code in:
- `agent_app/graphs/astrology_agent_graph.py` (timing logs, cache checks)
- `agent_app/conversation/manager.py` (timing logs)

**Options:**

#### **Option 1: If using `--reload` flag (Auto-reload)**
If you started the agent server with:
```bash
uvicorn agent_app.main:app --host 0.0.0.0 --port 8080 --reload
```

✅ **No restart needed!** FastAPI will auto-reload when files change.

Just wait a few seconds after the code changes, and you'll see:
```
INFO:     Detected file change in 'agent_app/graphs/astrology_agent_graph.py'. Reloading...
INFO:     Application startup complete.
```

#### **Option 2: If NOT using `--reload` flag**
❌ **Restart required!**

**Quick Restart:**
1. Stop the agent server (Ctrl+C in the terminal)
2. Restart:
   ```bash
   python3 -m uvicorn agent_app.main:app --host 0.0.0.0 --port 8080 --reload
   ```

---

### **BAV/SAV API (Port 8000) - NOT NEEDED**
✅ **No restart needed** - We didn't change this code

### **Dasha/Gochara API (Port 8001) - NOT NEEDED**
✅ **No restart needed** - We didn't change this code

---

## 🧪 How to Verify New Code is Loaded

### **Check 1: Look for timing logs**
After sending a query, check the agent server terminal. You should see:
```
⏱️ BAV/SAV API call took X.XXs
⏱️ Dasha API call took X.XXs
⏱️ Gochara API call took X.XXs
⏱️ Total calculate_chart_data took X.XXs
```

**If you DON'T see these logs:** Code hasn't reloaded yet.

### **Check 2: Look for cache messages**
On second query, you should see:
```
✅ Using cached BAV/SAV data
✅ Using cached Dasha data
✅ Using cached Gochara data
```

**If you DON'T see these:** Cache check isn't working (code not loaded).

---

## 🚀 Recommended: Use `--reload` Flag

For development, always use `--reload` so you don't need to manually restart:

```bash
# Terminal 3: Agent App (with auto-reload)
python3 -m uvicorn agent_app.main:app --host 0.0.0.0 --port 8080 --reload
```

**Benefits:**
- ✅ Auto-reloads on code changes
- ✅ No manual restart needed
- ✅ Faster development cycle

---

## 📋 Quick Checklist

- [ ] Check if agent server has `--reload` flag
- [ ] If yes: Wait for auto-reload (check terminal for reload message)
- [ ] If no: Restart agent server manually
- [ ] Test query and verify timing logs appear
- [ ] Test second query and verify cache messages appear

---

## ⚠️ Important Notes

1. **Old sessions are fine** - Existing chat sessions will continue working
2. **Cache is per-session** - Each session has its own cache
3. **First query always calculates** - Cache only helps on follow-up queries
4. **Timing logs appear in server terminal** - Not in browser console

---

## 🔍 Troubleshooting

### **Issue: No timing logs appearing**

**Solution:**
1. Check if agent server is running
2. Check if code was saved
3. Check if `--reload` detected the change
4. If not, restart manually

### **Issue: Cache not working**

**Solution:**
1. Verify code changes are loaded (check for timing logs)
2. Make sure you're using the same session (same birth data)
3. Check server logs for cache messages

