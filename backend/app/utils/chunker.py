"""
Text chunking utility using LangChain's RecursiveCharacterTextSplitter.

Chunking is the process of breaking down large documents into smaller pieces.
This is important because:
1. LLMs have token limits - they can't process huge documents at once
2. Embeddings work better on focused, coherent chunks
3. Retrieval is more precise when searching smaller, relevant pieces
"""
from typing import List
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document


def chunk_text(
    text: str,
    chunk_size: int = 1000,
    chunk_overlap: int = 200,
    metadata: dict = None
) -> List[Document]:
    """
    Split text into smaller chunks using RecursiveCharacterTextSplitter.

    This splitter tries to keep paragraphs, sentences, and words together,
    splitting only when necessary. It uses this hierarchy:
    1. Split by double newlines (paragraphs)
    2. Split by single newlines
    3. Split by spaces (sentences/words)
    4. Split by characters (last resort)

    Args:
        text: The text to split into chunks
        chunk_size: Maximum size of each chunk in characters (default: 1000)
        chunk_overlap: Number of characters to overlap between chunks (default: 200)
                      Overlap helps maintain context across chunk boundaries
        metadata: Optional metadata to attach to each chunk (e.g., filename, page number)

    Returns:
        List of Document objects, each containing a chunk of text and metadata

    Example:
        >>> text = "This is a long document..."
        >>> chunks = chunk_text(text, metadata={"source": "report.pdf"})
        >>> print(f"Created {len(chunks)} chunks")
    """
    # Initialize the text splitter with our configuration
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,  # Use character count
        separators=["\n\n", "\n", " ", ""]  # Split hierarchy
    )

    # Split the text into chunks
    chunks = text_splitter.split_text(text)

    # Convert plain text chunks into Document objects with metadata
    documents = []
    for i, chunk in enumerate(chunks):
        # Create metadata for this chunk
        chunk_metadata = metadata.copy() if metadata else {}
        chunk_metadata["chunk_index"] = i
        chunk_metadata["chunk_total"] = len(chunks)

        # Create a Document object
        doc = Document(
            page_content=chunk,
            metadata=chunk_metadata
        )
        documents.append(doc)

    return documents


def chunk_documents(
    documents: List[Document],
    chunk_size: int = 500,
    chunk_overlap: int = 100
) -> List[Document]:
    """
    Split a list of Document objects into smaller chunks.

    IMPROVED CHUNKING STRATEGY:
    - Reduced chunk_size from 1000 to 500 for more precise retrieval
    - Reduced overlap from 200 to 100 to avoid redundancy
    - Better for CV/resume documents where specific details matter

    This is useful when you've already loaded documents using LangChain loaders
    (like PyPDFLoader or UnstructuredWordDocumentLoader).

    Args:
        documents: List of Document objects to chunk
        chunk_size: Maximum size of each chunk in characters (default: 500)
        chunk_overlap: Number of characters to overlap between chunks (default: 100)

    Returns:
        List of chunked Document objects, preserving original metadata

    Example:
        >>> from langchain.document_loaders import PyPDFLoader
        >>> loader = PyPDFLoader("document.pdf")
        >>> docs = loader.load()
        >>> chunked_docs = chunk_documents(docs)
    """
    # Initialize the text splitter with IMPROVED settings
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        # Better separators for structured documents like CVs
        separators=["\n\n", "\n", ". ", " ", ""]
    )

    # Split all documents
    chunked_docs = text_splitter.split_documents(documents)

    # Add chunk index information to metadata
    for i, doc in enumerate(chunked_docs):
        doc.metadata["chunk_index"] = i
        doc.metadata["chunk_total"] = len(chunked_docs)

    return chunked_docs
