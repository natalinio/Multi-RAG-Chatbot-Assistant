"""Check what ASQL documentation is indexed"""
import json
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

processed_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'processed', 'processed_content.json')

with open(processed_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Cerca chunks che parlano di ASQL / Azure SQL
print("SEARCHING FOR AZURE SQL DOCUMENTATION...\n")
found_asql = False

# Handle both list and dict formats
chunks = data if isinstance(data, list) else data.get('chunks', data)

for idx, chunk in enumerate(chunks):
    # Handle different chunk formats
    text = chunk.get('text', chunk.get('content', ''))
    if 'asql' in text.lower() or 'connection_type' in text.lower():
        found_asql = True
        print(f"{'='*80}")
        entity = chunk.get('metadata', {}).get('entity', chunk.get('section', 'Doc chunk'))
        source = chunk.get('metadata', {}).get('source', chunk.get('content_type', 'N/A'))
        print(f"CHUNK {idx}: {entity}")
        print(f"Source: {source}")
        print(f"{'='*80}")
        print(text[:2000])
        print(f"\n(Total: {len(text)} chars)\n\n")

if not found_asql:
    print("❌ NO ASQL DOCUMENTATION FOUND IN INDEXED CHUNKS")
    print("\nAll chunks and their sources:")
    for idx, chunk in enumerate(chunks):
        entity = chunk.get('metadata', {}).get('entity', chunk.get('section', 'N/A'))[:50]
        source = chunk.get('metadata', {}).get('source', chunk.get('content_type', 'N/A'))[:20]
        print(f"{idx:2d}. {source:20s} - {entity}")
