-- Supabase RPC Function for Vector Similarity Search
-- Run this in Supabase SQL Editor for optimal performance

CREATE OR REPLACE FUNCTION match_vedic_knowledge(
    query_embedding vector(1536),
    match_threshold float DEFAULT 0.7,
    match_count int DEFAULT 5,
    filter_category text DEFAULT NULL,
    filter_house int DEFAULT NULL,
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
        vk.category::text,  -- Cast VARCHAR(50) to text
        vk.content,
        vk.metadata,
        vk.house_number,
        vk.planet::text,  -- Cast VARCHAR(20) to text
        1 - (vk.embedding <=> query_embedding) as similarity
    FROM vedic_knowledge vk
    WHERE
        (filter_category IS NULL OR vk.category = filter_category)
        AND (filter_house IS NULL OR vk.house_number = filter_house)
        AND (filter_planet IS NULL OR vk.planet = filter_planet)
        AND (1 - (vk.embedding <=> query_embedding)) >= match_threshold
    ORDER BY vk.embedding <=> query_embedding
    LIMIT match_count;
END;
$$;

-- Create index for better performance
CREATE INDEX IF NOT EXISTS vedic_knowledge_embedding_idx 
ON vedic_knowledge 
USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);

