from typing import List, Dict, Any
from psycopg2.extras import RealDictCursor

from mcp_server.app.db.connection import get_db_connection


def fetch_semantic_metrics() -> List[Dict[str, Any]]:
    """
    Returns approved metrics from the semantic layer.
    """
    query = """
        SELECT metric_name, description, sql_expression, default_table
        FROM semantic_metrics
        ORDER BY metric_name;
    """

    conn = get_db_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query)
            rows = cur.fetchall()
            return [dict(r) for r in rows]
    finally:
        conn.close()
