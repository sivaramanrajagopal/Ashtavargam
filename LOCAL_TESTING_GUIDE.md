# Local Testing Guide for Phase 1 Optimizations

## 🚀 Quick Start

### **Step 1: Ensure Environment Variables**

Create or check `.env` file in project root:

```bash
# Required environment variables
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
OPENAI_API_KEY=your_openai_api_key
BAV_SAV_API_URL=http://localhost:8000
DASHA_GOCHARA_API_URL=http://localhost:8001
```

### **Step 2: Start Required Services**

You need 3 services running:

1. **BAV/SAV API** (Port 8000)
2. **Dasha/Gochara API** (Port 8001)
3. **Agent App** (Port 8080)

---

## 📋 Detailed Setup

### **Option A: Start All Services Manually**

#### **Terminal 1: BAV/SAV API**
```bash
cd /Users/sivaramanrajagopal/Ashtavargam
python3 -m uvicorn api_server:app --host 0.0.0.0 --port 8000
```

#### **Terminal 2: Dasha/Gochara API**
```bash
cd /Users/sivaramanrajagopal/Ashtavargam
python3 -m uvicorn dasha_gochara_api:app --host 0.0.0.0 --port 8001
```

#### **Terminal 3: Agent App**
```bash
cd /Users/sivaramanrajagopal/Ashtavargam
python3 -m uvicorn agent_app.main:app --host 0.0.0.0 --port 8080
```

### **Option B: Use Start Scripts (if available)**

Check if you have:
- `start_all_servers.sh`
- `start_agent.sh`
- `start_dasha_gochara.sh`

---

## 🧪 Testing Steps

### **Step 1: Verify Services Are Running**

Open browser and check:

1. **BAV/SAV API Health:**
   ```
   http://localhost:8000/health
   ```
   Should return: `{"status":"healthy",...}`

2. **Dasha/Gochara API Health:**
   ```
   http://localhost:8001/health
   ```
   Should return: `{"status":"healthy",...}`

3. **Agent App Health:**
   ```
   http://localhost:8080/health
   ```
   Should return: `{"status":"healthy",...}`

### **Step 2: Open Chat Interface**

Open in browser:
```
http://localhost:8080/chat
```

### **Step 3: Test Queries**

#### **Test 1: Simple House Query**
1. Enter birth details:
   - DOB: 1978-09-18
   - TOB: 17:35
   - Lat: 13.0827
   - Lon: 80.2707
   - TZ: 5.5

2. Click "Start Chat"

3. Ask: **"What's my 7th house like?"**

4. **Measure time:**
   - Note start time when you click "Send"
   - Note end time when response appears
   - Calculate: End - Start = Response Time

5. **Verify quality:**
   - Response should mention actual SAV points
   - Should list individual BAV contributions
   - Should be specific (not generic)

#### **Test 2: Dasha Query**
Ask: **"Tell me about my current dasa"**

- Should mention current Dasha and Bhukti
- Should include dates and remaining years
- Response time should be faster

#### **Test 3: Gochara Query**
Ask: **"What are my current transits?"**

- Should mention transit scores
- Should include RAG status (GREEN/AMBER/RED)
- Response time should be faster

#### **Test 4: Complex Query**
Ask: **"Analyze my 7th and 10th houses"**

- Should analyze both houses
- Should be specific to each house
- Response time should be reasonable

---

## ⏱️ Performance Measurement

### **Method 1: Browser DevTools**

1. Open browser DevTools (F12)
2. Go to **Network** tab
3. Filter by **Fetch/XHR**
4. Send a query
5. Check the `/api/chat/message` request:
   - **Time**: Shows total request time
   - **Wait**: Shows server processing time

### **Method 2: Manual Timing**

1. Note time before clicking "Send"
2. Note time when response appears
3. Calculate difference

### **Method 3: Add Timing Logs (Optional)**

Add to `agent_app/main.py`:
```python
import time

@app.post("/api/chat/message")
async def send_chat_message(request: ChatMessageRequest):
    start_time = time.time()
    result = conversation_manager.process_message(...)
    duration = time.time() - start_time
    print(f"⏱️ Query took {duration:.2f}s")
    return result
```

---

## ✅ Expected Results

### **Before Phase 1:**
- Response time: 15-20 seconds

### **After Phase 1:**
- Response time: 12-17 seconds (2-3 seconds faster)
- Response quality: Should be maintained (same accuracy)

### **What to Check:**

1. **Functionality:**
   - ✅ Responses are accurate
   - ✅ SAV/BAV data is correct
   - ✅ Dasha data is correct
   - ✅ Gochara data is correct

2. **Performance:**
   - ✅ Response time is faster
   - ✅ No timeouts
   - ✅ No errors

3. **Quality:**
   - ✅ Responses are specific (not generic)
   - ✅ Uses actual chart data
   - ✅ Citations are present

---

## 🐛 Troubleshooting

### **Issue: Services won't start**

**Check:**
1. Ports are not in use:
   ```bash
   lsof -i :8000
   lsof -i :8001
   lsof -i :8080
   ```

2. Dependencies installed:
   ```bash
   pip install -r requirements_agent.txt
   ```

3. Environment variables set:
   ```bash
   echo $OPENAI_API_KEY
   echo $SUPABASE_URL
   ```

### **Issue: "Failed to fetch" errors**

**Check:**
1. All services are running
2. CORS is configured correctly
3. API URLs in `.env` are correct

### **Issue: Slow responses**

**Check:**
1. Network latency (local should be fast)
2. API services are responding quickly
3. Check server logs for errors

---

## 📊 Comparison Testing

### **Test Before/After:**

1. **Before Phase 1:**
   ```bash
   git checkout main
   # Start services and test
   ```

2. **After Phase 1:**
   ```bash
   git checkout performance-optimization
   # Start services and test
   ```

3. **Compare:**
   - Response times
   - Response quality
   - Error rates

---

## 🎯 Success Criteria

Phase 1 is successful if:

- ✅ Response time reduced by 2-3 seconds
- ✅ Response quality maintained (same accuracy)
- ✅ No new errors introduced
- ✅ All query types work correctly
- ✅ No timeouts or failures

---

## 📝 Test Checklist

- [ ] All 3 services start successfully
- [ ] Health checks pass
- [ ] Chat interface loads
- [ ] Simple house query works (7th house)
- [ ] Dasha query works
- [ ] Gochara query works
- [ ] Complex query works (multiple houses)
- [ ] Response time is faster
- [ ] Response quality is maintained
- [ ] No errors in console/logs

---

## 🚀 Next Steps After Testing

If tests pass:

1. **Push to remote:**
   ```bash
   git push origin performance-optimization
   ```

2. **Proceed to Phase 2:**
   - Chart Data Caching
   - Expected: -5 to -8 seconds (for follow-up queries)

If tests fail:

1. **Check logs for errors**
2. **Revert if needed:**
   ```bash
   git reset --hard v-working-before-optimization
   ```
3. **Debug and fix issues**

---

## 💡 Pro Tips

1. **Use browser DevTools** for accurate timing
2. **Test multiple query types** to ensure all work
3. **Compare before/after** to see improvements
4. **Check server logs** for any warnings/errors
5. **Test with different birth data** to ensure robustness

