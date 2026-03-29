from google.adk.agents.llm_agent import Agent
import random

# MOCK DATA (SIMULATION)

SCENARIOS = {
    "healthy": {
        "health": {"status": "ok", "message": "All systems operational"},
        "logs": "INFO: steady traffic\nINFO: no errors"
    },
    "degraded": {
        "health": {"status": "degraded", "message": "High latency detected"},
        "logs": "WARN: latency spikes\nWARN: retries increasing"
    },
    "critical": {
        "health": {"status": "error", "message": "Service failing"},
        "logs": "ERROR: 500 errors\nERROR: DB timeout\nERROR: cascading failures"
    }
}

# Pick scenario randomly (simulate production unpredictability)
CURRENT_SCENARIO = random.choice(list(SCENARIOS.keys()))


# TOOLS
def check_health(service_name: str) -> dict:
    """Simulated health check."""
    data = SCENARIOS[CURRENT_SCENARIO]["health"]
    return {
        "status": "success",
        "service": service_name,
        "health": data
    }


def fetch_logs(service_name: str) -> dict:
    """Simulated log fetch."""
    logs = SCENARIOS[CURRENT_SCENARIO]["logs"]
    return {
        "status": "success",
        "service": service_name,
        "logs": logs
    }


def send_alert(message: str) -> dict:
    """Simulated alert (prints instead of sending)."""
    print(f"\n🚨 ALERT SENT: {message}\n")
    return {
        "status": "sent",
        "message": message
    }


# AGENT

root_agent = Agent(
    model='gemini-2.5-flash',
    name='devops_triage_agent',
    description="Analyzes service health and decides whether to escalate incidents.",
    instruction=f"""
You are a DevOps triage agent operating in a ReAct-style loop.

You are debugging a service called: payment-service

Your job:
1. Check service health
2. If degraded or unclear, fetch logs
3. Analyze severity
4. Send alert ONLY if issue is critical

Rules:
- Do NOT assume anything — always use tools
- If health is not clearly OK, fetch logs before deciding
- Only send alert if logs show serious failure (errors, crashes, cascading issues)
- If system looks stable or mildly degraded, DO NOT escalate

Important:
- Think step-by-step
- Take multiple tool calls if needed
- Do NOT jump to conclusion early

Terminate when:
- You either send an alert OR confidently decide no escalation is needed
""",
    tools=[check_health, fetch_logs, send_alert],
)