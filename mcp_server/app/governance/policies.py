from dataclasses import dataclass
from typing import Set


@dataclass(frozen=True)
class SqlPolicy:
    allowed_tables: Set[str]
    max_limit: int = 500
    enforce_limit: bool = True


DEFAULT_POLICY = SqlPolicy(
    allowed_tables={
        "fact_sales",
        "dim_date",
        "dim_region",
        "dim_product",
        "semantic_metrics",
        "semantic_dimensions",
        "semantic_joins",
    },
    max_limit=500,
    enforce_limit=True,
)
