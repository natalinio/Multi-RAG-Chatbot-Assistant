"""
Re-index Azure AI Search with extended ETL documentation and JSON examples
Replaces old index with new content
"""

import json
import os
from pathlib import Path
from azure.search.documents import SearchClient
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    SearchIndex,
    SearchField,
    SearchFieldDataType,
    SimpleField,
    SearchableField,
    SemanticConfiguration,
    SemanticField,
    SemanticPrioritizedFields,
    SemanticSearch,
)
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

class AzureSearchReIndexer:
    """Re-index Azure AI Search with extended documentation and JSON examples"""
    
    def __init__(self):
        """Initialize Azure Search client"""
        self.endpoint = os.getenv("AZURE_AI_SEARCH_ENDPOINT")
        self.key = os.getenv("AZURE_AI_SEARCH_KEY")
        self.index_name = os.getenv("AZURE_AI_SEARCH_INDEX_NAME", "cpgai-gda-version")
        
        if not self.endpoint or not self.key:
            raise ValueError("AZURE_AI_SEARCH_ENDPOINT and AZURE_AI_SEARCH_KEY must be set")
        
        self.credential = AzureKeyCredential(self.key)
        self.index_client = SearchIndexClient(endpoint=self.endpoint, credential=self.credential)
        self.search_client = SearchClient(endpoint=self.endpoint, index_name=self.index_name, credential=self.credential)
        
        logger.info(f"Initialized Azure Search client for index: {self.index_name}")
    
    def delete_index(self):
        """Delete existing index"""
        try:
            self.index_client.delete_index(self.index_name)
            logger.info(f"✓ Deleted existing index: {self.index_name}")
        except Exception as e:
            logger.warning(f"Index {self.index_name} doesn't exist or error deleting: {e}")
    
    def create_index(self):
        """Create new index with semantic search configuration"""
        logger.info("Creating new index with semantic search...")
        
        fields = [
            SimpleField(
                name="id",
                type=SearchFieldDataType.String,
                key=True,
                filterable=True
            ),
            SearchableField(
                name="title",
                type=SearchFieldDataType.String,
                searchable=True,
                retrievable=True
            ),
            SearchableField(
                name="content",
                type=SearchFieldDataType.String,
                searchable=True,
                retrievable=True
            ),
            SimpleField(
                name="source",
                type=SearchFieldDataType.String,
                filterable=True,
                facetable=True
            ),
            SimpleField(
                name="source_file",
                type=SearchFieldDataType.String,
                filterable=True
            ),
            SimpleField(
                name="entity",
                type=SearchFieldDataType.String,
                filterable=True,
                facetable=True
            ),
            SimpleField(
                name="layer",
                type=SearchFieldDataType.String,
                filterable=True,
                facetable=True
            ),
            SimpleField(
                name="domain",
                type=SearchFieldDataType.String,
                filterable=True,
                facetable=True
            ),
            SimpleField(
                name="process_type",
                type=SearchFieldDataType.String,
                filterable=True,
                facetable=True
            ),
            SimpleField(
                name="metadata_json",
                type=SearchFieldDataType.String,
                retrievable=True
            ),
        ]
        
        # Configure semantic search
        semantic_config = SemanticConfiguration(
            name="default",
            prioritized_fields=SemanticPrioritizedFields(
                title_field=SemanticField(field_name="title"),  # Use semantic title instead of entity
                content_fields=[SemanticField(field_name="content")]
            )
        )
        
        semantic_search = SemanticSearch(configurations=[semantic_config])
        
        index = SearchIndex(
            name=self.index_name,
            fields=fields,
            semantic_search=semantic_search
        )
        
        self.index_client.create_index(index)
        logger.info(f"✓ Created new index: {self.index_name}")
    
    def load_processed_content(self):
        """Load processed content from extended processor"""
        processed_file = Path(__file__).parent / "processed" / "processed_content.json"
        
        if not processed_file.exists():
            raise FileNotFoundError(f"Processed content not found: {processed_file}")
        
        logger.info(f"Loading processed content from {processed_file}")
        
        with open(processed_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Handle both list format (new) and dict format (old)
        if isinstance(data, list):
            chunks = data
            logger.info(f"Loaded {len(chunks)} chunks from list format")
        else:
            chunks = data['chunks']
            logger.info(f"Loaded {data['total_chunks']} chunks from dict format")
        
        return chunks
    
    def upload_documents(self, chunks):
        """Upload documents to Azure Search"""
        logger.info(f"Uploading {len(chunks)} documents to Azure Search...")
        
        documents = []
        
        for idx, chunk in enumerate(chunks):
            metadata = chunk.get('metadata', {})
            
            # Extract key metadata for filtering/faceting
            source = metadata.get('source', 'unknown')
            entity = metadata.get('entity', '')
            layer = metadata.get('layer', '')
            domain = metadata.get('domain', '')
            process_type = metadata.get('process_type', '')
            source_file = metadata.get('source_file', '')
            
            # Get semantic title (prefer chunk title if available, fallback to entity or section)
            title = chunk.get('title', '')
            if not title:
                # Fallback: try section + subsection for DOCX chunks
                section = chunk.get('section', '')
                subsection = chunk.get('subsection', '')
                if section and subsection:
                    title = f"{section} - {subsection}"
                elif section:
                    title = section
                elif entity:
                    title = entity
                else:
                    title = "ETL Configuration"
            
            doc = {
                "id": f"chunk_{idx:04d}",
                "title": title,  # NEW: Semantic title field
                "content": chunk.get('text', '') or chunk.get('content', ''),  # Support both formats
                "source": source,
                "source_file": source_file,
                "entity": entity if entity else f"({source})",
                "layer": layer if layer else "General",
                "domain": domain if domain else "General",
                "process_type": process_type if process_type else "documentation",
                "metadata_json": json.dumps(metadata)
            }
            
            documents.append(doc)
        
        # Upload in batches
        batch_size = 100
        for i in range(0, len(documents), batch_size):
            batch = documents[i:i+batch_size]
            
            try:
                result = self.search_client.upload_documents(documents=batch)
                logger.info(f"  Batch {i//batch_size + 1}: Uploaded {len(batch)} documents (HTTP {result[0].status_code if result else 'N/A'})")
            except Exception as e:
                logger.error(f"Error uploading batch {i//batch_size + 1}: {e}")
                raise
        
        logger.info(f"✓ Successfully uploaded all {len(documents)} documents")
        
        return len(documents)
    
    def verify_index(self):
        """Verify index was created and populated"""
        try:
            # Get index stats
            stats = self.search_client.get_document_count()
            logger.info(f"✓ Index verification: {stats} documents in index")
            
            # Test a simple query
            results = self.search_client.search(search_text="SAPBW", top=3)
            doc_count = 0
            for result in results:
                doc_count += 1
                logger.info(f"  - Found: {result['entity']} ({result['source']})")
            
            logger.info(f"✓ Test query successful: Retrieved {doc_count} documents")
            
        except Exception as e:
            logger.error(f"Index verification failed: {e}")
            raise
    
    def reindex(self):
        """Execute full re-indexing process"""
        logger.info("=" * 70)
        logger.info("Starting Azure AI Search Re-Indexing")
        logger.info("=" * 70)
        
        try:
            # 1. Delete old index
            self.delete_index()
            
            # 2. Create new index
            self.create_index()
            
            # 3. Load processed content
            chunks = self.load_processed_content()
            
            # 4. Upload documents
            doc_count = self.upload_documents(chunks)
            
            # 5. Verify index
            self.verify_index()
            
            logger.info("\n" + "=" * 70)
            logger.info("✅ Re-Indexing Completed Successfully")
            logger.info("=" * 70)
            logger.info(f"Index: {self.index_name}")
            logger.info(f"Total documents: {doc_count}")
            logger.info(f"Status: Ready for RAG queries")
            logger.info("=" * 70 + "\n")
            
        except Exception as e:
            logger.error(f"\n❌ Re-Indexing Failed: {e}", exc_info=True)
            raise


def main():
    """Main entry point"""
    try:
        reindexer = AzureSearchReIndexer()
        reindexer.reindex()
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        exit(1)


if __name__ == "__main__":
    main()
