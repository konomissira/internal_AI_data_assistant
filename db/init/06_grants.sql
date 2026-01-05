-- 06_grants.sql
-- Grants that depend on tables created later (e.g. telemetry tables)

GRANT SELECT ON query_logs TO readonly_user;
