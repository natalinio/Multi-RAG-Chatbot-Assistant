"""Test Azure AI Search indexing after re-index"""
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential
import os
from dotenv import load_dotenv
import time

load_dotenv()

endpoint = os.getenv('AZURE_AI_SEARCH_ENDPOINT')
key = os.getenv('AZURE_AI_SEARCH_KEY')
index_name = os.getenv('AZURE_AI_SEARCH_INDEX_NAME', 'cpgai-gda-version')

client = SearchClient(endpoint=endpoint, index_name=index_name, credential=AzureKeyCredential(key))

print("Waiting 10 seconds for index to be fully indexed...")
time.sleep(10)

count = client.get_document_count()
print(f"\nTotal documents in index: {count}")

# Test query
print("\nTesting semantic search with query: 'SAPBW ingestion'")
results = list(client.search("SAPBW ingestion", query_type="semantic", semantic_configuration_name="default", top=3))

print(f"Found {len(results)} documents:\n")
for idx, result in enumerate(results, 1):
    print(f"{idx}. Entity: {result['entity']}")
    print(f"   Layer: {result['layer']}, Domain: {result['domain']}")
    print(f"   Source: {result['source']}")
    print(f"   Preview: {result['content'][:200]}...\n")
