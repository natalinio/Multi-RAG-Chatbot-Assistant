"""
Test script to verify Azure services connectivity and configuration
"""
import os
import sys
from dotenv import load_dotenv
from azure.cosmos import CosmosClient
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential
from openai import AzureOpenAI

# Load environment variables
load_dotenv()

def test_azure_openai():
    """Test Azure OpenAI connection and model availability"""
    print("\n" + "="*60)
    print("Testing Azure OpenAI Connection")
    print("="*60)
    
    try:
        endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        api_key = os.getenv("AZURE_OPENAI_API_KEY")
        api_version = os.getenv("AZURE_OPENAI_API_VERSION")
        model_name = os.getenv("AZURE_OPENAI_CHAT_MODEL_NAME")
        
        print(f"Endpoint: {endpoint}")
        print(f"API Version: {api_version}")
        print(f"Model Name: {model_name}")
        
        # Create client
        client = AzureOpenAI(
            azure_endpoint=endpoint,
            api_key=api_key,
            api_version=api_version
        )
        
        # Test with a simple chat completion
        print("\nSending test request...")
        
        # GPT-5 models use max_completion_tokens instead of max_tokens
        completion_params = {
            "model": model_name,
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Hello, this is a test. Please respond with 'OK'."}
            ]
        }
        
        # Use max_completion_tokens for newer models, max_tokens for older ones
        if "gpt-5" in model_name.lower() or "o1" in model_name.lower():
            completion_params["max_completion_tokens"] = 10
        else:
            completion_params["max_tokens"] = 10
        
        response = client.chat.completions.create(**completion_params)
        
        result = response.choices[0].message.content
        print(f"✅ Azure OpenAI is working!")
        print(f"Response: {result}")
        print(f"Model: {response.model}")
        print(f"Tokens used: {response.usage.total_tokens}")
        
        return True
        
    except Exception as e:
        print(f"❌ Azure OpenAI test failed: {str(e)}")
        return False


def test_cosmos_db():
    """Test Cosmos DB connection"""
    print("\n" + "="*60)
    print("Testing Cosmos DB Connection")
    print("="*60)
    
    try:
        endpoint = os.getenv("COSMOS_DB_ENDPOINT")
        key = os.getenv("COSMOS_DB_KEY")
        database_name = os.getenv("COSMOS_DB_DATABASE_NAME")
        container_name = os.getenv("COSMOS_DB_CONTAINER_NAME")
        
        print(f"Endpoint: {endpoint}")
        print(f"Database: {database_name}")
        print(f"Container: {container_name}")
        
        # Create client
        client = CosmosClient(endpoint, credential=key)
        database = client.get_database_client(database_name)
        container = database.get_container_client(container_name)
        
        # Try to query
        print("\nQuerying container...")
        items = list(container.query_items(
            query="SELECT TOP 1 * FROM c",
            enable_cross_partition_query=True
        ))
        
        print(f"✅ Cosmos DB is working!")
        print(f"Found {len(items)} items in test query")
        
        if items:
            print(f"Sample item keys: {list(items[0].keys())[:5]}")
        
        return True
        
    except Exception as e:
        print(f"❌ Cosmos DB test failed: {str(e)}")
        return False


def test_azure_search():
    """Test Azure AI Search connection"""
    print("\n" + "="*60)
    print("Testing Azure AI Search Connection")
    print("="*60)
    
    try:
        endpoint = os.getenv("AZURE_AI_SEARCH_ENDPOINT")
        key = os.getenv("AZURE_AI_SEARCH_KEY")
        index_name = os.getenv("AZURE_AI_SEARCH_INDEX_NAME")
        
        print(f"Endpoint: {endpoint}")
        print(f"Index Name: {index_name}")
        
        # Create search client
        search_client = SearchClient(
            endpoint=endpoint,
            index_name=index_name,
            credential=AzureKeyCredential(key)
        )
        
        # Try a simple search
        print("\nTesting search...")
        results = search_client.search(
            search_text="data ingestion",
            top=3
        )
        
        result_list = list(results)
        print(f"✅ Azure AI Search is working!")
        print(f"Found {len(result_list)} documents")
        
        if result_list:
            print("\nSample document fields:")
            sample = result_list[0]
            for key in list(sample.keys())[:5]:
                print(f"  - {key}")
        
        return True
        
    except Exception as e:
        print(f"❌ Azure AI Search test failed: {str(e)}")
        print(f"Error details: {type(e).__name__}")
        
        # Check if it's an index not found error
        if "not found" in str(e).lower() or "404" in str(e):
            print("\n⚠️  Index does not exist. You need to create it.")
            print(f"   Index name: {index_name}")
            return "INDEX_NOT_FOUND"
        
        return False


def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("Azure Services Connectivity Test")
    print("="*60)
    
    results = {
        "Azure OpenAI": test_azure_openai(),
        "Cosmos DB": test_cosmos_db(),
        "Azure AI Search": test_azure_search()
    }
    
    print("\n" + "="*60)
    print("Test Summary")
    print("="*60)
    
    for service, result in results.items():
        if result == True:
            status = "✅ PASSED"
        elif result == "INDEX_NOT_FOUND":
            status = "⚠️  INDEX NOT FOUND"
        else:
            status = "❌ FAILED"
        print(f"{service}: {status}")
    
    # Overall status
    all_passed = all(r == True for r in results.values())
    index_missing = any(r == "INDEX_NOT_FOUND" for r in results.values())
    
    if all_passed:
        print("\n✅ All services are working correctly!")
        return 0
    elif index_missing:
        print("\n⚠️  Services are reachable but index needs to be created.")
        return 2
    else:
        print("\n❌ Some services failed. Check the errors above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
