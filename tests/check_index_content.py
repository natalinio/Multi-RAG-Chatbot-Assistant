"""
Script to check what ADLS ingestion content is in the Azure AI Search index.
"""
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Create search client
endpoint = os.getenv('AZURE_AI_SEARCH_ENDPOINT')
index_name = os.getenv('AZURE_AI_SEARCH_INDEX_NAME', 'cpgai-gda-version')
api_key = os.getenv('AZURE_AI_SEARCH_KEY')

print(f"Connecting to: {endpoint}")
print(f"Index: {index_name}")
print("="*80)

client = SearchClient(
    endpoint=endpoint,
    index_name=index_name,
    credential=AzureKeyCredential(api_key)
)

# Search for ADLS ingestion configuration
query = "ADLS source ingestion configuration"
print(f"Search query: {query}\n")

results = client.search(
    search_text=query,
    top=3
)

for i, result in enumerate(results, 1):
    print(f"\n{'='*80}")
    print(f"RESULT {i}")
    print(f"{'='*80}")
    print(f"Available fields: {list(result.keys())}")
    print(f"\nContent preview (first 2000 chars):")
    print("-"*80)
    content = result.get('content', '')
    print(content[:2000])
    if len(content) > 2000:
        print(f"\n... [truncated, total length: {len(content)} chars]")
    print()
