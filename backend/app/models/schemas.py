"""
Pydantic schemas for request and response validation.
These models define the structure of data coming in and going out of our API.
"""
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


# ============================================================================
# UPLOAD ENDPOINT SCHEMAS
# ============================================================================

class UploadResponse(BaseModel):
    """
    Response returned after successfully uploading a document.

    Attributes:
        message: Success message
        filename: Name of the uploaded file
        chunks_created: Number of text chunks generated from the document
        document_id: Unique identifier for the uploaded document
    """
    message: str
    filename: str
    chunks_created: int
    document_id: str


# ============================================================================
# ASK ENDPOINT SCHEMAS
# ============================================================================

class AskRequest(BaseModel):
    """
    Request body for asking questions about uploaded documents.

    NEW: Added document filtering to prevent cross-document contamination

    Attributes:
        question: The user's question
        max_results: Maximum number of relevant chunks to retrieve (default: 4)
        use_tool_calling: Whether to enable function/tool calling (default: False)
        document_id: Filter by specific document ID (optional)
        filename: Filter by filename (optional)
        use_latest_document: Query only the latest uploaded document (default: True)
    """
    question: str = Field(..., description="The question to ask about your documents")
    max_results: int = Field(default=4, ge=1, le=10, description="Number of relevant chunks to retrieve")
    use_tool_calling: bool = Field(default=False, description="Enable tool/function calling")
    document_id: Optional[str] = Field(default=None, description="Filter results to specific document ID")
    filename: Optional[str] = Field(default=None, description="Filter results to specific filename")
    use_latest_document: bool = Field(default=True, description="Query only the most recently uploaded document")


class RetrievedChunk(BaseModel):
    """
    A single chunk of text retrieved from the vector database.

    Attributes:
        content: The actual text content of the chunk
        metadata: Additional information (filename, page number, etc.)
        similarity_score: How relevant this chunk is to the question (0-1)
    """
    content: str
    metadata: Dict[str, Any]
    similarity_score: Optional[float] = None


class ToolCall(BaseModel):
    """
    Represents a function/tool call made by the LLM.

    Attributes:
        tool_name: Name of the function/tool called
        arguments: Arguments passed to the function
        result: Result returned by the function
    """
    tool_name: str
    arguments: Dict[str, Any]
    result: Optional[Any] = None


class AskResponse(BaseModel):
    """
    Response returned after processing a question.

    Attributes:
        answer: The AI-generated answer
        retrieved_chunks: List of document chunks used to generate the answer
        tool_calls: Any function/tool calls made during processing (if enabled)
        tokens_used: Approximate number of tokens consumed (optional)
    """
    answer: str
    retrieved_chunks: List[RetrievedChunk]
    tool_calls: Optional[List[ToolCall]] = None
    tokens_used: Optional[int] = None


# ============================================================================
# ERROR RESPONSE SCHEMAS
# ============================================================================

class ErrorResponse(BaseModel):
    """
    Standard error response format.

    Attributes:
        error: Error message
        detail: Additional error details
    """
    error: str
    detail: Optional[str] = None
