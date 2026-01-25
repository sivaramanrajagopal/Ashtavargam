# Context Window Management for Chat Sessions

## Problem
As conversations get longer, the context window grows, leading to:
- Higher API costs
- Slower responses
- Token limit errors
- Poor performance

## Solution: Implement Context Window Management

### Current Implementation
The conversation manager stores all messages without limits. We need to add:
1. **Message count limits**
2. **Token-based truncation**
3. **Summary-based context compression**
4. **Smart message pruning**

---

## Implementation Options

### Option 1: Message Count Limit (Simple)
Limit the number of messages kept in context.

**Pros**: Simple, fast
**Cons**: May lose important early context

### Option 2: Token-Based Truncation (Recommended)
Keep messages until token limit is reached, then truncate oldest.

**Pros**: More precise, respects token limits
**Cons**: Requires token counting

### Option 3: Summary Compression (Advanced)
Summarize old messages when context gets too long.

**Pros**: Preserves context, reduces tokens
**Cons**: More complex, requires additional API calls

### Option 4: Hybrid Approach (Best)
Combine message limits + token limits + smart pruning.

**Pros**: Best of all worlds
**Cons**: Most complex

---

## Recommended Implementation: Hybrid Approach

### Step 1: Update Conversation Manager

Add to `agent_app/conversation/manager.py`:

```python
import tiktoken
from typing import List, Dict

class ConversationManager:
    def __init__(self):
        # ... existing code ...
        self.max_messages = 50  # Hard limit on messages
        self.max_tokens = 8000  # Token limit (leave room for response)
        self.encoding = tiktoken.encoding_for_model("gpt-4")  # or gpt-3.5-turbo
    
    def _count_tokens(self, text: str) -> int:
        """Count tokens in text"""
        return len(self.encoding.encode(text))
    
    def _truncate_messages(self, messages: List[Dict]) -> List[Dict]:
        """Truncate messages to fit token limit"""
        total_tokens = 0
        truncated = []
        
        # Always keep system message and last few messages
        system_msg = messages[0] if messages and messages[0].get('role') == 'system' else None
        recent_messages = messages[-10:]  # Keep last 10 messages
        
        # Count tokens in recent messages
        for msg in recent_messages:
            content = msg.get('content', '')
            tokens = self._count_tokens(content)
            if total_tokens + tokens > self.max_tokens:
                break
            total_tokens += tokens
            truncated.append(msg)
        
        # Add system message at start
        if system_msg:
            truncated.insert(0, system_msg)
        
        return truncated
    
    def add_message(self, role: str, content: str, session_id: str):
        """Add message with automatic truncation"""
        # Add message normally
        if session_id not in self.sessions:
            self.sessions[session_id] = {
                'messages': [],
                'chart_data': {},
                'context': {}
            }
        
        self.sessions[session_id]['messages'].append({
            'role': role,
            'content': content,
            'timestamp': datetime.now().isoformat()
        })
        
        # Truncate if needed
        messages = self.sessions[session_id]['messages']
        if len(messages) > self.max_messages:
            # Keep system message + recent messages
            system_msg = messages[0] if messages[0].get('role') == 'system' else None
            recent = messages[-self.max_messages+1:]  # Keep last N-1 messages
            self.sessions[session_id]['messages'] = ([system_msg] + recent) if system_msg else recent
        
        # Also truncate by tokens
        self.sessions[session_id]['messages'] = self._truncate_messages(
            self.sessions[session_id]['messages']
        )
    
    def get_messages(self, session_id: str) -> List[Dict]:
        """Get messages with automatic truncation"""
        if session_id not in self.sessions:
            return []
        
        messages = self.sessions[session_id]['messages']
        
        # Apply truncation
        messages = self._truncate_messages(messages)
        
        return messages
```

### Step 2: Add Configuration

Add to `agent_app/main.py` or environment variables:

```python
# In main.py
MAX_MESSAGES = int(os.getenv("MAX_MESSAGES", "50"))
MAX_TOKENS = int(os.getenv("MAX_TOKENS", "8000"))
```

### Step 3: Update Requirements

Add to `requirements_agent.txt`:
```
tiktoken>=0.5.0
```

---

## Alternative: Summary-Based Compression

For more advanced context management, summarize old messages:

```python
def _summarize_old_messages(self, old_messages: List[Dict]) -> str:
    """Summarize old messages to preserve context"""
    if not old_messages:
        return ""
    
    # Combine old messages
    combined = "\n".join([
        f"{msg['role']}: {msg['content']}" 
        for msg in old_messages
    ])
    
    # Create summary prompt
    summary_prompt = f"""Summarize the following conversation history in 2-3 sentences, focusing on key points and context:

{combined}

Summary:"""
    
    # Call OpenAI to summarize (or use cheaper model)
    # This is optional - can skip if cost is concern
    return combined[:500]  # Simple truncation fallback
```

---

## Implementation Steps

### Quick Fix (Immediate)
1. Add message count limit (50 messages)
2. Keep last N messages when limit reached
3. Always preserve system message

### Better Fix (Recommended)
1. Install `tiktoken`
2. Add token counting
3. Implement smart truncation
4. Keep recent messages + system message

### Best Fix (Advanced)
1. Implement summary compression
2. Use sliding window approach
3. Preserve important context markers
4. Add user option to "clear old context"

---

## User-Facing Features

### 1. "New Chat" Button
Already implemented - clears all context and starts fresh.

### 2. "Clear Context" Button (Optional)
Add button to clear old messages but keep current session:
```javascript
function clearOldContext() {
    // Keep last 5 messages, clear rest
    fetch(`${API_BASE}/api/chat/clear-context/${sessionId}`, {
        method: 'POST'
    });
}
```

### 3. Context Indicator
Show user how many messages/tokens in context:
```html
<div class="context-info">
    Messages: <span id="messageCount">0</span> / 50
    Tokens: <span id="tokenCount">0</span> / 8000
</div>
```

---

## Testing

### Test 1: Message Limit
1. Send 60 messages
2. Verify only last 50 are kept
3. Verify system message is preserved

### Test 2: Token Limit
1. Send very long messages
2. Verify truncation happens
3. Verify recent messages are preserved

### Test 3: Performance
1. Monitor API response times
2. Check token usage
3. Verify no errors

---

## Monitoring

Add logging to track:
- Average tokens per conversation
- Truncation frequency
- User complaints about lost context

---

## Recommendations

1. **Start with message limit** (50 messages)
2. **Add token counting** if issues persist
3. **Implement summary compression** only if needed
4. **Give users control** with "New Chat" and "Clear Context" buttons

---

## Code Changes Required

1. ✅ Update `agent_app/conversation/manager.py` - Add truncation logic
2. ✅ Update `requirements_agent.txt` - Add tiktoken
3. ✅ Update `agent_app/main.py` - Add configuration
4. ✅ Update `agent_app/templates/chat.html` - Add context indicator (optional)

---

## Example Usage

```python
# In conversation manager
manager = ConversationManager()

# Add messages (automatic truncation)
manager.add_message("user", "Hello", session_id)
manager.add_message("assistant", "Hi! How can I help?", session_id)

# Get messages (already truncated)
messages = manager.get_messages(session_id)
# Returns: Last 50 messages or messages within token limit
```

---

## Next Steps

1. Implement message count limit (quick fix)
2. Test with long conversations
3. Add token counting if needed
4. Monitor and adjust limits based on usage

