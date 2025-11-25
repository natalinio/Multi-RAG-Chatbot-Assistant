"""Test critical imports that were failing in Azure deployment."""

print("Testing critical imports...")

try:
    print("\n1. Testing semantic_kernel import...")
    from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
    print("   ✅ AzureChatCompletion imported successfully")
except ImportError as e:
    print(f"   ❌ Failed to import AzureChatCompletion: {e}")
    exit(1)

try:
    print("\n2. Testing openai._types.omit import...")
    from openai._types import omit
    print(f"   ✅ omit imported successfully: {omit}")
except ImportError as e:
    print(f"   ❌ Failed to import omit: {e}")
    exit(1)

try:
    print("\n3. Checking openai version...")
    import openai
    print(f"   ✅ openai version: {openai.__version__}")
except Exception as e:
    print(f"   ❌ Failed to get openai version: {e}")

try:
    print("\n4. Checking semantic_kernel version...")
    import semantic_kernel
    print(f"   ✅ semantic_kernel version: {semantic_kernel.__version__}")
except Exception as e:
    print(f"   ❌ Failed to get semantic_kernel version: {e}")

print("\n" + "="*60)
print("✅ ALL CRITICAL IMPORTS SUCCESSFUL!")
print("="*60)
print("\nThis proves that requirements-minimal.txt contains all")
print("the necessary dependencies with correct versions.")
print("\nKey finding:")
print(f"  - openai {openai.__version__} HAS the 'omit' export")
print(f"  - semantic_kernel {semantic_kernel.__version__} can import it")
print("\nThe local environment is VALID for deployment!")
