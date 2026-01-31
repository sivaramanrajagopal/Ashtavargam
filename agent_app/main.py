"""
FastAPI Agent Server for Vedic Astrology AI Agent
Production-ready server with LangGraph agent integration
"""

import os
import sys
import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
from typing import Dict, List, Optional
import uvicorn

from agent_app.graphs.astrology_agent_graph import agent_graph
from agent_app.conversation.manager import conversation_manager

# Configure logging for Railway (ensure logs are visible)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)  # Explicitly use stdout
    ]
)
# Force unbuffered output
sys.stdout.reconfigure(line_buffering=True) if hasattr(sys.stdout, 'reconfigure') else None
sys.stderr.reconfigure(line_buffering=True) if hasattr(sys.stderr, 'reconfigure') else None

logger = logging.getLogger(__name__)
logger.info("🚀 Agent App starting up...")


# Initialize FastAPI app
app = FastAPI(
    title="Vedic Astrology AI Agent",
    description="LangGraph-powered AI agent for comprehensive Vedic astrology analysis",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files if they exist
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")


# ============================================================================
# PYDANTIC MODELS
# ============================================================================

class BirthData(BaseModel):
    """Birth data model"""
    dob: str = Field(..., description="Date of birth in YYYY-MM-DD format")
    tob: str = Field(..., description="Time of birth in HH:MM format")
    latitude: float = Field(..., description="Latitude", ge=-90, le=90, alias="lat")
    longitude: float = Field(..., description="Longitude", ge=-180, le=180, alias="lon")
    tz_offset: float = Field(..., description="Timezone offset from UTC")
    name: Optional[str] = Field(None, description="Name of the native")
    place: Optional[str] = Field(None, description="Place of birth")
    
    class Config:
        populate_by_name = True  # Allow both lat/lon and latitude/longitude


class QueryRequest(BaseModel):
    """Request model for agent query"""
    query: str = Field(..., description="User query/question")
    birth_data: Optional[BirthData] = Field(None, description="Birth data (required for chart analysis)")


class QueryResponse(BaseModel):
    """Response model for agent query"""
    response: str = Field(..., description="Agent's response")
    chart_data: Optional[Dict] = Field(None, description="Chart data if calculated")
    citations: List[str] = Field(default_factory=list, description="Sources/citations")
    analysis_type: str = Field(..., description="Type of analysis performed")
    query_intent: str = Field(..., description="Detected query intent")


class DashboardRequest(BaseModel):
    """Request model for full dashboard"""
    birth_data: BirthData = Field(..., description="Birth data")


class DashboardResponse(BaseModel):
    """Response model for dashboard"""
    houses: List[Dict] = Field(..., description="Analysis for each house (1-12)")
    overall_summary: str = Field(..., description="Overall chart summary")
    bav_sav_data: Optional[Dict] = Field(None, description="BAV/SAV data")
    dasha_data: Optional[Dict] = Field(None, description="Dasha data")
    gochara_data: Optional[Dict] = Field(None, description="Gochara data")


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    version: str
    agent_available: bool


class ChatStartRequest(BaseModel):
    """Request to start a chat session"""
    birth_data: BirthData


class ChatStartResponse(BaseModel):
    """Response when starting a chat session"""
    session_id: str
    message: str
    suggestions: List[str] = Field(default_factory=list)


class ChatMessageRequest(BaseModel):
    """Request to send a chat message"""
    session_id: str
    message: str


class ChatMessageResponse(BaseModel):
    """Response to a chat message"""
    response: str
    citations: List[str] = Field(default_factory=list)
    suggestions: List[str] = Field(default_factory=list)
    chart_data: Optional[Dict] = None


# ============================================================================
# API ENDPOINTS
# ============================================================================

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "version": "1.0.0",
        "agent_available": True
    }


@app.get("/api/config")
async def get_config():
    """Get frontend configuration including API URLs"""
    return {
        "dasha_gochara_api_url": os.getenv("DASHA_GOCHARA_API_URL", "http://localhost:8001"),
        "bav_sav_api_url": os.getenv("BAV_SAV_API_URL", "http://localhost:8000")
    }


@app.get("/chat", response_class=HTMLResponse)
async def chat_interface():
    """Serve the interactive chat interface"""
    chat_template_path = os.path.join(os.path.dirname(__file__), "templates", "chat.html")
    if os.path.exists(chat_template_path):
        with open(chat_template_path, "r", encoding="utf-8") as f:
            return f.read()
    else:
        return HTMLResponse(content="<h1>Chat interface not found</h1>", status_code=404)


@app.get("/", response_class=HTMLResponse)
async def root():
    """Root endpoint - serve dashboard interface"""
    # Read dashboard.html template
    template_path = os.path.join(os.path.dirname(__file__), "templates", "dashboard.html")
    if os.path.exists(template_path):
        with open(template_path, "r", encoding="utf-8") as f:
            return f.read()
    
    # Fallback simple HTML with links to chat and dashboard
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Vedic Astrology AI Agent</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body { 
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; 
                max-width: 1200px; 
                margin: 0 auto; 
                padding: 40px 20px; 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
            }
            .container { 
                background: white; 
                padding: 40px; 
                border-radius: 15px; 
                box-shadow: 0 10px 40px rgba(0,0,0,0.2);
                text-align: center;
            }
            h1 { color: #333; margin-bottom: 10px; }
            p { color: #666; margin-bottom: 30px; }
            .options {
                display: flex;
                gap: 20px;
                justify-content: center;
                flex-wrap: wrap;
            }
            .option-card {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 30px;
                border-radius: 12px;
                text-decoration: none;
                min-width: 250px;
                transition: transform 0.2s;
            }
            .option-card:hover {
                transform: translateY(-5px);
            }
            .option-card h2 {
                margin-bottom: 10px;
            }
            .option-card p {
                color: rgba(255,255,255,0.9);
                margin: 0;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🕉️ Vedic Astrology AI Agent</h1>
            <p>Choose your preferred interface:</p>
            <div class="options">
                <a href="/chat" class="option-card">
                    <h2>💬 Interactive Chat</h2>
                    <p>ChatGPT-style conversational interface. Ask questions naturally and get intelligent responses.</p>
                </a>
                <a href="/" class="option-card" onclick="event.preventDefault(); window.location.reload();">
                    <h2>📊 Dashboard View</h2>
                    <p>Comprehensive dashboard with all houses, BAV/SAV charts, and detailed analysis.</p>
                </a>
            </div>
        </div>
    </body>
    </html>
    """
    return html_content


# ============================================================================
# AGENT ENDPOINTS
# ============================================================================

@app.post("/api/agent/query", response_model=QueryResponse)
async def query_agent(request: QueryRequest):
    """
    Main agent endpoint - agent decides what to do based on query.
    
    The agent will:
    1. Analyze query intent
    2. Decide which APIs to call (BAV/SAV, Dasha, Gochara)
    3. Retrieve relevant knowledge from RAG
    4. Generate comprehensive interpretation
    """
    try:
        # Prepare initial state
        initial_state = {
            "user_query": request.query,
            "birth_data": request.birth_data.dict() if request.birth_data else None,
            "query_intent": "",
            "selected_houses": [],
            "bav_sav_data": None,
            "dasha_data": None,
            "gochara_data": None,
            "rag_context": [],
            "current_step": "",
            "intermediate_results": {},
            "final_response": None,
            "citations": [],
            "needs_more_context": False
        }
        
        # Run agent graph
        result = agent_graph.invoke(initial_state)
        
        return QueryResponse(
            response=result.get("final_response", "I apologize, but I couldn't generate a response."),
            chart_data={
                "bav_sav": result.get("bav_sav_data"),
                "dasha": result.get("dasha_data"),
                "gochara": result.get("gochara_data")
            } if result.get("bav_sav_data") or result.get("dasha_data") or result.get("gochara_data") else None,
            citations=result.get("citations", []),
            analysis_type=result.get("query_intent", "general"),
            query_intent=result.get("query_intent", "general")
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent error: {str(e)}")


@app.post("/api/agent/dashboard", response_model=DashboardResponse)
async def get_dashboard(request: DashboardRequest):
    """
    Get complete dashboard data for all 12 houses.
    
    The agent will analyze all houses and provide comprehensive interpretations.
    """
    try:
        # Prepare state for full dashboard
        initial_state = {
            "user_query": "Analyze all houses with complete interpretations combining BAV/SAV, Dasha, and Gochara data",
            "birth_data": request.birth_data.dict(),
            "query_intent": "full_dashboard",
            "selected_houses": list(range(1, 13)),
            "bav_sav_data": None,
            "dasha_data": None,
            "gochara_data": None,
            "rag_context": [],
            "current_step": "",
            "intermediate_results": {},
            "final_response": None,
            "citations": [],
            "needs_more_context": False
        }
        
        # Run agent graph
        result = agent_graph.invoke(initial_state)
        
        # Process results for dashboard
        bav_sav_data = result.get("bav_sav_data")
        dasha_data = result.get("dasha_data")
        gochara_data = result.get("gochara_data")
        
        # Generate house-by-house analysis with fast rule-based interpretations
        houses = []
        
        print(f"📊 Generating dashboard for 12 houses...")
        print(f"   BAV/SAV data: {'✅' if bav_sav_data else '❌'}")
        print(f"   Dasha data: {'✅' if dasha_data else '❌'}")
        print(f"   Gochara data: {'✅' if gochara_data else '❌'}")
        
        # House significations for interpretations
        house_significations = {
            1: "Self, personality, physical appearance, and overall life direction",
            2: "Wealth, family, speech, and material possessions",
            3: "Siblings, courage, communication, and short journeys",
            4: "Home, mother, property, and emotional foundation",
            5: "Children, education, creativity, and intelligence",
            6: "Health, enemies, service, and daily routines",
            7: "Marriage, partnerships, spouse, and business relationships",
            8: "Longevity, transformation, obstacles, and hidden matters",
            9: "Fortune, father, spirituality, and higher learning",
            10: "Career, reputation, authority, and public image",
            11: "Gains, income, friends, and aspirations",
            12: "Losses, expenses, foreign lands, and spiritual liberation"
        }
        
        for house_num in range(1, 13):
            print(f"   Processing House {house_num}/12...", end=" ", flush=True)
            
            # Get SAV points for this house
            sav_points = None
            if bav_sav_data and "sav_chart" in bav_sav_data and len(bav_sav_data["sav_chart"]) >= house_num:
                sav_points = bav_sav_data["sav_chart"][house_num - 1]
            
            # Get BAV contributions for this house
            bav_contributions = {}
            if bav_sav_data and "bav_charts" in bav_sav_data:
                for planet, chart in bav_sav_data["bav_charts"].items():
                    if isinstance(chart, list) and len(chart) >= house_num:
                        planet_display = planet.title() if planet != "ASCENDANT" else "Ascendant"
                        bav_contributions[planet_display] = chart[house_num - 1]
            
            # Generate fast interpretation based on SAV points and rules (no OpenAI call)
            interpretation = None
            try:
                if sav_points is not None:
                    strength = "Strong" if sav_points >= 30 else "Good" if sav_points >= 28 else "Weak" if sav_points < 22 else "Moderate"
                    strength_desc = "excellent" if sav_points >= 30 else "good" if sav_points >= 28 else "challenging" if sav_points < 22 else "moderate"
                    
                    interpretation = f"House {house_num} ({house_significations.get(house_num, 'General matters')}) has {sav_points} SAV points, indicating {strength_desc} strength. "
                    
                    # Add BAV contributions
                    if bav_contributions:
                        top_contributors = sorted(bav_contributions.items(), key=lambda x: x[1], reverse=True)[:3]
                        interpretation += f"Key planetary influences: {', '.join([f'{p} ({v} points)' for p, v in top_contributors])}. "
                    
                    # Add strength-based guidance
                    if sav_points >= 30:
                        interpretation += "This house is very strong and will yield positive results. Transits and Dasha periods affecting this house will be highly beneficial."
                    elif sav_points >= 28:
                        interpretation += "This house has good strength and will generally yield positive results, though some challenges may arise."
                    elif sav_points < 22:
                        interpretation += "This house has lower strength and may present challenges. Careful attention and remedies may be beneficial."
                    else:
                        interpretation += "This house has moderate strength and will yield mixed results depending on transits and Dasha periods."
                    
                    # Add Dasha context if available
                    if dasha_data and dasha_data.get("current_dasa"):
                        interpretation += f" Current Dasha: {dasha_data.get('current_dasa')} with {dasha_data.get('current_bhukti', 'N/A')} Bhukti."
                else:
                    interpretation = f"House {house_num} ({house_significations.get(house_num, 'General matters')}) analysis based on SAV, Dasha, and Gochara data."
                
                print(f"✅", flush=True)
                    
            except Exception as e:
                print(f"❌ Error: {str(e)[:50]}", flush=True)
                interpretation = f"House {house_num} analysis based on SAV, Dasha, and Gochara data."
            
            house_data = {
                "house_number": house_num,
                "sav_points": sav_points,
                "bav_contributions": bav_contributions,
                "interpretation": interpretation
            }
            houses.append(house_data)
        
        return DashboardResponse(
            houses=houses,
            overall_summary=result.get("final_response", "Dashboard analysis completed"),
            bav_sav_data=bav_sav_data,
            dasha_data=dasha_data,
            gochara_data=gochara_data
        )
        
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print(f"❌ Dashboard error: {e}")
        print(f"Traceback: {error_trace}")
        raise HTTPException(status_code=500, detail=f"Dashboard error: {str(e)}")


# ============================================================================
# CHAT ENDPOINTS
# ============================================================================

@app.post("/api/chat/start", response_model=ChatStartResponse)
async def start_chat(request: ChatStartRequest):
    """
    Start a new chat conversation session.
    
    This initializes the session, stores birth data, and optionally
    pre-calculates chart data for faster responses.
    """
    try:
        # Start conversation
        session_id = conversation_manager.start_conversation(request.birth_data.dict())
        
        # Generate welcome message and suggestions
        welcome_message = f"Hello! I've initialized your astrological analysis. " \
                         f"What would you like to know about your chart?"
        
        suggestions = [
            "What's my 7th house like?",
            "Tell me about my career (10th house)",
            "What Dasha am I in?",
            "What are my current transits?",
            "Which houses are strongest?"
        ]
        
        return ChatStartResponse(
            session_id=session_id,
            message=welcome_message,
            suggestions=suggestions
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to start chat: {str(e)}")


@app.post("/api/chat/message", response_model=ChatMessageResponse)
async def send_chat_message(request: ChatMessageRequest):
    """
    Send a message in an active chat session.
    
    The agent will:
    1. Analyze the question
    2. Use cached chart data if available
    3. Call APIs if needed
    4. Retrieve RAG context
    5. Generate intelligent response
    """
    try:
        result = conversation_manager.process_message(
            request.session_id,
            request.message
        )
        
        return ChatMessageResponse(
            response=result["response"],
            citations=result.get("citations", []),
            suggestions=result.get("suggestions", []),
            chart_data=result.get("chart_data")
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process message: {str(e)}")


@app.get("/api/chat/history/{session_id}")
async def get_chat_history(session_id: str):
    """Get conversation history for a session"""
    try:
        conversation = conversation_manager.get_conversation(session_id)
        if not conversation:
            raise HTTPException(status_code=404, detail="Session not found")
        
        return {
            "session_id": session_id,
            "messages": conversation["messages"],
            "birth_data": conversation["birth_data"],
            "created_at": conversation["created_at"],
            "last_activity": conversation["last_activity"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get history: {str(e)}")


@app.post("/api/chat/reset/{session_id}")
async def reset_chat(session_id: str):
    """Reset conversation history but keep birth data and chart cache"""
    try:
        conversation_manager.reset_conversation(session_id)
        return {"message": "Conversation reset successfully", "session_id": session_id}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to reset chat: {str(e)}")


if __name__ == "__main__":
    # Railway sets PORT automatically, but we read it from environment
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)

