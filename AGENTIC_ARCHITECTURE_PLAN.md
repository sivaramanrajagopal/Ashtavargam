# Agentic Architecture Plan - Vedic Astrology AI Agent

## Current Issues Identified

### 1. **BAV/SAV Not Working in Agent Queries**
- Problem: API calls failing due to data format mismatches
- Impact: Agent can't provide accurate BAV/SAV analysis
- Root Cause: `lat`/`lon` vs `latitude`/`longitude` format inconsistency

### 2. **RAG Not Used for Dashboard Houses**
- Problem: Dashboard uses rule-based interpretations instead of RAG+AI
- Impact: Less intelligent, less personalized interpretations
- Root Cause: Performance optimization removed RAG calls

### 3. **Agent Not Truly Agentic**
- Problem: Agent doesn't intelligently decide what to do
- Impact: Fixed workflow, not adaptive to user queries
- Root Cause: Linear graph structure, no intelligent routing

## Proposed Agentic Architecture

### Core Principles

1. **Intelligent Decision Making**: Agent analyzes query and decides what tools/APIs to use
2. **RAG-First Approach**: All interpretations use RAG + AI for accuracy
3. **Parallel Processing**: Where possible, run operations concurrently
4. **Tool Selection**: Agent chooses tools based on query intent
5. **Iterative Refinement**: Agent can refine responses based on context

### Agent Workflow Design

```
┌─────────────────────────────────────────────────────────────┐
│                    USER QUERY                                 │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│        1. QUERY ANALYZER NODE                                │
│        - Analyze query intent                                │
│        - Extract entities (houses, planets, topics)          │
│        - Determine required data (BAV/SAV, Dasha, Gochara)  │
│        - Set query complexity                                │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│        2. AGENT DECISION ROUTER                              │
│        - Decide which APIs to call                          │
│        - Determine RAG retrieval strategy                   │
│        - Plan execution order (parallel vs sequential)       │
│        - Set priority for data sources                       │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
        ┌──────────────┴──────────────┐
        │                             │
        ▼                             ▼
┌───────────────┐          ┌──────────────────┐
│ 3a. DATA      │          │ 3b. RAG           │
│ COLLECTOR     │          │ RETRIEVER         │
│ (Parallel)    │          │ (Parallel)         │
│               │          │                   │
│ - BAV/SAV API │          │ - Supabase Vector │
│ - Dasha API   │          │ - Context Chunks     │
│ - Gochara API │          │ - Knowledge Base   │
└───────┬───────┘          └─────────┬──────────┘
        │                           │
        └──────────────┬────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│        4. CONTEXT SYNTHESIZER                                │
│        - Combine chart data + RAG context                   │
│        - Format data for LLM                                │
│        - Prioritize relevant information                    │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│        5. AI INTERPRETER                                     │
│        - Generate interpretation using OpenAI                │
│        - Use RAG context for accuracy                        │
│        - Reference specific chart data                       │
│        - Provide citations                                   │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│        6. RESPONSE FORMATTER                                 │
│        - Structure response                                  │
│        - Add citations                                       │
│        - Format for UI                                       │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                    FINAL RESPONSE                             │
└─────────────────────────────────────────────────────────────┘
```

## Implementation Plan

### Phase 1: Fix Core Issues

#### 1.1 Fix BAV/SAV API Integration
- **File**: `agent_app/graphs/astrology_agent_graph.py`
- **Changes**:
  - Standardize birth_data format (always use `latitude`/`longitude`)
  - Add proper error handling and retry logic
  - Validate API responses before using
  - Add debug logging

#### 1.2 Fix Data Format Consistency
- **Files**: `agent_app/main.py`, `agent_app/tools/astrology_tools.py`
- **Changes**:
  - Use consistent `latitude`/`longitude` everywhere
  - Add Pydantic validators for format conversion
  - Ensure all API calls use correct format

### Phase 2: Implement True Agentic Flow

#### 2.1 Create Intelligent Query Analyzer
- **New Node**: `analyze_query_intent`
- **Function**:
  - Use LLM to analyze query intent
  - Extract entities (houses, planets, topics)
  - Determine required data sources
  - Set query complexity level

#### 2.2 Create Agent Decision Router
- **New Node**: `agent_decision_router`
- **Function**:
  - Decide which APIs to call based on query
  - Determine RAG retrieval strategy
  - Plan parallel vs sequential execution
  - Set data priority

#### 2.3 Implement Parallel Data Collection
- **New Node**: `collect_data_parallel`
- **Function**:
  - Call multiple APIs concurrently
  - Handle errors gracefully
  - Merge results

#### 2.4 Implement RAG Retrieval Strategy
- **Enhanced Node**: `retrieve_knowledge_advanced`
- **Function**:
  - Multi-query RAG retrieval
  - House-specific context
  - Planet-specific context
  - Topic-specific context
  - Combine and deduplicate

### Phase 3: RAG Integration for All Interpretations

#### 3.1 Dashboard with RAG
- **Approach**: Hybrid with parallel processing
- **Implementation**:
  - Overview: RAG + AI (1 call)
  - Houses: Parallel RAG + AI (12 concurrent calls)
  - Expected time: 10-15 seconds (instead of 60-120s)

#### 3.2 Query Endpoint with Full RAG
- **Enhancement**: Always use RAG for interpretations
- **Implementation**:
  - Retrieve relevant context
  - Generate AI interpretation
  - Include citations

### Phase 4: Advanced Agent Features

#### 4.1 Tool Selection Logic
- Agent decides which tools to use
- Dynamic tool invocation
- Fallback mechanisms

#### 4.2 Iterative Refinement
- Agent can ask clarifying questions
- Refine responses based on feedback
- Multi-turn conversations

#### 4.3 Context Memory
- Remember previous queries
- Build context over conversation
- Reference previous analyses

## Technical Implementation Details

### New Agent Graph Structure

```python
# New nodes
1. analyze_query_intent()      # LLM-based intent analysis
2. agent_decision_router()      # Intelligent routing
3. collect_data_parallel()      # Parallel API calls
4. retrieve_knowledge_advanced() # Multi-query RAG
5. synthesize_context()         # Combine data + RAG
6. generate_interpretation()    # AI interpretation
7. format_response()            # Response formatting

# Edges
START → analyze_query_intent
analyze_query_intent → agent_decision_router
agent_decision_router → [collect_data_parallel, retrieve_knowledge_advanced]
[collect_data_parallel, retrieve_knowledge_advanced] → synthesize_context
synthesize_context → generate_interpretation
generate_interpretation → format_response
format_response → END
```

### Data Flow

```python
State = {
    "user_query": str,
    "birth_data": dict,
    "query_intent": str,           # Analyzed intent
    "required_apis": List[str],     # APIs to call
    "rag_strategy": dict,          # RAG retrieval plan
    "chart_data": dict,            # Collected data
    "rag_context": List[dict],     # Retrieved knowledge
    "synthesized_context": str,    # Combined context
    "interpretation": str,         # AI-generated
    "citations": List[str],        # Sources
    "final_response": str          # Formatted response
}
```

### Parallel Processing Strategy

```python
# For dashboard houses
async def generate_house_interpretations(houses, chart_data):
    tasks = []
    for house_num in houses:
        task = asyncio.create_task(
            generate_single_house_interpretation(house_num, chart_data)
        )
        tasks.append(task)
    
    results = await asyncio.gather(*tasks)
    return results

# Each house interpretation:
# 1. Retrieve RAG context (parallel)
# 2. Generate AI interpretation (parallel)
# Total time: ~10-15s instead of 60-120s
```

## Success Metrics

1. **BAV/SAV Working**: All queries return accurate BAV/SAV data
2. **RAG Used Everywhere**: All interpretations use RAG + AI
3. **Performance**: Dashboard <20 seconds, queries <10 seconds
4. **Intelligence**: Agent makes smart decisions about what to do
5. **Accuracy**: Interpretations reference specific chart data

## Next Steps

1. ✅ Create this plan
2. ⏳ Fix BAV/SAV API integration
3. ⏳ Implement intelligent query analyzer
4. ⏳ Create agent decision router
5. ⏳ Implement parallel data collection
6. ⏳ Add RAG to all interpretations
7. ⏳ Test end-to-end flow

