"""
Ask router for question answering using RAG.

This endpoint:
1. Receives a user question
2. Retrieves relevant document chunks from vector store
3. Builds context from retrieved chunks
4. Sends question + context to LLM
5. Returns AI-generated answer with sources
"""
from typing import List
from fastapi import APIRouter, HTTPException
from langchain_core.documents import Document

from app.models.schemas import (
    AskRequest,
    AskResponse,
    RetrievedChunk,
    ErrorResponse
)
from app.services.rag_pipeline import get_rag_pipeline

# Create router
router = APIRouter(prefix="/ask", tags=["ask"])


@router.post(
    "/",
    response_model=AskResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Invalid request"},
        500: {"model": ErrorResponse, "description": "Server error"}
    }
)
async def ask_question(request: AskRequest):
    """
    Ask a question about your uploaded documents using RAG.

    This endpoint implements the complete RAG pipeline:

    1. **Retrieval**: Search vector database for relevant document chunks
       - Converts your question to an embedding
       - Finds chunks with similar embeddings (semantic search)
       - Returns top K most relevant chunks

    2. **Augmentation**: Build context for the LLM
       - Formats retrieved chunks into a context string
       - Adds metadata (source, page numbers, relevance scores)

    3. **Generation**: Generate answer using LLM
       - Sends question + context to the language model
       - LLM generates an answer based on the provided context
       - Returns structured response with sources

    4. **Tool Calling** (Optional): Execute functions during processing
       - If enabled, LLM can call predefined functions
       - Example: fetch_company_policy() to get specific policies
       - Results are added to the context

    Args:
        request: AskRequest containing:
            - question: Your question (required)
            - max_results: Number of chunks to retrieve (1-10, default: 4)
            - use_tool_calling: Enable function calling (default: False)

    Returns:
        AskResponse with:
        - answer: AI-generated answer
        - retrieved_chunks: List of document chunks used as context
        - tool_calls: Functions called during processing (if any)
        - tokens_used: Approximate token count

    Example Usage:
        ```bash
        curl -X POST "http://localhost:8000/ask/" \\
             -H "Content-Type: application/json" \\
             -d '{
                   "question": "What is the refund policy?",
                   "max_results": 3,
                   "use_tool_calling": false
                 }'
        ```

    Example Response:
        ```json
        {
            "answer": "According to the documentation, the refund policy...",
            "retrieved_chunks": [
                {
                    "content": "Our refund policy states...",
                    "metadata": {
                        "source": "policy.pdf",
                        "page": 5
                    },
                    "similarity_score": 0.89
                }
            ],
            "tool_calls": null,
            "tokens_used": 450
        }
        ```
    """
    # Validate question
    if not request.question or len(request.question.strip()) == 0:
        raise HTTPException(
            status_code=400,
            detail={
                "error": "Invalid question",
                "detail": "Question cannot be empty"
            }
        )

    try:
        # Get RAG pipeline instance
        rag = get_rag_pipeline()

        # BUILD DOCUMENT FILTER to prevent cross-document contamination
        document_filter = None

        if request.document_id:
            # Filter by specific document ID
            document_filter = {"document_id": request.document_id}
        elif request.filename:
            # Filter by filename
            document_filter = {"source": request.filename}
        elif request.use_latest_document:
            # Query only the latest document (RECOMMENDED FOR CV/RESUME QUERIES)
            # Get the most recently uploaded filename
            from app.services.supabase_store import get_vector_store
            vector_store = get_vector_store()

            try:
                # Get the latest document by querying metadata
                # The metadata is stored as JSONB, so we need to extract the source field
                latest_doc_response = vector_store.supabase_client.table("documents").select(
                    "metadata, id"
                ).order("id", desc=True).limit(1).execute()

                print(f"📊 Latest doc query response: {latest_doc_response.data}")

                if latest_doc_response.data and len(latest_doc_response.data) > 0:
                    metadata = latest_doc_response.data[0].get("metadata", {})
                    latest_filename = metadata.get("source")

                    if latest_filename:
                        document_filter = {"source": latest_filename}
                        print(f"🎯 FILTERING TO LATEST DOCUMENT: {latest_filename}")
                        print(f"🔍 Filter being applied: {document_filter}")
                    else:
                        print(f"⚠️ No 'source' found in metadata: {metadata}")
                else:
                    print("⚠️ No documents found in database")
            except Exception as e:
                print(f"❌ Error determining latest document: {e}")
                import traceback
                traceback.print_exc()
                # Continue without filter (query all documents)

        # Generate answer using RAG with document filtering
        result = rag.generate_answer(
            question=request.question,
            max_results=request.max_results,
            use_tool_calling=request.use_tool_calling,
            document_filter=document_filter  # CRITICAL: Apply filter!
        )

        # Convert retrieved documents to RetrievedChunk schema
        retrieved_chunks = []
        for doc, score in result["retrieved_docs"]:
            chunk = RetrievedChunk(
                content=doc.page_content,
                metadata=doc.metadata,
                similarity_score=round(score, 4) if score else None
            )
            retrieved_chunks.append(chunk)

        # Build response
        response = AskResponse(
            answer=result["answer"],
            retrieved_chunks=retrieved_chunks,
            tool_calls=result.get("tool_calls"),
            tokens_used=result.get("tokens_used")
        )

        return response

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Failed to process question",
                "detail": str(e)
            }
        )


@router.get("/health")
async def health_check():
    """
    Health check endpoint for the ask service.

    Returns:
        Status message confirming the service is running

    Example Response:
        ```json
        {
            "status": "healthy",
            "service": "ask"
        }
        ```
    """
    return {
        "status": "healthy",
        "service": "ask"
    }


@router.post("/simple")
async def ask_simple(question: str):
    """
    Simplified ask endpoint that accepts just a question string.

    This is a convenience endpoint for quick testing.
    It uses default settings (4 chunks, no tool calling).

    Args:
        question: The question to ask (as query parameter or form data)

    Returns:
        Simple response with just the answer text

    Example Usage:
        ```bash
        curl -X POST "http://localhost:8000/ask/simple?question=What+is+the+refund+policy"
        ```

    Example Response:
        ```json
        {
            "answer": "The refund policy allows returns within 30 days..."
        }
        ```
    """
    try:
        # Use default settings
        request = AskRequest(
            question=question,
            max_results=4,
            use_tool_calling=False
        )

        # Get answer
        rag = get_rag_pipeline()
        result = rag.generate_answer(
            question=request.question,
            max_results=request.max_results,
            use_tool_calling=request.use_tool_calling
        )

        # Return simple response
        return {
            "answer": result["answer"]
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Failed to process question",
                "detail": str(e)
            }
        )
