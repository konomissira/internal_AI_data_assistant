-- 05_query_logs.sql
-- Telemetry table for observability & evaluation

CREATE TABLE IF NOT EXISTS query_logs (
    log_id          BIGSERIAL PRIMARY KEY,
    tool_name       TEXT NOT NULL,
    question        TEXT,
    raw_sql         TEXT,
    validated_sql   TEXT,
    status          TEXT NOT NULL, -- success | blocked | error
    violation_codes TEXT[],
    row_count       INTEGER,
    execution_ms    INTEGER,
    created_at      TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_query_logs_created_at
    ON query_logs (created_at);
