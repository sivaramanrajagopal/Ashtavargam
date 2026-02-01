# How to Check Performance Logs

## 🔍 Real-Time Log Monitoring

### Method 1: View Server Output Directly
The server is running in the background. To see real-time logs:

```bash
# Find the server process
ps aux | grep uvicorn

# The logs are going to stdout, but since it's running in background,
# you need to restart it in foreground to see logs
```

### Method 2: Restart Server in Foreground (Recommended)
```bash
# Stop current server
pkill -f "uvicorn.*agent_app"

# Start in foreground to see all logs
cd /Users/sivaramanrajagopal/Ashtavargam
python3 -m uvicorn agent_app.main:app --host 0.0.0.0 --port 8080
```

### Method 3: Filter Performance Logs
When server is running, look for these log patterns:

**Performance Timing Logs:**
- `⏱️` - Timing indicators
- `took` - Duration measurements
- `API call took` - API response times
- `Total agent_graph.invoke took` - Total processing time

**Example Performance Logs:**
```
⏱️ BAV/SAV API call took 0.20s
⏱️ Dasha API call took 0.20s
⏱️ Gochara API call took 0.20s
⏱️ Total calculate_chart_data took 0.61s
⏱️ retrieve_knowledge took 1.01s
⏱️ LLM call took 11.06s
⏱️ Total analyze_and_interpret took 11.06s
⏱️ Total agent_graph.invoke took 12.69s
```

## 📊 Performance Bottlenecks to Check

### 1. API Calls (Should be < 1s each)
Look for:
- `BAV/SAV API call took` - Should be < 0.5s
- `Dasha API call took` - Should be < 0.5s
- `Gochara API call took` - Should be < 0.5s

**If slow:**
- Check if APIs are running
- Check network latency
- Check API server logs

### 2. RAG Retrieval (Should be < 2s)
Look for:
- `retrieve_knowledge took` - Should be < 2s
- `Embedding generation took` - Should be < 1s

**If slow:**
- Check Supabase connection
- Check embedding API (OpenAI)
- Check vector search performance

### 3. LLM Calls (Usually 5-15s)
Look for:
- `LLM call took` - Usually 5-15s (this is normal)
- `Total analyze_and_interpret took` - Should be < 20s

**If very slow (>30s):**
- Check OpenAI API status
- Check network connection
- Check if timeout is too high

### 4. Total Request Time
Look for:
- `Total agent_graph.invoke took` - Total time for entire request

**Expected:**
- First request: 10-15s (with API calls)
- Cached requests: 6-12s (without API calls)

## 🐛 Common Performance Issues

### Issue 1: Slow API Calls
**Symptoms:**
- `API call took` > 1s
- Timeouts

**Check:**
```bash
# Test API endpoints directly
curl -X POST http://localhost:8000/api/v1/calculate/full \
  -H "Content-Type: application/json" \
  -d '{"dob":"1978-09-18","tob":"17:05","latitude":13.08,"longitude":80.28,"tz_offset":5.5}'
```

### Issue 2: Slow RAG Retrieval
**Symptoms:**
- `retrieve_knowledge took` > 5s
- `Embedding generation took` > 3s

**Check:**
- Supabase connection
- OpenAI embedding API status
- Network latency

### Issue 3: Slow LLM Calls
**Symptoms:**
- `LLM call took` > 30s
- Timeouts

**Check:**
- OpenAI API status: https://status.openai.com
- Network connection
- API key validity

## 📝 Log File Locations

### Current Logs
- **Server Output:** stdout (if running in foreground)
- **Old Logs:** `agent_logs.txt` (if redirected)

### Create Log File
To save logs to file:
```bash
# Stop current server
pkill -f "uvicorn.*agent_app"

# Start with log redirection
cd /Users/sivaramanrajagopal/Ashtavargam
python3 -m uvicorn agent_app.main:app --host 0.0.0.0 --port 8080 2>&1 | tee agent_logs.txt
```

## 🔧 Quick Performance Check

Run this to see current performance:
```bash
# Make a test request and time it
time curl -X POST http://localhost:8080/api/chat/message \
  -H "Content-Type: application/json" \
  -d '{"session_id":"test","message":"What is my 1st house?"}'
```

## 📊 Performance Benchmarks

**Good Performance:**
- API calls: < 0.5s each
- RAG retrieval: < 2s
- LLM call: 5-15s
- Total request: 8-15s (first), 6-10s (cached)

**Needs Optimization:**
- API calls: > 1s
- RAG retrieval: > 5s
- LLM call: > 30s
- Total request: > 20s

