from typing import List, Optional
from psycopg2.extras import execute_values

from mcp_server.app.db.connection import get_db_connection


def insert_query_log(
    tool_name: str,
    status: str,
    question: Optional[str],
    raw_sql: Optional[str],
    validated_sql: Optional[str],
    violation_codes: Optional[List[str]],
    row_count: Optional[int],
    execution_ms: Optional[int],
):
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO query_logs (
                    tool_name,
                    status,
                    question,
                    raw_sql,
                    validated_sql,
                    violation_codes,
                    row_count,
                    execution_ms
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    tool_name,
                    status,
                    question,
                    raw_sql,
                    validated_sql,
                    violation_codes,
                    row_count,
                    execution_ms,
                ),
            )
            conn.commit()
    finally:
        conn.close()
