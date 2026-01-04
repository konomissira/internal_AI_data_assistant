from typing import Dict, Any
from psycopg2.extras import RealDictCursor

from mcp_server.app.governance.validator import validate_sql
from mcp_server.app.db.connection import get_db_connection


def execute(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    MCP Tool: query.execute
    Executes only validated SQL. Applies server-side statement timeout.
    Input: {"sql": "..."}
    """
    sql = payload.get("sql", "")
    validation = validate_sql(sql)

    if not validation.is_valid:
        return {
            "ok": False,
            "error": "sql_validation_failed",
            "violations": validation.violations,
        }

    safe_sql = validation.sanitized_sql or sql

    conn = get_db_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            # safety: statement timeout (in ms)
            cur.execute("SET LOCAL statement_timeout = 3000;")
            cur.execute(safe_sql)
            rows = cur.fetchall()
            return {
                "ok": True,
                "row_count": len(rows),
                "rows": [dict(r) for r in rows],
                "sql": safe_sql,
            }
    finally:
        conn.close()
