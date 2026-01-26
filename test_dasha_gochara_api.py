"""
Test suite for Dasha/Gochara FastAPI endpoints
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8001"

# Test birth data (from user's example: 18-09-1978, 17:05, Chennai)
TEST_BIRTH_DATA = {
    "dob": "1978-09-18",
    "tob": "17:05",
    "lat": 13.0827,
    "lon": 80.2707,
    "tz_offset": 5.5
}


def test_health():
    """Test health check endpoint"""
    print("\n" + "="*60)
    print("Testing Health Check")
    print("="*60)
    
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
    print("✅ Health check passed")


def test_dasha_calculate():
    """Test Dasha calculation endpoint"""
    print("\n" + "="*60)
    print("Testing Dasha Calculation")
    print("="*60)
    
    response = requests.post(
        f"{BASE_URL}/api/v1/dasha/calculate",
        json=TEST_BIRTH_DATA,
        params={"total_years": 120}
    )
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Birth Nakshatra: {data['birth_nakshatra']}")
        print(f"Birth Pada: {data['birth_pada']}")
        print(f"Number of Dasa periods: {len(data['dasa_periods'])}")
        print("\nFirst 5 Dasa periods:")
        for period in data['dasa_periods'][:5]:
            print(f"  {period['planet']}: {period['start_age']:.2f} - {period['end_age']:.2f} years "
                  f"({period['start_date']} to {period['end_date']})")
        print("✅ Dasha calculation passed")
    else:
        print(f"❌ Error: {response.text}")
        assert False


def test_dasha_bhukti():
    """Test Dasha-Bhukti calculation endpoint"""
    print("\n" + "="*60)
    print("Testing Dasha-Bhukti Calculation")
    print("="*60)
    
    response = requests.post(
        f"{BASE_URL}/api/v1/dasha/bhukti",
        json=TEST_BIRTH_DATA
    )
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Birth Nakshatra: {data['birth_nakshatra']}")
        print(f"Birth Pada: {data['birth_pada']}")
        print(f"Total Bhukti periods: {len(data['dasa_bhukti_table'])}")
        print("\nFirst 10 Bhukti periods:")
        for period in data['dasa_bhukti_table'][:10]:
            print(f"  {period['maha_dasa']}-{period['bhukti']}: "
                  f"{period['start_date']} to {period['end_date']} "
                  f"({period['duration']:.2f} years)")
        print("✅ Dasha-Bhukti calculation passed")
    else:
        print(f"❌ Error: {response.text}")
        assert False


def test_current_dasha():
    """Test current Dasha endpoint"""
    print("\n" + "="*60)
    print("Testing Current Dasha")
    print("="*60)
    
    response = requests.post(
        f"{BASE_URL}/api/v1/dasha/current",
        json=TEST_BIRTH_DATA
    )
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Current Dasa: {data['current_dasa']}")
        print(f"Current Bhukti: {data['current_bhukti']}")
        print(f"Age: {data['age']:.2f} years")
        print(f"Remaining years in Dasa: {data['remaining_years']:.2f}")
        print(f"Period: {data['start_date']} to {data['end_date']}")
        print("✅ Current Dasha check passed")
    else:
        print(f"❌ Error: {response.text}")
        assert False


def test_gochara_calculate():
    """Test Gochara (transit) calculation endpoint"""
    print("\n" + "="*60)
    print("Testing Gochara Calculation")
    print("="*60)
    
    test_data = TEST_BIRTH_DATA.copy()
    test_data["transit_date"] = "2024-01-15"
    
    response = requests.post(
        f"{BASE_URL}/api/v1/gochara/calculate",
        json=TEST_BIRTH_DATA,
        params={"transit_date": "2024-01-15"}
    )
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Transit Date: {data['transit_date']}")
        print(f"Overall Health: {data['overall_health']['average_score']:.1f}/100")
        print(f"RAG Status: {data['overall_health']['rag']['status']} {data['overall_health']['rag']['emoji']}")
        print(f"Green: {data['overall_health']['green_count']}, "
              f"Amber: {data['overall_health']['amber_count']}, "
              f"Red: {data['overall_health']['red_count']}")
        print(f"\nNumber of transit analyses: {len(data['transit_analysis'])}")
        print("\nFirst 3 transit analyses:")
        for analysis in data['transit_analysis'][:3]:
            print(f"  {analysis['planet']}: H{analysis['transit_house']} "
                  f"(Score: {analysis['score']:.1f}, {analysis['rag']['status']})")
        print(f"\nTop 3 house rankings:")
        for ranking in data['house_rankings'][:3]:
            print(f"  H{ranking['house']} ({ranking['area']}): "
                  f"Score {ranking['weighted_score']:.1f}, "
                  f"{ranking['activation_count']} activations")
        print("✅ Gochara calculation passed")
    else:
        print(f"❌ Error: {response.text}")
        assert False


def test_current_gochara():
    """Test current Gochara endpoint"""
    print("\n" + "="*60)
    print("Testing Current Gochara")
    print("="*60)
    
    response = requests.post(
        f"{BASE_URL}/api/v1/gochara/current",
        json=TEST_BIRTH_DATA
    )
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Transit Date: {data['transit_date']}")
        print(f"Overall Health: {data['overall_health']['average_score']:.1f}/100")
        print(f"RAG Status: {data['overall_health']['rag']['status']} {data['overall_health']['rag']['emoji']}")
        print("✅ Current Gochara check passed")
    else:
        print(f"❌ Error: {response.text}")
        assert False


def run_all_tests():
    """Run all tests"""
    print("\n" + "="*60)
    print("DASHA/GOCHARA API TEST SUITE")
    print("="*60)
    print(f"Base URL: {BASE_URL}")
    print(f"Test Birth Data: {TEST_BIRTH_DATA}")
    print("\nMake sure the API server is running on port 8001!")
    print("Start it with: python dasha_gochara_api.py")
    print("\n" + "="*60)
    
    try:
        test_health()
        test_dasha_calculate()
        test_dasha_bhukti()
        test_current_dasha()
        test_gochara_calculate()
        test_current_gochara()
        
        print("\n" + "="*60)
        print("✅ ALL TESTS PASSED!")
        print("="*60)
    except requests.exceptions.ConnectionError:
        print("\n❌ Connection Error!")
        print("Make sure the API server is running on port 8001")
        print("Start it with: python dasha_gochara_api.py")
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    run_all_tests()

