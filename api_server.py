#!/usr/bin/env python3
"""
FastAPI Server for Ashtakavarga Calculations
RESTful API endpoints for BAV and SAV calculations
Safe to run alongside Flask app (different port)
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, validator
from typing import Dict, List, Optional
from datetime import datetime
import os
from ashtakavarga_calculator_final import AshtakavargaCalculatorFinal

# Initialize FastAPI app
app = FastAPI(
    title="Ashtakavarga Calculator API",
    description="RESTful API for Bhinnashtakavarga (BAV) and Sarvashtakavarga (SAV) calculations based on Parasara rules",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Enable CORS for AI agents and web clients
# Allow all origins for cross-origin requests
# IMPORTANT: Middleware order matters - CORS must be added before routes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=False,  # Must be False when using wildcard origins
    allow_methods=["*"],  # Allow all HTTP methods including OPTIONS
    allow_headers=["*"],  # Allow all headers
    expose_headers=["*"],  # Expose all headers
    max_age=3600,  # Cache preflight requests for 1 hour
)

# Add explicit OPTIONS handler for all routes (backup for CORS)
# This ensures OPTIONS requests are handled even if middleware fails
from fastapi.responses import Response

@app.options("/{full_path:path}")
async def options_handler(full_path: str):
    """Handle OPTIONS requests for CORS preflight - explicit handler"""
    return Response(
        status_code=200,
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS, HEAD, PATCH",
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Allow-Credentials": "false",
            "Access-Control-Max-Age": "3600",
        }
    )

# Also add OPTIONS handler for root and health endpoints
@app.options("/")
async def root_options():
    return Response(
        status_code=200,
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS, HEAD, PATCH",
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Max-Age": "3600",
        }
    )

@app.options("/health")
async def health_options():
    return Response(
        status_code=200,
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS, HEAD, PATCH",
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Max-Age": "3600",
        }
    )

# Pydantic Models for Request/Response

class BirthData(BaseModel):
    """Birth data model for calculations"""
    name: Optional[str] = Field(None, description="Name of the native")
    dob: str = Field(..., description="Date of birth in YYYY-MM-DD format")
    tob: str = Field(..., description="Time of birth in HH:MM format (24-hour)")
    place: Optional[str] = Field(None, description="Place of birth")
    latitude: float = Field(..., ge=-90, le=90, description="Latitude (-90 to 90)")
    longitude: float = Field(..., ge=-180, le=180, description="Longitude (-180 to 180)")
    tz_offset: float = Field(..., ge=-12, le=14, description="Timezone offset from UTC (-12 to 14)")
    
    @validator('dob')
    def validate_dob(cls, v):
        try:
            datetime.strptime(v, '%Y-%m-%d')
            return v
        except ValueError:
            raise ValueError('Date must be in YYYY-MM-DD format')
    
    @validator('tob')
    def validate_tob(cls, v):
        try:
            hour, minute = v.split(':')
            if not (0 <= int(hour) < 24 and 0 <= int(minute) < 60):
                raise ValueError
            return v
        except:
            raise ValueError('Time must be in HH:MM format (24-hour)')


class BAVResponse(BaseModel):
    """Response model for individual BAV"""
    planet: str
    bav_chart: List[int] = Field(..., description="12-element array (houses 1-12)")
    total: int = Field(..., description="Total bindus for this planet")
    planetary_position: Dict[str, int] = Field(..., description="Rasi positions of all planets")


class SAVResponse(BaseModel):
    """Response model for SAV"""
    sav_chart: List[int] = Field(..., description="12-element array (houses 1-12)")
    total: int = Field(..., description="Total bindus (should be 337)")
    house_strengths: Dict[str, str] = Field(..., description="Strength classification per house")


class FullCalculationResponse(BaseModel):
    """Response model for full calculation"""
    birth_data: Dict
    planetary_positions: Dict[str, int]
    planet_house_positions: Dict[str, int]
    bav_charts: Dict[str, List[int]]
    bav_totals: Dict[str, int]
    sav_chart: List[int]
    sav_total: int
    matrix_8x8: Dict
    calculation_timestamp: str


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    version: str
    calculator_available: bool


# API Endpoints

@app.get("/", response_model=HealthResponse)
async def root():
    """Root endpoint - Health check"""
    return {
        "status": "healthy",
        "version": "1.0.0",
        "calculator_available": True
    }


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint for monitoring"""
    return {
        "status": "healthy",
        "version": "1.0.0",
        "calculator_available": True
    }


@app.post("/api/v1/calculate/full", response_model=FullCalculationResponse)
async def calculate_full(birth_data: BirthData):
    """
    Calculate complete Ashtakavarga (all BAV charts + SAV)
    
    Returns all Bhinnashtakavarga charts for 8 planets (including Ascendant) 
    and Sarvashtakavarga (sum of 7 planets).
    
    **Expected BAV Totals:**
    - Sun: 48, Moon: 49, Mars: 39, Mercury: 54
    - Jupiter: 56, Venus: 52, Saturn: 39, Ascendant: 49
    
    **Expected SAV Total:** 337 bindus
    """
    try:
        birth_dict = birth_data.dict()
        calculator = AshtakavargaCalculatorFinal(birth_dict)
        calculator.calculate_all_charts()
        display_data = calculator.get_display_data()
        
        # Classify house strengths for SAV
        house_strengths = {}
        for i, points in enumerate(display_data['sarvashtakavarga'], 1):
            if points >= 30:
                house_strengths[str(i)] = "strong"
            elif points >= 28:
                house_strengths[str(i)] = "good"
            elif points < 22:
                house_strengths[str(i)] = "weak"
            else:
                house_strengths[str(i)] = "moderate"
        
        return FullCalculationResponse(
            birth_data=birth_dict,
            planetary_positions=display_data['planetary_positions'],
            planet_house_positions=display_data['planet_house_positions'],
            bav_charts=display_data['ashtakavarga_charts'],
            bav_totals=display_data['totals'],
            sav_chart=display_data['sarvashtakavarga'],
            sav_total=display_data['sarva_total'],
            matrix_8x8=display_data['matrix_8x8'],
            calculation_timestamp=datetime.now().isoformat()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Calculation error: {str(e)}")


@app.post("/api/v1/calculate/bav/{planet}", response_model=BAVResponse)
async def calculate_bav(planet: str, birth_data: BirthData):
    """
    Calculate Bhinnashtakavarga (BAV) for a specific planet
    
    **Supported planets:** SUN, MOON, MARS, MERCURY, JUPITER, VENUS, SATURN, ASCENDANT
    
    Returns BAV chart (12 houses) and total bindus for the specified planet.
    """
    planet = planet.upper()
    valid_planets = ['SUN', 'MOON', 'MARS', 'MERCURY', 'JUPITER', 'VENUS', 'SATURN', 'ASCENDANT']
    
    if planet not in valid_planets:
        raise HTTPException(
            status_code=400, 
            detail=f"Invalid planet. Must be one of: {', '.join(valid_planets)}"
        )
    
    try:
        birth_dict = birth_data.dict()
        calculator = AshtakavargaCalculatorFinal(birth_dict)
        calculator.calculate_all_charts()
        display_data = calculator.get_display_data()
        
        if planet not in display_data['ashtakavarga_charts']:
            raise HTTPException(status_code=500, detail=f"BAV calculation failed for {planet}")
        
        bav_chart = display_data['ashtakavarga_charts'][planet]
        
        return BAVResponse(
            planet=planet,
            bav_chart=bav_chart,
            total=sum(bav_chart),
            planetary_position=display_data['planetary_positions']
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Calculation error: {str(e)}")


@app.post("/api/v1/calculate/sav", response_model=SAVResponse)
async def calculate_sav(birth_data: BirthData):
    """
    Calculate Sarvashtakavarga (SAV) - Combined strength of all houses
    
    SAV is the sum of BAV charts for 7 planets (excluding Ascendant).
    Expected total: 337 bindus
    
    **House Strength Classification:**
    - >= 30: Strong (benefic)
    - >= 28: Good
    - >= 22: Moderate
    - < 22: Weak (malefic)
    """
    try:
        birth_dict = birth_data.dict()
        calculator = AshtakavargaCalculatorFinal(birth_dict)
        calculator.calculate_all_charts()
        display_data = calculator.get_display_data()
        
        sav_chart = display_data['sarvashtakavarga']
        sav_total = sum(sav_chart)
        
        # Classify house strengths
        house_strengths = {}
        for i, points in enumerate(sav_chart, 1):
            if points >= 30:
                house_strengths[str(i)] = "strong"
            elif points >= 28:
                house_strengths[str(i)] = "good"
            elif points >= 22:
                house_strengths[str(i)] = "moderate"
            else:
                house_strengths[str(i)] = "weak"
        
        return SAVResponse(
            sav_chart=sav_chart,
            total=sav_total,
            house_strengths=house_strengths
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Calculation error: {str(e)}")


@app.get("/api/v1/planets")
async def list_planets():
    """List all supported planets for BAV calculation"""
    return {
        "planets": [
            {"code": "SUN", "name": "Sun"},
            {"code": "MOON", "name": "Moon"},
            {"code": "MARS", "name": "Mars"},
            {"code": "MERCURY", "name": "Mercury"},
            {"code": "JUPITER", "name": "Jupiter"},
            {"code": "VENUS", "name": "Venus"},
            {"code": "SATURN", "name": "Saturn"},
            {"code": "ASCENDANT", "name": "Ascendant"}
        ]
    }


if __name__ == "__main__":
    import uvicorn
    
    # Get port from environment or use 8000 (Flask uses 5004)
    port = int(os.environ.get("PORT", 8000))
    
    print("🚀 Ashtakavarga Calculator API - FastAPI Server")
    print("=" * 60)
    print(f"📍 API Documentation: http://localhost:{port}/docs")
    print(f"📍 ReDoc: http://localhost:{port}/redoc")
    print(f"📍 Health Check: http://localhost:{port}/health")
    print(f"💡 Flask app runs on port 5004 (separate service)")
    print("=" * 60)
    
    uvicorn.run(app, host="0.0.0.0", port=port)

# Trigger BAV/SAV API redeploy - 2026-01-26 17:29:24
