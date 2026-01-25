-- Fix: Create Missing RPC Function for Vector Similarity Search
-- Run this in Supabase SQL Editor

-- IMPORTANT: The Python code uses 'filter_house' parameter name
-- This function matches the Python code expectations

CREATE OR REPLACE FUNCTION match_vedic_knowledge(
    query_embedding vector(1536),
    match_threshold float DEFAULT 0.78,
    match_count int DEFAULT 5,
    filter_category text DEFAULT NULL,
    filter_house int DEFAULT NULL,  -- Python code uses 'filter_house'
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
        AND (filter_house IS NULL OR vk.house_number = filter_house)
        AND (filter_planet IS NULL OR vk.planet = filter_planet)
        AND (1 - (vk.embedding <=> query_embedding)) >= match_threshold
    ORDER BY vk.embedding <=> query_embedding
    LIMIT match_count;
END;
$$;

-- Verify function was created
SELECT 
    routine_name,
    routine_type,
    data_type as return_type
FROM information_schema.routines
WHERE routine_schema = 'public'
AND routine_name = 'match_vedic_knowledge';

