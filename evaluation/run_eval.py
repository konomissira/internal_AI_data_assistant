from __future__ import annotations

import json
import os
import re
import sys
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List

import yaml

from ai_service.app.orchestrator import answer_question


@dataclass
class TestResult:
    id: str
    ok: bool
    error: str | None
    details: Dict[str, Any]


def _load_yaml(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def _ensure_columns(rows: List[Dict[str, Any]], expected_cols: List[str]) -> bool:
    if not rows:
        return False
    cols = set(rows[0].keys())
    return all(c in cols for c in expected_cols)


def _matches_forbidden(sql: str, patterns: List[str]) -> List[str]:
    hits = []
    for p in patterns:
        if re.search(p, sql or ""):
            hits.append(p)
    return hits


def run_test(mcp_base_url: str, test: Dict[str, Any]) -> TestResult:
    test_id = test["id"]
    question = test["question"]
    expect = test.get("expect", {})

    try:
        out = answer_question(mcp_base_url=mcp_base_url, question=question)

        # Basic expectations
        if expect.get("ok") is True and not out.get("ok", False):
            return TestResult(
                id=test_id,
                ok=False,
                error="expected_ok_but_failed",
                details={"response": out},
            )

        # Forbidden SQL patterns check (on generated + executed SQL)
        forbidden = expect.get("forbidden_sql_patterns", [])
        if forbidden:
            gen_sql = out.get("generated_sql", "") or ""
            exe_sql = out.get("executed_sql", "") or ""
            hits = _matches_forbidden(gen_sql + "\n" + exe_sql, forbidden)
            if hits:
                return TestResult(
                    id=test_id,
                    ok=False,
                    error="forbidden_sql_detected",
                    details={"hits": hits, "generated_sql": gen_sql, "executed_sql": exe_sql},
                )

        # Row/column checks (only if successful and result rows exist)
        result = out.get("result", {})
        rows = result.get("rows", []) if isinstance(result, dict) else []

        min_rows = expect.get("min_rows")
        if min_rows is not None:
            if len(rows) < int(min_rows):
                return TestResult(
                    id=test_id,
                    ok=False,
                    error="min_rows_not_met",
                    details={"expected_min_rows": min_rows, "actual_rows": len(rows), "response": out},
                )

        cols = expect.get("columns")
        if cols:
            if not _ensure_columns(rows, cols):
                return TestResult(
                    id=test_id,
                    ok=False,
                    error="missing_expected_columns",
                    details={"expected_columns": cols, "sample_row": rows[0] if rows else None, "response": out},
                )

        return TestResult(id=test_id, ok=True, error=None, details={"response": out})

    except Exception as e:
        return TestResult(id=test_id, ok=False, error="exception", details={"exception": str(e)})


def main() -> int:
    cfg_path = os.getenv("EVAL_CONFIG", "evaluation/golden_questions.yml")
    cfg = _load_yaml(cfg_path)

    mcp_base_url = cfg.get("config", {}).get("mcp_base_url", "http://localhost:8000")
    tests = cfg.get("tests", [])

    results: List[TestResult] = []
    for t in tests:
        results.append(run_test(mcp_base_url, t))

    passed = sum(1 for r in results if r.ok)
    failed = len(results) - passed

    report = {
        "timestamp": datetime.utcnow().isoformat(),
        "mcp_base_url": mcp_base_url,
        "summary": {"total": len(results), "passed": passed, "failed": failed},
        "results": [
            {"id": r.id, "ok": r.ok, "error": r.error, "details": r.details}
            for r in results
        ],
    }

    os.makedirs("evaluation/reports", exist_ok=True)
    out_path = "evaluation/reports/latest.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    print(json.dumps(report["summary"], indent=2))
    print(f"Report written to {out_path}")

    return 0 if failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
