from typing import List, Dict, Any
from mcp_server.app.db.repository import fetch_semantic_metrics


def list_metrics() -> List[Dict[str, Any]]:
    """
    MCP Tool: catalog.list_metrics
    Returns governed / approved metrics.
    """
    return fetch_semantic_metrics()
