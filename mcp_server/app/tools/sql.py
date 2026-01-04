from typing import Dict, Any
from mcp_server.app.governance.validator import validate_sql


def validate(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    MCP Tool: sql.validate
    Input: {"sql": "..."}
    Output: {"is_valid": bool, "violations": [...], "sanitized_sql": "...?"}
    """
    sql = payload.get("sql", "")
    result = validate_sql(sql)
    return {
        "is_valid": result.is_valid,
        "violations": result.violations,
        "sanitized_sql": result.sanitized_sql,
    }
