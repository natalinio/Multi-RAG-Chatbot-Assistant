"""
Test per la funzione count_configurations del Cosmos DB Plugin.
Verifica che il conteggio funzioni correttamente per vari filtri.
"""

import asyncio
import sys
import os
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.plugins.CosmosDbPlugin.CosmosDbPlugin import CosmosDbPlugin


async def test_count_all_configurations():
    """Test conteggio di tutte le configurazioni."""
    plugin = CosmosDbPlugin()
    
    print("\n" + "="*80)
    print("TEST 1: Count ALL configurations")
    print("="*80)
    
    result = await plugin.count_configurations(filter="")
    result_obj = json.loads(result)
    
    print(f"\n✅ Total configurations: {result_obj['total_count']}")
    print(f"\n📊 Statistics:")
    print(f"   Domains: {', '.join(result_obj['statistics']['unique_domains'])}")
    print(f"   Layers: {', '.join(result_obj['statistics']['unique_layers'])}")
    print(f"   Markets: {', '.join(result_obj['statistics']['unique_markets'][:10])}...")
    print(f"   Process Types: {', '.join(result_obj['statistics']['unique_process_types'])}")
    
    print(f"\n📄 Sample entities:")
    for entity in result_obj['sample_entities']:
        print(f"   - {entity}")
    
    await plugin.cleanup()


async def test_count_by_domain():
    """Test conteggio per dominio specifico."""
    plugin = CosmosDbPlugin()
    
    print("\n" + "="*80)
    print("TEST 2: Count configurations for NielsenGB domain")
    print("="*80)
    
    result = await plugin.count_configurations(filter="c.domain = 'NielsenGB'")
    result_obj = json.loads(result)
    
    print(f"\n✅ Configurations for NielsenGB: {result_obj['total_count']}")
    print(f"\n📊 Markets in NielsenGB:")
    for market in result_obj['statistics']['unique_markets']:
        print(f"   - {market}")
    
    print(f"\n📊 Layers in NielsenGB:")
    for layer in result_obj['statistics']['unique_layers']:
        print(f"   - {layer}")
    
    await plugin.cleanup()


async def test_count_by_layer():
    """Test conteggio per layer."""
    plugin = CosmosDbPlugin()
    
    print("\n" + "="*80)
    print("TEST 3: Count Bronze layer configurations")
    print("="*80)
    
    result = await plugin.count_configurations(filter="c.layer = 'Bronze'")
    result_obj = json.loads(result)
    
    print(f"\n✅ Bronze layer configurations: {result_obj['total_count']}")
    print(f"\n📊 Domains with Bronze layer:")
    for domain in result_obj['statistics']['unique_domains']:
        print(f"   - {domain}")
    
    await plugin.cleanup()


async def test_count_complex_filter():
    """Test conteggio con filtro complesso."""
    plugin = CosmosDbPlugin()
    
    print("\n" + "="*80)
    print("TEST 4: Count NielsenGB Bronze ingestion configs")
    print("="*80)
    
    result = await plugin.count_configurations(
        filter="c.domain = 'NielsenGB' AND c.layer = 'Bronze' AND c.process_requested = 'ingestion'"
    )
    result_obj = json.loads(result)
    
    print(f"\n✅ Matching configurations: {result_obj['total_count']}")
    print(f"\n📊 Markets:")
    for market in result_obj['statistics']['unique_markets']:
        print(f"   - {market}")
    
    print(f"\n📄 Entities:")
    for entity in result_obj['sample_entities']:
        print(f"   - {entity}")
    
    await plugin.cleanup()


async def test_count_by_source_type():
    """Test conteggio per source type (nested field)."""
    plugin = CosmosDbPlugin()
    
    print("\n" + "="*80)
    print("TEST 5: Count ASQL source configurations")
    print("="*80)
    
    result = await plugin.count_configurations(
        filter="c.I1_data_extract_process.source.type = 'ASQL'"
    )
    result_obj = json.loads(result)
    
    print(f"\n✅ ASQL configurations: {result_obj['total_count']}")
    print(f"\n📊 Domains using ASQL:")
    for domain in result_obj['statistics']['unique_domains']:
        print(f"   - {domain}")
    
    print(f"\n📄 Sample entities:")
    for entity in result_obj['sample_entities']:
        print(f"   - {entity}")
    
    await plugin.cleanup()


async def test_answer_user_question():
    """
    Simula la domanda dell'utente:
    "How many configs do we have in cosmos for NielsenGB and for how many partitions (market)?"
    """
    plugin = CosmosDbPlugin()
    
    print("\n" + "="*80)
    print("TEST 6: Answer User Question")
    print("Question: How many configs for NielsenGB and how many partitions?")
    print("="*80)
    
    # Query 1: Count total configs for NielsenGB
    print("\n🔍 Step 1: Count total configurations for NielsenGB...")
    result1 = await plugin.count_configurations(filter="c.domain = 'NielsenGB'")
    result1_obj = json.loads(result1)
    
    total_configs = result1_obj['total_count']
    markets = result1_obj['statistics']['unique_markets']
    num_markets = len(markets)
    
    # Query 2: Get distinct markets (già nel risultato precedente!)
    
    print(f"\n📊 ANSWER:")
    print(f"   ✅ Total configurations for NielsenGB: {total_configs}")
    print(f"   ✅ Number of distinct markets (partitions): {num_markets}")
    print(f"\n   Markets:")
    for market in markets:
        print(f"      - {market}")
    
    print(f"\n💡 Note: Used count_configurations() function instead of COUNT() aggregation")
    print(f"          because Cosmos DB SQL API doesn't support COUNT natively.")
    
    await plugin.cleanup()


async def main():
    """Run all count tests."""
    print("\n" + "="*80)
    print("COSMOS DB COUNT CONFIGURATIONS - TEST SUITE")
    print("="*80)
    
    await test_count_all_configurations()
    await test_count_by_domain()
    await test_count_by_layer()
    await test_count_complex_filter()
    await test_count_by_source_type()
    await test_answer_user_question()
    
    print("\n" + "="*80)
    print("✅ ALL COUNT TESTS COMPLETED!")
    print("="*80 + "\n")


if __name__ == "__main__":
    asyncio.run(main())
