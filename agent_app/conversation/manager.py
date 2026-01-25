"""
Conversation Manager for Interactive Chat Interface
Manages conversation state, chart data caching, and message history
"""

import uuid
from typing import Dict, List, Optional
from datetime import datetime
from agent_app.graphs.astrology_agent_graph import agent_graph


class ConversationManager:
    """Manages conversation sessions and state"""
    
    def __init__(self):
        # In-memory storage (in production, use Redis or database)
        self.sessions: Dict[str, Dict] = {}
    
    def start_conversation(self, birth_data: Dict) -> str:
        """
        Initialize a new conversation session
        
        Args:
            birth_data: Birth details (dob, tob, latitude, longitude, tz_offset, etc.)
        
        Returns:
            session_id: Unique session identifier
        """
        session_id = str(uuid.uuid4())
        
        # Normalize birth_data format
        normalized_birth_data = {
            "dob": birth_data.get("dob"),
            "tob": birth_data.get("tob"),
            "latitude": birth_data.get("latitude") or birth_data.get("lat"),
            "longitude": birth_data.get("longitude") or birth_data.get("lon"),
            "tz_offset": birth_data.get("tz_offset"),
            "name": birth_data.get("name"),
            "place": birth_data.get("place")
        }
        
        # Initialize session
        self.sessions[session_id] = {
            "session_id": session_id,
            "birth_data": normalized_birth_data,
            "messages": [],
            "chart_cache": {
                "bav_sav_data": None,
                "dasha_data": None,
                "gochara_data": None,
                "cached_at": None
            },
            "context": {
                "discussed_houses": [],
                "discussed_topics": [],
                "user_interests": []
            },
            "created_at": datetime.now().isoformat(),
            "last_activity": datetime.now().isoformat()
        }
        
        return session_id
    
    def add_message(self, session_id: str, role: str, content: str, metadata: Optional[Dict] = None) -> None:
        """
        Add a message to conversation history
        
        Args:
            session_id: Session identifier
            role: 'user' or 'assistant'
            content: Message content
            metadata: Optional metadata (citations, chart_data, etc.)
        """
        if session_id not in self.sessions:
            raise ValueError(f"Session {session_id} not found")
        
        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat(),
            "metadata": metadata or {}
        }
        
        self.sessions[session_id]["messages"].append(message)
        self.sessions[session_id]["last_activity"] = datetime.now().isoformat()
    
    def get_conversation(self, session_id: str) -> Optional[Dict]:
        """Get full conversation state"""
        return self.sessions.get(session_id)
    
    def get_messages(self, session_id: str) -> List[Dict]:
        """Get conversation messages"""
        if session_id not in self.sessions:
            return []
        return self.sessions[session_id]["messages"]
    
    def update_chart_cache(self, session_id: str, chart_data: Dict) -> None:
        """
        Update cached chart data
        
        Args:
            session_id: Session identifier
            chart_data: Dictionary with bav_sav_data, dasha_data, gochara_data
        """
        if session_id not in self.sessions:
            raise ValueError(f"Session {session_id} not found")
        
        self.sessions[session_id]["chart_cache"].update({
            "bav_sav_data": chart_data.get("bav_sav_data"),
            "dasha_data": chart_data.get("dasha_data"),
            "gochara_data": chart_data.get("gochara_data"),
            "cached_at": datetime.now().isoformat()
        })
    
    def get_chart_cache(self, session_id: str) -> Dict:
        """Get cached chart data"""
        if session_id not in self.sessions:
            return {}
        return self.sessions[session_id]["chart_cache"]
    
    def update_context(self, session_id: str, context_updates: Dict) -> None:
        """Update conversation context"""
        if session_id not in self.sessions:
            raise ValueError(f"Session {session_id} not found")
        
        self.sessions[session_id]["context"].update(context_updates)
    
    def get_context(self, session_id: str) -> Dict:
        """Get conversation context"""
        if session_id not in self.sessions:
            return {}
        return self.sessions[session_id]["context"]
    
    def reset_conversation(self, session_id: str) -> None:
        """Reset conversation but keep birth data and chart cache"""
        if session_id not in self.sessions:
            raise ValueError(f"Session {session_id} not found")
        
        birth_data = self.sessions[session_id]["birth_data"]
        chart_cache = self.sessions[session_id]["chart_cache"]
        
        self.sessions[session_id] = {
            "session_id": session_id,
            "birth_data": birth_data,
            "messages": [],
            "chart_cache": chart_cache,
            "context": {
                "discussed_houses": [],
                "discussed_topics": [],
                "user_interests": []
            },
            "created_at": self.sessions[session_id]["created_at"],
            "last_activity": datetime.now().isoformat()
        }
    
    def process_message(self, session_id: str, user_message: str) -> Dict:
        """
        Process user message through agent and return response
        
        Args:
            session_id: Session identifier
            user_message: User's question/message
        
        Returns:
            Dictionary with response, citations, chart_data, etc.
        """
        if session_id not in self.sessions:
            raise ValueError(f"Session {session_id} not found")
        
        session = self.sessions[session_id]
        birth_data = session["birth_data"]
        chart_cache = session["chart_cache"]
        context = session["context"]
        previous_messages = session["messages"]
        
        # Add user message to history
        self.add_message(session_id, "user", user_message)
        
        # Prepare agent state with conversation context
        # Include recent messages for context
        recent_messages = previous_messages[-5:] if len(previous_messages) > 5 else previous_messages
        conversation_context = "\n".join([
            f"{msg['role']}: {msg['content']}" 
            for msg in recent_messages
        ])
        
        # Build query with conversation context
        enhanced_query = user_message
        if conversation_context:
            enhanced_query = f"Previous conversation:\n{conversation_context}\n\nCurrent question: {user_message}"
        
        # Prepare initial state for agent
        initial_state = {
            "user_query": enhanced_query,
            "birth_data": birth_data,
            "query_intent": "",
            "selected_houses": context.get("discussed_houses", []),
            "bav_sav_data": chart_cache.get("bav_sav_data"),
            "dasha_data": chart_cache.get("dasha_data"),
            "gochara_data": chart_cache.get("gochara_data"),
            "rag_context": [],
            "current_step": "",
            "intermediate_results": {},
            "final_response": None,
            "citations": [],
            "needs_more_context": False
        }
        
        # Run agent graph
        result = agent_graph.invoke(initial_state)
        
        # Update chart cache if new data was retrieved
        if result.get("bav_sav_data") or result.get("dasha_data") or result.get("gochara_data"):
            self.update_chart_cache(session_id, {
                "bav_sav_data": result.get("bav_sav_data"),
                "dasha_data": result.get("dasha_data"),
                "gochara_data": result.get("gochara_data")
            })
        
        # Extract response
        response = result.get("final_response", "I apologize, but I couldn't generate a response.")
        citations = result.get("citations", [])
        
        # Update context based on query
        # Extract discussed houses/topics from response
        discussed_houses = self._extract_houses(user_message, response)
        discussed_topics = self._extract_topics(user_message)
        
        if discussed_houses:
            context["discussed_houses"] = list(set(context.get("discussed_houses", []) + discussed_houses))
        if discussed_topics:
            context["discussed_topics"] = list(set(context.get("discussed_topics", []) + discussed_topics))
        
        self.update_context(session_id, context)
        
        # Add assistant response to history
        self.add_message(session_id, "assistant", response, {
            "citations": citations,
            "chart_data": {
                "bav_sav": result.get("bav_sav_data"),
                "dasha": result.get("dasha_data"),
                "gochara": result.get("gochara_data")
            }
        })
        
        return {
            "response": response,
            "citations": citations,
            "chart_data": {
                "bav_sav": result.get("bav_sav_data"),
                "dasha": result.get("dasha_data"),
                "gochara": result.get("gochara_data")
            },
            "suggestions": self._generate_suggestions(context, result)
        }
    
    def _extract_houses(self, query: str, response: str) -> List[int]:
        """Extract house numbers mentioned in query/response"""
        houses = []
        query_lower = query.lower()
        response_lower = response.lower()
        
        house_patterns = {
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
        
        for pattern, house_num in house_patterns.items():
            if pattern in query_lower or pattern in response_lower:
                houses.append(house_num)
        
        return houses
    
    def _extract_topics(self, query: str) -> List[str]:
        """Extract topics from query"""
        topics = []
        query_lower = query.lower()
        
        topic_keywords = {
            "marriage": "marriage",
            "career": "career",
            "health": "health",
            "wealth": "wealth",
            "education": "education",
            "children": "children",
            "dasha": "dasha",
            "transit": "transit",
            "gochara": "gochara"
        }
        
        for keyword, topic in topic_keywords.items():
            if keyword in query_lower:
                topics.append(topic)
        
        return topics
    
    def _generate_suggestions(self, context: Dict, result: Dict) -> List[str]:
        """Generate follow-up question suggestions"""
        suggestions = []
        
        # Based on discussed houses
        discussed_houses = context.get("discussed_houses", [])
        if discussed_houses:
            for house in discussed_houses[:3]:
                if house == 7:
                    suggestions.append("When will I get married?")
                elif house == 10:
                    suggestions.append("What career path is best for me?")
                elif house == 6:
                    suggestions.append("Tell me about my health")
        
        # General suggestions
        if not suggestions:
            suggestions = [
                "What's my 7th house like?",
                "Tell me about my career (10th house)",
                "What Dasha am I in?",
                "What are my current transits?",
                "Which houses are strongest?"
            ]
        
        return suggestions[:5]  # Limit to 5 suggestions


# Global conversation manager instance
conversation_manager = ConversationManager()

