# AI Document Assistant

A full-stack AI-powered document assistant that allows users to upload documents (PDF, DOCX) and ask questions about their content using natural language. Built with FastAPI, LangChain, Next.js, and Supabase vector storage.

## Features

- Upload and process multiple document formats (PDF, DOCX)
- Intelligent document chunking and vector embeddings
- Natural language querying using OpenAI GPT or Anthropic Claude
- Real-time chat interface
- Vector similarity search using Supabase
- Clean, modern UI built with Next.js and TailwindCSS

## Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **LangChain** - LLM orchestration framework
- **OpenAI/Anthropic** - Language models and embeddings
- **Supabase** - PostgreSQL with pgvector for vector storage
- **Uvicorn** - ASGI server
- **Python 3.11.6**

### Frontend
- **Next.js 14** - React framework
- **TypeScript** - Type-safe JavaScript
- **TailwindCSS** - Utility-first CSS framework
- **ShadCN UI** - Component library
- **Axios** - HTTP client

## Prerequisites

Before you begin, ensure you have the following installed:

- **Node.js** (v18 or higher) - [Download](https://nodejs.org/)
- **Python** (3.11.6 recommended) - [Download](https://www.python.org/)
- **npm** or **yarn** - Package managers
- **Git** - Version control

You'll also need accounts and API keys for:

- **OpenAI API Key** - [Get it here](https://platform.openai.com/api-keys)
- **Supabase Account** - [Sign up here](https://supabase.com/)

## Project Structure

```
ai_assistant/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── main.py         # FastAPI application entry point
│   │   ├── routers/        # API route handlers
│   │   ├── services/       # Business logic
│   │   ├── models/         # Data models
│   │   └── utils/          # Utility functions
│   ├── .env                # Backend environment variables
│   ├── requirements.txt    # Python dependencies
│   └── download_nltk_data.py  # NLTK setup script
│
├── frontend/               # Next.js frontend
│   ├── app/               # Next.js app directory
│   ├── public/            # Static assets
│   ├── .env               # Frontend environment variables
│   ├── package.json       # Node dependencies
│   └── tailwind.config.ts # Tailwind configuration
│
└── README.md              # This file
```

## Installation and Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd ai_assistant
```

### 2. Backend Setup

#### Step 2.1: Navigate to Backend Directory

```bash
cd backend
```

#### Step 2.2: Create Python Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

#### Step 2.3: Install Python Dependencies

```bash
pip install -r requirements.txt
```

#### Step 2.4: Download NLTK Data

```bash
python download_nltk_data.py
```

#### Step 2.5: Configure Environment Variables

Create a `.env` file in the `backend` directory with the following variables:

```env
# OpenAI Configuration
OPENAI_API_KEY=your-openai-api-key-here

# Optional: OpenRouter API (if using)
OPENROUTER_API_KEY=your-openrouter-api-key-here

# Supabase Configuration
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-supabase-service-role-key

# Optional: Anthropic Claude
# ANTHROPIC_API_KEY=your-anthropic-api-key-here

# Application Configuration
PORT=9000
MAX_UPLOAD_SIZE_MB=10
TOKENIZERS_PARALLELISM=false
```

**Important Notes:**
- Use your **service_role** key from Supabase (not the anon key)
- Never commit `.env` files to version control
- Get your Supabase credentials from: Dashboard → Project Settings → API

#### Step 2.6: Set Up Supabase Vector Store

1. Create a new Supabase project at [supabase.com](https://supabase.com)
2. Enable the `pgvector` extension in your database:
   - Go to Database → Extensions
   - Search for "vector" and enable it
3. The backend will automatically create the necessary tables on first run

### 3. Frontend Setup

#### Step 3.1: Navigate to Frontend Directory

```bash
# From the ai_assistant root directory
cd frontend
```

#### Step 3.2: Install Node Dependencies

```bash
npm install
# or
yarn install
```

#### Step 3.3: Configure Environment Variables

Create a `.env` or `.env.local` file in the `frontend` directory:

```env
# Backend API URL
NEXT_PUBLIC_API_URL=http://localhost:9000

# Optional: Change frontend port
PORT=4000
```

## Running the Application

### Start the Backend Server

```bash
# Navigate to backend directory
cd backend

# Activate virtual environment (if not already activated)
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate     # Windows

# Start the FastAPI server
uvicorn app.main:app --reload --port 9000
```

The backend API will be available at: `http://localhost:9000`

API documentation will be available at:
- Swagger UI: `http://localhost:9000/docs`
- ReDoc: `http://localhost:9000/redoc`

### Start the Frontend Server

Open a new terminal window:

```bash
# Navigate to frontend directory
cd frontend

# Start the Next.js development server
npm run dev
# or
yarn dev
```

The frontend will be available at: `http://localhost:4000`

## Usage

1. **Open the application** in your browser at `http://localhost:4000`
2. **Upload a document** (PDF or DOCX) using the upload interface
3. **Wait for processing** - The document will be chunked and stored in the vector database
4. **Ask questions** - Type your question in natural language about the document content
5. **Get AI-powered answers** - The system will search relevant document chunks and generate answers

## API Endpoints

### Documents

- `POST /api/documents/upload` - Upload and process a document
- `GET /api/documents` - List all uploaded documents
- `DELETE /api/documents/{document_id}` - Delete a document

### Chat

- `POST /api/chat` - Send a question and get an AI-generated answer
- `GET /api/chat/history` - Retrieve chat history

### Health

- `GET /health` - Check API health status

## Development

### Backend Development

```bash
# Run with auto-reload
uvicorn app.main:app --reload --port 9000

# Run tests (if available)
pytest

# Format code
black .

# Type checking
mypy .
```

### Frontend Development

```bash
# Development server with hot reload
npm run dev

# Build for production
npm run build

# Start production server
npm run start

# Lint code
npm run lint
```

## Environment Variables Reference

### Backend (.env)

| Variable | Required | Description |
|----------|----------|-------------|
| `OPENAI_API_KEY` | Yes | OpenAI API key for LLM and embeddings |
| `SUPABASE_URL` | Yes | Your Supabase project URL |
| `SUPABASE_KEY` | Yes | Supabase service_role key |
| `OPENROUTER_API_KEY` | No | OpenRouter API key (alternative to OpenAI) |
| `ANTHROPIC_API_KEY` | No | Anthropic Claude API key (alternative LLM) |
| `PORT` | No | Backend server port (default: 9000) |
| `MAX_UPLOAD_SIZE_MB` | No | Max file upload size in MB (default: 10) |
| `TOKENIZERS_PARALLELISM` | No | Set to false to suppress warnings |

### Frontend (.env or .env.local)

| Variable | Required | Description |
|----------|----------|-------------|
| `NEXT_PUBLIC_API_URL` | Yes | Backend API URL (e.g., http://localhost:9000) |
| `PORT` | No | Frontend server port (default: 3000) |

## Troubleshooting

### Common Issues

#### Backend won't start

**Error:** `ModuleNotFoundError: No module named 'fastapi'`

**Solution:** Make sure you've activated the virtual environment and installed dependencies:
```bash
source venv/bin/activate
pip install -r requirements.txt
```

#### NLTK Data Errors

**Error:** `Resource punkt_tab not found`

**Solution:** Run the NLTK data download script:
```bash
python download_nltk_data.py
```

#### Supabase Connection Errors

**Error:** `Could not connect to Supabase`

**Solution:**
- Check that your `SUPABASE_URL` and `SUPABASE_KEY` are correct
- Ensure you're using the **service_role** key, not the anon key
- Verify pgvector extension is enabled in your Supabase database

#### Frontend API Connection Issues

**Error:** `Network Error` or `CORS Error`

**Solution:**
- Verify backend is running on the correct port (9000)
- Check `NEXT_PUBLIC_API_URL` in frontend `.env` file
- Ensure CORS is properly configured in the backend

#### Port Already in Use

**Error:** `Address already in use`

**Solution:**
```bash
# Find process using the port (e.g., 9000)
lsof -ti:9000

# Kill the process
kill -9 <PID>

# Or use a different port in your .env file
```

### Getting Help

If you encounter issues:

1. Check the console/terminal for error messages
2. Review the backend logs at `http://localhost:9000/docs`
3. Ensure all environment variables are correctly set
4. Verify API keys are valid and have proper permissions

## Production Deployment

### Backend Deployment

Consider deploying to:
- **Railway** - Easy Python deployments
- **Render** - Free tier available
- **AWS Lambda** - Serverless option
- **DigitalOcean** - Traditional VPS

### Frontend Deployment

Deploy to:
- **Vercel** - Optimized for Next.js (recommended)
- **Netlify** - Easy deployment with CLI
- **AWS Amplify** - Full-stack deployment

### Production Checklist

- [ ] Set `DEBUG=false` in backend
- [ ] Use production-grade database
- [ ] Enable HTTPS/SSL certificates
- [ ] Set up proper CORS policies
- [ ] Configure rate limiting
- [ ] Set up monitoring and logging
- [ ] Use environment variables (never hardcode secrets)
- [ ] Enable database backups

## License

MIT License - See LICENSE file for details

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Support

For questions or support:
- Open an issue in the GitHub repository
- Check the [documentation](./backend/PROJECT_OVERVIEW.md)
- Review the [Quick Start Guide](./backend/QUICKSTART.md)

---

**Built with by DevScourt AI**
