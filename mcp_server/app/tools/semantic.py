from typing import Dict, Any
from mcp_server.app.governance.policies import DEFAULT_POLICY
from mcp_server.app.db.repository import fetch_semantic_metrics


def get_semantic_model() -> Dict[str, Any]:
    """
    MCP Tool: catalog.get_semantic_model
    Returns allowed tables + available metrics (MVP).
    In the future it will include joins + dimensions, too.
    """
    metrics = fetch_semantic_metrics()
    return {
        "allowed_tables": sorted(list(DEFAULT_POLICY.allowed_tables)),
        "metrics": metrics,
    }
