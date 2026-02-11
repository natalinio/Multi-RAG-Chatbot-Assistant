"""
Test Cosmos DB connection and list available databases/containers
"""
import asyncio
from azure.cosmos.aio import CosmosClient
from dotenv import load_dotenv
import os

load_dotenv()

async def test_cosmos():
    endpoint = os.getenv("COSMOS_DB_ENDPOINT")
    key = os.getenv("COSMOS_DB_KEY")
    db_name = os.getenv("COSMOS_DB_DATABASE_NAME")
    container_name = os.getenv("COSMOS_DB_CONTAINER_NAME")
    
    print(f"🔍 Testing Cosmos DB Connection...")
    print(f"   Endpoint: {endpoint}")
    print(f"   Configured Database: {db_name}")
    print(f"   Configured Container: {container_name}")
    print()
    
    async with CosmosClient(endpoint, key) as client:
        # List all databases
        print("📁 Available Databases:")
        databases = [db async for db in client.list_databases()]
        for db in databases:
            print(f"   - {db['id']}")
        print()
        
        # Try to access the configured database
        if db_name in [db['id'] for db in databases]:
            print(f"✅ Database '{db_name}' exists!")
            database = client.get_database_client(db_name)
            
            # List containers
            print(f"\n📦 Containers in '{db_name}':")
            containers = [c async for c in database.list_containers()]
            for container in containers:
                print(f"   - {container['id']}")
            
            if container_name in [c['id'] for c in containers]:
                print(f"\n✅ Container '{container_name}' exists!")
                
                # Count documents
                container_client = database.get_container_client(container_name)
                query = "SELECT VALUE COUNT(1) FROM c"
                items = [item async for item in container_client.query_items(query, enable_cross_partition_query=True)]
                print(f"   Total documents: {items[0] if items else 0}")
            else:
                print(f"\n❌ Container '{container_name}' NOT FOUND!")
                print(f"   Available containers: {[c['id'] for c in containers]}")
        else:
            print(f"❌ Database '{db_name}' NOT FOUND!")
            print(f"   Available databases: {[db['id'] for db in databases]}")
            print(f"\n💡 Update COSMOS_DB_DATABASE_NAME in .env file with one of the above")

if __name__ == "__main__":
    asyncio.run(test_cosmos())
