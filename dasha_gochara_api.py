"""
FastAPI Server for Dasha/Bhukti and Gochara (Transit) Calculations
Uses extracted logic from OpenAIAstroPrediction and cosmicconnection repos
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
import swisseph as swe
import datetime

from calculators.dasha_calculator import (
    generate_dasa_table,
    generate_dasa_bhukti_table,
    get_current_dasa_bhukti
)
from calculators.transit_calculator import calculate_transits, calculate_auspicious_dates

app = FastAPI(
    title="Dasha/Gochara API",
    description="FastAPI endpoints for Dasha, Bhukti, and Gochara (Transit) calculations",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Swiss Ephemeris
swe.set_sid_mode(swe.SIDM_LAHIRI)


# ============================================================================
# PYDANTIC MODELS
# ============================================================================

class BirthData(BaseModel):
    dob: str = Field(..., description="Date of birth in YYYY-MM-DD format")
    tob: str = Field(..., description="Time of birth in HH:MM format")
    lat: float = Field(..., description="Latitude", ge=-90, le=90)
    lon: float = Field(..., description="Longitude", ge=-180, le=180)
    tz_offset: float = Field(..., description="Timezone offset from UTC")


class DashaPeriod(BaseModel):
    planet: str
    start_age: float
    end_age: float
    start_date: str
    end_date: str
    duration: float


class DashaResponse(BaseModel):
    birth_nakshatra: str
    birth_pada: int
    dasa_periods: List[DashaPeriod]


class BhuktiPeriod(BaseModel):
    maha_dasa: str
    bhukti: str
    start_date: str
    end_date: str
    duration: float


class DashaBhuktiResponse(BaseModel):
    birth_nakshatra: str
    birth_pada: int
    dasa_bhukti_table: List[BhuktiPeriod]


class CurrentDashaResponse(BaseModel):
    current_dasa: str
    current_bhukti: Optional[str]
    start_date: str
    end_date: str
    remaining_years: float
    age: float


class TransitAnalysis(BaseModel):
    planet: str
    natal_house: int
    transit_house: int
    transit_sign: str
    transit_degree: float
    nakshatra: str
    pada: int
    pada_lord: str
    activated_houses: List[int]
    score: float
    rag: Dict
    interpretation: Dict


class GocharaResponse(BaseModel):
    transit_date: str
    overall_health: Dict
    transit_analysis: List[TransitAnalysis]
    house_rankings: List[Dict]


class AuspiciousDate(BaseModel):
    date: str
    score: float
    base_score: float
    sav_modifier: float
    rag: Dict
    reasons: List[str]
    detailed_explanation: str
    planetary_details: List[Dict]
    sav_explanation: str
    overall_health: Dict
    transit_count: int
    green_count: int
    amber_count: int
    red_count: int


class AuspiciousDatesRequest(BaseModel):
    dob: str = Field(..., description="Date of birth in YYYY-MM-DD format")
    tob: str = Field(..., description="Time of birth in HH:MM format")
    lat: float = Field(..., description="Latitude", ge=-90, le=90)
    lon: float = Field(..., description="Longitude", ge=-180, le=180)
    tz_offset: float = Field(..., description="Timezone offset from UTC")
    month: str = Field(..., description="Month in YYYY-MM format (e.g., 2024-01)")
    sav_chart: Optional[List[int]] = Field(None, description="SAV chart (12 houses) to factor into scoring")
    top_n: int = Field(10, description="Number of top dates to return", ge=1, le=31)


class AuspiciousDatesResponse(BaseModel):
    month: str
    total_dates_analyzed: int
    top_5: List[AuspiciousDate]
    top_10: List[AuspiciousDate]
    all_dates: List[AuspiciousDate]


class HealthResponse(BaseModel):
    status: str
    version: str


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def calculate_julian_day(dob: str, tob: str, tz_offset: float) -> float:
    """Calculate Julian Day from birth data"""
    dob_date = datetime.datetime.strptime(dob, '%Y-%m-%d').date()
    tob_time = datetime.datetime.strptime(tob, '%H:%M').time()
    local_dt = datetime.datetime.combine(dob_date, tob_time)
    utc_dt = local_dt - datetime.timedelta(hours=tz_offset)
    return swe.julday(utc_dt.year, utc_dt.month, utc_dt.day, utc_dt.hour + utc_dt.minute/60.0)


def get_moon_longitude(jd: float) -> float:
    """Get Moon's longitude for Dasha calculations"""
    FLAGS = swe.FLG_SIDEREAL
    moon_result = swe.calc_ut(jd, swe.MOON, FLAGS)[0]
    return moon_result[0]


# ============================================================================
# API ENDPOINTS
# ============================================================================

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "version": "1.0.0"
    }


@app.post("/api/v1/dasha/calculate", response_model=DashaResponse)
async def calculate_dasha(birth_data: BirthData, total_years: int = 120):
    """
    Calculate Vimshottari Dasa periods.
    
    Returns all Dasa periods up to total_years (default 120 for full cycle).
    """
    try:
        jd = calculate_julian_day(birth_data.dob, birth_data.tob, birth_data.tz_offset)
        moon_longitude = get_moon_longitude(jd)
        
        birth_nakshatra, birth_pada, dasa_table = generate_dasa_table(
            jd, moon_longitude, total_years
        )
        
        return DashaResponse(
            birth_nakshatra=birth_nakshatra,
            birth_pada=birth_pada,
            dasa_periods=[DashaPeriod(**period) for period in dasa_table]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Calculation error: {str(e)}")


@app.post("/api/v1/dasha/bhukti", response_model=DashaBhuktiResponse)
async def calculate_dasha_bhukti(birth_data: BirthData):
    """
    Calculate Dasha-Bhukti table with all sub-periods.
    
    Returns complete Dasha-Bhukti table showing all Maha Dasa periods
    with their corresponding Bhukti (sub-period) breakdowns.
    """
    try:
        jd = calculate_julian_day(birth_data.dob, birth_data.tob, birth_data.tz_offset)
        moon_longitude = get_moon_longitude(jd)
        
        birth_nakshatra, birth_pada, bhukti_table = generate_dasa_bhukti_table(jd, moon_longitude)
        
        return DashaBhuktiResponse(
            birth_nakshatra=birth_nakshatra,
            birth_pada=birth_pada,
            dasa_bhukti_table=[BhuktiPeriod(**period) for period in bhukti_table]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Calculation error: {str(e)}")


@app.post("/api/v1/dasha/current", response_model=CurrentDashaResponse)
async def get_current_dasha(birth_data: BirthData, current_date: Optional[str] = None):
    """
    Get current Dasha and Bhukti periods.
    
    Returns the current Maha Dasa, Bhukti, remaining time, and age.
    If current_date is not provided, uses today's date.
    """
    try:
        jd = calculate_julian_day(birth_data.dob, birth_data.tob, birth_data.tz_offset)
        moon_longitude = get_moon_longitude(jd)
        
        if current_date:
            current_dt = datetime.datetime.strptime(current_date, '%Y-%m-%d')
        else:
            current_dt = datetime.datetime.now()
        
        current_info = get_current_dasa_bhukti(jd, moon_longitude, current_dt)
        
        return CurrentDashaResponse(**current_info)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Calculation error: {str(e)}")


@app.post("/api/v1/gochara/calculate", response_model=GocharaResponse)
async def calculate_gochara(birth_data: BirthData, transit_date: Optional[str] = None):
    """
    Calculate planetary transits (Gochara) for a specific date.
    
    Returns detailed transit analysis including:
    - Overall transit health (RAG scoring)
    - Individual planet transits with scores and interpretations
    - House activation rankings
    
    If transit_date is not provided, uses today's date.
    """
    try:
        result = calculate_transits(
            birth_data.dob,
            birth_data.tob,
            birth_data.lat,
            birth_data.lon,
            birth_data.tz_offset,
            transit_date
        )
        
        return GocharaResponse(
            transit_date=result['transit_date'],
            overall_health=result['overall_health'],
            transit_analysis=[TransitAnalysis(**ta) for ta in result['transit_analysis']],
            house_rankings=result['house_rankings']
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Calculation error: {str(e)}")


@app.post("/api/v1/gochara/current", response_model=GocharaResponse)
async def get_current_gochara(birth_data: BirthData):
    """
    Get current planetary transits (Gochara).
    
    Convenience endpoint that always uses today's date for transit analysis.
    """
    return await calculate_gochara(birth_data, transit_date=None)


@app.post("/api/v1/gochara/auspicious-dates", response_model=AuspiciousDatesResponse)
async def get_auspicious_dates(request: AuspiciousDatesRequest):
    """
    Calculate auspicious dates for a given month based on Gochara and BAV/SAV.
    
    Returns top 5 and top 10 dates ranked by transit scores, factoring in:
    - Planetary transits and their scores
    - SAV (Sarvashtakavarga) house strengths
    - Overall transit health
    
    **Scoring Logic:**
    - Base score: Average of all planetary transit scores
    - SAV Modifier: 
      - +5 points if planet transits house with SAV ≥30 (strong)
      - -3 points if planet transits house with SAV <22 (weak)
    - Final score: Base score + SAV modifier (capped at 0-100)
    
    **RAG Status:**
    - GREEN (≥70): Highly auspicious
    - AMBER (40-69): Moderately auspicious
    - RED (<40): Less auspicious
    """
    try:
        result = calculate_auspicious_dates(
            dob=request.dob,
            tob=request.tob,
            lat=request.lat,
            lon=request.lon,
            tz_offset=request.tz_offset,
            month=request.month,
            sav_chart=request.sav_chart,
            top_n=request.top_n
        )
        
        # Convert to response models
        return AuspiciousDatesResponse(
            month=result['month'],
            total_dates_analyzed=result['total_dates_analyzed'],
            top_5=[AuspiciousDate(**date) for date in result['top_5']],
            top_10=[AuspiciousDate(**date) for date in result['top_10']],
            all_dates=[AuspiciousDate(**date) for date in result['all_dates']]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Calculation error: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.environ.get("PORT", 8001))
    uvicorn.run(app, host="0.0.0.0", port=port)

