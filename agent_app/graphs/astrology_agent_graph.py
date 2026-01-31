"""
LangGraph Agent for Vedic Astrology Analysis
Intelligent agent that routes queries, calls APIs, retrieves RAG context, and generates interpretations
"""

import os
import time
import logging
from typing import TypedDict, List, Optional, Dict, Annotated, Literal
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

from agent_app.tools.astrology_tools import get_all_tools
from agent_app.rag.supabase_rag import SupabaseRAGSystem

# Configure logger for this module
logger = logging.getLogger(__name__)


# Initialize OpenAI LLM
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.7,
    openai_api_key=os.getenv("OPENAI_API_KEY")
)

# Initialize RAG system
rag_system = SupabaseRAGSystem()

# Get tools
tools = get_all_tools()
tools_dict = {tool.name: tool for tool in tools}


class AgentState(TypedDict):
    """Agent state schema for LangGraph"""
    user_query: str
    birth_data: Optional[Dict]
    query_intent: str  # 'house_analysis', 'dasha_analysis', 'gochara_analysis', 'full_dashboard', 'general'
    selected_houses: List[int]  # Which houses to analyze
    bav_sav_data: Optional[Dict]
    dasha_data: Optional[Dict]
    gochara_data: Optional[Dict]
    rag_context: Annotated[List[str], "append"]
    current_step: str
    intermediate_results: Dict
    final_response: Optional[str]
    citations: Annotated[List[str], "append"]
    needs_more_context: bool


def route_query(state: AgentState) -> AgentState:
    """Router node: Analyze query intent and determine which path to take"""
    
    query = state["user_query"].lower()
    birth_data = state.get("birth_data")
    
    # Determine intent
    intent = "general"
    selected_houses = []
    
    # Check for house-specific queries
    house_keywords = {
        "1st house": 1, "first house": 1, "lagna": 1, "ascendant": 1,
        "2nd house": 2, "second house": 2, "wealth": 2,
        "3rd house": 3, "third house": 3, "siblings": 3,
        "4th house": 4, "fourth house": 4, "home": 4, "mother": 4,
        "5th house": 5, "fifth house": 5, "children": 5, "education": 5,
        "6th house": 6, "sixth house": 6, "enemies": 6, "health": 6,
        "7th house": 7, "seventh house": 7, "marriage": 7, "spouse": 7,
        "8th house": 8, "eighth house": 8, "longevity": 8,
        "9th house": 9, "ninth house": 9, "fortune": 9, "father": 9,
        "10th house": 10, "tenth house": 10, "career": 10, "profession": 10,
        "11th house": 11, "eleventh house": 11, "gains": 11, "income": 11,
        "12th house": 12, "twelfth house": 12, "losses": 12, "expenses": 12
    }
    
    for keyword, house_num in house_keywords.items():
        if keyword in query:
            selected_houses.append(house_num)
            intent = "house_analysis"
            break
    
    # Check for Dasha queries
    if any(word in query for word in ["dasha", "dasa", "planetary period", "maha dasa", "bhukti"]):
        intent = "dasha_analysis"
    
    # Check for Gochara/transit queries
    elif any(word in query for word in ["gochara", "transit", "current transits", "planetary transit"]):
        intent = "gochara_analysis"
    
    # Check for full dashboard requests
    elif any(word in query for word in ["complete", "full", "all houses", "dashboard", "analyze chart"]):
        intent = "full_dashboard"
        selected_houses = list(range(1, 13))
    
    # Check if birth data is needed
    needs_birth_data = intent != "general" and not birth_data
    
    state["query_intent"] = intent
    state["selected_houses"] = selected_houses
    state["current_step"] = "routed"
    
    if needs_birth_data:
        state["final_response"] = "Please provide your birth details (date, time, location) to proceed with the analysis."
        return state
    
    return state


def calculate_chart_data(state: AgentState) -> AgentState:
    """Calculator node: Agent decides which APIs to call based on intent"""
    
    calc_start = time.time()
    intent = state["query_intent"]
    birth_data = state.get("birth_data")
    
    if not birth_data:
        return state
    
    # Check if we already have cached data (from previous queries in same session)
    existing_bav_sav = state.get("bav_sav_data")
    existing_dasha = state.get("dasha_data")
    existing_gochara = state.get("gochara_data")
    
    # Agent decision: Which APIs to call?
    # ALWAYS call BAV/SAV if query mentions houses or is general (might need chart data)
    query_lower = state.get("user_query", "").lower()
    needs_bav_sav = (
        intent in ["house_analysis", "full_dashboard", "general"] or
        any(word in query_lower for word in ["house", "7th", "10th", "career", "marriage", "health", "wealth", "sav", "bav", "ashtakavarga"])
    )
    
    # Only call API if we don't have cached data
    if needs_bav_sav and not existing_bav_sav:
        # Need BAV/SAV for house analysis
        try:
            import requests
            import os
            api_url = os.getenv("BAV_SAV_API_URL", "http://localhost:8000")
            
            # Convert birth_data to API format (latitude/longitude instead of lat/lon)
            # Handle both lat/lon and latitude/longitude formats
            api_birth_data = {
                "dob": birth_data.get("dob"),
                "tob": birth_data.get("tob"),
                "latitude": birth_data.get("latitude") or birth_data.get("lat"),
                "longitude": birth_data.get("longitude") or birth_data.get("lon"),
                "tz_offset": birth_data.get("tz_offset"),
                "name": birth_data.get("name"),
                "place": birth_data.get("place")
            }
            
            # Debug: Log API request data
            logger.info(f"🔍 Calling BAV/SAV API with: dob={api_birth_data.get('dob')}, lat={api_birth_data.get('latitude')}, lon={api_birth_data.get('longitude')}")
            
            api_start = time.time()
            response = requests.post(
                f"{api_url}/api/v1/calculate/full",
                json=api_birth_data,
                timeout=30
            )
            api_duration = time.time() - api_start
            logger.info(f"⏱️ BAV/SAV API call took {api_duration:.2f}s")
            
            response.raise_for_status()
            bav_sav_result = response.json()
            if isinstance(bav_sav_result, dict) and "error" not in bav_sav_result and "detail" not in bav_sav_result:
                state["bav_sav_data"] = bav_sav_result
                logger.info(f"✅ BAV/SAV data retrieved: SAV total={bav_sav_result.get('sav_total', 'N/A')}, Houses={len(bav_sav_result.get('sav_chart', []))}")
            else:
                logger.warning(f"⚠️ BAV/SAV API returned error: {bav_sav_result}")
        except Exception as e:
            logger.error(f"❌ Error calling BAV/SAV API: {e}")
            import traceback
            traceback.print_exc()
    
    # ALWAYS call Dasha if query mentions dasha, period, timing, or is general
    needs_dasha = (
        intent in ["dasha_analysis", "full_dashboard", "house_analysis"] or
        any(word in query_lower for word in ["dasha", "dasa", "period", "bhukti", "when", "timing", "current"])
    )
    
    # Only call API if we don't have cached data
    if needs_dasha and not existing_dasha:
        # Need Dasha for period analysis
        try:
            import requests
            import os
            api_url = os.getenv("DASHA_GOCHARA_API_URL", "http://localhost:8001")
            
            # Convert birth_data to API format (Dasha API expects lat/lon, not latitude/longitude)
            api_birth_data = {
                "dob": birth_data.get("dob"),
                "tob": birth_data.get("tob"),
                "lat": birth_data.get("lat") or birth_data.get("latitude"),
                "lon": birth_data.get("lon") or birth_data.get("longitude"),
                "tz_offset": birth_data.get("tz_offset"),
                "name": birth_data.get("name"),
                "place": birth_data.get("place")
            }
            
            logger.info(f"🔍 Calling Dasha API with: dob={api_birth_data.get('dob')}, lat={api_birth_data.get('lat')}, lon={api_birth_data.get('lon')}")
            
            api_start = time.time()
            response = requests.post(
                f"{api_url}/api/v1/dasha/current",
                json=api_birth_data,
                timeout=30
            )
            api_duration = time.time() - api_start
            logger.info(f"⏱️ Dasha API call took {api_duration:.2f}s")
            
            response.raise_for_status()
            dasha_result = response.json()
            if isinstance(dasha_result, dict) and "error" not in dasha_result and "detail" not in dasha_result:
                state["dasha_data"] = dasha_result
                logger.info(f"✅ Dasha data retrieved: {dasha_result.get('current_dasa', 'N/A')} - {dasha_result.get('current_bhukti', 'N/A')}")
            else:
                logger.warning(f"⚠️ Dasha API returned error: {dasha_result}")
                import traceback
                traceback.print_exc()
        except Exception as e:
            logger.error(f"❌ Error calling Dasha API: {e}")
            import traceback
            traceback.print_exc()
    
    # ALWAYS call Gochara if query mentions transits, gochara, or current influences
    needs_gochara = (
        intent in ["gochara_analysis", "full_dashboard", "house_analysis"] or
        any(word in query_lower for word in ["gochara", "transit", "current", "now", "influence"])
    )
    
    # Only call API if we don't have cached data
    if needs_gochara and not existing_gochara:
        # Need Gochara for transit analysis
        try:
            import requests
            import os
            api_url = os.getenv("DASHA_GOCHARA_API_URL", "http://localhost:8001")
            
            # Convert birth_data to API format (Gochara API expects lat/lon)
            api_birth_data = {
                "dob": birth_data.get("dob"),
                "tob": birth_data.get("tob"),
                "lat": birth_data.get("lat") or birth_data.get("latitude"),
                "lon": birth_data.get("lon") or birth_data.get("longitude"),
                "tz_offset": birth_data.get("tz_offset"),
                "name": birth_data.get("name"),
                "place": birth_data.get("place")
            }
            
            api_start = time.time()
            response = requests.post(
                f"{api_url}/api/v1/gochara/current",
                json=api_birth_data,
                timeout=30
            )
            api_duration = time.time() - api_start
            logger.info(f"⏱️ Gochara API call took {api_duration:.2f}s")
            
            response.raise_for_status()
            gochara_result = response.json()
            if isinstance(gochara_result, dict) and "error" not in gochara_result:
                state["gochara_data"] = gochara_result
                logger.info(f"✅ Gochara data retrieved")
            else:
                logger.warning(f"⚠️ Gochara API returned error: {gochara_result}")
        except Exception as e:
            logger.error(f"❌ Error calling Gochara API: {e}")
            import traceback
            traceback.print_exc()
    
    # Use cached data if available and API wasn't called
    if needs_bav_sav and existing_bav_sav and not state.get("bav_sav_data"):
        state["bav_sav_data"] = existing_bav_sav
        logger.info(f"✅ Using cached BAV/SAV data")
    
    if needs_dasha and existing_dasha and not state.get("dasha_data"):
        state["dasha_data"] = existing_dasha
        logger.info(f"✅ Using cached Dasha data")
    
    if needs_gochara and existing_gochara and not state.get("gochara_data"):
        state["gochara_data"] = existing_gochara
        logger.info(f"✅ Using cached Gochara data")
    
    calc_duration = time.time() - calc_start
    logger.info(f"⏱️ Total calculate_chart_data took {calc_duration:.2f}s")
    state["current_step"] = "calculated"
    return state


def retrieve_knowledge(state: AgentState) -> AgentState:
    """RAG Retrieval node: Retrieve relevant Vedic knowledge from Supabase"""
    
    retrieve_start = time.time()
    query = state["user_query"]
    intent = state["query_intent"]
    selected_houses = state.get("selected_houses", [])
    
    # Determine category and filters
    category = None
    if intent == "dasha_analysis":
        category = "dasha"
    elif intent == "gochara_analysis":
        category = "gochara"
    elif intent == "house_analysis":
        category = "house"
    
    # Retrieve context for each selected house (or general)
    context_chunks = []
    
    if selected_houses:
        for house_num in selected_houses:
            chunks = rag_system.retrieve_context(
                query=query,
                top_k=2,  # Reduced from 3 for faster retrieval
                category=category,
                house_number=house_num
            )
            context_chunks.extend(chunks)
    else:
        # General retrieval
        chunks = rag_system.retrieve_context(
            query=query,
            top_k=3,  # Reduced from 5 for faster retrieval
            category=category
        )
        context_chunks.extend(chunks)
    
    # Store context in state
    for chunk in context_chunks:
        state["rag_context"].append(chunk.get("content", ""))
        # Add citation
        source = f"{chunk.get('category', 'general')}"
        if chunk.get("house_number"):
            source += f" - House {chunk['house_number']}"
        if chunk.get("planet"):
            source += f" - {chunk['planet']}"
        state["citations"].append(source)
    
    retrieve_duration = time.time() - retrieve_start
    logger.info(f"⏱️ retrieve_knowledge took {retrieve_duration:.2f}s")
    state["current_step"] = "retrieved"
    return state


def analyze_and_interpret(state: AgentState) -> AgentState:
    """Analysis node: Combine data and generate interpretation using OpenAI"""
    
    analyze_start = time.time()
    query = state["user_query"]
    intent = state["query_intent"]
    rag_context = state.get("rag_context", [])
    bav_sav_data = state.get("bav_sav_data")
    dasha_data = state.get("dasha_data")
    gochara_data = state.get("gochara_data")
    selected_houses = state.get("selected_houses", [])
    
    # Prepare chart data
    chart_data = {
        "bav_sav": bav_sav_data,
        "dasha": dasha_data,
        "gochara": gochara_data
    }
    
    # Build context chunks for RAG
    context_chunks = [{"content": ctx, "category": "general"} for ctx in rag_context]
    
    # Generate interpretation using RAG system
    try:
        llm_start = time.time()
        interpretation = rag_system.generate_interpretation(
            query=query,
            context_chunks=context_chunks,
            chart_data=chart_data
        )
        llm_duration = time.time() - llm_start
        logger.info(f"⏱️ LLM call took {llm_duration:.2f}s")
        state["final_response"] = interpretation
    except Exception as e:
        # Fallback: Use LLM directly if RAG fails
        logger.warning(f"RAG generation failed, using LLM directly: {e}")
        import traceback
        traceback.print_exc()
        
        # Format chart data properly for fallback
        from agent_app.rag.supabase_rag import SupabaseRAGSystem
        rag_temp = SupabaseRAGSystem()
        chart_data_formatted = rag_temp._format_chart_data({
            "bav_sav": bav_sav_data,
            "dasha": dasha_data,
            "gochara": gochara_data
        })
        
        # Build prompt
        system_prompt = """You are an expert Vedic astrologer. Provide accurate, 
        traditional interpretations based on the provided chart data.
        
        CRITICAL: You MUST use the actual chart data provided below. DO NOT give generic 
        interpretations. Always reference specific SAV points, BAV contributions, 
        Dasha periods, and transit data. If the data shows specific numbers, use them."""
        
        user_prompt = f"""Query: {query}

ACTUAL CHART DATA (USE THESE EXACT NUMBERS):
{chart_data_formatted}

Context from Knowledge Base:
{chr(10).join(rag_context[:3]) if rag_context else "No specific context available"}

IMPORTANT: 
- If SAV points are provided, state them explicitly (e.g., "Your 7th house has 28 SAV points")
- If Dasha data is provided, state it explicitly (e.g., "You are in Moon Dasha with Mercury Bhukti")
- DO NOT say "if your house has X points" - use the actual numbers provided
- DO NOT give generic interpretations - be specific to the data provided

Provide a comprehensive interpretation using the ACTUAL data above."""
        
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt)
        ]
        
        llm_start = time.time()
        response = llm.invoke(messages)
        llm_duration = time.time() - llm_start
        logger.info(f"⏱️ LLM fallback call took {llm_duration:.2f}s")
        state["final_response"] = response.content
    
    analyze_duration = time.time() - analyze_start
    logger.info(f"⏱️ Total analyze_and_interpret took {analyze_duration:.2f}s")
    state["current_step"] = "analyzed"
    return state


def format_response(state: AgentState) -> AgentState:
    """Response node: Format final response with citations"""
    
    response = state.get("final_response", "I apologize, but I couldn't generate a response.")
    citations = state.get("citations", [])
    
    # Add citations to response
    if citations:
        unique_citations = list(set(citations))
        response += f"\n\n**Sources:** {', '.join(unique_citations[:5])}"
    
    state["final_response"] = response
    state["current_step"] = "completed"
    return state


def should_continue(state: AgentState) -> str:
    """Conditional edge: Determine next step based on state"""
    
    # If final_response already exists (e.g., missing birth data), go to format
    if state.get("final_response"):
        return "format"
    
    # Otherwise continue to calculate
    return "calculate"


def create_agent_graph() -> StateGraph:
    """Create and compile the LangGraph agent"""
    
    # Create graph
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("route", route_query)
    workflow.add_node("calculate", calculate_chart_data)
    workflow.add_node("retrieve", retrieve_knowledge)
    workflow.add_node("analyze", analyze_and_interpret)
    workflow.add_node("format", format_response)
    
    # Set entry point
    workflow.set_entry_point("route")
    
    # Add edges - linear flow with conditional check
    workflow.add_conditional_edges(
        "route",
        should_continue,
        {
            "calculate": "calculate",
            "format": "format"
        }
    )
    
    workflow.add_edge("calculate", "retrieve")
    workflow.add_edge("retrieve", "analyze")
    workflow.add_edge("analyze", "format")
    workflow.add_edge("format", END)
    
    # Compile graph
    return workflow.compile()


# Initialize agent graph
agent_graph = create_agent_graph()

