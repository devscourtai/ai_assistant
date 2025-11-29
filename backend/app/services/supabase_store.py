"""
Supabase Vector Store service for storing and retrieving document embeddings.

What is a vector store?
A vector store is a specialized database that can:
1. Store embeddings (vectors) along with their original text
2. Perform similarity search (find vectors close to a query vector)
3. Return the most relevant documents based on semantic similarity

We use Supabase with pgvector extension, which adds vector capabilities to PostgreSQL.
"""
import os
from typing import List, Tuple, Optional
from langchain_core.documents import Document
from langchain_community.vectorstores import SupabaseVectorStore
from supabase.client import Client, create_client
from dotenv import load_dotenv

from app.services.embeddings import get_embedding_service

# Load environment variables
load_dotenv()


class VectorStoreService:
    """
    Service for managing document storage and retrieval in Supabase vector database.

    This class provides a simple interface for:
    - Storing documents with their embeddings
    - Searching for similar documents
    - Managing the vector store
    """

    def __init__(self, table_name: str = "documents"):
        """
        Initialize the Supabase vector store connection.

        Args:
            table_name: Name of the table in Supabase to store documents
                       Default: "documents"

        Note:
            Requires environment variables:
            - SUPABASE_URL: Your Supabase project URL
            - SUPABASE_KEY: Your Supabase API key (service_role key recommended)
        """
        # Get Supabase credentials from environment
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_KEY")

        if not supabase_url or not supabase_key:
            raise ValueError(
                "SUPABASE_URL and SUPABASE_KEY must be set in environment variables. "
                "Please add them to your .env file."
            )

        # Create Supabase client
        self.supabase_client: Client = create_client(supabase_url, supabase_key)
        self.table_name = table_name

        # Get embedding service
        self.embedding_service = get_embedding_service()

        # Initialize LangChain's SupabaseVectorStore
        # This will handle all vector operations for us
        self.vector_store = SupabaseVectorStore(
            client=self.supabase_client,
            embedding=self.embedding_service.embeddings,
            table_name=self.table_name,
            query_name=f"match_{self.table_name}"  # Name of the similarity search function
        )

    def store_documents(
        self,
        documents: List[Document],
        batch_size: int = 100
    ) -> List[str]:
        """
        Store documents and their embeddings in Supabase.

        This method:
        1. Takes a list of Document objects
        2. Generates embeddings for each document
        3. Stores both the text and embeddings in Supabase

        Args:
            documents: List of Document objects to store
            batch_size: Number of documents to process at once (for large uploads)

        Returns:
            List of document IDs that were created

        Example:
            >>> from langchain.schema import Document
            >>> docs = [Document(page_content="text", metadata={"source": "file.pdf"})]
            >>> store = VectorStoreService()
            >>> ids = store.store_documents(docs)
            >>> print(f"Stored {len(ids)} documents")
        """
        # Use LangChain's add_documents method
        # This automatically generates embeddings and stores them
        document_ids = self.vector_store.add_documents(documents)

        return document_ids

    def search(
        self,
        query: str,
        k: int = 4,
        filter_dict: Optional[dict] = None
    ) -> List[Tuple[Document, float]]:
        """
        Search for documents similar to the query with POST-FILTERING.

        IMPORTANT: LangChain's JSONB filter doesn't work reliably with Supabase,
        so we retrieve MORE results and filter in Python.

        This performs semantic similarity search:
        1. Convert query to embedding
        2. Find documents with similar embeddings
        3. Filter by metadata in Python (more reliable!)
        4. Return the top K most similar documents

        Args:
            query: The search query (user's question)
            k: Number of results to return (default: 4)
            filter_dict: Optional metadata filter (e.g., {"source": "specific.pdf"})

        Returns:
            List of tuples (Document, similarity_score)
            similarity_score ranges from 0 to 1, where 1 is most similar
        """
        # DEBUG LOGGING
        print(f"\n{'='*60}")
        print(f"🔍 VECTOR SEARCH CALLED")
        print(f"📝 Query: {query[:100]}...")
        print(f"🎯 K requested: {k}")
        print(f"🔧 Filter: {filter_dict}")

        # CRITICAL FIX: Retrieve MORE results to ensure we get matches
        # Then filter in Python since LangChain's JSONB filter is unreliable
        retrieve_k = k * 10 if filter_dict else k  # Get 10x more if filtering
        print(f"📊 Retrieving {retrieve_k} results (will filter to {k})")
        print(f"{'='*60}\n")

        # Get results WITHOUT LangChain filter (it doesn't work!)
        results = self.vector_store.similarity_search_with_relevance_scores(
            query=query,
            k=retrieve_k,
            filter=None  # DON'T use LangChain's filter - it fails!
        )

        print(f"📥 Raw results before filtering: {len(results)}")

        # DEBUG: Show what metadata we got
        if results and filter_dict:
            print(f"\n🔬 INSPECTING METADATA (first 3 results):")
            for i, (doc, score) in enumerate(results[:3], 1):
                print(f"  Result {i}:")
                print(f"    Score: {score:.3f}")
                print(f"    Metadata keys: {list(doc.metadata.keys())}")
                print(f"    source: {doc.metadata.get('source', 'MISSING!')}")
                print(f"    document_id: {doc.metadata.get('document_id', 'MISSING!')[:20]}...")
                print(f"    Filtering for: {filter_dict}")
                print()

        # POST-FILTER in Python (much more reliable!)
        if filter_dict:
            filtered_results = []
            for doc, score in results:
                # Check if document matches ALL filter criteria
                matches = True
                for key, value in filter_dict.items():
                    doc_value = doc.metadata.get(key)
                    if doc_value != value:
                        print(f"  ❌ MISMATCH: {key}='{doc_value}' != '{value}'")
                        matches = False
                        break

                if matches:
                    print(f"  ✅ MATCH: Adding document with {key}='{value}'")
                    filtered_results.append((doc, score))

                # Stop once we have enough matching results
                if len(filtered_results) >= k:
                    break

            results = filtered_results
            print(f"\n✅ After Python filtering: {len(results)} matches")
        else:
            results = results[:k]

        # DEBUG: Show what was retrieved
        print(f"\n{'='*60}")
        print(f"✅ FINAL SEARCH RESULTS ({len(results)} documents)")
        for i, (doc, score) in enumerate(results, 1):
            source = doc.metadata.get('source', 'Unknown')
            doc_id = doc.metadata.get('document_id', 'Unknown')[:8]
            print(f"  {i}. {source} (doc_id: {doc_id}..., score: {score:.3f})")
        print(f"{'='*60}\n")

        return results

    def search_by_vector(
        self,
        embedding: List[float],
        k: int = 4
    ) -> List[Tuple[Document, float]]:
        """
        Search for documents similar to a given embedding vector.

        This is useful when you already have an embedding and want to find similar documents
        without generating a new embedding.

        Args:
            embedding: The query embedding vector
            k: Number of results to return

        Returns:
            List of tuples (Document, similarity_score)
        """
        # Use the underlying Supabase client for vector similarity search
        # This is more advanced usage
        results = self.vector_store.similarity_search_by_vector(
            embedding=embedding,
            k=k
        )

        # Convert to (Document, score) tuples
        # Note: When using similarity_search_by_vector, we don't get scores by default
        # For simplicity, we'll return score as None or 1.0
        return [(doc, 1.0) for doc in results]

    def delete_documents(self, document_ids: List[str]) -> bool:
        """
        Delete documents from the vector store.

        Args:
            document_ids: List of document IDs to delete

        Returns:
            True if deletion was successful

        Note:
            This requires direct access to Supabase client
        """
        try:
            # Delete from Supabase table
            self.supabase_client.table(self.table_name).delete().in_(
                "id", document_ids
            ).execute()
            return True
        except Exception as e:
            print(f"Error deleting documents: {e}")
            return False

    def get_collection_stats(self) -> dict:
        """
        Get statistics about the document collection.

        Returns:
            Dictionary with stats like total document count

        Example:
            >>> store = VectorStoreService()
            >>> stats = store.get_collection_stats()
            >>> print(f"Total documents: {stats['total_documents']}")
        """
        try:
            # Query the total count of documents
            response = self.supabase_client.table(self.table_name).select(
                "id", count="exact"
            ).execute()

            return {
                "total_documents": response.count if hasattr(response, 'count') else 0,
                "table_name": self.table_name
            }
        except Exception as e:
            print(f"Error getting stats: {e}")
            return {"total_documents": 0, "table_name": self.table_name}


# Global instance for easy access
_vector_store_service = None


def get_vector_store() -> VectorStoreService:
    """
    Get or create the global vector store service instance.

    Returns:
        The global VectorStoreService instance

    Example:
        >>> store = get_vector_store()
        >>> results = store.search("my query")
    """
    global _vector_store_service
    if _vector_store_service is None:
        _vector_store_service = VectorStoreService()
    return _vector_store_service
