"""
Test diretto della funzione count_configurations per verificare che funzioni.
"""
import asyncio
import sys
import os
from pathlib import Path

# Aggiungi la root del progetto al path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Importa dopo aver aggiustato il path
from app.plugins.CosmosDbPlugin.CosmosDbPlugin import CosmosDbPlugin
from app.services.cosmos_service import CosmosService
from app.core.config import get_settings
import json

# Ottieni le settings
settings = get_settings()


async def test_count_nielsenGB():
    """
    Test: Quante configurazioni abbiamo per NielsenGB e per quante partitions (market)?
    """
    print("\n" + "=" * 80)
    print("TEST: Count NielsenGB configurations with count_configurations() function")
    print("=" * 80)
    
    # Inizializza il plugin (crea il cosmos_service internamente)
    plugin = CosmosDbPlugin()
    
    # Esegui la count
    print("\n🔍 Calling count_configurations with filter: c.domain = 'NielsenGB'")
    result = await plugin.count_configurations(filter="c.domain = 'NielsenGB'")
    
    # Parse del risultato
    result_obj = json.loads(result)
    
    print("\n📊 RESULT:")
    print(json.dumps(result_obj, indent=2))
    
    # Estrai le informazioni chiave
    total_count = result_obj.get('total_count', 0)
    statistics = result_obj.get('statistics', {})
    unique_markets = statistics.get('unique_markets', [])
    
    print("\n" + "=" * 80)
    print("✅ RISPOSTA ALLA DOMANDA DELL'UTENTE:")
    print("=" * 80)
    print(f"📌 Total configurations for NielsenGB: {total_count}")
    print(f"📌 Number of distinct markets (partitions): {len(unique_markets)}")
    print(f"📌 Markets: {', '.join(unique_markets)}")
    print("=" * 80)
    
    # Verifica che ci siano risultati
    assert total_count > 0, "Should find at least some configurations for NielsenGB"
    assert len(unique_markets) > 0, "Should find at least one market"
    
    print("\n✅ TEST PASSED: count_configurations() works correctly!")
    
    return result_obj


async def test_count_all():
    """
    Test: Quante configurazioni abbiamo in totale?
    """
    print("\n" + "=" * 80)
    print("TEST: Count ALL configurations")
    print("=" * 80)
    
    # Inizializza il plugin (crea il cosmos_service internamente)
    plugin = CosmosDbPlugin()
    
    # Esegui la count senza filtro
    print("\n🔍 Calling count_configurations with NO filter (count all)")
    result = await plugin.count_configurations()
    
    # Parse del risultato
    result_obj = json.loads(result)
    
    print("\n📊 RESULT:")
    print(json.dumps(result_obj, indent=2))
    
    total_count = result_obj.get('total_count', 0)
    statistics = result_obj.get('statistics', {})
    
    print("\n" + "=" * 80)
    print(f"✅ Total configurations in database: {total_count}")
    print(f"✅ Unique domains: {len(statistics.get('unique_domains', []))}")
    print(f"✅ Unique layers: {len(statistics.get('unique_layers', []))}")
    print(f"✅ Unique markets: {len(statistics.get('unique_markets', []))}")
    print("=" * 80)
    
    assert total_count > 0, "Should find at least some configurations"
    
    print("\n✅ TEST PASSED: count_configurations() works without filter!")
    
    return result_obj


async def main():
    """Esegue tutti i test"""
    try:
        print("\n🚀 Starting direct count_configurations() tests...")
        
        # Test 1: Count per NielsenGB (la domanda originale dell'utente)
        await test_count_nielsenGB()
        
        # Test 2: Count totale
        await test_count_all()
        
        print("\n" + "=" * 80)
        print("🎉 ALL TESTS PASSED!")
        print("=" * 80)
        print("\n📝 CONCLUSION:")
        print("   ✅ count_configurations() function works correctly")
        print("   ✅ Can count with filters (c.domain = 'NielsenGB')")
        print("   ✅ Can count without filters (all configurations)")
        print("   ✅ Returns statistics (unique domains, layers, markets)")
        print("   ✅ User's question can now be answered correctly!")
        print("=" * 80)
        
    except Exception as e:
        print(f"\n❌ TEST FAILED with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
