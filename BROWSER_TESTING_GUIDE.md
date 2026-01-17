# Browser Testing Guide - FastAPI Endpoints

## 🚀 Quick Start

### Step 1: Start the API Server

The server is already running! If not, run:
```bash
python3 api_server.py
```

You should see:
```
🚀 Ashtakavarga Calculator API - FastAPI Server
============================================================
📍 API Documentation: http://localhost:8000/docs
📍 ReDoc: http://localhost:8000/redoc
📍 Health Check: http://localhost:8000/health
```

---

## 🌐 Method 1: Interactive Swagger UI (EASIEST)

### Step 2: Open Swagger UI in Browser

1. **Open your web browser**
2. **Navigate to:** `http://localhost:8000/docs`
3. You'll see an interactive API documentation page

### Step 3: Test Health Endpoint (GET)

1. Find **`GET /health`** section
2. Click **"Try it out"** button
3. Click **"Execute"** button
4. Scroll down to see the response:
   ```json
   {
     "status": "healthy",
     "version": "1.0.0",
     "calculator_available": true
   }
   ```

### Step 4: Test Full Calculation (POST)

1. Find **`POST /api/v1/calculate/full`** section
2. Click **"Try it out"** button
3. You'll see a Request body editor
4. **Replace the example JSON** with this test data:
   ```json
   {
     "name": "Test User",
     "dob": "1978-09-18",
     "tob": "17:35",
     "place": "Chennai",
     "latitude": 13.0827,
     "longitude": 80.2707,
     "tz_offset": 5.5
   }
   ```
5. Click **"Execute"** button
6. Scroll down to see the full response with:
   - `sav_total`: Should be **337**
   - `bav_totals`: All 8 planets with their totals
   - `bav_charts`: Full BAV arrays for each planet

### Step 5: Test Individual BAV (POST)

1. Find **`POST /api/v1/calculate/bav/{planet}`** section
2. Click **"Try it out"** button
3. In the **Parameters** section:
   - **planet**: Enter `SUN` (or MOON, MARS, etc.)
4. In the **Request body**, paste:
   ```json
   {
     "dob": "1978-09-18",
     "tob": "17:35",
     "latitude": 13.0827,
     "longitude": 80.2707,
     "tz_offset": 5.5
   }
   ```
5. Click **"Execute"** button
6. Check response:
   - `total`: Should be **48** for Sun
   - `bav_chart`: Array of 12 numbers

### Step 6: Test SAV Calculation (POST)

1. Find **`POST /api/v1/calculate/sav`** section
2. Click **"Try it out"** button
3. Paste the same request body as above
4. Click **"Execute"** button
5. Check response:
   - `total`: Should be **337**
   - `house_strengths`: Object with strength for each house

### Step 7: Test List Planets (GET)

1. Find **`GET /api/v1/planets`** section
2. Click **"Try it out"** → **"Execute"**
3. See list of all 8 supported planets

---

## 🌐 Method 2: Direct URL Testing (Simple GET endpoints)

### Health Check
Just open in browser:
```
http://localhost:8000/health
```

### List Planets
Open in browser:
```
http://localhost:8000/api/v1/planets
```

You'll see JSON response directly in the browser.

---

## 🌐 Method 3: Browser Developer Tools (For POST requests)

### Step 1: Open Browser Developer Tools

1. Press `F12` (Windows/Linux) or `Cmd+Option+I` (Mac)
2. Go to **Console** tab

### Step 2: Test Full Calculation

Paste this JavaScript code in the console:

```javascript
fetch('http://localhost:8000/api/v1/calculate/full', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    name: "Test User",
    dob: "1978-09-18",
    tob: "17:35",
    place: "Chennai",
    latitude: 13.0827,
    longitude: 80.2707,
    tz_offset: 5.5
  })
})
.then(response => response.json())
.then(data => {
  console.log('✅ Full Calculation Results:');
  console.log('SAV Total:', data.sav_total);
  console.log('Sun BAV Total:', data.bav_totals.SUN);
  console.log('Sun BAV Chart:', data.bav_charts.SUN);
  console.log('Full Data:', data);
})
.catch(error => console.error('Error:', error));
```

### Step 3: Test SAV

```javascript
fetch('http://localhost:8000/api/v1/calculate/sav', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    dob: "1978-09-18",
    tob: "17:35",
    latitude: 13.0827,
    longitude: 80.2707,
    tz_offset: 5.5
  })
})
.then(r => r.json())
.then(d => {
  console.log('✅ SAV Results:');
  console.log('Total:', d.total);
  console.log('House Strengths:', d.house_strengths);
});
```

### Step 4: Test Individual BAV

```javascript
fetch('http://localhost:8000/api/v1/calculate/bav/SUN', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    dob: "1978-09-18",
    tob: "17:35",
    latitude: 13.0827,
    longitude: 80.2707,
    tz_offset: 5.5
  })
})
.then(r => r.json())
.then(d => {
  console.log('✅ Sun BAV:');
  console.log('Total:', d.total);
  console.log('Chart:', d.bav_chart);
});
```

---

## 📋 Test Checklist

Use this checklist to verify all endpoints:

- [ ] **GET /health** - Returns `{"status": "healthy"}`
- [ ] **GET /api/v1/planets** - Returns list of 8 planets
- [ ] **POST /api/v1/calculate/full** - Returns all BAV + SAV
  - [ ] `sav_total` = 337
  - [ ] `bav_totals.SUN` = 48
  - [ ] `bav_totals.MOON` = 49
  - [ ] All 8 planets in `bav_charts`
- [ ] **POST /api/v1/calculate/bav/SUN** - Returns Sun BAV
  - [ ] `total` = 48
  - [ ] `bav_chart` has 12 elements
- [ ] **POST /api/v1/calculate/sav** - Returns SAV
  - [ ] `total` = 337
  - [ ] `house_strengths` has 12 houses

---

## 🎯 Expected Results

### Full Calculation Response Should Include:

```json
{
  "sav_total": 337,  ← Should be exactly 337
  "bav_totals": {
    "SUN": 48,      ← Should be 48
    "MOON": 49,     ← Should be 49
    "MARS": 39,     ← Should be 39
    "MERCURY": 54,  ← Should be 54
    "JUPITER": 56,  ← Should be 56
    "VENUS": 52,    ← Should be 52
    "SATURN": 39,   ← Should be 39
    "ASCENDANT": 49 ← Should be 49
  },
  "bav_charts": {
    "SUN": [1, 4, 6, 7, 4, 4, 3, 3, 3, 4, 5, 4],  ← 12 numbers
    ...
  },
  "sav_chart": [24, 24, 32, 36, ...]  ← 12 numbers, sum = 337
}
```

---

## 🐛 Troubleshooting

### Server Not Starting?
```bash
# Check if port 8000 is already in use
lsof -i :8000

# Kill any process on port 8000
kill -9 $(lsof -t -i:8000)

# Start server again
python3 api_server.py
```

### Cannot Access http://localhost:8000
- Make sure server is running (check terminal output)
- Try `http://127.0.0.1:8000` instead
- Check firewall settings

### CORS Errors in Browser Console?
- FastAPI has CORS enabled by default
- If issues persist, check `api_server.py` CORS settings

### JSON Errors?
- Make sure request body is valid JSON
- Use Swagger UI which handles JSON validation automatically

---

## 📸 Screenshots to Take

While testing, take screenshots of:
1. Swagger UI page (`/docs`)
2. Full calculation response
3. SAV calculation response
4. Any errors (if they occur)

These will help verify the API is working correctly.

---

## ✅ Ready to Commit?

After testing all endpoints successfully:
1. ✅ All endpoints respond correctly
2. ✅ Calculations match expected values (337 SAV, correct BAV totals)
3. ✅ No errors in browser console
4. ✅ JSON responses are properly formatted

**Then you're ready to commit!** 🚀

