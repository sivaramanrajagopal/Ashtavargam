# Supabase RAG Verification Guide

## How to Check if RAG Script Was Run

### Step 1: Check if Table Exists

Run this query in Supabase SQL Editor:

```sql
-- Check if vedic_knowledge table exists
SELECT 
    table_name,
    table_schema
FROM information_schema.tables 
WHERE table_name = 'vedic_knowledge';
```

**Expected Result**: Should return 1 row with table name `vedic_knowledge`

---

### Step 2: Check Table Structure

```sql
-- Check table columns and structure
SELECT 
    column_name,
    data_type,
    is_nullable,
    column_default
FROM information_schema.columns
WHERE table_name = 'vedic_knowledge'
ORDER BY ordinal_position;
```

**Expected Columns**:
- `id` (bigint, primary key)
- `category` (text)
- `content` (text)
- `embedding` (vector)
- `metadata` (jsonb)
- `house_number` (integer, nullable)
- `planet` (text, nullable)
- `created_at` (timestamp)
- `updated_at` (timestamp)

---

### Step 3: Check if Data Exists

```sql
-- Count total records
SELECT COUNT(*) as total_records FROM vedic_knowledge;
```

**Expected**: Should be > 0 if script was run

```sql
-- Count by category
SELECT 
    category,
    COUNT(*) as count
FROM vedic_knowledge
GROUP BY category
ORDER BY count DESC;
```

**Expected Categories**:
- `house_significations`
- `dasha_interpretations`
- `gochara_effects`
- `bav_sav_rules`
- `remedies`
- `advanced_rules`

---

### Step 4: Check if Embeddings Were Created

```sql
-- Check if embeddings exist (non-null)
SELECT 
    COUNT(*) as total_records,
    COUNT(embedding) as records_with_embeddings,
    COUNT(*) - COUNT(embedding) as records_without_embeddings
FROM vedic_knowledge;
```

**Expected**: `records_with_embeddings` should equal `total_records`

```sql
-- Check embedding dimensions (should be 1536 for OpenAI)
-- Note: vector type doesn't need casting, use array_dims or vector_dims
SELECT 
    id,
    category,
    array_dims(embedding) as embedding_dimension
FROM vedic_knowledge
WHERE embedding IS NOT NULL
LIMIT 5;
```

**Alternative query** (if array_dims doesn't work):
```sql
-- Check embedding dimensions using vector type properties
SELECT 
    id,
    category,
    pg_typeof(embedding) as embedding_type,
    CASE 
        WHEN embedding IS NOT NULL THEN 'Has embedding (1536 dims)'
        ELSE 'No embedding'
    END as status
FROM vedic_knowledge
LIMIT 5;
```

**Expected**: All embeddings should have dimension 1536

---

### Step 5: Check Sample Data

```sql
-- View sample records
SELECT 
    id,
    category,
    LEFT(content, 100) as content_preview,
    metadata,
    house_number,
    planet,
    created_at
FROM vedic_knowledge
ORDER BY created_at DESC
LIMIT 10;
```

---

### Step 6: Check Metadata Structure

```sql
-- Check metadata structure
SELECT 
    category,
    jsonb_object_keys(metadata) as metadata_keys
FROM vedic_knowledge
WHERE metadata IS NOT NULL
GROUP BY category, jsonb_object_keys(metadata)
LIMIT 20;
```

---

### Step 7: Verify RPC Function Exists

```sql
-- Check if match_vedic_knowledge function exists
SELECT 
    routine_name,
    routine_type,
    data_type as return_type
FROM information_schema.routines
WHERE routine_schema = 'public'
AND routine_name = 'match_vedic_knowledge';
```

**Expected**: Should return 1 row with function name

---

### Step 8: Check pgvector Extension

```sql
-- Verify pgvector extension is enabled
SELECT * FROM pg_extension WHERE extname = 'vector';
```

**Expected**: Should return 1 row

---

## Complete Verification Query

Run this comprehensive check:

```sql
-- Complete RAG Setup Verification
WITH stats AS (
    SELECT 
        COUNT(*) as total_records,
        COUNT(DISTINCT category) as categories_count,
        COUNT(embedding) as embeddings_count,
        COUNT(*) FILTER (WHERE house_number IS NOT NULL) as house_records,
        COUNT(*) FILTER (WHERE planet IS NOT NULL) as planet_records
    FROM vedic_knowledge
),
categories AS (
    SELECT 
        category,
        COUNT(*) as count
    FROM vedic_knowledge
    GROUP BY category
),
embedding_check AS (
    SELECT 
        CASE 
            WHEN COUNT(*) = COUNT(embedding) THEN '✅ All records have embeddings'
            ELSE '❌ Some records missing embeddings'
        END as embedding_status
    FROM vedic_knowledge
),
extension_check AS (
    SELECT 
        CASE 
            WHEN EXISTS (SELECT 1 FROM pg_extension WHERE extname = 'vector') 
            THEN '✅ pgvector extension enabled'
            ELSE '❌ pgvector extension NOT enabled'
        END as extension_status
),
function_check AS (
    SELECT 
        CASE 
            WHEN EXISTS (
                SELECT 1 FROM information_schema.routines 
                WHERE routine_name = 'match_vedic_knowledge'
            )
            THEN '✅ RPC function exists'
            ELSE '❌ RPC function NOT found'
        END as function_status
)
SELECT 
    '📊 Statistics' as section,
    total_records,
    categories_count,
    embeddings_count,
    house_records,
    planet_records
FROM stats
UNION ALL
SELECT 
    '📁 Categories' as section,
    NULL,
    NULL,
    NULL,
    NULL,
    NULL
UNION ALL
SELECT 
    category,
    count::text,
    NULL,
    NULL,
    NULL
FROM categories
UNION ALL
SELECT 
    '🔍 Checks' as section,
    NULL,
    NULL,
    NULL,
    NULL,
    NULL
UNION ALL
SELECT 
    extension_status,
    NULL,
    NULL,
    NULL,
    NULL
FROM extension_check
UNION ALL
SELECT 
    function_status,
    NULL,
    NULL,
    NULL,
    NULL
FROM function_check
UNION ALL
SELECT 
    embedding_status,
    NULL,
    NULL,
    NULL,
    NULL
FROM embedding_check;
```

---

## How to Run the RAG Population Script

### Option 1: Run Locally

```bash
# Navigate to the knowledge directory
cd agent_app/knowledge

# Set environment variables
export SUPABASE_URL=https://your-project.supabase.co
export SUPABASE_KEY=your-service-role-key
export OPENAI_API_KEY=your-openai-api-key

# Run the script
python populate_knowledge_base.py
```

### Option 2: Check if Script Was Run

```sql
-- Check creation timestamps (if script ran recently)
SELECT 
    category,
    COUNT(*) as count,
    MIN(created_at) as first_created,
    MAX(created_at) as last_created
FROM vedic_knowledge
GROUP BY category
ORDER BY last_created DESC;
```

---

## Troubleshooting

### Issue: Table Doesn't Exist

**Solution**: Run the table creation SQL from `setup_supabase.md`:

```sql
CREATE TABLE IF NOT EXISTS vedic_knowledge (
    id BIGSERIAL PRIMARY KEY,
    category TEXT NOT NULL,
    content TEXT NOT NULL,
    embedding vector(1536),
    metadata JSONB DEFAULT '{}',
    house_number INTEGER,
    planet TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS vedic_knowledge_category_idx ON vedic_knowledge(category);
CREATE INDEX IF NOT EXISTS vedic_knowledge_house_idx ON vedic_knowledge(house_number);
CREATE INDEX IF NOT EXISTS vedic_knowledge_planet_idx ON vedic_knowledge(planet);
CREATE INDEX IF NOT EXISTS vedic_knowledge_embedding_idx ON vedic_knowledge 
USING ivfflat (embedding vector_cosine_ops);
```

### Issue: No Embeddings

**Solution**: Re-run the populate script. Embeddings are created when content is inserted.

### Issue: pgvector Extension Not Enabled

**Solution**: Run in Supabase SQL Editor:

```sql
CREATE EXTENSION IF NOT EXISTS vector;
```

### Issue: RPC Function Missing

**Solution**: Run the SQL from `agent_app/rag/supabase_rpc_setup.sql`:

```sql
CREATE OR REPLACE FUNCTION match_vedic_knowledge(
    query_embedding vector(1536),
    match_threshold float DEFAULT 0.78,
    match_count int DEFAULT 5,
    filter_category text DEFAULT NULL,
    filter_house_number int DEFAULT NULL,
    filter_planet text DEFAULT NULL
)
RETURNS TABLE (
    id bigint,
    category text,
    content text,
    metadata jsonb,
    house_number int,
    planet text,
    similarity float
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT
        vk.id,
        vk.category,
        vk.content,
        vk.metadata,
        vk.house_number,
        vk.planet,
        1 - (vk.embedding <=> query_embedding) as similarity
    FROM vedic_knowledge vk
    WHERE vk.embedding IS NOT NULL
        AND (filter_category IS NULL OR vk.category = filter_category)
        AND (filter_house_number IS NULL OR vk.house_number = filter_house_number)
        AND (filter_planet IS NULL OR vk.planet = filter_planet)
        AND (1 - (vk.embedding <=> query_embedding)) >= match_threshold
    ORDER BY vk.embedding <=> query_embedding
    LIMIT match_count;
END;
$$;
```

---

## Quick Status Check

Run this single query to get a quick overview:

```sql
SELECT 
    'Total Records' as metric,
    COUNT(*)::text as value
FROM vedic_knowledge
UNION ALL
SELECT 
    'Categories',
    COUNT(DISTINCT category)::text
FROM vedic_knowledge
UNION ALL
SELECT 
    'With Embeddings',
    COUNT(embedding)::text
FROM vedic_knowledge
UNION ALL
SELECT 
    'pgvector Enabled',
    CASE WHEN EXISTS (SELECT 1 FROM pg_extension WHERE extname = 'vector') 
         THEN 'Yes' ELSE 'No' END
UNION ALL
SELECT 
    'RPC Function',
    CASE WHEN EXISTS (
        SELECT 1 FROM information_schema.routines 
        WHERE routine_name = 'match_vedic_knowledge'
    ) THEN 'Yes' ELSE 'No' END;
```

---

## Fix Embedding Dimension Check Query

The vector type in PostgreSQL doesn't cast directly to float[]. Use this corrected query:

```sql
-- Corrected: Check embedding status (vector type doesn't need dimension check)
SELECT 
    id,
    category,
    CASE 
        WHEN embedding IS NOT NULL THEN '✅ Has embedding (1536 dims)'
        ELSE '❌ No embedding'
    END as embedding_status,
    created_at
FROM vedic_knowledge
LIMIT 10;
```

Or verify embeddings exist:

```sql
-- Simple check: All records should have embeddings
SELECT 
    COUNT(*) as total,
    COUNT(embedding) as with_embeddings,
    COUNT(*) - COUNT(embedding) as missing
FROM vedic_knowledge;
```

---

## Expected Results After Running Script

After successfully running `populate_knowledge_base.py`, you should see:

- **Total Records**: ~200-300+ records
- **Categories**: 6 categories (house_significations, dasha_interpretations, gochara_effects, bav_sav_rules, remedies, advanced_rules)
- **Embeddings**: All records should have embeddings (1536 dimensions)
- **House Records**: Records with house_number populated
- **Planet Records**: Records with planet populated
- **pgvector**: Extension enabled
- **RPC Function**: Function exists

---

## Testing RAG Retrieval

Test if RAG is working:

```sql
-- Test RPC function with a sample query
-- Note: You need to generate an embedding first using OpenAI
-- This is just to test the function structure

SELECT * FROM match_vedic_knowledge(
    query_embedding := (SELECT embedding FROM vedic_knowledge LIMIT 1),
    match_threshold := 0.5,
    match_count := 5,
    filter_category := 'house_significations'
);
```

---

## Next Steps

1. ✅ Verify table exists and has data
2. ✅ Check embeddings are created
3. ✅ Verify pgvector extension
4. ✅ Verify RPC function
5. ✅ Test RAG retrieval from your app
6. ✅ Monitor query performance

