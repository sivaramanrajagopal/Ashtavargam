"""
LangChain Tools for Vedic Astrology API Integration
Tools that the agent can use to call BAV/SAV, Dasha, and Gochara APIs
"""

import os
import requests
from typing import Dict, List, Optional
from langchain_core.tools import tool
from pydantic import BaseModel, Field


# Get API URLs from environment or use defaults
BAV_SAV_API_URL = os.getenv("BAV_SAV_API_URL", "http://localhost:8000")
DASHA_GOCHARA_API_URL = os.getenv("DASHA_GOCHARA_API_URL", "http://localhost:8001")


class BirthDataModel(BaseModel):
    """Birth data model for API calls"""
    dob: str = Field(..., description="Date of birth in YYYY-MM-DD format")
    tob: str = Field(..., description="Time of birth in HH:MM format")
    lat: float = Field(..., description="Latitude")
    lon: float = Field(..., description="Longitude")
    tz_offset: float = Field(..., description="Timezone offset from UTC")


@tool
def calculate_bav_sav(birth_data: Dict) -> Dict:
    """
    Calculate BAV (Bhinnashtakavarga) and SAV (Sarvashtakavarga) charts.
    
    Use this tool when:
    - User asks about house strengths
    - User asks about Ashtakavarga
    - User wants to know which houses are strong/weak
    - User asks about planetary contributions to houses
    
    Args:
        birth_data: Dictionary with keys: dob, tob, lat, lon, tz_offset
    
    Returns:
        Dictionary containing BAV charts, SAV chart, totals, and planetary positions
    """
    try:
        response = requests.post(
            f"{BAV_SAV_API_URL}/api/v1/calculate/full",
            json=birth_data,
            timeout=30
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"Failed to calculate BAV/SAV: {str(e)}"}


@tool
def get_current_dasha(birth_data: Dict) -> Dict:
    """
    Get current Dasha and Bhukti periods.
    
    Use this tool when:
    - User asks about current planetary period
    - User asks "What Dasha am I in?"
    - User wants to know current Dasha/Bhukti
    - User asks about timing of events
    
    Args:
        birth_data: Dictionary with keys: dob, tob, lat, lon, tz_offset
    
    Returns:
        Dictionary containing current_dasa, current_bhukti, start_date, end_date, remaining_years, age
    """
    try:
        response = requests.post(
            f"{DASHA_GOCHARA_API_URL}/api/v1/dasha/current",
            json=birth_data,
            timeout=30
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"Failed to get Dasha data: {str(e)}"}


@tool
def get_dasha_periods(birth_data: Dict, total_years: int = 120) -> Dict:
    """
    Get all Dasha periods for the native's lifetime.
    
    Use this tool when:
    - User asks about future Dasha periods
    - User wants to see Dasha timeline
    - User asks "When will my Jupiter Dasha start?"
    
    Args:
        birth_data: Dictionary with keys: dob, tob, lat, lon, tz_offset
        total_years: Total years to calculate (default 120 for full cycle)
    
    Returns:
        Dictionary containing birth_nakshatra, birth_pada, and dasa_periods list
    """
    try:
        response = requests.post(
            f"{DASHA_GOCHARA_API_URL}/api/v1/dasha/calculate",
            json=birth_data,
            params={"total_years": total_years},
            timeout=30
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"Failed to get Dasha periods: {str(e)}"}


@tool
def get_current_gochara(birth_data: Dict) -> Dict:
    """
    Get current planetary transits (Gochara).
    
    Use this tool when:
    - User asks about current transits
    - User asks "What planets are affecting me now?"
    - User wants to know current planetary influences
    - User asks about transit effects
    
    Args:
        birth_data: Dictionary with keys: dob, tob, lat, lon, tz_offset
    
    Returns:
        Dictionary containing transit_date, overall_health, transit_analysis, house_rankings
    """
    try:
        response = requests.post(
            f"{DASHA_GOCHARA_API_URL}/api/v1/gochara/current",
            json=birth_data,
            timeout=30
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"Failed to get Gochara data: {str(e)}"}


@tool
def get_gochara_for_date(birth_data: Dict, transit_date: str) -> Dict:
    """
    Get planetary transits for a specific date.
    
    Use this tool when:
    - User asks about transits on a specific date
    - User wants to know future transit effects
    - User asks "What will transits be like on [date]?"
    
    Args:
        birth_data: Dictionary with keys: dob, tob, lat, lon, tz_offset
        transit_date: Date in YYYY-MM-DD format
    
    Returns:
        Dictionary containing transit analysis for the specified date
    """
    try:
        response = requests.post(
            f"{DASHA_GOCHARA_API_URL}/api/v1/gochara/calculate",
            json=birth_data,
            params={"transit_date": transit_date},
            timeout=30
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"Failed to get Gochara for date: {str(e)}"}


@tool
def get_dasha_bhukti_table(birth_data: Dict) -> Dict:
    """
    Get complete Dasha-Bhukti table with all sub-periods.
    
    Use this tool when:
    - User asks for detailed Dasha-Bhukti breakdown
    - User wants to see all sub-periods
    - User asks about specific Bhukti periods
    
    Args:
        birth_data: Dictionary with keys: dob, tob, lat, lon, tz_offset
    
    Returns:
        Dictionary containing birth_nakshatra, birth_pada, and dasa_bhukti_table
    """
    try:
        response = requests.post(
            f"{DASHA_GOCHARA_API_URL}/api/v1/dasha/bhukti",
            json=birth_data,
            timeout=30
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"Failed to get Dasha-Bhukti table: {str(e)}"}


def get_all_tools():
    """Get all astrology tools as a list for LangChain agent"""
    return [
        calculate_bav_sav,
        get_current_dasha,
        get_dasha_periods,
        get_current_gochara,
        get_gochara_for_date,
        get_dasha_bhukti_table
    ]

