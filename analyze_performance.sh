#!/bin/bash
# Performance log analyzer

echo "📊 PERFORMANCE ANALYSIS"
echo "======================"
echo ""

LOG_FILE="/tmp/agent_server.log"

if [ ! -f "$LOG_FILE" ]; then
    echo "❌ Log file not found: $LOG_FILE"
    exit 1
fi

echo "🔍 Analyzing last 20 requests..."
echo ""

# Extract timing information
echo "Request Performance Summary:"
echo "----------------------------"
grep -E "⏱️ Total agent_graph.invoke took|⏱️ retrieve_knowledge took|⏱️ LLM call took" "$LOG_FILE" | tail -20 | \
awk '
/retrieve_knowledge took/ {
    match($0, /([0-9]+\.[0-9]+)s/, arr)
    if (arr[1] > 5) print "⚠️  SLOW RAG: " arr[1] "s"
    else if (arr[1] > 2) print "🟡 Medium RAG: " arr[1] "s"
    else print "✅ Fast RAG: " arr[1] "s"
}
/LLM call took/ {
    match($0, /([0-9]+\.[0-9]+)s/, arr)
    if (arr[1] > 15) print "⚠️  SLOW LLM: " arr[1] "s"
    else if (arr[1] > 10) print "🟡 Medium LLM: " arr[1] "s"
    else print "✅ Fast LLM: " arr[1] "s"
}
/Total agent_graph.invoke took/ {
    match($0, /([0-9]+\.[0-9]+)s/, arr)
    if (arr[1] > 20) print "⚠️  SLOW TOTAL: " arr[1] "s"
    else if (arr[1] > 10) print "🟡 Medium TOTAL: " arr[1] "s"
    else print "✅ Fast TOTAL: " arr[1] "s"
    print ""
}
'

echo ""
echo "📈 Statistics:"
echo "--------------"

# Count slow requests
SLOW_RAG=$(grep "retrieve_knowledge took" "$LOG_FILE" | tail -20 | grep -E "([5-9][0-9]|[0-9]{2,})\.[0-9]+s" | wc -l | tr -d ' ')
SLOW_LLM=$(grep "LLM call took" "$LOG_FILE" | tail -20 | grep -E "([2-9][0-9]|[0-9]{2,})\.[0-9]+s" | wc -l | tr -d ' ')
SLOW_TOTAL=$(grep "Total agent_graph.invoke took" "$LOG_FILE" | tail -20 | grep -E "([3-9][0-9]|[0-9]{2,})\.[0-9]+s" | wc -l | tr -d ' ')

echo "Slow RAG retrievals (>5s): $SLOW_RAG"
echo "Slow LLM calls (>15s): $SLOW_LLM"
echo "Slow total requests (>20s): $SLOW_TOTAL"

echo ""
echo "🔍 Finding the slowest request..."
echo "---------------------------------"
grep "retrieve_knowledge took" "$LOG_FILE" | tail -20 | \
grep -E "([5-9][0-9]|[0-9]{2,})\.[0-9]+s" | \
head -1

