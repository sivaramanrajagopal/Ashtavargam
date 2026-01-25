# Supabase Setup Guide for Vedic Astrology RAG System

## Step 1: Create Supabase Account and Project

1. Go to [https://supabase.com](https://supabase.com)
2. Sign up for a free account
3. Create a new project
4. Note down your project URL and API keys

## Step 2: Enable pgvector Extension

1. Go to your Supabase project dashboard
2. Navigate to **SQL Editor**
3. Run the following SQL:

```sql
-- Enable pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;
```

## Step 3: Create Knowledge Base Table

Run this SQL in the SQL Editor:

```sql
-- Create vedic_knowledge table
CREATE TABLE vedic_knowledge (
    id BIGSERIAL PRIMARY KEY,
    content TEXT NOT NULL,
    embedding vector(1536),  -- OpenAI text-embedding-3-small dimension
    metadata JSONB,
    category VARCHAR(50),  -- 'dasha', 'gochara', 'bav_sav', 'house', 'remedy', 'general'
    house_number INTEGER,  -- 1-12 if house-specific (NULL if not)
    planet VARCHAR(20),   -- If planet-specific (NULL if not)
    created_at TIMESTAMP DEFAULT NOW()
);

-- Create index for vector similarity search
CREATE INDEX vedic_knowledge_embedding_idx 
ON vedic_knowledge 
USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);

-- Create indexes for filtering
CREATE INDEX vedic_knowledge_category_idx ON vedic_knowledge(category);
CREATE INDEX vedic_knowledge_house_idx ON vedic_knowledge(house_number);
CREATE INDEX vedic_knowledge_planet_idx ON vedic_knowledge(planet);
```

## Step 4: Get API Keys

1. Go to **Settings** → **API**
2. Copy the following:
   - **Project URL**: `https://your-project.supabase.co`
   - **anon/public key**: Use this for client-side access
   - **service_role key**: Use this for server-side operations (keep secret!)

## Step 5: Set Environment Variables

Add these to your `.env` file or Railway environment variables:

```bash
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-service-role-key-here
OPENAI_API_KEY=your-openai-api-key-here
```

## Step 6: Verify Setup

You can verify the table was created by running:

```sql
SELECT * FROM vedic_knowledge LIMIT 1;
```

## Notes

- **Vector Dimension**: 1536 is for `text-embedding-3-small` model
- **Index Type**: `ivfflat` is efficient for similarity search
- **Metadata**: Use JSONB for flexible filtering (e.g., `{"source": "Parasara", "language": "tamil"}`)
- **Category Values**: 'dasha', 'gochara', 'bav_sav', 'house', 'remedy', 'general'

## Next Steps

After setup, run `populate_knowledge_base.py` to populate the database with Vedic astrology knowledge.

