"""
Supabase RAG System for Vedic Astrology Knowledge Retrieval
Uses Supabase PG Vector with OpenAI embeddings
"""

import os
from typing import List, Dict, Optional
from supabase import create_client, Client
from openai import OpenAI

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


class SupabaseRAGSystem:
    """RAG system using Supabase PG Vector and OpenAI embeddings"""
    
    def __init__(self, supabase_url: str = None, supabase_key: str = None, openai_key: str = None):
        """
        Initialize RAG system with Supabase and OpenAI clients.
        
        Args:
            supabase_url: Supabase project URL (or from env)
            supabase_key: Supabase service role key (or from env)
            openai_key: OpenAI API key (or from env)
        """
        # Get from environment if not provided
        self.supabase_url = supabase_url or os.getenv("SUPABASE_URL")
        self.supabase_key = supabase_key or os.getenv("SUPABASE_KEY")
        self.openai_key = openai_key or os.getenv("OPENAI_API_KEY")
        
        if not self.supabase_url or not self.supabase_key:
            raise ValueError("Supabase URL and key must be provided or set in environment variables")
        
        if not self.openai_key:
            raise ValueError("OpenAI API key must be provided or set in environment variables")
        
        # Initialize clients
        self.supabase: Client = create_client(self.supabase_url, self.supabase_key)
        # Initialize OpenAI with timeout configuration
        self.openai = OpenAI(
            api_key=self.openai_key,
            timeout=30.0,  # Increased to 30s for production (network latency can be higher)
            max_retries=2  # Retry up to 2 times on failure
        )
        
        # Embedding model
        self.embedding_model = "text-embedding-3-small"
        self.embedding_dimension = 1536
    
    def embed_text(self, text: str) -> List[float]:
        """
        Generate embedding for text using OpenAI.
        
        Args:
            text: Text to embed
        
        Returns:
            List of floats representing the embedding vector
        """
        import time
        start_time = time.time()
        try:
            # Use explicit timeout parameter (in addition to client-level timeout)
            response = self.openai.embeddings.create(
                model=self.embedding_model,
                input=text,
                timeout=30.0  # 30s timeout for embeddings (matches LLM timeout for production)
            )
            duration = time.time() - start_time
            if duration > 2.0:  # Log if embedding takes > 2s
                print(f"⚠️ Embedding took {duration:.2f}s (slower than expected)")
            return response.data[0].embedding
        except Exception as e:
            duration = time.time() - start_time
            print(f"❌ Embedding failed after {duration:.2f}s: {str(e)}")
            # Re-raise with more context
            raise Exception(f"Error generating embedding after {duration:.2f}s: {str(e)}")
    
    def store_knowledge(self, content: str, metadata: Dict = None, 
                       category: str = None, house_number: int = None, 
                       planet: str = None) -> Dict:
        """
        Store knowledge in Supabase with embedding.
        
        Args:
            content: Knowledge content text
            metadata: Additional metadata (JSONB)
            category: Knowledge category ('dasha', 'gochara', 'bav_sav', 'house', 'remedy', 'general')
            house_number: House number if house-specific (1-12)
            planet: Planet name if planet-specific
        
        Returns:
            Dict with stored record
        """
        try:
            # Generate embedding
            embedding = self.embed_text(content)
            
            # Prepare data
            data = {
                "content": content,
                "embedding": embedding,
                "metadata": metadata or {},
                "category": category,
                "house_number": house_number,
                "planet": planet
            }
            
            # Insert into Supabase
            result = self.supabase.table("vedic_knowledge").insert(data).execute()
            
            if result.data:
                return result.data[0]
            else:
                raise Exception("Failed to store knowledge")
        except Exception as e:
            raise Exception(f"Error storing knowledge: {str(e)}")
    
    def retrieve_context(self, query: str, top_k: int = 5, 
                        category: str = None, house_number: int = None,
                        planet: str = None) -> List[Dict]:
        """
        Retrieve relevant context from Supabase using vector similarity search.
        
        Args:
            query: Search query text
            top_k: Number of results to return
            category: Filter by category
            house_number: Filter by house number
            planet: Filter by planet
        
        Returns:
            List of relevant knowledge chunks with content and metadata
        """
        try:
            # Generate query embedding (with timeout protection)
            import time
            embed_start = time.time()
            try:
                query_embedding = self.embed_text(query)
            except Exception as embed_error:
                # If embedding fails, try to continue with empty context (graceful degradation)
                print(f"⚠️ Embedding generation failed: {embed_error}")
                print(f"⚠️ Continuing with empty context (RAG will be limited)")
                return []  # Return empty context instead of failing completely
            
            embed_duration = time.time() - embed_start
            if embed_duration > 2.0:  # Log if embedding takes > 2s
                print(f"⏱️ Embedding generation took {embed_duration:.2f}s")
            
            # Build base query with filters
            query = self.supabase.table("vedic_knowledge").select("id, content, metadata, category, house_number, planet")
            
            # Add filters
            if category:
                query = query.eq("category", category)
            if house_number:
                query = query.eq("house_number", house_number)
            if planet:
                query = query.eq("planet", planet)
            
            # Execute query
            result = query.limit(top_k * 2).execute()  # Get more results for filtering
            
            if not result.data:
                return []
            
            # Calculate cosine similarity for each result
            # Note: In production, you'd want to use Supabase RPC function for efficient vector search
            scored_results = []
            for record in result.data:
                # For now, return filtered results
                # In production, implement proper vector similarity search via Supabase RPC
                scored_results.append({
                    "content": record["content"],
                    "metadata": record.get("metadata", {}),
                    "category": record.get("category"),
                    "house_number": record.get("house_number"),
                    "planet": record.get("planet"),
                    "score": 1.0  # Placeholder - would be similarity score
                })
            
            # Sort by score and return top_k
            scored_results.sort(key=lambda x: x["score"], reverse=True)
            return scored_results[:top_k]
            
        except Exception as e:
            # Fallback: return empty list on error
            print(f"Error retrieving context: {str(e)}")
            return []
    
    def retrieve_context_advanced(self, query: str, top_k: int = 5,
                                  category: str = None, house_number: int = None,
                                  planet: str = None) -> List[Dict]:
        """
        Advanced retrieval using Supabase RPC function for vector similarity.
        Requires creating a custom function in Supabase.
        
        This is the recommended approach for production.
        """
        try:
            # Generate query embedding
            query_embedding = self.embed_text(query)
            
            # Call Supabase RPC function for vector search
            # Note: You need to create this function in Supabase first
            result = self.supabase.rpc(
                "match_vedic_knowledge",
                {
                    "query_embedding": query_embedding,
                    "match_threshold": 0.7,
                    "match_count": top_k,
                    "filter_category": category,
                    "filter_house": house_number,
                    "filter_planet": planet
                }
            ).execute()
            
            return result.data if result.data else []
            
        except Exception as e:
            # Fallback to basic retrieval
            print(f"Advanced retrieval failed, using basic: {str(e)}")
            return self.retrieve_context(query, top_k, category, house_number, planet)
    
    def generate_interpretation(self, query: str, context_chunks: List[Dict], 
                                chart_data: Dict = None) -> str:
        """
        Generate interpretation using OpenAI with RAG context.
        
        Args:
            query: User query
            context_chunks: Retrieved context from vector store
            chart_data: Optional chart data (BAV/SAV, Dasha, Gochara)
        
        Returns:
            Generated interpretation text
        """
        try:
            # Handle None or empty context_chunks
            if not context_chunks:
                context_chunks = []
            
            # Build context string
            context_text = "\n\n".join([
                f"[Source: {chunk.get('category', 'general')}] {chunk.get('content', '')}"
                for chunk in context_chunks if chunk and isinstance(chunk, dict)
            ])
            
            # Build prompt (condensed for faster processing)
            system_prompt = """Expert Vedic astrologer. Use ACTUAL chart data provided. 
            Reference specific SAV points, BAV contributions, Dasha periods, and transit data. 
            DO NOT give generic interpretations."""
            
            # Format chart data with specific details
            chart_data_text = self._format_chart_data(chart_data) if chart_data else "No chart data provided"
            
            # Extract specific house information if query mentions a house
            house_specific_info = ""
            house_num = None
            
            # Extract Dasha-specific information if query mentions Dasha
            dasha_specific_info = ""
            query_lower = query.lower()
            
            # Check if query is about Dasha
            dasha_keywords = ["dasha", "dasa", "period", "bhukti", "current", "planetary period", "maha dasa"]
            is_dasha_query = any(keyword in query_lower for keyword in dasha_keywords)
            
            if is_dasha_query and chart_data and chart_data.get("dasha"):
                dasha = chart_data["dasha"]
                if dasha and isinstance(dasha, dict):
                    dasha_specific_info = f"\n\nCURRENT DASHA DATA (YOU MUST USE THIS - DO NOT SAY IT'S NOT AVAILABLE):\n"
                    dasha_specific_info += f"- Current Dasha: {dasha.get('current_dasa', 'N/A')}\n"
                    dasha_specific_info += f"- Current Bhukti: {dasha.get('current_bhukti', 'N/A')}\n"
                    if dasha.get('start_date'):
                        dasha_specific_info += f"- Dasha Start Date: {dasha.get('start_date', 'N/A')}\n"
                    if dasha.get('end_date'):
                        dasha_specific_info += f"- Dasha End Date: {dasha.get('end_date', 'N/A')}\n"
                    if dasha.get('age'):
                        dasha_specific_info += f"- Age: {dasha.get('age', 'N/A')} years\n"
                    if dasha.get('remaining_years'):
                        dasha_specific_info += f"- Remaining Years in Current Dasha: {dasha.get('remaining_years', 'N/A')} years\n"
                    dasha_specific_info += f"\nCRITICAL: The Dasha data above is REAL and CALCULATED. You MUST state it explicitly in your response."
                    dasha_specific_info += f" DO NOT say 'Dasha is not mentioned' or 'I need your birth details' - the data is provided above."
            
            # Detect house number from query
            house_keywords = {
                "1st": 1, "first": 1, "lagna": 1, "ascendant": 1,
                "2nd": 2, "second": 2, "wealth": 2,
                "3rd": 3, "third": 3, "siblings": 3,
                "4th": 4, "fourth": 4, "home": 4, "mother": 4,
                "5th": 5, "fifth": 5, "children": 5, "education": 5,
                "6th": 6, "sixth": 6, "enemies": 6, "health": 6,
                "7th": 7, "seventh": 7, "marriage": 7, "spouse": 7,
                "8th": 8, "eighth": 8, "longevity": 8,
                "9th": 9, "ninth": 9, "fortune": 9, "father": 9,
                "10th": 10, "tenth": 10, "career": 10, "profession": 10,
                "11th": 11, "eleventh": 11, "gains": 11, "income": 11,
                "12th": 12, "twelfth": 12, "losses": 12, "expenses": 12
            }
            
            for keyword, num in house_keywords.items():
                if keyword in query_lower:
                    house_num = num
                    break
            
            if house_num and chart_data and chart_data.get("bav_sav") and chart_data["bav_sav"].get("sav_chart"):
                sav_chart = chart_data["bav_sav"]["sav_chart"]
                if len(sav_chart) >= house_num:
                    house_points = sav_chart[house_num - 1]  # 0-indexed
                    house_specific_info = f"\n\nSPECIFIC HOUSE {house_num} DATA:\n"
                    house_specific_info += f"- SAV Points: {house_points} (This is the CORRECT total for House {house_num})\n"
                    house_specific_info += f"- Strength: Strong if >=30, Good if >=28, Weak if <22\n\n"
                    house_specific_info += f"Individual BAV Contributions to House {house_num}:\n"
                    house_specific_info += f"IMPORTANT: SAV is the sum of 7 planets ONLY (excluding Ascendant).\n"
                    house_specific_info += f"Individual BAV values show each planet's contribution:\n"
                    
                    if chart_data["bav_sav"].get("bav_charts"):
                        bav_list = []
                        # API returns planet names in UPPERCASE, convert to title case for display
                        planet_display_map = {
                            'SUN': 'Sun', 'MOON': 'Moon', 'MARS': 'Mars', 
                            'MERCURY': 'Mercury', 'JUPITER': 'Jupiter', 
                            'VENUS': 'Venus', 'SATURN': 'Saturn', 'ASCENDANT': 'Ascendant'
                        }
                        # Order planets for consistent display (7 planets first, then Ascendant)
                        planet_order = ['SUN', 'MOON', 'MARS', 'MERCURY', 'JUPITER', 'VENUS', 'SATURN', 'ASCENDANT']
                        seven_planets_sum = 0
                        for planet_key in planet_order:
                            if planet_key in chart_data["bav_sav"]["bav_charts"]:
                                bav = chart_data["bav_sav"]["bav_charts"][planet_key]
                                if isinstance(bav, list) and len(bav) >= house_num:
                                    planet_points = bav[house_num - 1]
                                    planet_display = planet_display_map.get(planet_key, planet_key.title())
                                    bav_list.append(f"  - {planet_display}: {planet_points} points")
                                    if planet_key != 'ASCENDANT':
                                        seven_planets_sum += planet_points
                        house_specific_info += "\n".join(bav_list)
                        house_specific_info += f"\n\nCRITICAL: SAV of {house_points} = Sum of 7 planets ({seven_planets_sum}), NOT including Ascendant."
                        house_specific_info += f" The Ascendant BAV is shown separately for reference but is NOT included in SAV calculation."
            
            user_prompt = f"""Query: {query}

Context from Vedic Astrology Knowledge Base:
{context_text}

ACTUAL CHART DATA (YOU MUST USE THESE EXACT NUMBERS - DO NOT GIVE GENERIC INTERPRETATIONS):
{chart_data_text}
{house_specific_info}
{dasha_specific_info}

RULES:
1. SAV = sum of 7 planets ONLY (Sun+Moon+Mars+Mercury+Jupiter+Venus+Saturn). Ascendant NOT included.
2. Start with ACTUAL SAV value (e.g., "Your 7th house has 28 SAV points")
3. Use ACTUAL numbers - DO NOT say "if your house has X points"
4. List BAV contributions with actual numbers
5. For Dasha queries: State current Dasha/Bhukti explicitly if data provided
6. SAV strength: >=30 Strong, >=28 Good, <22 Weak
7. DO NOT add all 8 BAV points - only 7 planets make SAV
8. DO NOT ask for birth details if chart data is provided"""
            
            # Call OpenAI with shorter response for dashboard
            response = self.openai.chat.completions.create(
                model="gpt-4o-mini",  # Using gpt-4o-mini for cost efficiency
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
                max_tokens=800,  # Reduced from 1500 for faster generation
                timeout=30  # Increased to 30s for production (network latency can be higher)
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            raise Exception(f"Error generating interpretation: {str(e)}")
    
    def _format_chart_data(self, chart_data: Dict) -> str:
        """Format chart data for prompt with detailed house-specific information"""
        if not chart_data:
            return "No chart data provided"
        
        formatted = []
        
        if "bav_sav" in chart_data and chart_data["bav_sav"]:
            bav_sav = chart_data["bav_sav"]
            
            # SAV Chart (12 houses with points)
            sav_chart = bav_sav.get('sav_chart', [])
            if sav_chart and len(sav_chart) == 12:
                formatted.append("SAV (Sarvashtakavarga) Points by House:")
                for i, points in enumerate(sav_chart, 1):
                    strength = "Strong" if points >= 30 else "Good" if points >= 28 else "Weak" if points < 22 else "Moderate"
                    formatted.append(f"  House {i}: {points} points ({strength})")
                formatted.append(f"Total SAV: {sum(sav_chart)} points (should be 337)")
            
            # BAV Charts for each planet
            bav_charts = bav_sav.get('bav_charts', {})
            if bav_charts:
                formatted.append("\nBAV (Bhinnashtakavarga) - Individual Planetary Contributions:")
                formatted.append("IMPORTANT: BAV points are individual contributions from each planet/ascendant.")
                formatted.append("DO NOT add them together. SAV is the sum of all BAV contributions.")
                
                # Show BAV for specific house if query mentions a house
                # Extract house number from query if possible (will be done in prompt)
                for planet, chart in bav_charts.items():
                    if isinstance(chart, list) and len(chart) == 12:
                        total = sum(chart)  # Total for this planet across all houses
                        formatted.append(f"  {planet}: Total {total} points across all 12 houses")
        
        if "dasha" in chart_data and chart_data["dasha"]:
            dasha = chart_data["dasha"]
            if dasha and isinstance(dasha, dict):
                formatted.append(f"\n=== CURRENT DASHA DATA (REAL CALCULATED VALUES - USE THESE) ===")
                formatted.append(f"Current Dasha: {dasha.get('current_dasa', 'N/A')}")
                formatted.append(f"Current Bhukti: {dasha.get('current_bhukti', 'N/A')}")
                if dasha.get('start_date'):
                    formatted.append(f"Dasha Start Date: {dasha.get('start_date', 'N/A')}")
                if dasha.get('end_date'):
                    formatted.append(f"Dasha End Date: {dasha.get('end_date', 'N/A')}")
                if dasha.get('age'):
                    formatted.append(f"Age: {dasha.get('age', 'N/A')} years")
                if dasha.get('remaining_years'):
                    formatted.append(f"Remaining Years in Current Dasha: {dasha.get('remaining_years', 'N/A')} years")
                formatted.append(f"=== END DASHA DATA ===")
                formatted.append("CRITICAL: The Dasha data above is REAL and CALCULATED. You MUST state it explicitly.")
                formatted.append("DO NOT say 'Dasha is not mentioned' or 'I need your birth details' - the data is provided above.")
            else:
                formatted.append("\nDasha data: Not available or invalid format")
        
        if "gochara" in chart_data and chart_data["gochara"]:
            gochara = chart_data["gochara"]
            formatted.append(f"\nGochara (Transits):")
            if gochara.get('overall_health'):
                health = gochara['overall_health']
                formatted.append(f"  Overall Health Score: {health.get('average_score', 'N/A')}/100")
                formatted.append(f"  Status: {health.get('status', 'N/A')}")
            
            # Transit analysis for each planet
            transit_analysis = gochara.get('transit_analysis', [])
            if transit_analysis:
                formatted.append("  Current Transits (Planet → Transit House, Score, RAG):")
                for transit in transit_analysis[:9]:  # All planets
                    planet = transit.get('planet', 'N/A')
                    natal_house = transit.get('natal_house', 'N/A')
                    transit_house = transit.get('transit_house', 'N/A')
                    score = transit.get('score', 'N/A')
                    rag_data = transit.get('rag', {})
                    if isinstance(rag_data, dict):
                        rag = rag_data.get('status', rag_data.get('label', 'N/A'))
                    else:
                        rag = str(rag_data)
                    activated = transit.get('activated_houses', [])
                    formatted.append(f"    {planet}: Natal H{natal_house} → Transit H{transit_house}, Score {score}, RAG {rag}")
                    if activated and len(activated) > 1:
                        formatted.append(f"      Activates: {activated}")
        
        return "\n".join(formatted) if formatted else "Chart data available but format unknown"


# Helper function for easy initialization
def get_rag_system() -> SupabaseRAGSystem:
    """Get initialized RAG system from environment variables"""
    return SupabaseRAGSystem()

