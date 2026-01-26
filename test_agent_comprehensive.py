#!/usr/bin/env python3
"""
Comprehensive test script for the Agent API
Tests various query types and verifies responses use actual data
"""

import requests
import json
import time

BASE_URL = "http://localhost:8080"
BIRTH_DATA = {
    "dob": "1978-09-18",
    "tob": "17:35",
    "latitude": 13.0827,
    "longitude": 80.2707,
    "tz_offset": 5.5,
    "name": "Test User",
    "place": "Chennai"
}

def test_query(query, expected_keywords=None):
    """Test a single query and check for expected keywords"""
    print(f"\n{'='*60}")
    print(f"Query: {query}")
    print(f"{'='*60}")
    
    try:
        # Start a chat session
        session_response = requests.post(
            f"{BASE_URL}/api/chat/start",
            json={"birth_data": BIRTH_DATA},
            timeout=10
        )
        
        if session_response.status_code != 200:
            print(f"❌ Failed to start session: {session_response.status_code}")
            return False
        
        session_data = session_response.json()
        session_id = session_data.get("session_id")
        
        if not session_id:
            print(f"❌ No session ID returned")
            return False
        
        print(f"✅ Session started: {session_id}")
        
        # Send query
        query_response = requests.post(
            f"{BASE_URL}/api/chat/message",
            json={
                "session_id": session_id,
                "message": query
            },
            timeout=120  # 2 minutes for complex queries
        )
        
        if query_response.status_code != 200:
            print(f"❌ Query failed: {query_response.status_code}")
            print(f"   Response: {query_response.text[:200]}")
            return False
        
        result = query_response.json()
        response_text = result.get("response", "")
        
        print(f"\n📝 Response (first 500 chars):")
        print(f"{response_text[:500]}...")
        
        # Check for expected keywords
        if expected_keywords:
            found = []
            missing = []
            for keyword in expected_keywords:
                if keyword.lower() in response_text.lower():
                    found.append(keyword)
                else:
                    missing.append(keyword)
            
            print(f"\n✅ Found keywords: {found}")
            if missing:
                print(f"⚠️  Missing keywords: {missing}")
                return False
        
        # Check for generic responses
        generic_phrases = [
            "I need your birth details",
            "Dasha is not mentioned",
            "chart data is not available",
            "if your house has",
            "I would need",
            "cannot determine"
        ]
        
        found_generic = []
        for phrase in generic_phrases:
            if phrase.lower() in response_text.lower():
                found_generic.append(phrase)
        
        if found_generic:
            print(f"⚠️  Generic phrases found: {found_generic}")
            return False
        
        print(f"✅ Query passed")
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("🧪 Comprehensive Agent API Test Suite")
    print("="*60)
    
    # Test cases
    test_cases = [
        {
            "query": "Tell me about my current dasa",
            "expected_keywords": ["Moon", "Dasha", "Bhukti", "Mercury"]
        },
        {
            "query": "What's my 7th house like?",
            "expected_keywords": ["7th", "house", "SAV", "points"]
        },
        {
            "query": "What are my SAV points for each house?",
            "expected_keywords": ["SAV", "house"]
        },
        {
            "query": "Tell me about my transits",
            "expected_keywords": ["transit", "Gochara"]
        },
        {
            "query": "What's my 1st house strength?",
            "expected_keywords": ["1st", "house", "SAV", "points"]
        }
    ]
    
    results = []
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n\n🔍 Test {i}/{len(test_cases)}")
        passed = test_query(
            test_case["query"],
            test_case.get("expected_keywords")
        )
        results.append({
            "test": test_case["query"],
            "passed": passed
        })
        time.sleep(2)  # Small delay between tests
    
    # Summary
    print(f"\n\n{'='*60}")
    print("📊 Test Summary")
    print(f"{'='*60}")
    
    passed_count = sum(1 for r in results if r["passed"])
    total_count = len(results)
    
    for i, result in enumerate(results, 1):
        status = "✅ PASS" if result["passed"] else "❌ FAIL"
        print(f"{i}. {status}: {result['test']}")
    
    print(f"\n✅ Passed: {passed_count}/{total_count}")
    print(f"❌ Failed: {total_count - passed_count}/{total_count}")
    
    if passed_count == total_count:
        print("\n🎉 All tests passed!")
        return 0
    else:
        print("\n⚠️  Some tests failed")
        return 1

if __name__ == "__main__":
    exit(main())

