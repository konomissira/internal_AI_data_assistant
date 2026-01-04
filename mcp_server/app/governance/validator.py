import re
from dataclasses import dataclass
from typing import List, Optional, Tuple

from mcp_server.app.governance.policies import SqlPolicy, DEFAULT_POLICY


@dataclass
class ValidationResult:
    is_valid: bool
    violations: List[str]
    sanitized_sql: Optional[str] = None


_DISALLOWED_KEYWORDS = [
    r"\bINSERT\b",
    r"\bUPDATE\b",
    r"\bDELETE\b",
    r"\bDROP\b",
    r"\bTRUNCATE\b",
    r"\bALTER\b",
    r"\bCREATE\b",
    r"\bGRANT\b",
    r"\bREVOKE\b",
    r"\bCOPY\b",
    r"\bCALL\b",
    r"\bDO\b",
]


def _strip_sql_comments(sql: str) -> str:
    # remove -- comments
    sql = re.sub(r"--.*?$", "", sql, flags=re.MULTILINE)
    # remove /* */ comments
    sql = re.sub(r"/\*.*?\*/", "", sql, flags=re.DOTALL)
    return sql.strip()


def _extract_table_names(sql: str) -> List[str]:
    """
    Very lightweight table extraction:
    - captures identifiers after FROM/JOIN
    - handles schema.table by taking the last segment
    """
    pattern = r"\b(?:FROM|JOIN)\s+([a-zA-Z_][\w\.]*)"
    matches = re.findall(pattern, sql, flags=re.IGNORECASE)
    tables = []
    for m in matches:
        base = m.split(".")[-1]  # drop schema if present
        tables.append(base.lower())
    return tables


def _has_select_only(sql: str) -> bool:
    sql_clean = sql.strip().rstrip(";").strip()
    return sql_clean.upper().startswith("SELECT")


def _has_multiple_statements(sql: str) -> bool:
    # crude: more than one semicolon (after stripping comments)
    parts = [p.strip() for p in sql.split(";") if p.strip()]
    return len(parts) > 1


def _contains_disallowed(sql: str) -> Optional[str]:
    for kw in _DISALLOWED_KEYWORDS:
        if re.search(kw, sql, flags=re.IGNORECASE):
            return kw.strip(r"\b")
    return None


def _ensure_limit(sql: str, max_limit: int) -> Tuple[str, bool]:
    """
    Enforce LIMIT if missing. If present and higher than max_limit, clamp it.
    Returns (sql_out, changed)
    """
    sql_no_semicolon = sql.strip().rstrip(";")
    limit_match = re.search(r"\bLIMIT\s+(\d+)\b", sql_no_semicolon, flags=re.IGNORECASE)

    if not limit_match:
        return f"{sql_no_semicolon} LIMIT {max_limit};", True

    current = int(limit_match.group(1))
    if current > max_limit:
        sql_out = re.sub(
            r"\bLIMIT\s+\d+\b",
            f"LIMIT {max_limit}",
            sql_no_semicolon,
            flags=re.IGNORECASE,
        )
        return f"{sql_out};", True

    return f"{sql_no_semicolon};", True if not sql_no_semicolon.endswith(";") else False


def validate_sql(sql: str, policy: SqlPolicy = DEFAULT_POLICY) -> ValidationResult:
    violations: List[str] = []

    if not sql or not sql.strip():
        return ValidationResult(is_valid=False, violations=["empty_sql"])

    stripped = _strip_sql_comments(sql)

    if _has_multiple_statements(stripped):
        return ValidationResult(is_valid=False, violations=["multiple_statements_not_allowed"])

    if not _has_select_only(stripped):
        violations.append("only_select_allowed")

    disallowed = _contains_disallowed(stripped)
    if disallowed:
        violations.append(f"disallowed_keyword:{disallowed}")

    # very basic injection-ish guardrails
    if re.search(r"\bpg_sleep\b", stripped, flags=re.IGNORECASE):
        violations.append("disallowed_function:pg_sleep")

    tables = _extract_table_names(stripped)
    for t in tables:
        if t not in {x.lower() for x in policy.allowed_tables}:
            violations.append(f"table_not_allowed:{t}")

    sanitized = stripped
    changed = False

    if policy.enforce_limit and "only_select_allowed" not in violations:
        sanitized, changed = _ensure_limit(sanitized, policy.max_limit)

    is_valid = len(violations) == 0
    return ValidationResult(
        is_valid=is_valid,
        violations=violations,
        sanitized_sql=sanitized if (is_valid and (changed or sanitized != sql)) else (sanitized if is_valid else None),
    )
