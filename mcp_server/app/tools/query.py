# from typing import Dict, Any
# from psycopg2.extras import RealDictCursor

# from mcp_server.app.governance.validator import validate_sql
# from mcp_server.app.db.connection import get_db_connection


# def execute(payload: Dict[str, Any]) -> Dict[str, Any]:
#     """
#     MCP Tool: query.execute
#     Executes only validated SQL. Applies server-side statement timeout.
#     Input: {"sql": "..."}
#     """
#     sql = payload.get("sql", "")
#     validation = validate_sql(sql)

#     if not validation.is_valid:
#         return {
#             "ok": False,
#             "error": "sql_validation_failed",
#             "violations": validation.violations,
#         }

#     safe_sql = validation.sanitized_sql or sql

#     conn = get_db_connection()
#     try:
#         with conn.cursor(cursor_factory=RealDictCursor) as cur:
#             # safety: statement timeout (in ms)
#             cur.execute("SET LOCAL statement_timeout = 3000;")
#             cur.execute(safe_sql)
#             rows = cur.fetchall()
#             return {
#                 "ok": True,
#                 "row_count": len(rows),
#                 "rows": [dict(r) for r in rows],
#                 "sql": safe_sql,
#             }
#     finally:
#         conn.close()

import time
from typing import Dict, Any
from psycopg2.extras import RealDictCursor

from mcp_server.app.governance.validator import validate_sql
from mcp_server.app.db.connection import get_db_connection
from mcp_server.app.db.telemetry_repository import insert_query_log
from mcp_server.app.telemetry.logger import log_event


def execute(payload: Dict[str, Any]) -> Dict[str, Any]:
    sql = payload.get("sql", "")
    question = payload.get("question")

    start = time.time()
    validation = validate_sql(sql)

    if not validation.is_valid:
        duration_ms = int((time.time() - start) * 1000)

        insert_query_log(
            tool_name="query.execute",
            status="blocked",
            question=question,
            raw_sql=sql,
            validated_sql=None,
            violation_codes=validation.violations,
            row_count=None,
            execution_ms=duration_ms,
        )

        log_event({
            "tool_name": "query.execute",
            "status": "blocked",
            "violations": validation.violations,
            "execution_ms": duration_ms,
        })

        return {
            "ok": False,
            "error": "sql_validation_failed",
            "violations": validation.violations,
        }

    safe_sql = validation.sanitized_sql or sql

    conn = get_db_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SET LOCAL statement_timeout = 3000;")
            cur.execute(safe_sql)
            rows = cur.fetchall()

            duration_ms = int((time.time() - start) * 1000)

            insert_query_log(
                tool_name="query.execute",
                status="success",
                question=question,
                raw_sql=sql,
                validated_sql=safe_sql,
                violation_codes=None,
                row_count=len(rows),
                execution_ms=duration_ms,
            )

            log_event({
                "tool_name": "query.execute",
                "status": "success",
                "row_count": len(rows),
                "execution_ms": duration_ms,
            })

            return {
                "ok": True,
                "row_count": len(rows),
                "rows": [dict(r) for r in rows],
                "sql": safe_sql,
            }
    except Exception as e:
        duration_ms = int((time.time() - start) * 1000)

        insert_query_log(
            tool_name="query.execute",
            status="error",
            question=question,
            raw_sql=sql,
            validated_sql=None,
            violation_codes=[str(e)],
            row_count=None,
            execution_ms=duration_ms,
        )

        log_event({
            "tool_name": "query.execute",
            "status": "error",
            "error": str(e),
            "execution_ms": duration_ms,
        })

        raise
    finally:
        conn.close()