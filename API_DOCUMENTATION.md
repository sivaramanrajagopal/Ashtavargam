# Ashtakavarga Calculator API Documentation

FastAPI RESTful API for deterministic BAV and SAV calculations. Safe to run alongside Flask app on a different port.

## Quick Start

### Run API Server
```bash
python api_server.py
```

The API will run on **port 8000** by default (Flask runs on 5004, so no conflicts).

### Using Docker (optional)
```bash
docker build -t ashtakavarga-api .
docker run -p 8000:8000 ashtakavarga-api
```

## API Endpoints

### Base URL
- **Development:** `http://localhost:8000`
- **Production:** `https://your-domain.com`

### Interactive Documentation
- **Swagger UI:** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`

---

## Endpoints

### 1. Health Check

**GET** `/health`

Check if the API is running.

**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "calculator_available": true
}
```

---

### 2. Full Calculation

**POST** `/api/v1/calculate/full`

Calculate all BAV charts + SAV in one request.

**Request Body:**
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

**Response:**
```json
{
  "birth_data": {...},
  "planetary_positions": {
    "SUN": 6,
    "MOON": 12,
    ...
  },
  "planet_house_positions": {
    "SUN": 8,
    "MOON": 2,
    ...
  },
  "bav_charts": {
    "SUN": [1, 4, 6, 7, ...],  // 12 houses
    "MOON": [...],
    ...
  },
  "bav_totals": {
    "SUN": 48,
    "MOON": 49,
    ...
  },
  "sav_chart": [28, 30, 25, ...],  // 12 houses
  "sav_total": 337,
  "matrix_8x8": {...},
  "calculation_timestamp": "2024-01-01T12:00:00"
}
```

**Expected BAV Totals:**
- Sun: 48, Moon: 49, Mars: 39, Mercury: 54
- Jupiter: 56, Venus: 52, Saturn: 39, Ascendant: 49

**Expected SAV Total:** 337 bindus

---

### 3. Individual BAV Calculation

**POST** `/api/v1/calculate/bav/{planet}`

Calculate BAV for a specific planet only.

**Path Parameters:**
- `planet`: One of `SUN`, `MOON`, `MARS`, `MERCURY`, `JUPITER`, `VENUS`, `SATURN`, `ASCENDANT`

**Request Body:** (same as full calculation)

**Example:**
```bash
POST /api/v1/calculate/bav/SUN
```

**Response:**
```json
{
  "planet": "SUN",
  "bav_chart": [1, 4, 6, 7, 4, 4, 3, 3, 3, 4, 5, 4],  // 12 houses
  "total": 48,
  "planetary_position": {
    "SUN": 6,
    "MOON": 12,
    ...
  }
}
```

---

### 4. SAV Calculation

**POST** `/api/v1/calculate/sav`

Calculate Sarvashtakavarga (combined strength) only.

**Request Body:** (same as full calculation)

**Response:**
```json
{
  "sav_chart": [28, 30, 25, 32, 28, 26, 29, 31, 27, 28, 30, 33],
  "total": 337,
  "house_strengths": {
    "1": "good",
    "2": "strong",
    "3": "moderate",
    ...
  }
}
```

**House Strength Classification:**
- `>= 30`: strong (benefic)
- `>= 28`: good
- `>= 22`: moderate
- `< 22`: weak (malefic)

---

### 5. List Planets

**GET** `/api/v1/planets`

Get list of all supported planets.

**Response:**
```json
{
  "planets": [
    {"code": "SUN", "name": "Sun"},
    {"code": "MOON", "name": "Moon"},
    ...
  ]
}
```

---

## Usage Examples

### Python

```python
import requests

# Full calculation
response = requests.post(
    "http://localhost:8000/api/v1/calculate/full",
    json={
        "dob": "1978-09-18",
        "tob": "17:35",
        "latitude": 13.0827,
        "longitude": 80.2707,
        "tz_offset": 5.5
    }
)
data = response.json()
print(f"Sun BAV: {data['bav_charts']['SUN']}")
print(f"SAV Total: {data['sav_total']}")

# Individual BAV
response = requests.post(
    "http://localhost:8000/api/v1/calculate/bav/SUN",
    json={...}
)
sun_bav = response.json()
print(f"Sun BAV Total: {sun_bav['total']}")
```

### cURL

```bash
# Full calculation
curl -X POST "http://localhost:8000/api/v1/calculate/full" \
  -H "Content-Type: application/json" \
  -d '{
    "dob": "1978-09-18",
    "tob": "17:35",
    "latitude": 13.0827,
    "longitude": 80.2707,
    "tz_offset": 5.5
  }'

# SAV only
curl -X POST "http://localhost:8000/api/v1/calculate/sav" \
  -H "Content-Type: application/json" \
  -d '{...}'
```

### JavaScript/Fetch

```javascript
// Full calculation
const response = await fetch('http://localhost:8000/api/v1/calculate/full', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    dob: '1978-09-18',
    tob: '17:35',
    latitude: 13.0827,
    longitude: 80.2707,
    tz_offset: 5.5
  })
});

const data = await response.json();
console.log('SAV Total:', data.sav_total);
console.log('Sun BAV:', data.bav_charts.SUN);
```

---

## For AI Agents

### Deterministic Calculations

All calculations use the same logic as the Flask app (`AshtakavargaCalculatorFinal`). Results are deterministic:

- Same input → Same output
- No randomness
- Reproducible across different calls

### Error Handling

All endpoints return proper HTTP status codes:
- `200`: Success
- `400`: Bad request (invalid input)
- `500`: Server error (calculation failure)

### Validation

Input is validated using Pydantic models:
- Date format: `YYYY-MM-DD`
- Time format: `HH:MM` (24-hour)
- Latitude: -90 to 90
- Longitude: -180 to 180
- Timezone: -12 to 14

---

## Running Both Flask and FastAPI

### Option 1: Separate Terminals

```bash
# Terminal 1: Flask app
python app_complete.py  # Runs on port 5004

# Terminal 2: FastAPI
python api_server.py    # Runs on port 8000
```

### Option 2: Production with Gunicorn + Uvicorn

```bash
# Flask (port 5004)
gunicorn -w 4 -b 0.0.0.0:5004 app_complete:app

# FastAPI (port 8000)
uvicorn api_server:app --host 0.0.0.0 --port 8000
```

### Option 3: Process Manager (PM2)

```bash
pm2 start app_complete.py --name flask-app --interpreter python3
pm2 start api_server.py --name fastapi-api --interpreter python3
```

---

## Railway Deployment

Both can be deployed on Railway as separate services:

1. **Flask App Service:**
   - Port: 5004
   - Procfile: `web: python app_complete.py`

2. **FastAPI Service:**
   - Port: 8000
   - Procfile: `web: python api_server.py` or `web: uvicorn api_server:app --host 0.0.0.0 --port $PORT`

---

## Notes

- ✅ Flask app remains untouched
- ✅ Both can run simultaneously (different ports)
- ✅ Same calculation logic (deterministic)
- ✅ FastAPI provides interactive docs at `/docs`
- ✅ CORS enabled for web/AI agent access
- ✅ Production-ready with proper error handling

