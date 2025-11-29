# AI Document Assistant - Backend

A clean, minimal, beginner-friendly backend for an AI Document Assistant using FastAPI, LangChain, and Supabase Vector Store.

Perfect for workshops and learning RAG (Retrieval-Augmented Generation) systems!

## Table of Contents

- [Features](#features)
- [How It Works](#how-it-works)
- [Architecture](#architecture)
- [Setup](#setup)
- [Supabase Configuration](#supabase-configuration)
- [Running the Application](#running-the-application)
- [Testing the API](#testing-the-api)
- [Project Structure](#project-structure)
- [Key Concepts Explained](#key-concepts-explained)
- [Troubleshooting](#troubleshooting)

---

## Features

- **Document Upload**: Support for PDF, DOCX, and TXT files
- **Text Extraction**: Automatic text extraction from documents
- **Smart Chunking**: Intelligent text splitting for optimal retrieval
- **Vector Embeddings**: Semantic search using OpenAI embeddings
- **Supabase Vector Store**: Persistent storage with pgvector
- **RAG Pipeline**: Complete retrieval-augmented generation
- **Tool Calling**: Function calling demonstration
- **Clean API**: Well-documented REST endpoints
- **FastAPI**: Modern, fast, async Python web framework

---

## How It Works

### The RAG Pipeline

RAG stands for **Retrieval-Augmented Generation**. Here's how it works:

```
1. UPLOAD PHASE
   User uploads document → Extract text → Split into chunks → Generate embeddings → Store in vector DB

2. QUERY PHASE
   User asks question → Convert to embedding → Search for similar chunks → Build context → LLM generates answer
```

### Step-by-Step Flow

1. **Document Upload** (`/upload/`)
   - User uploads a PDF, DOCX, or TXT file
   - LangChain extracts text from the document
   - Text is split into ~1000 character chunks with 200 character overlap
   - Each chunk is converted to a 1536-dimensional vector (embedding)
   - Vectors and text are stored in Supabase

2. **Question Answering** (`/ask/`)
   - User asks a question
   - Question is converted to an embedding
   - Vector search finds the most similar chunks
   - Retrieved chunks are formatted as context
   - Context + question is sent to the LLM
   - LLM generates an answer based on the context
   - Answer is returned with source citations

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      FastAPI Application                     │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌─────────────┐                  ┌─────────────┐           │
│  │   Upload    │                  │     Ask     │           │
│  │   Router    │                  │   Router    │           │
│  └──────┬──────┘                  └──────┬──────┘           │
│         │                                 │                  │
│         ├─────────────┬───────────────────┤                  │
│         │             │                   │                  │
│  ┌──────▼──────┐ ┌───▼────────┐ ┌────────▼────────┐        │
│  │   Chunker   │ │ Embeddings │ │  RAG Pipeline   │        │
│  │   Utility   │ │  Service   │ │     Service     │        │
│  └─────────────┘ └────┬───────┘ └────────┬────────┘        │
│                       │                   │                  │
│                       └───────┬───────────┘                  │
│                               │                              │
│                      ┌────────▼─────────┐                   │
│                      │  Vector Store    │                   │
│                      │    Service       │                   │
│                      └────────┬─────────┘                   │
└───────────────────────────────┼──────────────────────────────┘
                                │
                    ┌───────────▼──────────┐
                    │  Supabase (pgvector) │
                    │   Vector Database    │
                    └──────────────────────┘
```

---

## Setup

### Prerequisites

- Python 3.9 or higher
- Supabase account (free tier works!)
- OpenAI API key

### Installation

1. **Clone or download the project**

```bash
cd backend
```

2. **Create a virtual environment**

```bash
# Create virtual environment
python -m venv venv

# Activate it
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Set up environment variables**

```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your keys
# You need:
# - OPENAI_API_KEY
# - SUPABASE_URL
# - SUPABASE_KEY
```

---

## Supabase Configuration

### Step 1: Create a Supabase Project

1. Go to [supabase.com](https://supabase.com)
2. Sign up / Log in
3. Click "New Project"
4. Fill in project details
5. Wait for project to be created (~2 minutes)

### Step 2: Enable pgvector Extension

1. In your Supabase dashboard, go to **Database** → **Extensions**
2. Search for `vector`
3. Enable the `vector` extension

### Step 3: Create Documents Table

Run this SQL in the Supabase SQL Editor:

```sql
-- Create the documents table for storing embeddings
CREATE TABLE documents (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  content TEXT NOT NULL,
  metadata JSONB,
  embedding VECTOR(1536),  -- OpenAI text-embedding-3-small uses 1536 dimensions
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create an index for faster similarity search
CREATE INDEX ON documents
USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);

-- Create the similarity search function
CREATE OR REPLACE FUNCTION match_documents(
  query_embedding VECTOR(1536),
  match_threshold FLOAT,
  match_count INT
)
RETURNS TABLE (
  id UUID,
  content TEXT,
  metadata JSONB,
  similarity FLOAT
)
LANGUAGE SQL STABLE
AS $$
  SELECT
    documents.id,
    documents.content,
    documents.metadata,
    1 - (documents.embedding <=> query_embedding) AS similarity
  FROM documents
  WHERE 1 - (documents.embedding <=> query_embedding) > match_threshold
  ORDER BY similarity DESC
  LIMIT match_count;
$$;
```

### Step 4: Get API Credentials

1. Go to **Project Settings** → **API**
2. Copy your **Project URL** (this is `SUPABASE_URL`)
3. Copy your **service_role key** (this is `SUPABASE_KEY`)
   - **Important**: Use the `service_role` key, NOT the `anon` key!
   - The service_role key has full access and is needed for vector operations

### Step 5: Add to .env File

```bash
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-service-role-key-here
```

---

## Running the Application

### Development Mode

```bash
# Make sure your virtual environment is activated
# and you're in the backend directory

# Run the server
uvicorn app.main:app --reload --host 0.0.0.0 --port 9000
```

The API will be available at:
- **API**: http://localhost:9000
- **Interactive Docs**: http://localhost:9000/docs
- **ReDoc**: http://localhost:9000/redoc

### Production Mode

```bash
uvicorn app.main:app --host 0.0.0.0 --port 9000 --workers 4
```

---

## Testing the API

### Using the Interactive Docs

1. Open http://localhost:9000/docs in your browser
2. Try the endpoints interactively!

### Using cURL

#### 1. Upload a Document

```bash
curl -X POST "http://localhost:8000/upload/" \
  -F "file=@/path/to/your/document.pdf"
```

Response:
```json
{
  "message": "Document uploaded successfully",
  "filename": "document.pdf",
  "chunks_created": 15,
  "document_id": "123e4567-e89b-12d3-a456-426614174000"
}
```

#### 2. Ask a Question

```bash
curl -X POST "http://localhost:8000/ask/" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is the refund policy?",
    "max_results": 4,
    "use_tool_calling": false
  }'
```

Response:
```json
{
  "answer": "According to the documentation, the refund policy allows...",
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

#### 3. Check Stats

```bash
curl "http://localhost:8000/upload/stats"
```

### Using Python

```python
import requests

# Upload a document
with open("document.pdf", "rb") as f:
    response = requests.post(
        "http://localhost:8000/upload/",
        files={"file": f}
    )
    print(response.json())

# Ask a question
response = requests.post(
    "http://localhost:8000/ask/",
    json={
        "question": "What is the refund policy?",
        "max_results": 4,
        "use_tool_calling": False
    }
)
print(response.json())
```

---

## Project Structure

```
backend/
├── app/
│   ├── main.py              # FastAPI application entry point
│   ├── routers/
│   │   ├── upload.py        # Document upload endpoint
│   │   └── ask.py           # Question answering endpoint
│   ├── services/
│   │   ├── embeddings.py    # Embedding generation service
│   │   ├── supabase_store.py # Vector store operations
│   │   └── rag_pipeline.py  # RAG orchestration
│   ├── utils/
│   │   └── chunker.py       # Text splitting utility
│   └── models/
│       └── schemas.py       # Pydantic models
├── requirements.txt         # Python dependencies
├── .env.example            # Environment variables template
└── README.md               # This file
```

---

## Key Concepts Explained

### What are Embeddings?

Embeddings are numerical representations (vectors) of text. Similar texts have similar vectors.

Example:
```
"What is the refund policy?" → [0.1, -0.3, 0.5, ..., 0.2]  (1536 numbers)
"How do I get a refund?"     → [0.09, -0.29, 0.48, ..., 0.19] (similar!)
```

This allows us to find semantically similar content, not just keyword matches.

### What is Chunking?

Chunking is splitting large documents into smaller pieces because:
1. **LLM Token Limits**: Models can't process huge documents at once
2. **Better Embeddings**: Shorter, focused chunks create more precise embeddings
3. **More Relevant Retrieval**: Return specific sections, not entire documents

Our chunking strategy:
- **Chunk Size**: 1000 characters
- **Overlap**: 200 characters (maintains context across boundaries)
- **Smart Splitting**: Tries to split on paragraphs, then sentences, then words

### What is a Vector Store?

A vector store is a specialized database that:
1. Stores embeddings (vectors) efficiently
2. Performs fast similarity search using algorithms like HNSW or IVFFlat
3. Returns the most similar vectors to a query

We use Supabase with pgvector, which adds vector capabilities to PostgreSQL.

### What is RAG?

**Retrieval-Augmented Generation** combines:
1. **Retrieval**: Finding relevant information from a knowledge base
2. **Augmentation**: Adding that information to the prompt
3. **Generation**: LLM generates an answer using the provided context

Benefits:
- LLM can answer about specific, current information
- Reduces hallucinations (making up facts)
- Provides source citations
- No need to fine-tune models

### Tool/Function Calling

Tool calling allows the LLM to:
1. Recognize when it needs external information
2. Call predefined functions
3. Use the results in its response

Example in our code:
- User asks: "What is the vacation policy?"
- LLM recognizes "policy" keyword
- Calls `fetch_company_policy("vacation")`
- Uses result to augment response

---

## Troubleshooting

### "OPENAI_API_KEY not found"

Make sure you:
1. Created a `.env` file (not `.env.example`)
2. Added your OpenAI API key
3. Activated your virtual environment

### "SUPABASE_URL not found"

Make sure you:
1. Set up Supabase project
2. Added credentials to `.env`
3. Used the `service_role` key, not `anon` key

### "relation 'documents' does not exist"

You need to create the Supabase table. Run the SQL from [Supabase Configuration](#supabase-configuration).

### "Could not load document"

Supported file types:
- PDF: `.pdf`
- Word: `.docx`, `.doc`
- Text: `.txt`

For PDF issues, you might need to install poppler:
```bash
# macOS
brew install poppler

# Ubuntu/Debian
sudo apt-get install poppler-utils

# Windows
# Download from: https://github.com/oschwartz10612/poppler-windows/releases
```

### Import Errors

Make sure you:
1. Activated your virtual environment
2. Installed all requirements: `pip install -r requirements.txt`
3. Are in the correct directory

### Slow Performance

For production:
1. Use a better LLM model (gpt-4o instead of gpt-4o-mini)
2. Optimize chunk size and overlap
3. Adjust `max_results` parameter
4. Use Redis for caching
5. Add connection pooling

---

## Next Steps

### For Workshop Participants

1. **Experiment with Parameters**
   - Try different chunk sizes
   - Adjust the number of retrieved documents
   - Test with various document types

2. **Enhance the RAG Pipeline**
   - Add reranking for better results
   - Implement hybrid search (keyword + semantic)
   - Add conversation memory

3. **Add Features**
   - User authentication
   - Document management (delete, update)
   - Multiple collections/namespaces
   - Real-time updates with WebSockets

4. **Improve Tool Calling**
   - Add more tools
   - Use OpenAI's native function calling API
   - Implement agent patterns

### Resources

- [LangChain Documentation](https://python.langchain.com/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Supabase Documentation](https://supabase.com/docs)
- [OpenAI Embeddings Guide](https://platform.openai.com/docs/guides/embeddings)

---

## Contributing

This is a workshop project designed for learning. Feel free to:
- Modify the code
- Add features
- Experiment with different approaches
- Share your improvements!

---

## License

MIT License - Feel free to use this for learning and building your own projects!

---

## Support

For questions during the workshop, ask your instructor!

For issues with:
- **FastAPI**: Check the official docs
- **LangChain**: Visit LangChain documentation
- **Supabase**: Check Supabase docs or community

---

**Happy Learning! Build something awesome!** 🚀
