"""
Upload router for handling document uploads.

This endpoint:
1. Accepts file uploads (PDF, DOCX, TXT)
2. Extracts text from the files
3. Chunks the text
4. Generates embeddings
5. Stores everything in Supabase
"""
import os
import uuid
import tempfile
from typing import List
from fastapi import APIRouter, UploadFile, File, HTTPException
from langchain_core.documents import Document
from langchain_community.document_loaders import (
    PyPDFLoader,
    UnstructuredWordDocumentLoader,
    TextLoader
)

from app.models.schemas import UploadResponse, ErrorResponse
from app.utils.chunker import chunk_documents
from app.services.supabase_store import get_vector_store

# Create router
router = APIRouter(prefix="/upload", tags=["upload"])

# Allowed file extensions
ALLOWED_EXTENSIONS = {".pdf", ".docx", ".doc", ".txt"}


def get_file_extension(filename: str) -> str:
    """
    Extract file extension from filename.

    Args:
        filename: Name of the file

    Returns:
        File extension (e.g., ".pdf")
    """
    return os.path.splitext(filename)[1].lower()


def load_document(file_path: str, filename: str) -> List[Document]:
    """
    Load a document using the appropriate LangChain loader.

    Args:
        file_path: Path to the file on disk
        filename: Original filename (used to determine file type)

    Returns:
        List of Document objects

    Raises:
        ValueError: If file type is not supported
    """
    extension = get_file_extension(filename)

    try:
        if extension == ".pdf":
            # Use PyPDFLoader for PDF files
            # This extracts text page by page
            loader = PyPDFLoader(file_path)
            documents = loader.load()

        elif extension in [".docx", ".doc"]:
            # Use UnstructuredWordDocumentLoader for Word files
            loader = UnstructuredWordDocumentLoader(file_path)
            documents = loader.load()

        elif extension == ".txt":
            # Use TextLoader for plain text files
            loader = TextLoader(file_path, encoding="utf-8")
            documents = loader.load()

        else:
            raise ValueError(f"Unsupported file type: {extension}")

        # Add filename to metadata for all documents
        for doc in documents:
            doc.metadata["source"] = filename
            doc.metadata["file_type"] = extension

        return documents

    except Exception as e:
        raise ValueError(f"Error loading document: {str(e)}")


@router.post(
    "/",
    response_model=UploadResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Invalid file type or processing error"},
        500: {"model": ErrorResponse, "description": "Server error"}
    }
)
async def upload_document(
    file: UploadFile = File(..., description="Document file to upload (PDF, DOCX, or TXT)")
):
    """
    Upload a document and process it for question answering.

    This endpoint performs the following steps:
    1. Validates the file type
    2. Saves the file temporarily
    3. Extracts text using LangChain document loaders
    4. Chunks the text into smaller pieces
    5. Generates embeddings for each chunk
    6. Stores chunks and embeddings in Supabase vector database

    Args:
        file: The uploaded file (FastAPI automatically handles multipart/form-data)

    Returns:
        UploadResponse with:
        - Success message
        - Filename
        - Number of chunks created
        - Document ID

    Example Usage:
        ```bash
        curl -X POST "http://localhost:8000/upload/" \\
             -F "file=@document.pdf"
        ```

    Example Response:
        ```json
        {
            "message": "Document uploaded successfully",
            "filename": "document.pdf",
            "chunks_created": 15,
            "document_id": "123e4567-e89b-12d3-a456-426614174000"
        }
        ```
    """
    # Step 1: Validate file type
    extension = get_file_extension(file.filename)

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail={
                "error": "Invalid file type",
                "detail": f"Allowed types: {', '.join(ALLOWED_EXTENSIONS)}"
            }
        )

    # Step 2: Save file temporarily
    # We need to save the uploaded file to disk so LangChain loaders can read it
    try:
        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=extension) as tmp_file:
            # Read uploaded file content
            content = await file.read()

            # Write to temporary file
            tmp_file.write(content)
            tmp_file_path = tmp_file.name

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Failed to save file",
                "detail": str(e)
            }
        )

    try:
        # Step 3: Load and extract text from document
        documents = load_document(tmp_file_path, file.filename)

        # Step 4: Chunk the documents with IMPROVED strategy
        # Smaller chunks (500) for better precision
        # Less overlap (100) to avoid redundancy
        chunked_docs = chunk_documents(
            documents,
            chunk_size=500,
            chunk_overlap=100
        )

        # Generate a unique document ID
        document_id = str(uuid.uuid4())

        # Add document_id to all chunks for tracking
        for doc in chunked_docs:
            doc.metadata["document_id"] = document_id

        # Step 5 & 6: Generate embeddings and store in Supabase
        # The vector store handles this automatically
        vector_store = get_vector_store()
        chunk_ids = vector_store.store_documents(chunked_docs)

        # Step 7: Clean up temporary file
        os.unlink(tmp_file_path)

        # Step 8: Return success response
        return UploadResponse(
            message="Document uploaded successfully",
            filename=file.filename,
            chunks_created=len(chunked_docs),
            document_id=document_id
        )

    except ValueError as e:
        # Clean up temp file on error
        if os.path.exists(tmp_file_path):
            os.unlink(tmp_file_path)

        raise HTTPException(
            status_code=400,
            detail={
                "error": "Document processing error",
                "detail": str(e)
            }
        )

    except Exception as e:
        # Clean up temp file on error
        if os.path.exists(tmp_file_path):
            os.unlink(tmp_file_path)

        raise HTTPException(
            status_code=500,
            detail={
                "error": "Failed to process document",
                "detail": str(e)
            }
        )


@router.get("/stats")
async def get_upload_stats():
    """
    Get statistics about uploaded documents.

    Returns:
        Dictionary with collection statistics

    Example Response:
        ```json
        {
            "total_documents": 42,
            "table_name": "documents"
        }
        ```
    """
    try:
        vector_store = get_vector_store()
        stats = vector_store.get_collection_stats()
        return stats

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Failed to get stats",
                "detail": str(e)
            }
        )


@router.get("/list-documents")
async def list_all_documents():
    """
    List all unique documents in the database with their metadata.

    This helps debug which documents are actually stored.
    """
    try:
        vector_store = get_vector_store()

        # Get all unique document sources
        response = vector_store.supabase_client.table("documents").select(
            "id, metadata"
        ).order("id", desc=True).execute()

        documents = []
        seen_sources = set()

        for row in response.data:
            metadata = row.get("metadata", {})
            source = metadata.get("source", "Unknown")

            if source not in seen_sources:
                seen_sources.add(source)
                documents.append({
                    "filename": source,
                    "document_id": metadata.get("document_id"),
                    "file_type": metadata.get("file_type"),
                    "id": row.get("id")
                })

        return {
            "total_chunks": len(response.data),
            "unique_documents": len(documents),
            "documents": documents
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Failed to list documents",
                "detail": str(e)
            }
        )


@router.get("/debug-embeddings")
async def debug_embeddings():
    """
    🔍 DEBUG: Check if embeddings are actually stored in the database.
    """
    try:
        vector_store = get_vector_store()

        # Query to check if documents have non-null embeddings
        response = vector_store.supabase_client.table("documents").select(
            "id, metadata, embedding"
        ).limit(5).execute()

        results = []
        for row in response.data:
            embedding = row.get("embedding")
            results.append({
                "id": row.get("id"),
                "source": row.get("metadata", {}).get("source"),
                "has_embedding": embedding is not None,
                "embedding_length": len(embedding) if embedding else 0,
                "embedding_preview": str(embedding[:3]) if embedding else "NULL"
            })

        return {
            "total_documents": len(response.data),
            "documents": results
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Failed to debug embeddings",
                "detail": str(e)
            }
        )


@router.delete("/clear-all")
async def clear_all_documents():
    """
    ⚠️ DANGER: Delete ALL documents from the vector store.

    Use this to start fresh when testing.
    """
    try:
        vector_store = get_vector_store()

        # Delete all rows from documents table
        # Use minimum UUID to match all rows (works with UUID primary key)
        delete_response = vector_store.supabase_client.table("documents").delete().gte(
            "id", "00000000-0000-0000-0000-000000000000"  # Match all UUIDs
        ).execute()

        return {
            "message": "All documents deleted",
            "details": "Vector store cleared successfully"
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Failed to clear documents",
                "detail": str(e)
            }
        )
