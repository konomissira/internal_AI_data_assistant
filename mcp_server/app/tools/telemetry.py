from typing import Dict, Any

from mcp_server.app.db.telemetry_repository import insert_query_log
from mcp_server.app.telemetry.logger import log_event


def log(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    MCP Tool: telemetry.log_event
    """
    insert_query_log(
        tool_name=payload.get("tool_name"),
        status=payload.get("status"),
        question=payload.get("question"),
        raw_sql=payload.get("raw_sql"),
        validated_sql=payload.get("validated_sql"),
        violation_codes=payload.get("violation_codes"),
        row_count=payload.get("row_count"),
        execution_ms=payload.get("execution_ms"),
    )

    log_event(payload)

    return {"ok": True}
