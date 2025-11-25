"""
Analyze chunk sizes in processed_content.json
"""
import json
from pathlib import Path

# Load the processed content
processed_file = Path(__file__).parent / "processed" / "processed_content.json"

with open(processed_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Handle both list and dict formats
if isinstance(data, list):
    chunks = data
else:
    chunks = data.get('chunks', data)

print("="*70)
print("CHUNK SIZE ANALYSIS")
print("="*70)
print(f"\nTotal chunks: {len(chunks)}")

# Calculate sizes
sizes = [len(c.get('content', '')) for c in chunks]

print(f"\nChunk size statistics:")
print(f"  Minimum: {min(sizes):,} characters")
print(f"  Maximum: {max(sizes):,} characters")
print(f"  Average: {sum(sizes)//len(sizes):,} characters")
print(f"  Median: {sorted(sizes)[len(sizes)//2]:,} characters")

# Distribution
print(f"\nSize distribution:")
ranges = [
    (0, 500, "Very small (0-500)"),
    (500, 1000, "Small (500-1000)"),
    (1000, 2000, "Medium (1000-2000)"),
    (2000, 3000, "Large (2000-3000)"),
    (3000, 5000, "Very large (3000-5000)"),
    (5000, 10000, "Huge (5000-10000)"),
    (10000, 999999, "Massive (>10000)")
]

for min_size, max_size, label in ranges:
    count = sum(1 for s in sizes if min_size <= s < max_size)
    if count > 0:
        pct = (count / len(sizes)) * 100
        print(f"  {label:25} {count:3} chunks ({pct:5.1f}%)")

# Show examples
print(f"\n{'='*70}")
print("EXAMPLE CHUNKS")
print("="*70)

for i, chunk in enumerate(chunks[:3]):
    content = chunk.get('content', '')
    section = chunk.get('section', 'N/A')
    subsection = chunk.get('subsection', 'N/A')
    content_type = chunk.get('content_type', 'N/A')
    
    print(f"\nChunk {i+1}:")
    print(f"  Section: {section}")
    print(f"  Subsection: {subsection}")
    print(f"  Type: {content_type}")
    print(f"  Size: {len(content):,} characters")
    print(f"  Content preview:")
    print(f"  {'-'*66}")
    preview = content[:300].replace('\n', '\n  ')
    print(f"  {preview}")
    if len(content) > 300:
        print(f"  ... [truncated]")
    print()

# Check for problematic small chunks
small_chunks = [c for c in chunks if len(c.get('content', '')) < 1000]
print(f"\n{'='*70}")
print(f"SMALL CHUNKS ANALYSIS (< 1000 chars)")
print("="*70)
print(f"Found {len(small_chunks)} small chunks ({len(small_chunks)/len(chunks)*100:.1f}%)")

if small_chunks:
    print("\nExamples of small chunks:")
    for i, chunk in enumerate(small_chunks[:5]):
        content = chunk.get('content', '')
        section = chunk.get('section', 'N/A')
        print(f"\n  {i+1}. Section: {section}")
        print(f"     Size: {len(content)} chars")
        print(f"     Content: {content[:150]}...")
