#!/usr/bin/env python3
"""
Test script to verify the therapy search functionality.
"""
import requests
import json

def test_therapy_search():
    """Test the therapy search endpoint."""
    
    # Test data with both English and non-English issues
    test_issues = [
        "I feel anxious about my future",
        "I'm struggling with loneliness",
        "I need guidance and peace",
        "I feel lost and need direction",
        "أشعر بالقلق حول مستقبلي",  # Arabic: I feel anxious about my future
        "Je me sens perdu et j'ai besoin de direction",  # French: I feel lost and need direction
        "Me siento ansioso por mi futuro"  # Spanish: I feel anxious about my future
    ]
    
    base_url = "http://localhost:5000/api"
    
    print("Testing therapy search endpoint...")
    
    # Test health endpoint first
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        if response.status_code == 200:
            print("✅ Health check passed")
        else:
            print("❌ Health check failed")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Cannot connect to server: {e}")
        print("Make sure the Flask app is running on port 5000")
        return False
    
    # Test therapy search
    for issue in test_issues:
        print(f"\n🧠 Testing issue: '{issue}'")
        
        try:
            response = requests.post(
                f"{base_url}/therapy-search",
                json={"issue": issue, "k": 3},
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ AI Response: {data.get('ai_response', 'None')}")
                print(f"🔍 Search Query: {data.get('search_query', 'None')}")
                
                results = data.get('results', [])
                print(f"📖 Found {len(results)} verses:")
                
                for i, result in enumerate(results[:2], 1):  # Show first 2 results
                    print(f"  {i}. {result.get('id', 'Unknown')} (score: {result.get('score', 0):.3f})")
                    print(f"     EN: {result.get('verse_en', result.get('text', 'No English text'))[:100]}...")
                    print(f"     AR: {result.get('verse_ar', 'No Arabic text')[:50]}...")
                    
            else:
                print(f"❌ Request failed: {response.status_code}")
                try:
                    error_data = response.json()
                    print(f"Error: {error_data.get('error', 'Unknown error')}")
                except:
                    print(f"Response: {response.text}")
                    
        except requests.exceptions.RequestException as e:
            print(f"❌ Request error: {e}")
    
    print("\n✅ Test completed!")
    return True

if __name__ == "__main__":
    test_therapy_search()
