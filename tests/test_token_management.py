"""
Test Token Management and Overflow Protection
Tests all 3 levels of token protection to ensure the system handles large queries safely.
"""

import asyncio
import httpx
import json
from typing import Dict, Any

# Configuration
BASE_URL = "http://127.0.0.1:8000"
SESSION_ID = "test_token_management"

# ANSI color codes for terminal output
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_test_header(scenario: str):
    """Print a formatted test header."""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*80}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{scenario}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*80}{Colors.END}\n")

def print_result(success: bool, message: str):
    """Print a colored result message."""
    color = Colors.GREEN if success else Colors.RED
    symbol = "✅" if success else "❌"
    print(f"{color}{symbol} {message}{Colors.END}")

def print_warning(message: str):
    """Print a warning message."""
    print(f"{Colors.YELLOW}⚠️  {message}{Colors.END}")

def print_info(message: str):
    """Print an info message."""
    print(f"{Colors.BLUE}ℹ️  {message}{Colors.END}")

async def send_chat_message(message: str, session_id: str = SESSION_ID) -> Dict[str, Any]:
    """Send a chat message to the API."""
    async with httpx.AsyncClient(timeout=120.0) as client:
        response = await client.post(
            f"{BASE_URL}/api/chat",
            json={"message": message, "session_id": session_id}
        )
        return response.json()

async def clear_session(session_id: str = SESSION_ID):
    """Clear the chat session."""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{BASE_URL}/api/clear-session",
            json={"session_id": session_id}
        )
        return response.json()

def estimate_tokens(text: str) -> int:
    """Rough token estimation (1 token ≈ 4 characters)."""
    return len(text) // 4

async def test_scenario_a_normal_query():
    """
    Scenario A: Normal Query (5 configurations)
    Expected: No limitations, returns all results
    """
    print_test_header("SCENARIO A: Normal Query (5 configurations)")
    
    await clear_session()
    print_info("Session cleared")
    
    # Query for a specific entity (should return 1 config)
    query = "Show me the configuration for AggregatedData-NielsenGB-Bronze-RTD"
    print_info(f"Query: {query}")
    
    result = await send_chat_message(query)
    
    if result.get("success"):
        response_text = result.get("response", "")
        tokens = estimate_tokens(response_text)
        print_result(True, f"Query successful - Response tokens: ~{tokens:,}")
        print_info(f"Response length: {len(response_text):,} characters")
        
        # Check if response contains configuration
        if "domain" in response_text.lower() and "nielsenGB" in response_text.lower():
            print_result(True, "Configuration data returned correctly")
        else:
            print_result(False, "Configuration data not found in response")
    else:
        print_result(False, f"Query failed: {result.get('error', 'Unknown error')}")

async def test_scenario_b_large_query():
    """
    Scenario B: Large Query (110 configurations)
    Expected: Level 1 protection - Limited to 50 results with warning
    """
    print_test_header("SCENARIO B: Large Query (~110 configurations)")
    
    await clear_session()
    print_info("Session cleared")
    
    # Query for all NielsenGB configs (returns ~110)
    query = "Show me all configurations for NielsenGB domain"
    print_info(f"Query: {query}")
    
    result = await send_chat_message(query)
    
    if result.get("success"):
        response_text = result.get("response", "")
        tokens = estimate_tokens(response_text)
        print_result(True, f"Query successful - Response tokens: ~{tokens:,}")
        print_info(f"Response length: {len(response_text):,} characters")
        
        # Check for truncation warning
        if "truncated" in response_text.lower() or "50" in response_text:
            print_result(True, "✂️  Results truncated to 50 (Level 1 protection active)")
        else:
            print_warning("No truncation warning found - may need to verify")
        
        if tokens > 100000:
            print_warning(f"Response is very large ({tokens:,} tokens) - might cause issues")
        else:
            print_result(True, f"Token count within safe range ({tokens:,} < 100,000)")
    else:
        print_result(False, f"Query failed: {result.get('error', 'Unknown error')}")

async def test_scenario_c_multiple_large_queries():
    """
    Scenario C: Multiple Large Queries Consecutively
    Expected: Level 2 protection - History truncated to last 3 messages
    """
    print_test_header("SCENARIO C: Multiple Large Queries (3+ consecutive)")
    
    await clear_session()
    print_info("Session cleared")
    
    queries = [
        "Show me all SAPBW Bronze layer configurations",
        "Show me all NielsenUS configurations", 
        "Show me all Profisee configurations",
        "Show me all SFAsseco configurations"
    ]
    
    total_tokens = 0
    
    for i, query in enumerate(queries, 1):
        print_info(f"Query {i}/{len(queries)}: {query}")
        result = await send_chat_message(query)
        
        if result.get("success"):
            response_text = result.get("response", "")
            tokens = estimate_tokens(response_text)
            total_tokens += tokens
            print_result(True, f"Query {i} successful - Tokens: ~{tokens:,}")
        else:
            print_result(False, f"Query {i} failed: {result.get('error', 'Unknown error')}")
        
        await asyncio.sleep(1)  # Small delay between queries
    
    print_info(f"Total tokens across all queries: ~{total_tokens:,}")
    
    # Try one more query to see if old history was truncated
    print_info("\nTesting history truncation with one more query...")
    final_query = "What was my first question?"
    result = await send_chat_message(final_query)
    
    if result.get("success"):
        response_text = result.get("response", "")
        # If history was truncated, AI won't remember the first query
        if "don't" in response_text.lower() or "can't" in response_text.lower() or "recent" in response_text.lower():
            print_result(True, "🔄 Level 2 protection active - Old history truncated (can't remember first query)")
        else:
            print_info("AI seems to remember first query - history may not be truncated yet")

async def test_scenario_d_extreme_overflow():
    """
    Scenario D: Extreme Token Overflow
    Expected: Level 3 protection - Fresh session created
    """
    print_test_header("SCENARIO D: Extreme Token Overflow (Multiple huge queries)")
    
    await clear_session()
    print_info("Session cleared")
    
    # Fill up the session with multiple large queries
    queries = [
        "Show me all NielsenGB configurations",
        "Show me all SAPBW configurations",
        "Show me all Profisee configurations",
        "Show me all NielsenUS configurations",
        "Show me all SFAsseco Bronze layer configurations"
    ]
    
    print_info(f"Sending {len(queries)} consecutive large queries to fill history...")
    
    for i, query in enumerate(queries, 1):
        print_info(f"Large query {i}/{len(queries)}")
        result = await send_chat_message(query)
        
        if result.get("success"):
            response_text = result.get("response", "")
            tokens = estimate_tokens(response_text)
            print_result(True, f"Query {i} completed - ~{tokens:,} tokens")
        else:
            # Check if error is context_length_exceeded
            error_msg = result.get("error", "")
            if "context" in error_msg.lower() or "token" in error_msg.lower():
                print_result(False, f"❌ Token overflow error: {error_msg}")
                print_warning("Level 3 protection should have prevented this!")
                return
            else:
                print_result(False, f"Other error: {error_msg}")
        
        await asyncio.sleep(1)
    
    # Now try a simple query - should work if fresh session was created
    print_info("\nTesting with a simple query after overflow prevention...")
    simple_query = "Hello, what can you help me with?"
    result = await send_chat_message(simple_query)
    
    if result.get("success"):
        print_result(True, "✅ Simple query works - Level 3 protection active (fresh session created)")
    else:
        error_msg = result.get("error", "")
        if "context" in error_msg.lower() or "token" in error_msg.lower():
            print_result(False, "❌ Still getting token overflow - Level 3 protection failed!")
        else:
            print_result(False, f"Other error: {error_msg}")

async def test_clear_button_functionality():
    """
    Test: Clear Button Functionality
    Expected: Session is completely cleared
    """
    print_test_header("TEST: Clear Button Functionality")
    
    # Send a query
    query = "Show me SAPBW configurations"
    print_info(f"Initial query: {query}")
    result = await send_chat_message(query)
    
    if result.get("success"):
        print_result(True, "Initial query successful")
    else:
        print_result(False, "Initial query failed")
        return
    
    # Clear session
    print_info("Clicking 'Clear' button (calling /api/clear-session)")
    clear_result = await clear_session()
    print_result(True, f"Session cleared: {clear_result}")
    
    # Ask about previous query
    print_info("Testing if history was cleared...")
    followup_query = "What did I just ask you about?"
    result = await send_chat_message(followup_query)
    
    if result.get("success"):
        response_text = result.get("response", "")
        # If cleared properly, AI won't remember the previous query
        if "don't" in response_text.lower() or "can't" in response_text.lower() or "first" in response_text.lower():
            print_result(True, "✅ Clear button works - AI doesn't remember previous conversation")
        else:
            print_warning("AI seems to remember previous query - clear may not have worked")
            print_info(f"Response: {response_text[:200]}...")

async def run_all_tests():
    """Run all token management tests."""
    print(f"\n{Colors.BOLD}🧪 TOKEN MANAGEMENT TEST SUITE{Colors.END}")
    print(f"{Colors.BOLD}Testing 3-Level Token Protection System{Colors.END}\n")
    
    tests = [
        ("Scenario A: Normal Query", test_scenario_a_normal_query),
        ("Scenario B: Large Query (110 configs)", test_scenario_b_large_query),
        ("Scenario C: Multiple Large Queries", test_scenario_c_multiple_large_queries),
        ("Scenario D: Extreme Overflow", test_scenario_d_extreme_overflow),
        ("Clear Button Test", test_clear_button_functionality)
    ]
    
    for i, (name, test_func) in enumerate(tests, 1):
        try:
            await test_func()
        except Exception as e:
            print_result(False, f"Test failed with exception: {str(e)}")
        
        if i < len(tests):
            print(f"\n{Colors.BLUE}{'─'*80}{Colors.END}")
            await asyncio.sleep(2)  # Pause between tests
    
    print(f"\n{Colors.BOLD}{Colors.GREEN}{'='*80}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.GREEN}ALL TESTS COMPLETED{Colors.END}")
    print(f"{Colors.BOLD}{Colors.GREEN}{'='*80}{Colors.END}\n")

if __name__ == "__main__":
    asyncio.run(run_all_tests())
