-- ============================================================================
-- Fix Vector Dimensions for HuggingFace Embeddings (384 dimensions)
-- ============================================================================
-- Run this SQL in your Supabase SQL Editor to update the vector dimensions
-- from 1536 (OpenAI) to 384 (HuggingFace all-MiniLM-L6-v2)
-- ============================================================================

-- Step 1: Drop existing function
DROP FUNCTION IF EXISTS match_documents(vector(1536), int, jsonb);
DROP FUNCTION IF EXISTS match_documents(vector(384), int, jsonb);

-- Step 2: Drop and recreate the documents table with 384 dimensions
DROP TABLE IF EXISTS documents CASCADE;

CREATE TABLE documents (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),  -- Changed to UUID
  content text NOT NULL,
  metadata jsonb,
  embedding vector(384) NOT NULL  -- Changed from 1536 to 384
);

-- Step 3: Create index for fast similarity search
CREATE INDEX ON documents USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);

-- Step 4: Create the similarity search function with 384 dimensions
CREATE OR REPLACE FUNCTION match_documents(
  query_embedding vector(384),  -- Changed from 1536 to 384
  match_count int DEFAULT 5,
  filter jsonb DEFAULT '{}'
)
RETURNS TABLE (
  id uuid,  -- Changed to uuid
  content text,
  metadata jsonb,
  similarity float
)
LANGUAGE plpgsql
AS $$
BEGIN
  RETURN QUERY
  SELECT
    documents.id,
    documents.content,
    documents.metadata,
    1 - (documents.embedding <=> query_embedding) AS similarity
  FROM documents
  WHERE documents.metadata @> COALESCE(filter, '{}')
  ORDER BY documents.embedding <=> query_embedding
  LIMIT match_count;
END;
$$;

-- ============================================================================
-- Done! Your database now accepts 384-dimensional vectors
-- ============================================================================
