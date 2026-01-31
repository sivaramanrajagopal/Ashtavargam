-- RAG Setup Verification Script
-- Run this in Supabase SQL Editor to verify your RAG setup

-- ============================================
-- 1. CHECK IF RPC FUNCTION EXISTS
-- ============================================
SELECT 
    routine_name, 
    routine_type,
    CASE 
        WHEN routine_name = 'match_vedic_knowledge' THEN '✅ RPC Function EXISTS'
        ELSE '❌ RPC Function NOT FOUND'
    END as status
FROM information_schema.routines
WHERE routine_schema = 'public'
AND routine_name = 'match_vedic_knowledge';

-- ============================================
-- 2. CHECK EMBEDDINGS STATUS
-- ============================================
SELECT 
    COUNT(*) as total_records,
    COUNT(embedding) as records_with_embeddings,
    COUNT(*) - COUNT(embedding) as records_without_embeddings,
    CASE 
        WHEN COUNT(embedding) = COUNT(*) THEN '✅ All records have embeddings'
        WHEN COUNT(embedding) > 0 THEN '⚠️ Some records missing embeddings'
        ELSE '❌ No embeddings found'
    END as embedding_status
FROM vedic_knowledge;

-- ============================================
-- 3. CHECK EMBEDDING DIMENSIONS
-- ============================================
-- Note: pgvector stores dimensions in the type itself
-- We can't directly check dimension, but we can verify embeddings exist
SELECT 
    id,
    category,
    house_number,
    CASE 
        WHEN embedding IS NULL THEN '❌ NULL'
        ELSE '✅ Has embedding (vector type)'
    END as embedding_status,
    'vector(1536)' as expected_type
FROM vedic_knowledge
WHERE embedding IS NOT NULL
LIMIT 10;

-- ============================================
-- 4. CHECK DATA DISTRIBUTION BY CATEGORY
-- ============================================
SELECT 
    category,
    COUNT(*) as count,
    COUNT(embedding) as with_embeddings,
    ROUND(100.0 * COUNT(embedding) / COUNT(*), 2) as embedding_percentage
FROM vedic_knowledge
GROUP BY category
ORDER BY count DESC;

-- ============================================
-- 5. CHECK DATA DISTRIBUTION BY HOUSE
-- ============================================
SELECT 
    house_number,
    COUNT(*) as count,
    COUNT(embedding) as with_embeddings
FROM vedic_knowledge
WHERE house_number IS NOT NULL
GROUP BY house_number
ORDER BY house_number;

-- ============================================
-- 6. SAMPLE RECORDS WITH EMBEDDINGS
-- ============================================
SELECT 
    id,
    category,
    house_number,
    planet,
    LEFT(content, 100) as content_preview,
    CASE 
        WHEN embedding IS NOT NULL THEN '✅ Has embedding'
        ELSE '❌ No embedding'
    END as embedding_status
FROM vedic_knowledge
ORDER BY id
LIMIT 5;

-- ============================================
-- 7. TEST RPC FUNCTION (if it exists)
-- ============================================
-- Test the RPC function with a sample embedding
-- This will only work if the RPC function exists
SELECT 
    CASE 
        WHEN EXISTS (
            SELECT 1 FROM information_schema.routines 
            WHERE routine_name = 'match_vedic_knowledge'
        ) THEN '✅ RPC Function exists - ready to test'
        ELSE '❌ RPC Function not found - run FIX_RPC_FUNCTION.sql first'
    END as rpc_test_status;

-- To actually test the function, use this query (uncomment when ready):
-- SELECT * FROM match_vedic_knowledge(
--     (SELECT embedding FROM vedic_knowledge WHERE embedding IS NOT NULL LIMIT 1),
--     0.7,  -- match_threshold
--     5,    -- match_count
--     'house',  -- filter_category
--     10,   -- filter_house
--     NULL  -- filter_planet
-- );

-- ============================================
-- SUMMARY
-- ============================================
SELECT 
    'RAG Setup Verification' as check_type,
    CASE 
        WHEN EXISTS (
            SELECT 1 FROM information_schema.routines 
            WHERE routine_name = 'match_vedic_knowledge'
        ) THEN '✅ RPC Function: EXISTS'
        ELSE '❌ RPC Function: MISSING'
    END as rpc_status,
    CASE 
        WHEN (SELECT COUNT(embedding) FROM vedic_knowledge) > 0 
        THEN '✅ Embeddings: POPULATED'
        ELSE '❌ Embeddings: EMPTY'
    END as embedding_status,
    (SELECT COUNT(*) FROM vedic_knowledge) as total_records,
    (SELECT COUNT(embedding) FROM vedic_knowledge) as records_with_embeddings;

