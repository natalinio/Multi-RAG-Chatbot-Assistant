"""
Test script to verify Azure AI Search is working and contains ETL documentation.
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential

# Load environment variables
env_file = Path(__file__).parent / ".env"
if env_file.exists():
    load_dotenv(dotenv_path=env_file)
    print(f"✅ Loaded environment from {env_file}")

# Get Azure Search configuration
search_endpoint = os.getenv("AZURE_AI_SEARCH_ENDPOINT")
search_key = os.getenv("AZURE_AI_SEARCH_KEY")
index_name = os.getenv("AZURE_AI_SEARCH_INDEX_NAME")

print(f"\n📊 Azure AI Search Configuration:")
print(f"  Endpoint: {search_endpoint}")
print(f"  Index: {index_name}")
print(f"  Key: {'*' * 10}...{search_key[-5:] if search_key else 'NOT SET'}")

if not all([search_endpoint, search_key, index_name]):
    print("❌ Missing Azure AI Search configuration!")
    exit(1)

# Initialize search client
credential = AzureKeyCredential(search_key)
search_client = SearchClient(
    endpoint=search_endpoint,
    index_name=index_name,
    credential=credential
)

print("\n🔍 Testing queries against Azure AI Search:\n")

# Test queries
test_queries = [
    "SAPBW template configuration",
    "SAP BW ingestion",
    "Bronze layer ingestion setup",
    "JSON template for SAP",
    "SAP data source",
]

for query in test_queries:
    print(f"\n{'='*60}")
    print(f"Query: {query}")
    print(f"{'='*60}")
    
    try:
        # Simple search
        results = search_client.search(
            search_text=query,
            query_type="simple",
            top=3
        )
        
        result_list = list(results)
        print(f"Found {len(result_list)} results\n")
        
        for i, result in enumerate(result_list, 1):
            print(f"Result {i}:")
            print(f"  ID: {result['id']}")
            print(f"  Section: {result['section']}")
            print(f"  Subsection: {result['subsection']}")
            print(f"  Type: {result['content_type']}")
            print(f"  Content (first 300 chars):")
            content = result['content']
            print(f"    {content[:300]}...")
            print()
        
    except Exception as e:
        print(f"❌ Error: {str(e)}\n")

# Try semantic search if available
print(f"\n{'='*60}")
print("Semantic Search Test (with semantic configuration)")
print(f"{'='*60}\n")

try:
    results = search_client.search(
        search_text="SAP BW configuration template",
        query_type="semantic",
        semantic_configuration_name="default",
        top=3
    )
    
    result_list = list(results)
    print(f"Found {len(result_list)} semantic search results\n")
    
    for i, result in enumerate(result_list, 1):
        print(f"Result {i}:")
        print(f"  ID: {result['id']}")
        print(f"  Section: {result['section']}")
        print(f"  Content (first 300 chars):")
        content = result['content']
        print(f"    {content[:300]}...")
        print()
        
except Exception as e:
    print(f"⚠️  Semantic search not available: {str(e)}\n")

print("\n✅ Azure AI Search test completed!")
