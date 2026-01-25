# 🕉️ Vedic Astrology AI Agent - User Guide

## What This App Does

This is an **AI-powered Vedic Astrology analysis tool** that combines:
- **Ashtakavarga Calculations** (BAV/SAV) - House strength analysis
- **Dasha/Bhukti** - Planetary period predictions
- **Gochara (Transits)** - Current planetary influences
- **RAG (Retrieval-Augmented Generation)** - AI interpretations using Vedic knowledge base
- **Interactive Chat** - ChatGPT-style conversational interface

The app analyzes your birth chart and provides intelligent, personalized astrological insights.

---

## Quick Start

### 1. Start All Servers

You need to run **4 servers** for the full functionality:

```bash
cd /Users/sivaramanrajagopal/Ashtavargam

# Option 1: Use the startup script
./start_all_servers.sh

# Option 2: Start manually
# Terminal 1 - BAV/SAV API (Port 8000)
python3 -m uvicorn api_server:app --host 0.0.0.0 --port 8000

# Terminal 2 - Dasha/Gochara API (Port 8001)
python3 -m uvicorn dasha_gochara_api:app --host 0.0.0.0 --port 8001

# Terminal 3 - Agent Server (Port 8080)
export PYTHONPATH=/Users/sivaramanrajagopal/Ashtavargam:$PYTHONPATH
python3 -m uvicorn agent_app.main:app --host 0.0.0.0 --port 8080 --reload

# Terminal 4 - Flask App (Port 5004) - Optional, for traditional interface
python3 app_complete.py
```

### 2. Verify Servers Are Running

Check all servers:
```bash
curl http://localhost:8000/health  # BAV/SAV API
curl http://localhost:8001/health  # Dasha/Gochara API
curl http://localhost:8080/health  # Agent Server
curl http://localhost:5004/         # Flask App
```

---

## Two Ways to Use the App

### Option 1: Interactive Chat Interface (Recommended) 🎯

**Best for**: Natural conversation, asking questions, getting personalized insights

#### Access:
- **URL**: `http://localhost:8080/chat`
- **Or**: Go to `http://localhost:8080` and click "Interactive Chat"

#### How to Use:

1. **Enter Birth Details**
   - Date of Birth (YYYY-MM-DD)
   - Time of Birth (HH:MM, 24-hour format)
   - Latitude & Longitude (e.g., Chennai: 13.0827, 80.2707)
   - Timezone Offset (e.g., IST: 5.5)
   - Name & Place (optional)

2. **Click "Start Chat"**
   - App calculates your chart
   - Welcome message appears
   - Suggested questions shown

3. **Ask Questions Naturally**
   Examples:
   - "What's my 7th house like?"
   - "When will I get married?"
   - "Tell me about my career"
   - "What Dasha am I in?"
   - "What are my current transits?"
   - "Which houses are strongest?"

4. **Continue Conversation**
   - Agent remembers previous questions
   - Follow-up suggestions guide you
   - Ask follow-up questions based on responses

#### Example Conversation:

```
You: "What's my 7th house like?"

AI: "Your 7th house has 28 SAV points, indicating good strength for 
     partnerships and marriage. The house shows potential for stable 
     relationships, though some challenges may arise. Your current 
     Dasha is Moon-Mercury, which is favorable for relationships..."
     
     [Suggestions: "When will I get married?", "Tell me about my spouse"]

You: "When will I get married?"

AI: "Based on your current Dasha (Moon-Mercury) and 7th house analysis,
     the favorable period for marriage would be during Jupiter's transit
     over your 7th house, which occurs in [specific timeframe]..."
```

#### Features:
- ✅ ChatGPT-style interface
- ✅ Context-aware (remembers previous questions)
- ✅ Chart data cached (faster responses)
- ✅ Follow-up suggestions
- ✅ Citations for sources
- ✅ Natural language questions

---

### Option 2: Dashboard Interface 📊

**Best for**: Comprehensive overview, all houses at once, detailed analysis

#### Access:
- **URL**: `http://localhost:8080`** (click "Dashboard View")
- **Or**: `http://localhost:5004` (traditional Flask interface)

#### How to Use:

1. **Enter Birth Details** (same as chat)

2. **Click "Get Full Dashboard"**
   - App calculates all chart data
   - Generates interpretations for all 12 houses
   - Shows BAV/SAV, Dasha, Gochara data

3. **Navigate Tabs**
   - **Overview**: Summary of chart
   - **House 1-12**: Individual house analysis
   - Each house shows:
     - SAV points
     - BAV contributions
     - Dasha analysis
     - Gochara (transit) analysis
     - AI interpretation

#### Features:
- ✅ Complete chart overview
- ✅ All 12 houses analyzed
- ✅ Visual BAV/SAV charts
- ✅ Detailed interpretations
- ✅ Tabbed navigation

---

## What Each Component Does

### 1. **BAV/SAV (Ashtakavarga)**
- **BAV (Bhinnashtakavarga)**: Individual planetary strength charts
- **SAV (Sarvashtakavarga)**: Combined house strength
- **Purpose**: Determines which houses are strong/weak
- **Interpretation**: 
  - ≥30 points = Strong
  - ≥28 points = Good
  - <22 points = Weak

### 2. **Dasha/Bhukti**
- **Dasha**: Major planetary period (e.g., Moon Dasha)
- **Bhukti**: Sub-period within Dasha (e.g., Mercury Bhukti)
- **Purpose**: Predicts timing of events
- **Use**: "When will X happen?" questions

### 3. **Gochara (Transits)**
- **Definition**: Current planetary positions relative to birth chart
- **Purpose**: Shows current influences
- **Use**: "What's happening now?" questions

### 4. **RAG (AI Knowledge Base)**
- **Definition**: Retrieval-Augmented Generation
- **Purpose**: Provides accurate Vedic astrology interpretations
- **Source**: Supabase knowledge base with 59+ advanced rules
- **Use**: All AI responses use this for accuracy

---

## Example Questions You Can Ask

### House-Specific Questions
- "What's my 7th house like?"
- "Tell me about my 10th house (career)"
- "How is my 6th house (health)?"
- "What does my 1st house say about me?"

### Timing Questions
- "When will I get married?"
- "When will my career peak?"
- "What Dasha am I in?"
- "When will I have children?"

### General Questions
- "Which houses are strongest?"
- "What are my current transits?"
- "Tell me about my chart"
- "What should I focus on?"

### Follow-up Questions
- "Tell me more about that"
- "What about my spouse?"
- "How does this affect my career?"
- "What remedies can help?"

---

## Understanding the Responses

### Response Structure:
1. **Direct Answer**: Answers your question
2. **Chart Data**: References specific SAV points, Dasha, etc.
3. **Interpretation**: Explains what it means
4. **Citations**: Sources from knowledge base
5. **Suggestions**: Follow-up questions

### Key Terms:
- **SAV Points**: House strength (higher = stronger)
- **BAV Contributions**: Individual planet's influence on a house
- **Dasha**: Current major planetary period
- **Bhukti**: Current sub-period
- **Transit**: Current planetary position
- **RAG Status**: Transit health indicator (Green/Amber/Red)

---

## Tips for Best Results

1. **Be Specific**: 
   - ✅ "What's my 7th house like?"
   - ❌ "Tell me about marriage" (less specific)

2. **Use Follow-up Questions**:
   - Start broad, then go deeper
   - Use suggested questions as guides

3. **Check Citations**:
   - Responses cite sources
   - Based on traditional Vedic principles

4. **Context Matters**:
   - Agent remembers previous questions
   - Build on previous answers

5. **Multiple Sessions**:
   - Each session is independent
   - Can start new chat anytime

---

## Troubleshooting

### Server Not Starting?
```bash
# Check if ports are in use
lsof -i :8000
lsof -i :8001
lsof -i :8080

# Kill existing processes
pkill -f "uvicorn"
pkill -f "python.*app_complete"
```

### API Errors?
- Ensure all 4 servers are running
- Check server logs for errors
- Verify environment variables (.env file)

### Chat Not Working?
- Check browser console (F12)
- Verify session_id is set
- Check network tab for API calls

### Slow Responses?
- First question: 10-20 seconds (calculates chart)
- Follow-up questions: 3-5 seconds (uses cache)
- Dashboard: 15-25 seconds (generates all houses)

---

## API Endpoints (For Developers)

### Chat Endpoints:
- `POST /api/chat/start` - Start conversation
- `POST /api/chat/message` - Send message
- `GET /api/chat/history/{session_id}` - Get history
- `POST /api/chat/reset/{session_id}` - Reset chat

### Agent Endpoints:
- `POST /api/agent/query` - Single query
- `POST /api/agent/dashboard` - Full dashboard

### Health Checks:
- `GET /health` - Server health
- `GET /docs` - API documentation

---

## Next Steps

1. **Start the servers** (see Quick Start above)
2. **Open chat interface**: `http://localhost:8080/chat`
3. **Enter your birth details**
4. **Start asking questions!**

---

## Support

- **Documentation**: See `INTERACTIVE_CHAT_DESIGN.md` and `CHAT_IMPLEMENTATION_SUMMARY.md`
- **API Docs**: `http://localhost:8080/docs`
- **Logs**: Check terminal output for debugging

---

**Enjoy exploring your astrological chart! 🕉️**

