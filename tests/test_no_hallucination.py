"""Test the RAG with strict anti-hallucination prompt"""
import requests
import json
import time

BASE_URL = "http://localhost:8005"

# Test queries
test_cases = [
    {
        "query": "Give me the template I need to fill to configure an ingestion for Azure SQL server",
        "description": "Azure SQL (ASQL) ingestion - should retrieve correct properties"
    },
    {
        "query": "What are the exact properties for SAPBW Bronze layer ingestion?",
        "description": "SAPBW Bronze ingestion - should show real SAPBW configuration"
    },
    {
        "query": "Show me a complete Silver layer transformation configuration",
        "description": "Silver layer transformation - should show real example from index"
    },
]

print("\n" + "="*80)
print("RAG ANTI-HALLUCINATION TEST")
print("="*80)

for test_idx, test_case in enumerate(test_cases, 1):
    print(f"\n{'='*80}")
    print(f"TEST {test_idx}: {test_case['description']}")
    print(f"{'='*80}")
    print(f"Query: {test_case['query']}\n")
    
    try:
        response = requests.post(
            f"{BASE_URL}/chat",
            json={
                "message": test_case['query'],
                "session_id": f"test_{test_idx}"
            },
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            answer = data.get('response', '')
            
            print("RESPONSE:")
            print("-" * 80)
            print(answer[:1500])
            if len(answer) > 1500:
                print(f"\n... [Response continues, {len(answer)} total chars]")
            print("-" * 80)
            
            # Check for hallucinated properties
            hallucination_markers = [
                "connection_string",
                "YourDomain",
                "YourEntity",
                "YourConnectionString",
                "YourTableName",
                "pipeline_name",
                "typical",
                "usually"
            ]
            
            found_hallucinations = [m for m in hallucination_markers if m.lower() in answer.lower()]
            
            if found_hallucinations:
                print(f"\n⚠️  HALLUCINATION DETECTED: {found_hallucinations}")
            else:
                print(f"\n✅ NO HALLUCINATED CONTENT DETECTED")
        else:
            print(f"❌ Error: HTTP {response.status_code}")
            print(response.text)
    
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Make sure it's running on http://localhost:8004")
        break
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Wait between requests
    if test_idx < len(test_cases):
        time.sleep(2)

print("\n" + "="*80)
print("TEST COMPLETE")
print("="*80 + "\n")
