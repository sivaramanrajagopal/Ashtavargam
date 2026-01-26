# Dasha/Gochara API Documentation

FastAPI RESTful API for Dasha, Bhukti, and Gochara (Transit) calculations. This API uses extracted and adapted logic from:
- **Dasha/Bhukti**: OpenAIAstroPrediction repository
- **Gochara/Transit**: cosmicconnection repository

## Quick Start

### Run API Server

```bash
python dasha_gochara_api.py
```

The API will run on **port 8001** by default (BAV/SAV API runs on 8000, so no conflicts).

### Using Environment Variables

```bash
PORT=8001 python dasha_gochara_api.py
```

## API Endpoints

### Base URL
- **Development:** `http://localhost:8001`
- **Production:** `https://your-domain.com`

### Interactive Documentation
- **Swagger UI:** `http://localhost:8001/docs`
- **ReDoc:** `http://localhost:8001/redoc`

---

## Endpoints

### 1. Health Check

**GET** `/health`

Check if the API is running.

**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0"
}
```

---

### 2. Calculate Dasha Periods

**POST** `/api/v1/dasha/calculate`

Calculate Vimshottari Dasa periods (120-year cycle).

**Request Body:**
```json
{
  "dob": "1978-09-18",
  "tob": "17:05",
  "lat": 13.0827,
  "lon": 80.2707,
  "tz_offset": 5.5
}
```

**Query Parameters:**
- `total_years` (optional): Total years to calculate (default: 120)

**Response:**
```json
{
  "birth_nakshatra": "Purva Phalguni",
  "birth_pada": 1,
  "dasa_periods": [
    {
      "planet": "Jupiter",
      "start_age": 0.0,
      "end_age": 16.0,
      "start_date": "1978-09-18",
      "end_date": "1994-09-18",
      "duration": 16.0
    },
    {
      "planet": "Saturn",
      "start_age": 16.0,
      "end_age": 35.0,
      "start_date": "1994-09-18",
      "end_date": "2013-09-18",
      "duration": 19.0
    },
    ...
  ]
}
```

**Dasa Durations:**
- Ketu: 7 years
- Venus: 20 years
- Sun: 6 years
- Moon: 10 years
- Mars: 7 years
- Rahu: 18 years
- Jupiter: 16 years
- Saturn: 19 years
- Mercury: 17 years

---

### 3. Calculate Dasha-Bhukti Table

**POST** `/api/v1/dasha/bhukti`

Calculate complete Dasha-Bhukti table with all sub-periods.

**Request Body:**
```json
{
  "dob": "1978-09-18",
  "tob": "17:05",
  "lat": 13.0827,
  "lon": 80.2707,
  "tz_offset": 5.5
}
```

**Response:**
```json
{
  "birth_nakshatra": "Purva Phalguni",
  "birth_pada": 1,
  "dasa_bhukti_table": [
    {
      "maha_dasa": "Jupiter",
      "bhukti": "Jupiter",
      "start_date": "1978-09-18",
      "end_date": "1980-03-15",
      "duration": 1.5
    },
    {
      "maha_dasa": "Jupiter",
      "bhukti": "Saturn",
      "start_date": "1980-03-15",
      "end_date": "1982-06-20",
      "duration": 2.3
    },
    ...
  ]
}
```

**Note:** This returns all Bhukti sub-periods for all 120 years of Dasa periods.

---

### 4. Get Current Dasha/Bhukti

**POST** `/api/v1/dasha/current`

Get current Dasha and Bhukti periods.

**Request Body:**
```json
{
  "dob": "1978-09-18",
  "tob": "17:05",
  "lat": 13.0827,
  "lon": 80.2707,
  "tz_offset": 5.5,
  "current_date": "2024-01-15"
}
```

**Query Parameters:**
- `current_date` (optional): Date to check (YYYY-MM-DD format, defaults to today)

**Response:**
```json
{
  "current_dasa": "Saturn",
  "current_bhukti": "Venus",
  "start_date": "2020-01-15",
  "end_date": "2025-06-20",
  "remaining_years": 1.4,
  "age": 45.3
}
```

---

### 5. Calculate Gochara (Transits)

**POST** `/api/v1/gochara/calculate`

Calculate planetary transits (Gochara) for a specific date.

**Request Body:**
```json
{
  "dob": "1978-09-18",
  "tob": "17:05",
  "lat": 13.0827,
  "lon": 80.2707,
  "tz_offset": 5.5
}
```

**Query Parameters:**
- `transit_date` (optional): Date for transit analysis (YYYY-MM-DD format, defaults to today)

**Response:**
```json
{
  "transit_date": "2024-01-15",
  "overall_health": {
    "average_score": 65.5,
    "rag": {
      "status": "AMBER",
      "emoji": "🟡",
      "label": "Neutral/Mixed"
    },
    "green_count": 3,
    "amber_count": 4,
    "red_count": 2,
    "total_planets": 9
  },
  "transit_analysis": [
    {
      "planet": "Jupiter",
      "natal_house": 6,
      "transit_house": 5,
      "transit_sign": "Leo",
      "transit_degree": 12.5,
      "nakshatra": "Magha",
      "pada": 2,
      "pada_lord": "Ketu",
      "activated_houses": [5, 7, 9],
      "score": 72.5,
      "rag": {
        "status": "GREEN",
        "emoji": "🟢",
        "label": "Positive/Supportive"
      },
      "interpretation": {
        "impact": "Jupiter is favorably positioned, bringing positive energy to Intelligence & Children",
        "advice": "Good time to focus on creativity, children, romance. Take proactive steps.",
        "life_areas": ["Intelligence & Children", "Partnership & Marriage", "Fortune & Higher Learning"]
      }
    },
    ...
  ],
  "house_rankings": [
    {
      "house": 5,
      "area": "Intelligence & Children",
      "themes": ["creativity", "children", "romance", "speculation", "intellect"],
      "activation_count": 3,
      "planets": ["Jupiter", "Mars", "Mercury"],
      "quality_score": 90,
      "weighted_score": 85.2,
      "rag": {
        "status": "GREEN",
        "emoji": "🟢",
        "label": "Positive/Supportive"
      }
    },
    ...
  ]
}
```

**RAG Scoring:**
- **GREEN (🟢)**: Score >= 70 - Positive/Supportive
- **AMBER (🟡)**: Score 40-69 - Neutral/Mixed
- **RED (🔴)**: Score < 40 - Challenging

---

### 6. Get Current Gochara

**POST** `/api/v1/gochara/current`

Get current planetary transits (convenience endpoint that always uses today's date).

**Request Body:**
```json
{
  "dob": "1978-09-18",
  "tob": "17:05",
  "lat": 13.0827,
  "lon": 80.2707,
  "tz_offset": 5.5
}
```

**Response:** Same format as `/gochara/calculate`

---

## Testing

### Run Test Suite

```bash
# Start the API server first
python dasha_gochara_api.py

# In another terminal, run tests
python test_dasha_gochara_api.py
```

### Manual Testing with cURL

```bash
# Health check
curl http://localhost:8001/health

# Calculate Dasha
curl -X POST http://localhost:8001/api/v1/dasha/calculate \
  -H "Content-Type: application/json" \
  -d '{
    "dob": "1978-09-18",
    "tob": "17:05",
    "lat": 13.0827,
    "lon": 80.2707,
    "tz_offset": 5.5
  }'

# Get current Dasha
curl -X POST http://localhost:8001/api/v1/dasha/current \
  -H "Content-Type: application/json" \
  -d '{
    "dob": "1978-09-18",
    "tob": "17:05",
    "lat": 13.0827,
    "lon": 80.2707,
    "tz_offset": 5.5
  }'

# Calculate Gochara
curl -X POST "http://localhost:8001/api/v1/gochara/calculate?transit_date=2024-01-15" \
  -H "Content-Type: application/json" \
  -d '{
    "dob": "1978-09-18",
    "tob": "17:05",
    "lat": 13.0827,
    "lon": 80.2707,
    "tz_offset": 5.5
  }'
```

---

## Integration with AI Agents

These endpoints are designed to be used by AI agents (LangGraph, LangChain, etc.) for deterministic astrological calculations.

### Example: LangChain Tool

```python
from langchain.tools import tool
import requests

@tool
def get_current_dasha(birth_data: dict) -> dict:
    """Get current Dasha and Bhukti periods for birth data"""
    response = requests.post(
        "http://localhost:8001/api/v1/dasha/current",
        json=birth_data
    )
    return response.json()

@tool
def calculate_transits(birth_data: dict, transit_date: str = None) -> dict:
    """Calculate planetary transits for a specific date"""
    params = {}
    if transit_date:
        params['transit_date'] = transit_date
    response = requests.post(
        "http://localhost:8001/api/v1/gochara/calculate",
        json=birth_data,
        params=params
    )
    return response.json()
```

---

## Error Handling

All endpoints return standard HTTP status codes:

- **200**: Success
- **400**: Bad Request (invalid input data)
- **500**: Internal Server Error (calculation error)

Error response format:
```json
{
  "detail": "Error message description"
}
```

---

## Notes

1. **Swiss Ephemeris**: Uses Lahiri Ayanamsa (sidereal calculations)
2. **Dasa System**: Vimshottari Dasa (120-year cycle)
3. **Transit Scoring**: Based on house quality, planetary nature, and dignity
4. **RAG System**: Red/Amber/Green scoring for transit health assessment

---

## Dependencies

- `fastapi`
- `uvicorn[standard]`
- `pydantic`
- `pyswisseph`
- `python-dateutil` (for date handling)

---

## Architecture

```
dasha_gochara_api.py (FastAPI server)
├── calculators/
│   ├── dasha_calculator.py (Dasha/Bhukti logic)
│   └── transit_calculator.py (Gochara/Transit logic)
└── test_dasha_gochara_api.py (Test suite)
```

The calculation logic is extracted from existing repositories and adapted for FastAPI integration, ensuring proven accuracy while providing clean REST API endpoints.

