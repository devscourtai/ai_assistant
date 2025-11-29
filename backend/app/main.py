"""
Main FastAPI application entry point.

This file:
1. Creates the FastAPI application
2. Configures CORS (Cross-Origin Resource Sharing)
3. Registers all routers
4. Defines health check endpoints
5. Sets up application metadata
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# Import routers
from app.routers import upload, ask

# ============================================================================
# APPLICATION SETUP
# ============================================================================

# Create FastAPI application with metadata
app = FastAPI(
    title="AI Document Assistant API",
    description="""
    A powerful RAG (Retrieval-Augmented Generation) API for document question answering.

    ## Features
    - 📄 Upload documents (PDF, DOCX, TXT)
    - 🔍 Semantic search using vector embeddings
    - 🤖 AI-powered question answering
    - 🛠️ Function/tool calling support
    - 💾 Supabase vector store for persistence

    ## How it works
    1. **Upload**: Upload your documents via `/upload/`
    2. **Process**: Documents are chunked and embedded automatically
    3. **Ask**: Query your documents via `/ask/`
    4. **Retrieve**: Get AI-generated answers with sources

    ## Tech Stack
    - **Framework**: FastAPI
    - **AI**: LangChain + OpenAI/Claude
    - **Vector DB**: Supabase (pgvector)
    - **Embeddings**: OpenAI text-embedding-3-small
    """,
    version="1.0.0",
    docs_url="/docs",  # Swagger UI
    redoc_url="/redoc",  # ReDoc UI
)

# ============================================================================
# CORS CONFIGURATION
# ============================================================================

# Configure CORS to allow frontend applications to call this API
# In production, replace "*" with your actual frontend domain
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production: ["https://yourdomain.com"]
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# ============================================================================
# REGISTER ROUTERS
# ============================================================================

# Register the upload router
# All endpoints in upload.py will be prefixed with /upload
app.include_router(upload.router)

# Register the ask router
# All endpoints in ask.py will be prefixed with /ask
app.include_router(ask.router)

# ============================================================================
# ROOT ENDPOINTS
# ============================================================================


@app.get("/", tags=["root"])
async def root():
    """
    Root endpoint - API welcome message.

    Returns basic information about the API and links to documentation.

    Example Response:
        ```json
        {
            "message": "Welcome to AI Document Assistant API",
            "version": "1.0.0",
            "docs": "/docs",
            "health": "/health"
        }
        ```
    """
    return {
        "message": "Welcome to AI Document Assistant API",
        "version": "1.0.0",
        "description": "A RAG-powered document question answering system",
        "docs": "/docs",
        "health": "/health",
        "endpoints": {
            "upload": "/upload/",
            "ask": "/ask/",
            "stats": "/upload/stats"
        }
    }


@app.get("/health", tags=["root"])
async def health_check():
    """
    Health check endpoint.

    Use this to verify the API is running and healthy.
    This is useful for:
    - Docker health checks
    - Load balancer health probes
    - Monitoring systems

    Example Response:
        ```json
        {
            "status": "healthy",
            "message": "AI Document Assistant API is running"
        }
        ```
    """
    return {
        "status": "healthy",
        "message": "AI Document Assistant API is running"
    }


# ============================================================================
# ERROR HANDLERS
# ============================================================================


@app.exception_handler(404)
async def not_found_handler(request, exc):
    """
    Custom 404 error handler.

    Returns a user-friendly message when an endpoint is not found.
    """
    return JSONResponse(
        status_code=404,
        content={
            "error": "Endpoint not found",
            "detail": f"The endpoint {request.url.path} does not exist",
            "available_endpoints": {
                "docs": "/docs",
                "upload": "/upload/",
                "ask": "/ask/"
            }
        }
    )


@app.exception_handler(500)
async def internal_error_handler(request, exc):
    """
    Custom 500 error handler.

    Returns a user-friendly message when an internal server error occurs.
    """
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "detail": "An unexpected error occurred. Please try again later."
        }
    )


# ============================================================================
# STARTUP AND SHUTDOWN EVENTS
# ============================================================================


@app.on_event("startup")
async def startup_event():
    """
    Runs when the application starts.

    You can use this to:
    - Initialize database connections
    - Load models into memory
    - Set up logging
    - Validate environment variables
    """
    print("🚀 Starting AI Document Assistant API...")
    print("📚 Loading services...")

    # Optionally, you can initialize services here
    # This ensures they're ready before the first request
    try:
        from app.services.embeddings import get_embedding_service
        from app.services.supabase_store import get_vector_store
        from app.services.rag_pipeline import get_rag_pipeline

        # Initialize services
        get_embedding_service()
        get_vector_store()
        get_rag_pipeline()

        print("✅ All services initialized successfully")

    except Exception as e:
        print(f"⚠️  Warning: Some services could not be initialized: {e}")
        print("   Make sure your .env file is configured correctly")


@app.on_event("shutdown")
async def shutdown_event():
    """
    Runs when the application shuts down.

    You can use this to:
    - Close database connections
    - Save state
    - Clean up resources
    """
    print("👋 Shutting down AI Document Assistant API...")


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    import uvicorn

    # Run the application with Uvicorn
    # This is useful for development
    # In production, use: uvicorn app.main:app --host 0.0.0.0 --port 9000
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=9000,
        reload=True,  # Auto-reload on code changes (development only)
        log_level="info"
    )
