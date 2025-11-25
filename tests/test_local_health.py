"""Quick test script to verify the health endpoint works locally."""
import asyncio
import httpx

async def test_health():
    """Test the health endpoint."""
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get("http://localhost:8000/api/health")
            print(f"Status Code: {response.status_code}")
            print(f"Response: {response.json()}")
            return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    result = asyncio.run(test_health())
    print(f"\nHealth check {'PASSED' if result else 'FAILED'}")
