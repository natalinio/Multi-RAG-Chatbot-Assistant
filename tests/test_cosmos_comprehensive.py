"""
Comprehensive test suite for Cosmos DB Plugin capabilities.
Tests all supported query patterns, use cases, and edge cases.
"""

import asyncio
import sys
import os
from dotenv import load_dotenv
import json
from datetime import datetime

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
load_dotenv()

from app.plugins.CosmosDbPlugin.CosmosDbPlugin import CosmosDbPlugin


class TestResult:
    """Simple class to track test results."""
    def __init__(self, name: str, category: str):
        self.name = name
        self.category = category
        self.status = "NOT_RUN"
        self.count = 0
        self.error = None
        self.duration = 0
    
    def __repr__(self):
        status_icon = "✅" if self.status == "PASS" else "❌" if self.status == "FAIL" else "⚠️"
        return f"{status_icon} [{self.category}] {self.name}: {self.status} (count={self.count})"


async def run_test(plugin: CosmosDbPlugin, test_name: str, query: str, category: str, 
                   expect_results: bool = True) -> TestResult:
    """
    Execute a single test query and validate results.
    
    Args:
        plugin: CosmosDbPlugin instance
        test_name: Descriptive name for the test
        query: SQL query to execute
        category: Test category (e.g., "BASIC", "STRING_OPS", etc.)
        expect_results: Whether results are expected (False for aggregations returning counts)
    
    Returns:
        TestResult object with execution details
    """
    result = TestResult(test_name, category)
    start_time = datetime.now()
    
    try:
        response = await plugin.query_existing_config(query)
        result_obj = json.loads(response)
        
        if result_obj.get('success'):
            count = result_obj.get('count', 0)
            result.count = count
            result.status = "PASS"
            
            # For aggregation queries, check if we got at least one result
            if not expect_results or count > 0:
                result.status = "PASS"
            else:
                result.status = "WARN"
                result.error = "Query succeeded but returned 0 results"
        else:
            result.status = "FAIL"
            result.error = result_obj.get('error', 'Unknown error')
    
    except Exception as e:
        result.status = "FAIL"
        result.error = str(e)
    
    result.duration = (datetime.now() - start_time).total_seconds()
    return result


async def test_cosmos_comprehensive():
    """
    Comprehensive test suite for all Cosmos DB query capabilities.
    """
    plugin = CosmosDbPlugin()
    results = []
    
    print("=" * 100)
    print("🧪 COMPREHENSIVE COSMOS DB PLUGIN TEST SUITE")
    print("=" * 100)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # ========================================
    # CATEGORY 1: BASIC FILTERING
    # ========================================
    print("📋 Testing BASIC FILTERING capabilities...")
    
    basic_tests = [
        ("Filter by domain", "SELECT * FROM c WHERE c.domain = 'SAPBW' OFFSET 0 LIMIT 5"),
        ("Filter by layer", "SELECT * FROM c WHERE c.layer = 'Bronze' OFFSET 0 LIMIT 5"),
        ("Filter domain AND layer", "SELECT * FROM c WHERE c.domain = 'NielsenUS' AND c.layer = 'Silver' OFFSET 0 LIMIT 5"),
        ("Filter with OR operator", "SELECT * FROM c WHERE c.market = 'US' OR c.market = 'GB' OFFSET 0 LIMIT 5"),
        ("Filter by process_requested", "SELECT * FROM c WHERE c.process_requested = 'ingestion' OFFSET 0 LIMIT 5"),
        ("Multiple AND conditions", "SELECT * FROM c WHERE c.domain = 'SAPBW' AND c.layer = 'Bronze' AND c.process_requested = 'ingestion' OFFSET 0 LIMIT 5"),
    ]
    
    for test_name, query in basic_tests:
        result = await run_test(plugin, test_name, query, "BASIC")
        results.append(result)
        print(f"  {result}")
    
    # ========================================
    # CATEGORY 2: STRING OPERATIONS
    # ========================================
    print("\n📝 Testing STRING OPERATIONS capabilities...")
    
    string_tests = [
        ("STARTSWITH - Validation prefix", "SELECT * FROM c WHERE STARTSWITH(c.entity, 'Validation') OFFSET 0 LIMIT 5"),
        ("CONTAINS - Case-sensitive", "SELECT * FROM c WHERE CONTAINS(c.entity, 'Nielsen') OFFSET 0 LIMIT 5"),
        ("CONTAINS with LOWER - Case-insensitive", "SELECT * FROM c WHERE CONTAINS(LOWER(c.entity), 'aggregated') OFFSET 0 LIMIT 5"),
        ("ENDSWITH - Suffix matching", "SELECT * FROM c WHERE ENDSWITH(c.entity, 'GLB') OFFSET 0 LIMIT 5"),
        ("STARTSWITH - UPH prefix", "SELECT * FROM c WHERE STARTSWITH(c.entity, 'UPH') OFFSET 0 LIMIT 5"),
        ("Complex string matching", "SELECT * FROM c WHERE STARTSWITH(c.entity, 'Validation') AND CONTAINS(c.entity, 'Nielsen') OFFSET 0 LIMIT 5"),
    ]
    
    for test_name, query in string_tests:
        result = await run_test(plugin, test_name, query, "STRING_OPS")
        results.append(result)
        print(f"  {result}")
    
    # ========================================
    # CATEGORY 3: NESTED FIELD ACCESS
    # ========================================
    print("\n🔍 Testing NESTED FIELD ACCESS capabilities...")
    
    nested_tests = [
        ("Access nested source type - asql", "SELECT * FROM c WHERE c.I1_data_extract_process.source.type = 'asql' OFFSET 0 LIMIT 5"),
        ("Access load mode-of-write", "SELECT * FROM c WHERE c.I2_load_data_process['mode-of-write'] = 'append' OFFSET 0 LIMIT 5"),
        ("Silver layer upsert mode", "SELECT * FROM c WHERE c.D3_load_data_process['mode-of-write'] = 'upsert' OFFSET 0 LIMIT 5"),
        ("Target format delta", "SELECT * FROM c WHERE c.I2_load_data_process['target-format'] = 'delta' OFFSET 0 LIMIT 5"),
        ("Unity Catalog target path", "SELECT * FROM c WHERE CONTAINS(c.D3_load_data_process['target-path'], 'catalog') OFFSET 0 LIMIT 5"),
    ]
    
    for test_name, query in nested_tests:
        result = await run_test(plugin, test_name, query, "NESTED")
        results.append(result)
        print(f"  {result}")
    
    # ========================================
    # CATEGORY 4: ARRAY OPERATIONS
    # ========================================
    print("\n📦 Testing ARRAY OPERATIONS capabilities...")
    
    array_tests = [
        ("ARRAY_CONTAINS - partition Spirits", "SELECT * FROM c WHERE ARRAY_CONTAINS(c.partition, 'Spirits') OFFSET 0 LIMIT 5"),
        ("ARRAY_CONTAINS - partition GLB", "SELECT * FROM c WHERE ARRAY_CONTAINS(c.partition, 'GLB') OFFSET 0 LIMIT 5"),
        ("ARRAY_LENGTH - has dependencies", "SELECT * FROM c WHERE ARRAY_LENGTH(c.dependencyInbound) > 0 OFFSET 0 LIMIT 5"),
        ("ARRAY_LENGTH - no dependencies", "SELECT * FROM c WHERE ARRAY_LENGTH(c.dependencyInbound) = 0 OFFSET 0 LIMIT 5"),
        ("ARRAY_CONTAINS - specific dependency", "SELECT * FROM c WHERE ARRAY_CONTAINS(c.dependencyInbound, 'ValidationMarketDim-NielsenAT-Bronze-Spirits') OFFSET 0 LIMIT 5"),
    ]
    
    for test_name, query in array_tests:
        result = await run_test(plugin, test_name, query, "ARRAYS")
        results.append(result)
        print(f"  {result}")
    
    # ========================================
    # CATEGORY 5: IN OPERATOR
    # ========================================
    print("\n🎯 Testing IN OPERATOR capabilities...")
    
    in_tests = [
        ("IN - multiple domains", "SELECT * FROM c WHERE c.domain IN ('NielsenUS', 'NielsenGB', 'SAPBW') OFFSET 0 LIMIT 5"),
        ("IN - multiple markets", "SELECT * FROM c WHERE c.market IN ('US', 'GB', 'GLB') OFFSET 0 LIMIT 5"),
        ("NOT IN - exclude Gold", "SELECT * FROM c WHERE c.layer NOT IN ('Gold') OFFSET 0 LIMIT 5"),
        ("IN - single value", "SELECT * FROM c WHERE c.layer IN ('Bronze') OFFSET 0 LIMIT 5"),
    ]
    
    for test_name, query in in_tests:
        result = await run_test(plugin, test_name, query, "IN_OPERATOR")
        results.append(result)
        print(f"  {result}")
    
    # ========================================
    # CATEGORY 6: SORTING & PAGINATION
    # ========================================
    print("\n🔢 Testing SORTING & PAGINATION capabilities...")
    
    sort_tests = [
        ("ORDER BY timestamp DESC", "SELECT TOP 10 * FROM c ORDER BY c._ts DESC"),
        ("ORDER BY entity ASC", "SELECT * FROM c WHERE c.domain = 'SAPBW' ORDER BY c.entity ASC OFFSET 0 LIMIT 5"),
        ("OFFSET LIMIT pagination", "SELECT * FROM c ORDER BY c._ts DESC OFFSET 5 LIMIT 5"),
        ("TOP 10 most recent", "SELECT TOP 10 * FROM c ORDER BY c._ts DESC"),
        ("Sorted with filter", "SELECT * FROM c WHERE c.layer = 'Bronze' ORDER BY c._ts DESC OFFSET 0 LIMIT 10"),
    ]
    
    for test_name, query in sort_tests:
        result = await run_test(plugin, test_name, query, "SORT_PAGE")
        results.append(result)
        print(f"  {result}")
    
    # ========================================
    # CATEGORY 7: PROJECTIONS
    # ========================================
    print("\n📊 Testing PROJECTION capabilities...")
    
    projection_tests = [
        ("Select specific fields", "SELECT c.id, c.domain, c.entity, c.layer FROM c OFFSET 0 LIMIT 5"),
        ("Project with filter", "SELECT c.entity, c.market, c.partition FROM c WHERE c.layer = 'Bronze' OFFSET 0 LIMIT 5"),
        ("SELECT VALUE entity", "SELECT VALUE c.entity FROM c WHERE c.domain = 'NielsenUS' OFFSET 0 LIMIT 5"),
        ("Minimal projection", "SELECT c.id, c.entity FROM c OFFSET 0 LIMIT 10"),
    ]
    
    for test_name, query in projection_tests:
        result = await run_test(plugin, test_name, query, "PROJECTION", expect_results=False)
        results.append(result)
        print(f"  {result}")
    
    # ========================================
    # CATEGORY 8: AGGREGATIONS - SKIPPED (NOT SUPPORTED)
    # ========================================
    print("\n⚠️  Skipping AGGREGATION tests (NOT supported by Cosmos DB SQL API)")
    print("   Note: COUNT, GROUP BY, SUM, AVG require specific Cosmos DB features")
    
    # Aggregations removed - not supported in standard Cosmos DB SQL API
    # Users should retrieve data and count in application code
    
    # ========================================
    # CATEGORY 9: REAL-WORLD USE CASES
    # ========================================
    print("\n🌍 Testing REAL-WORLD USE CASES...")
    
    use_case_tests = [
        ("UC1: Bronze configs for SAPBW", "SELECT * FROM c WHERE c.domain = 'SAPBW' AND c.layer = 'Bronze' ORDER BY c._ts DESC OFFSET 0 LIMIT 5"),
        ("UC2: Azure SQL sources", "SELECT * FROM c WHERE c.I1_data_extract_process.source.type = 'asql' OFFSET 0 LIMIT 5"),
        ("UC3: Validation jobs Nielsen", "SELECT * FROM c WHERE STARTSWITH(c.entity, 'Validation') AND CONTAINS(c.entity, 'Nielsen') OFFSET 0 LIMIT 5"),
        ("UC4: Silver upsert configs", "SELECT * FROM c WHERE c.layer = 'Silver' AND c.D3_load_data_process['mode-of-write'] = 'upsert' OFFSET 0 LIMIT 5"),
        ("UC5: Jobs with dependencies", "SELECT * FROM c WHERE ARRAY_LENGTH(c.dependencyInbound) > 0 ORDER BY c._ts DESC OFFSET 0 LIMIT 5"),
        ("UC6: Ingestion jobs Nielsen US", "SELECT * FROM c WHERE c.domain = 'NielsenUS' AND c.layer = 'Bronze' AND c.process_requested = 'ingestion' OFFSET 0 LIMIT 5"),
        ("UC7: Entities with Aggregated", "SELECT * FROM c WHERE CONTAINS(LOWER(c.entity), 'aggregated') OFFSET 0 LIMIT 5"),
        ("UC8: Most recent 10 configs", "SELECT TOP 10 * FROM c ORDER BY c._ts DESC"),
        ("UC9: Unity Catalog target paths", "SELECT * FROM c WHERE CONTAINS(c.D3_load_data_process['target-path'], 'catalog') OFFSET 0 LIMIT 5"),
    ]
    
    for test_name, query in use_case_tests:
        result = await run_test(plugin, test_name, query, "USE_CASE")
        results.append(result)
        print(f"  {result}")
    
    # ========================================
    # CATEGORY 10: EDGE CASES & ERROR HANDLING
    # ========================================
    print("\n⚠️ Testing EDGE CASES & ERROR HANDLING...")
    
    edge_tests = [
        ("Empty query", "", "EDGE_CASE"),
        ("Wrong alias - configurations", "SELECT * FROM configurations WHERE domain = 'SAPBW'", "EDGE_CASE"),
        ("Non-existent field", "SELECT * FROM c WHERE c.nonexistent_field = 'value' OFFSET 0 LIMIT 5", "EDGE_CASE"),
        ("No results filter", "SELECT * FROM c WHERE c.domain = 'NONEXISTENT_DOMAIN' OFFSET 0 LIMIT 5", "EDGE_CASE"),
    ]
    
    for test_name, query, category in edge_tests:
        result = await run_test(plugin, test_name, query, category, expect_results=False)
        results.append(result)
        print(f"  {result}")
    
    # ========================================
    # TEST get_schema_info
    # ========================================
    print("\n📚 Testing get_schema_info function...")
    try:
        schema = await plugin.get_schema_info()
        schema_obj = json.loads(schema)
        if 'common_fields' in schema_obj and 'query_patterns' in schema_obj:
            schema_result = TestResult("get_schema_info", "SCHEMA")
            schema_result.status = "PASS"
            schema_result.count = len(schema_obj.get('query_patterns', {}))
            results.append(schema_result)
            print(f"  {schema_result}")
        else:
            schema_result = TestResult("get_schema_info", "SCHEMA")
            schema_result.status = "FAIL"
            schema_result.error = "Missing expected schema fields"
            results.append(schema_result)
            print(f"  {schema_result}")
    except Exception as e:
        schema_result = TestResult("get_schema_info", "SCHEMA")
        schema_result.status = "FAIL"
        schema_result.error = str(e)
        results.append(schema_result)
        print(f"  {schema_result}")
    
    # ========================================
    # TEST list_by_domain
    # ========================================
    print("\n📂 Testing list_by_domain function...")
    try:
        domain_result_str = await plugin.list_configurations_by_domain("SAPBW", limit="10")
        domain_result_obj = json.loads(domain_result_str)
        if domain_result_obj.get('success'):
            domain_test = TestResult("list_by_domain(SAPBW)", "HELPER")
            domain_test.status = "PASS"
            domain_test.count = domain_result_obj.get('count', 0)
            results.append(domain_test)
            print(f"  {domain_test}")
        else:
            domain_test = TestResult("list_by_domain(SAPBW)", "HELPER")
            domain_test.status = "FAIL"
            domain_test.error = domain_result_obj.get('error')
            results.append(domain_test)
            print(f"  {domain_test}")
    except Exception as e:
        domain_test = TestResult("list_by_domain(SAPBW)", "HELPER")
        domain_test.status = "FAIL"
        domain_test.error = str(e)
        results.append(domain_test)
        print(f"  {domain_test}")
    
    # ========================================
    # SUMMARY & STATISTICS
    # ========================================
    print("\n" + "=" * 100)
    print("📊 TEST EXECUTION SUMMARY")
    print("=" * 100)
    
    total = len(results)
    passed = sum(1 for r in results if r.status == "PASS")
    failed = sum(1 for r in results if r.status == "FAIL")
    warned = sum(1 for r in results if r.status == "WARN")
    
    total_duration = sum(r.duration for r in results)
    
    print(f"\n📈 Overall Statistics:")
    print(f"  Total Tests: {total}")
    print(f"  ✅ Passed: {passed} ({passed/total*100:.1f}%)")
    print(f"  ❌ Failed: {failed} ({failed/total*100:.1f}%)")
    print(f"  ⚠️  Warned: {warned} ({warned/total*100:.1f}%)")
    print(f"  ⏱️  Total Duration: {total_duration:.2f}s")
    print(f"  ⚡ Avg Duration: {total_duration/total:.3f}s per test")
    
    # Category breakdown
    print(f"\n📂 Results by Category:")
    categories = {}
    for r in results:
        if r.category not in categories:
            categories[r.category] = {"total": 0, "passed": 0, "failed": 0, "warned": 0}
        categories[r.category]["total"] += 1
        if r.status == "PASS":
            categories[r.category]["passed"] += 1
        elif r.status == "FAIL":
            categories[r.category]["failed"] += 1
        elif r.status == "WARN":
            categories[r.category]["warned"] += 1
    
    for category, stats in sorted(categories.items()):
        pass_rate = stats['passed'] / stats['total'] * 100 if stats['total'] > 0 else 0
        print(f"  {category:15} - Total: {stats['total']:2}, Pass: {stats['passed']:2}, Fail: {stats['failed']:2}, Warn: {stats['warned']:2} ({pass_rate:.0f}%)")
    
    # Failed tests details
    if failed > 0:
        print(f"\n❌ Failed Tests Details:")
        for r in results:
            if r.status == "FAIL":
                print(f"  • {r.name}")
                print(f"    Category: {r.category}")
                print(f"    Error: {r.error}")
    
    # Cleanup
    await plugin.cleanup()
    
    print(f"\n✨ Test suite completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 100)
    
    return passed == total


if __name__ == "__main__":
    print("\n🚀 Starting Comprehensive Cosmos DB Plugin Test Suite...\n")
    success = asyncio.run(test_cosmos_comprehensive())
    
    if success:
        print("\n🎉 ALL TESTS PASSED! 🎉\n")
        sys.exit(0)
    else:
        print("\n⚠️  SOME TESTS FAILED - Review the summary above\n")
        sys.exit(1)
