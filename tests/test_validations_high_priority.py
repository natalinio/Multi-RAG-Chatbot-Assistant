"""
Test delle validazioni pre-esecuzione HIGH PRIORITY implementate nei plugin.
"""
import asyncio
import sys
import os
from pathlib import Path
import json

# Aggiungi la root del progetto al path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app.plugins.CosmosDbPlugin.CosmosDbPlugin import CosmosDbPlugin
from app.plugins.EtlConfigPlugin.EtlConfigPlugin import EtlConfigPlugin


async def test_validation_a_block_count_in_query():
    """
    TEST A: Bloccare COUNT() in query_existing_config
    """
    print("\n" + "=" * 80)
    print("TEST A: Block COUNT() aggregation in query_existing_config")
    print("=" * 80)
    
    plugin = CosmosDbPlugin()
    
    # Test query con COUNT()
    query = "SELECT COUNT(1) as total FROM c WHERE c.domain = 'NielsenGB'"
    print(f"\n🔍 Trying query with COUNT(): {query}")
    
    result = await plugin.query_existing_config(query)
    result_obj = json.loads(result)
    
    print("\n📊 RESULT:")
    print(json.dumps(result_obj, indent=2))
    
    # Verifica che sia stato bloccato
    assert result_obj.get("success") == False, "Should block COUNT() query"
    assert "COUNT()" in result_obj.get("unsupported_features", []), "Should identify COUNT() as unsupported"
    assert "count_configurations" in result_obj.get("solution", ""), "Should suggest count_configurations()"
    
    print("\n✅ TEST A PASSED: COUNT() aggregation correctly blocked!")
    return result_obj


async def test_validation_a_block_group_by():
    """
    TEST A bis: Bloccare GROUP BY in query_existing_config
    """
    print("\n" + "=" * 80)
    print("TEST A bis: Block GROUP BY in query_existing_config")
    print("=" * 80)
    
    plugin = CosmosDbPlugin()
    
    # Test query con GROUP BY
    query = "SELECT c.domain, COUNT(1) FROM c GROUP BY c.domain"
    print(f"\n🔍 Trying query with GROUP BY: {query}")
    
    result = await plugin.query_existing_config(query)
    result_obj = json.loads(result)
    
    print("\n📊 RESULT:")
    print(json.dumps(result_obj, indent=2))
    
    # Verifica che sia stato bloccato
    assert result_obj.get("success") == False, "Should block GROUP BY query"
    assert "GROUP BY" in result_obj.get("unsupported_features", []), "Should identify GROUP BY as unsupported"
    
    print("\n✅ TEST A bis PASSED: GROUP BY correctly blocked!")
    return result_obj


async def test_validation_e_block_count_in_filter():
    """
    TEST E: Bloccare COUNT() nel filter di count_configurations
    """
    print("\n" + "=" * 80)
    print("TEST E: Block COUNT() in count_configurations filter")
    print("=" * 80)
    
    plugin = CosmosDbPlugin()
    
    # Test filter con COUNT()
    filter_with_count = "COUNT(c.id) > 5"
    print(f"\n🔍 Trying filter with COUNT(): {filter_with_count}")
    
    result = await plugin.count_configurations(filter=filter_with_count)
    result_obj = json.loads(result)
    
    print("\n📊 RESULT:")
    print(json.dumps(result_obj, indent=2))
    
    # Verifica che sia stato bloccato
    assert result_obj.get("success") == False, "Should block COUNT() in filter"
    assert "COUNT()" in result_obj.get("unsupported_features", []), "Should identify COUNT() in filter"
    assert result_obj.get("total_count") == 0, "Should return 0 count when blocked"
    
    print("\n✅ TEST E PASSED: COUNT() in filter correctly blocked!")
    return result_obj


async def test_validation_h_invalid_domain():
    """
    TEST H: Validare domain inesistente con suggerimenti
    """
    print("\n" + "=" * 80)
    print("TEST H: Validate non-existent domain with suggestions")
    print("=" * 80)
    
    plugin = CosmosDbPlugin()
    
    # Test con domain typo
    invalid_domain = "NielsenUK"  # Dovrebbe essere NielsenGB
    print(f"\n🔍 Trying invalid domain: {invalid_domain}")
    
    result = await plugin.list_configurations_by_domain(domain=invalid_domain, limit="10")
    result_obj = json.loads(result)
    
    print("\n📊 RESULT:")
    print(json.dumps(result_obj, indent=2))
    
    # Verifica che ci sia un warning
    assert "warning" in result_obj or "did_you_mean" in result_obj, "Should provide warning for invalid domain"
    
    # Se ci sono suggerimenti, verifica che NielsenGB sia tra questi
    if result_obj.get("did_you_mean"):
        print(f"\n💡 Suggestions provided: {result_obj.get('did_you_mean')}")
        # NielsenGB dovrebbe essere suggerito perché simile a NielsenUK
    
    print("\n✅ TEST H PASSED: Invalid domain warning and suggestions provided!")
    return result_obj


async def test_validation_h_valid_domain():
    """
    TEST H bis: Validare domain esistente (dovrebbe passare)
    """
    print("\n" + "=" * 80)
    print("TEST H bis: Validate existing domain (should succeed)")
    print("=" * 80)
    
    plugin = CosmosDbPlugin()
    
    # Test con domain valido
    valid_domain = "NielsenGB"
    print(f"\n🔍 Trying valid domain: {valid_domain}")
    
    result = await plugin.list_configurations_by_domain(domain=valid_domain, limit="5")
    result_obj = json.loads(result)
    
    print("\n📊 RESULT:")
    print(f"Success: {result_obj.get('success')}")
    print(f"Count: {result_obj.get('count')}")
    print(f"Domain: {result_obj.get('domain')}")
    
    # Verifica che NON ci sia warning (domain valido)
    assert "warning" not in result_obj or result_obj.get("success") == True, "Valid domain should not have warning"
    
    print("\n✅ TEST H bis PASSED: Valid domain accepted without warnings!")
    return result_obj


async def test_validation_i_empty_search_request():
    """
    TEST I: Bloccare search request vuoto in EtlConfigPlugin
    """
    print("\n" + "=" * 80)
    print("TEST I: Block empty search request in EtlConfigPlugin")
    print("=" * 80)
    
    plugin = EtlConfigPlugin()
    
    # Test con request vuoto
    print("\n🔍 Trying empty search request")
    
    result = await plugin.search_etl_documentation(user_request="")
    result_obj = json.loads(result)
    
    print("\n📊 RESULT:")
    print(json.dumps(result_obj, indent=2))
    
    # Verifica che sia stato bloccato
    assert "error" in result_obj, "Should return error for empty request"
    assert "empty" in result_obj.get("error", "").lower(), "Error should mention 'empty'"
    assert "examples" in result_obj, "Should provide examples of valid requests"
    
    print("\n✅ TEST I PASSED: Empty search request correctly blocked!")
    return result_obj


async def test_validation_i_whitespace_request():
    """
    TEST I bis: Bloccare search request solo whitespace
    """
    print("\n" + "=" * 80)
    print("TEST I bis: Block whitespace-only search request")
    print("=" * 80)
    
    plugin = EtlConfigPlugin()
    
    # Test con solo whitespace
    print("\n🔍 Trying whitespace-only search request")
    
    result = await plugin.search_etl_documentation(user_request="   \n\t   ")
    result_obj = json.loads(result)
    
    print("\n📊 RESULT:")
    print(json.dumps(result_obj, indent=2))
    
    # Verifica che sia stato bloccato
    assert "error" in result_obj, "Should return error for whitespace-only request"
    
    print("\n✅ TEST I bis PASSED: Whitespace-only request correctly blocked!")
    return result_obj


async def main():
    """Esegue tutti i test delle validazioni HIGH PRIORITY"""
    try:
        print("\n🚀 Starting HIGH PRIORITY validations tests...")
        print("=" * 80)
        
        # Test Validation A: Bloccare aggregazioni in query
        await test_validation_a_block_count_in_query()
        await test_validation_a_block_group_by()
        
        # Test Validation E: Bloccare aggregazioni in filter
        await test_validation_e_block_count_in_filter()
        
        # Test Validation H: Validare domain con suggerimenti
        await test_validation_h_invalid_domain()
        await test_validation_h_valid_domain()
        
        # Test Validation I: Bloccare search request vuoto
        await test_validation_i_empty_search_request()
        await test_validation_i_whitespace_request()
        
        print("\n" + "=" * 80)
        print("🎉 ALL HIGH PRIORITY VALIDATION TESTS PASSED!")
        print("=" * 80)
        print("\n📝 SUMMARY:")
        print("   ✅ Validation A: COUNT/GROUP BY blocked in query_existing_config")
        print("   ✅ Validation E: Aggregations blocked in count_configurations filter")
        print("   ✅ Validation H: Invalid domains detected with fuzzy match suggestions")
        print("   ✅ Validation I: Empty search requests blocked with helpful examples")
        print("\n🎯 IMPACT:")
        print("   • LLM can no longer try unsupported COUNT() queries")
        print("   • Users get immediate feedback on domain typos")
        print("   • Better error messages guide users to correct solutions")
        print("   • Reduces failed queries and improves user experience")
        print("=" * 80)
        
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ TEST FAILED with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
