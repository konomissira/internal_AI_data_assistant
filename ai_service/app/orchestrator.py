from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

import requests


@dataclass
class SqlPlan:
    metric: str
    dimensions: List[str]
    sql: str


class MCPClient:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")

    def list_metrics(self) -> List[Dict]:
        r = requests.get(f"{self.base_url}/tools/catalog/list-metrics", timeout=5)
        r.raise_for_status()
        return r.json()["data"]

    def get_semantic_model(self) -> Dict:
        r = requests.get(f"{self.base_url}/tools/catalog/get-semantic-model", timeout=5)
        r.raise_for_status()
        return r.json()["data"]

    def validate_sql(self, sql: str) -> Dict:
        r = requests.post(f"{self.base_url}/tools/sql/validate", json={"sql": sql}, timeout=5)
        r.raise_for_status()
        return r.json()["data"]

    def execute_query(self, sql: str, question: Optional[str] = None) -> Dict:
        payload = {"sql": sql}
        if question:
            payload["question"] = question
        r = requests.post(f"{self.base_url}/tools/query/execute", json=payload, timeout=10)
        r.raise_for_status()
        return r.json()["data"]


def _normalize(q: str) -> str:
    return re.sub(r"\s+", " ", q.strip().lower())


def _pick_metric(question: str) -> str:
    q = _normalize(question)

    # metric selection
    if "order" in q and ("count" in q or "number" in q or "how many" in q):
        return "total_orders"
    if "avg" in q or "average" in q:
        return "avg_order_value"
    if "quantity" in q or "units" in q:
        return "total_quantity"
    # default
    return "total_sales"


def _pick_dimensions(question: str) -> List[str]:
    q = _normalize(question)
    dims: List[str] = []

    # dimensions (simple keyword triggers)
    if "region" in q or "city" in q or "location" in q:
        dims.append("region")
    if "product" in q:
        dims.append("product")
    if "category" in q:
        dims.append("category")
    if "date" in q or "day" in q:
        dims.append("date")
    if "month" in q:
        dims.append("month")
    if "year" in q:
        dims.append("year")

    # default dimension for common phrasing "by region"
    if " by " in q and not dims:
        if "region" in q:
            dims.append("region")

    # If nothing, return empty = total metric only
    return dims


def _build_sql(metric: str, dimensions: List[str]) -> str:
    """
    Builds a safe SQL statement using the known star schema.
    NOTE: governance still applies in sql.validate + query.execute.
    """
    metric_expr_map = {
        "total_sales": "SUM(f.total_amount)",
        "total_orders": "COUNT(DISTINCT f.order_id)",
        "avg_order_value": "AVG(f.total_amount)",
        "total_quantity": "SUM(f.quantity)",
    }

    dim_select_map = {
        "region": ("r.region_name", "dim_region r", "f.region_id = r.region_id"),
        "product": ("p.product_name", "dim_product p", "f.product_id = p.product_id"),
        "category": ("p.product_category", "dim_product p", "f.product_id = p.product_id"),
        "date": ("d.date_value", "dim_date d", "f.date_id = d.date_id"),
        "month": ("d.month", "dim_date d", "f.date_id = d.date_id"),
        "year": ("d.year", "dim_date d", "f.date_id = d.date_id"),
    }

    metric_expr = metric_expr_map.get(metric, metric_expr_map["total_sales"])

    select_cols: List[str] = []
    joins: Dict[str, Tuple[str, str]] = {}  # table_alias -> (table, condition)

    for dim in dimensions:
        if dim not in dim_select_map:
            continue
        col, table, cond = dim_select_map[dim]
        select_cols.append(col)
        alias = table.split()[-1]
        joins[alias] = (table, cond)

    # Build query
    select_clause = ", ".join(select_cols + [f"{metric_expr} AS {metric}"]) if select_cols else f"{metric_expr} AS {metric}"
    sql = f"SELECT {select_clause} FROM fact_sales f "

    for alias, (table, cond) in joins.items():
        sql += f"JOIN {table} ON {cond} "

    if select_cols:
        sql += "GROUP BY " + ", ".join(select_cols) + " "
        sql += f"ORDER BY {metric} DESC "

    # No ORDER BY by default (keeps it simple and deterministic)
    return sql.strip()


def generate_sql_plan(question: str) -> SqlPlan:
    metric = _pick_metric(question)
    dims = _pick_dimensions(question)
    sql = _build_sql(metric, dims)
    return SqlPlan(metric=metric, dimensions=dims, sql=sql)


def answer_question(mcp_base_url: str, question: str) -> Dict:
    """
    Orchestrates: question -> sql plan -> validate -> execute
    """
    client = MCPClient(mcp_base_url)

    plan = generate_sql_plan(question)
    validation = client.validate_sql(plan.sql)

    if not validation["is_valid"]:
        return {
            "ok": False,
            "stage": "validate",
            "metric": plan.metric,
            "dimensions": plan.dimensions,
            "sql": plan.sql,
            "violations": validation["violations"],
        }

    # use sanitized SQL if provided
    safe_sql = validation.get("sanitized_sql") or plan.sql
    result = client.execute_query(safe_sql, question=question)

    return {
        "ok": result.get("ok", False),
        "metric": plan.metric,
        "dimensions": plan.dimensions,
        "generated_sql": plan.sql,
        "executed_sql": result.get("sql", safe_sql),
        "result": result,
    }
