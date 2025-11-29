# AI Document Assistant - Project Overview

## What You've Got

A complete, production-ready RAG (Retrieval-Augmented Generation) backend for document question answering!

## Project Structure

```
backend/
│
├── 📄 README.md                    # Comprehensive documentation
├── 📄 QUICKSTART.md                # 5-minute setup guide
├── 📄 PROJECT_OVERVIEW.md          # This file
├── 📄 requirements.txt             # Python dependencies
├── 📄 .env.example                 # Environment variables template
├── 📄 .gitignore                   # Git ignore rules
├── 📄 test_api.py                  # Automated test suite
│
└── app/                            # Main application package
    │
    ├── 📄 main.py                  # FastAPI application entry point
    │                                 • Creates FastAPI app
    │                                 • Configures CORS
    │                                 • Registers routers
    │                                 • Defines health endpoints
    │
    ├── routers/                    # API endpoint routes
    │   ├── 📄 upload.py            # Document upload endpoint
    │   │                             • Accept PDF/DOCX/TXT files
    │   │                             • Extract text
    │   │                             • Chunk and embed
    │   │                             • Store in Supabase
    │   │
    │   └── 📄 ask.py               # Question answering endpoint
    │                                 • Retrieve relevant chunks
    │                                 • Build context
    │                                 • Generate answer with LLM
    │                                 • Return structured response
    │
    ├── services/                   # Core business logic
    │   │
    │   ├── 📄 embeddings.py        # Embedding generation service
    │   │                             • OpenAI embeddings API wrapper
    │   │                             • Batch processing
    │   │                             • 1536-dimensional vectors
    │   │
    │   ├── 📄 supabase_store.py    # Vector database operations
    │   │                             • Store documents + embeddings
    │   │                             • Similarity search
    │   │                             • Collection management
    │   │
    │   └── 📄 rag_pipeline.py      # RAG orchestration
    │                                 • Retrieval logic
    │                                 • Context formatting
    │                                 • LLM integration
    │                                 • Tool calling demo
    │
    ├── utils/                      # Helper utilities
    │   └── 📄 chunker.py           # Text splitting utility
    │                                 • RecursiveCharacterTextSplitter
    │                                 • Smart chunking strategy
    │                                 • Metadata preservation
    │
    └── models/                     # Data models
        └── 📄 schemas.py           # Pydantic schemas
                                      • Request/response models
                                      • Data validation
                                      • API documentation
```

## Key Features

### ✅ Complete RAG Pipeline
- Document upload and processing
- Vector embeddings generation
- Semantic search with Supabase
- LLM-powered answer generation
- Source citation with similarity scores

### ✅ Production Ready
- Error handling
- Input validation
- CORS configuration
- Environment variables
- Health check endpoints
- Comprehensive logging

### ✅ Beginner Friendly
- Heavily commented code
- Clear function documentation
- Step-by-step README
- Quick start guide
- Test suite included
- Interactive API docs

### ✅ Extensible Architecture
- Modular design
- Clean separation of concerns
- Easy to add new features
- Swappable components (LLM, embeddings, vector store)

## Technology Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Web Framework** | FastAPI | Modern, fast, async API framework |
| **AI Framework** | LangChain | Document loading, chunking, RAG chains |
| **LLM** | OpenAI GPT-4 | Answer generation |
| **Embeddings** | OpenAI text-embedding-3-small | Vector representations |
| **Vector DB** | Supabase (pgvector) | Persistent vector storage |
| **Validation** | Pydantic | Data validation and serialization |
| **Server** | Uvicorn | ASGI server for FastAPI |

## API Endpoints

### Core Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Welcome message and API info |
| `GET` | `/health` | Health check |
| `POST` | `/upload/` | Upload and process documents |
| `GET` | `/upload/stats` | Get collection statistics |
| `POST` | `/ask/` | Ask questions (full response) |
| `POST` | `/ask/simple` | Ask questions (simple response) |
| `GET` | `/ask/health` | Ask service health check |

### Documentation Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/docs` | Interactive Swagger UI |
| `GET` | `/redoc` | Alternative ReDoc documentation |

## How RAG Works (Simple Explanation)

```
┌─────────────────────────────────────────────────────────────┐
│                     UPLOAD PHASE                             │
└─────────────────────────────────────────────────────────────┘

Document → Extract Text → Split into Chunks → Generate Embeddings → Store in DB

Example:
"policy.pdf" → "Our refund policy..." →
["Our refund policy...", "Customers can return..."] →
[[0.1, -0.3, ...], [0.09, -0.29, ...]] →
Supabase Vector Store


┌─────────────────────────────────────────────────────────────┐
│                     QUERY PHASE                              │
└─────────────────────────────────────────────────────────────┘

Question → Generate Embedding → Search Similar Chunks →
Build Context → Send to LLM → Return Answer

Example:
"What is the refund policy?" →
[0.11, -0.31, ...] →
Find similar vectors →
"Context: Our refund policy allows returns within 30 days..." →
Send to GPT-4 →
"According to the company policy, you can return items within 30 days."
```

## What Makes This Special?

### 🎓 Educational Focus
- Perfect for workshops and learning
- Every line is explained
- Concepts are documented
- Progressive complexity

### 🏗️ Clean Architecture
- No over-engineering
- Clear folder structure
- Single responsibility principle
- Easy to understand flow

### 🚀 Ready to Extend
- Add authentication
- Implement multi-user support
- Add more document types
- Integrate different LLMs
- Add conversation memory
- Implement reranking

## Code Quality Features

### ✅ Type Hints
All functions use Python type hints for better IDE support and code clarity.

### ✅ Docstrings
Every function has detailed docstrings explaining:
- What it does
- Parameters and types
- Return values
- Usage examples

### ✅ Error Handling
Comprehensive error handling with user-friendly messages.

### ✅ Validation
Pydantic models validate all inputs and outputs.

### ✅ Comments
Inline comments explain complex logic and design decisions.

## Testing Strategy

### Manual Testing
- Interactive API docs at `/docs`
- Test script: `python test_api.py`
- cURL examples in README

### Automated Testing (Future Enhancement)
- Unit tests for services
- Integration tests for endpoints
- End-to-end RAG pipeline tests

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `OPENAI_API_KEY` | ✅ Yes | OpenAI API key for embeddings and LLM |
| `SUPABASE_URL` | ✅ Yes | Your Supabase project URL |
| `SUPABASE_KEY` | ✅ Yes | Your Supabase service_role key |
| `ANTHROPIC_API_KEY` | ❌ No | Optional, if using Claude instead of GPT |

## Performance Considerations

### Current Configuration
- **Chunk Size**: 1000 characters
- **Chunk Overlap**: 200 characters
- **Retrieval**: Top 4 chunks
- **Embedding Model**: text-embedding-3-small (fast, cheap)
- **LLM Model**: gpt-4o-mini (fast, cost-effective)

### Optimization Options
1. **For Better Quality**: Use gpt-4o or claude-3-5-sonnet
2. **For Faster Retrieval**: Reduce max_results to 2-3
3. **For Better Context**: Increase chunk_size to 1500
4. **For Cost Savings**: Use cached embeddings

## Security Best Practices

### ✅ Implemented
- Environment variables for secrets
- CORS configuration
- Input validation
- File type restrictions

### 🔒 Production Recommendations
- Add authentication (JWT tokens)
- Implement rate limiting
- Use HTTPS only
- Validate file contents
- Add file size limits
- Implement user isolation
- Use database Row Level Security

## Deployment Options

### Local Development
```bash
uvicorn app.main:app --reload
```

### Production (Basic)
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Docker
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Cloud Platforms
- **Railway**: Direct deployment from GitHub
- **Render**: One-click deploy
- **Fly.io**: Global edge deployment
- **AWS**: ECS/Lambda deployment
- **Google Cloud**: Cloud Run deployment

## Next Steps for Workshop Participants

### Level 1: Beginner
1. ✅ Get the API running
2. ✅ Upload a test document
3. ✅ Ask questions and see results
4. ✅ Read through the code
5. ✅ Understand the RAG flow

### Level 2: Intermediate
1. 🔨 Modify chunk size and see effects
2. 🔨 Try different embedding models
3. 🔨 Add a new document type (CSV)
4. 🔨 Implement document deletion
5. 🔨 Add basic authentication

### Level 3: Advanced
1. 🚀 Implement conversation memory
2. 🚀 Add hybrid search (keyword + semantic)
3. 🚀 Implement reranking
4. 🚀 Add real function calling with OpenAI
5. 🚀 Build a frontend with React/Vue
6. 🚀 Deploy to production

## Resources

### Documentation
- [Full README](README.md)
- [Quick Start](QUICKSTART.md)
- [API Docs](http://localhost:8000/docs) (when running)

### Learning Resources
- [LangChain Docs](https://python.langchain.com/)
- [FastAPI Tutorial](https://fastapi.tiangolo.com/tutorial/)
- [Supabase Guide](https://supabase.com/docs/guides/database)
- [OpenAI Embeddings Guide](https://platform.openai.com/docs/guides/embeddings)
- [RAG Explanation](https://www.pinecone.io/learn/retrieval-augmented-generation/)

### Community
- LangChain Discord
- FastAPI Discord
- Supabase Discord

## FAQs

**Q: Can I use Claude instead of GPT?**
A: Yes! Just change the model name in `rag_pipeline.py` and add `ANTHROPIC_API_KEY` to your `.env`.

**Q: Can I use a different vector database?**
A: Yes! LangChain supports Pinecone, Weaviate, Chroma, and more. Replace the vector store in `supabase_store.py`.

**Q: How much does this cost to run?**
A: Very little! With OpenAI's pricing:
- Embeddings: ~$0.0001 per 1K tokens
- GPT-4o-mini: ~$0.15 per 1M tokens
- Example: 100 documents + 100 questions ≈ $0.50

**Q: Can this handle large documents?**
A: Yes! Documents are automatically chunked. A 100-page PDF works fine.

**Q: Is this production ready?**
A: The core is solid, but add authentication, rate limiting, and monitoring for production use.

---

## Summary

You now have a **complete, working RAG system** that demonstrates:

✅ Modern Python web development (FastAPI)
✅ AI/ML integration (LangChain + OpenAI)
✅ Vector databases (Supabase + pgvector)
✅ Clean code practices
✅ Documentation and testing

**This is a real, working example of production RAG systems used by companies today!**

---

**Ready to dive in? Start with [QUICKSTART.md](QUICKSTART.md)!** 🚀
