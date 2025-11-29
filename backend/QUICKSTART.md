# Quick Start Guide

Get up and running in 5 minutes!

## Prerequisites Checklist

- [ ] Python 3.9+ installed
- [ ] OpenAI API key ([Get one here](https://platform.openai.com/api-keys))
- [ ] Supabase account ([Sign up here](https://supabase.com))

## Step-by-Step Setup

### 1. Install Dependencies (2 minutes)

```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install packages
pip install -r requirements.txt
```

### 2. Set Up Supabase (2 minutes)

1. Create a new project at [supabase.com](https://supabase.com)
2. Go to **Database** → **Extensions** → Enable `vector`
3. Go to **SQL Editor** and run this:

```sql
CREATE TABLE documents (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  content TEXT NOT NULL,
  metadata JSONB,
  embedding VECTOR(1536),
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX ON documents
USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);

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

4. Go to **Project Settings** → **API**
   - Copy **Project URL**
   - Copy **service_role key** (NOT anon key!)

### 3. Configure Environment (1 minute)

```bash
# Create .env file
cp .env.example .env

# Edit .env and add your keys:
# OPENAI_API_KEY=sk-your-key-here
# SUPABASE_URL=https://your-project.supabase.co
# SUPABASE_KEY=your-service-role-key
```

### 4. Run the Server (30 seconds)

```bash
uvicorn app.main:app --reload
```

Visit http://localhost:8000/docs to see the interactive API documentation!

### 5. Test It (30 seconds)

Open a new terminal and run:

```bash
python test_api.py
```

This will:
- Create a sample document
- Upload it
- Ask questions about it
- Show you how everything works!

## What's Next?

1. **Try with your own documents**: Upload PDFs, DOCX, or TXT files
2. **Experiment with questions**: Ask anything about your documents
3. **Check the code**: Everything is heavily commented for learning
4. **Read the full README**: Understand how RAG works

## Common Issues

### "OPENAI_API_KEY not found"
- Make sure you created `.env` (not just `.env.example`)
- Check that you added your actual API key

### "relation 'documents' does not exist"
- You need to run the SQL in Supabase (Step 2, part 3)

### "Module not found"
- Make sure you activated your virtual environment
- Run `pip install -r requirements.txt` again

## Need Help?

- Check the full [README.md](README.md) for detailed explanations
- Ask your workshop instructor
- Check the API docs at http://localhost:8000/docs

---

**Ready to build something awesome? Let's go! 🚀**
